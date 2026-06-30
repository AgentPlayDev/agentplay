#!/usr/bin/env python3
"""
MMHK Agent Tool — Zero pip-dependency game loop helper.
Claude Code acts as the decision-maker; this script handles the mechanics.

Authentication: Bearer api_key only (no cookies). The api_key is loaded
from `$WORKDIR/api_key` where $WORKDIR = /tmp/agentplay/<player_name>.
Obtain one by running the AgentPlay register + claim flow once
(see SKILL.md). The current world_id is cached at $WORKDIR/world_id so
state/exec/etc. don't need to repeat it.

Usage (Claude Code calls these via Bash tool):
  python3 agent_loop.py <player> worlds                      # list joinable worlds
  python3 agent_loop.py <player> login [world_id]            # world_id optional (auto-picked)
  python3 agent_loop.py <player> register <faction_id> [world_id]
  python3 agent_loop.py <player> state
  python3 agent_loop.py <player> content '<el_param_list_json>'
  python3 agent_loop.py <player> exec '<actions_json>'
  python3 agent_loop.py <player> wait <seconds>
  python3 agent_loop.py _ base                               # print resolved API host

All output is JSON to stdout. Errors go to stderr.
No pip installs required — uses only Python standard library.
"""

import json
import math
import os
import ssl
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

SKILL_DIR = Path(__file__).parent
# Per-agent runtime data (api_key, world_id) lives under the running agent's
# HOME so it survives reboots — re-claiming a lost api_key needs a fresh tweet,
# so ephemeral /tmp is a poor home for it. AGENTPLAY_HOME overrides the base for
# sandboxed hosts (e.g. Codex workspace-write) where $HOME isn't writable.
# Each player gets an isolated subdir: <base>/<player>/
_env_home = os.environ.get("AGENTPLAY_HOME", "").strip()
if _env_home:
    WORKDIR_ROOT = Path(_env_home).expanduser()
else:
    try:
        WORKDIR_ROOT = Path.home() / ".agentplay"
    except Exception:
        WORKDIR_ROOT = Path("/tmp/agentplay")

def base_url() -> str:
    return "https://agentplay.dev"


# ── HTTP client (stdlib only, Bearer auth) ────────────────────────────────────

class GameClient:
    def __init__(self, player_name: str):
        self.player_name = player_name
        self.workdir = WORKDIR_ROOT / player_name
        self.workdir.mkdir(parents=True, exist_ok=True)
        try:
            # Long-lived api_key lives here now (persistent home, not /tmp) — lock
            # it down so other users on the box can't read the Bearer token.
            WORKDIR_ROOT.chmod(0o700)
            self.workdir.chmod(0o700)
        except OSError:
            pass
        self.api_key_file = self.workdir / "api_key"
        self.world_file   = self.workdir / "world_id"

        self.api_key = None
        if self.api_key_file.exists():
            self.api_key = self.api_key_file.read_text().strip() or None

        self.world_id = None
        if self.world_file.exists():
            try:
                self.world_id = int(self.world_file.read_text().strip())
            except ValueError:
                pass

        # Self-signed / Tailscale TLS — skip verification.
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        self.opener = urllib.request.build_opener(urllib.request.HTTPSHandler(context=ctx))

    # ── auth helpers ──
    def _require_key(self):
        if not self.api_key:
            raise RuntimeError(
                f"No api_key found at {self.api_key_file}. "
                "Run AgentPlay register + claim first (see SKILL.md)."
            )

    def _headers(self) -> dict:
        # Browser-like User-Agent: urllib's default ("Python-urllib/x") trips
        # Cloudflare bot protection on the game host (error 1010). The real fix
        # is to allowlist /agent and /agentplay from bot protection server-side;
        # this header keeps the skill working until that's done.
        h = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/126.0.0.0 Safari/537.36"
            ),
        }
        if self.api_key:
            h["Authorization"] = f"Bearer {self.api_key}"
        return h

    def _save_world(self, world_id):
        if not world_id:
            return
        self.world_id = int(world_id)
        self.world_file.write_text(str(self.world_id))

    def _request(self, method: str, path: str, body: dict = None) -> dict:
        data = json.dumps(body).encode() if body is not None else None
        req = urllib.request.Request(
            f"{base_url()}{path}", data=data, headers=self._headers(), method=method,
        )
        try:
            with self.opener.open(req, timeout=30) as resp:
                return json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            # Server returns structured JSON on errors (401, 404, 409, etc.) —
            # surface those instead of a bare HTTPError.
            try:
                return json.loads(e.read().decode())
            except Exception:
                return {"ok": False, "error": {"code": "HTTP_" + str(e.code), "message": str(e)}}

    def get(self, path: str) -> dict:
        return self._request("GET", path)

    def post(self, path: str, body: dict) -> dict:
        return self._request("POST", path, body)

    # ── /agent/* endpoints ──
    def worlds(self) -> dict:
        """List joinable worlds for this environment (id/name/subscriptionStatus)."""
        self._require_key()
        return self.get("/agent/worlds")

    def login(self, world_id: int = None) -> dict:
        self._require_key()
        body = {"worldId": world_id} if world_id else {}
        result = self.post("/agent/login", body)
        if result.get("ok"):
            self._save_world(result.get("data", {}).get("worldId") or world_id)
        return result

    def register(self, faction_id: int, world_id: int = None) -> dict:
        self._require_key()
        body = {"factionId": faction_id}
        if world_id:
            body["worldId"] = world_id
        result = self.post("/agent/register", body)
        if result.get("ok"):
            self._save_world(result.get("data", {}).get("worldId") or world_id)
        return result

    def game_state(self) -> dict:
        self._require_key()
        if not self.world_id:
            raise RuntimeError("worldId unknown — run `login` or `register` first.")
        return self.get(f"/agent/gameState?worldId={self.world_id}")

    def action(self, action_type: str, params: dict) -> dict:
        self._require_key()
        if not self.world_id:
            raise RuntimeError("worldId unknown — run `login` or `register` first.")
        return self.post("/agent/action", {
            "worldId": self.world_id,
            "type":    action_type,
            "params":  params,
        })


# ── State formatter ───────────────────────────────────────────────────────────

def format_state(gs: dict, extra: dict = None) -> dict:
    """Condense raw gameState into a Claude-readable summary."""
    player = gs.get("player", {})
    now = int(time.time())

    pending = [
        {
            "type": a.get("actionType", a.get("type", "?")),
            "endsInSecs": max(0, a.get("endDate", now) - now),
            "endDate": a.get("endDate"),
        }
        for a in gs.get("timeline", {}).get("attachedMasterActionList", [])
    ]

    heroes = []
    for h in gs.get("heroes", []):
        troops = [
            {
                "stackId": s.get("id"),
                "unitEntityId": s.get("unitEntityId"),
                "type": s.get("unitEntityType"),
                "power": s.get("unitEntityPower"),
                "qty": s.get("quantity"),
            }
            for s in h.get("unitStackList", [])
        ]
        heroes.append({
            "id": h.get("id"),
            "name": h.get("name"),
            "level": h.get("_level"),
            "xpPoints": h.get("availXpSkills"),  # available skill points
            "xp": h.get("xp"),
            "attack": h.get("attack"),
            "defense": h.get("defense"),
            "idle": h.get("_current_slaveActionId") is None,
            "regionId": h.get("regionId"),
            "totalPower": sum((s["power"] or 0) * s["qty"] for s in troops),
            "troops": troops,
        })

    cities = []
    for c in gs.get("cities", []):
        res = c.get("resources", {})
        inc = c.get("income", {})
        liberate = [
            {
                "buildingId": b.get("id"),
                "buildingType": b.get("tagName") or b.get("buildingTypeEntityTagName"),
                "npcPower": b.get("npcPower"),
                "npcStacks": [
                    {
                        "type": s.get("unitEntityType"),
                        "power": s.get("unitEntityPower"),
                        "qty": s.get("quantity"),
                    }
                    for s in b.get("npcStacks", [])
                ],
            }
            for b in c.get("buildings", {}).get("liberate", [])
        ]
        buildable = [
            {
                "buildingId": b.get("id"),
                "buildingType": b.get("tagName") or b.get("buildingTypeEntityTagName"),
                "goldCost": b.get("goldCost", 0),
                "woodCost": b.get("woodCost", 0),
                "oreCost": b.get("oreCost", 0),
                "durationSecs": b.get("duration"),
                "resourcesSufficient": (
                    res.get("GOLD", 0) >= b.get("goldCost", 0)
                    and res.get("WOOD", 0) >= b.get("woodCost", 0)
                    and res.get("ORE", 0) >= b.get("oreCost", 0)
                    and res.get("CRYSTAL", 0) >= b.get("crystalCost", 0)
                    and res.get("MERCURY", 0) >= b.get("mercuryCost", 0)
                    and res.get("SULFUR", 0) >= b.get("sulfurCost", 0)
                    and res.get("GEM", 0) >= b.get("gemCost", 0)
                ),
            }
            for b in c.get("buildings", {}).get("buildable", [])
        ]
        res_max = c.get("resourcesMax", {})
        cities.append({
            "regionId": c.get("regionId"),
            "name": c.get("name"),
            "buildingQueue": c.get("buildingQueue", []),
            "currentBuildingAction": c.get("currentBuildingAction"),
            "resources": {k: res.get(k) for k in ("GOLD", "WOOD", "ORE", "MERCURY", "CRYSTAL", "SULFUR", "GEM")},
            "resourcesMax": {k: res_max.get(k) for k in ("WOOD", "ORE", "MERCURY", "CRYSTAL", "SULFUR", "GEM")},
            "income": {k: inc.get(k) for k in ("GOLD", "WOOD", "ORE")},
            "garrison": [
                {
                    "stackId": s.get("id"),
                    "unitEntityId": s.get("unitEntityId"),
                    "type": s.get("unitEntityType"),
                    "power": s.get("unitEntityPower"),
                    "qty": s.get("quantity"),
                }
                for s in c.get("garrison", [])
            ],
            "liberateBuildings": liberate,
            "buildableBuildings": buildable,
        })

    npc_zones = [
        {
            "zoneId": z.get("id"),
            "regionId": z.get("regionId"),
            "status": z.get("status"),
            "npcPower": z.get("npcPower"),
            "npcComposition": z.get("npcComposition"),
            "npcStacks": [
                {
                    "type": s.get("unitEntityType"),
                    "power": s.get("unitEntityPower") or s.get("power"),
                    "qty": s.get("quantity"),
                }
                for s in z.get("npcStacks", [])
            ],
            "mineType": (z.get("mine") or {}).get("ressourceEntityTagName"),
            "mine": z.get("mine"),
        }
        for z in gs.get("zones", [])
        if z.get("npcPower", 0) > 0 or z.get("mine")
    ]

    ended_quests = [
        {"questId": q.get("id"), "targetId": q.get("targetId"), "title": q.get("title")}
        for q in gs.get("quests", [])
        if q.get("status") == "ended"
    ]

    summary = {
        "scores": {
            "domination": player.get("dominationScore"),
            "dominationRank": player.get("dominationRank"),
            "dominationThreshold": player.get("dominationRankingThreshold"),
            "nextDominationObjective": player.get("nextDominationObjective"),
            "wealth": player.get("wealthScore"),
            "wealthRank": player.get("wealthRank"),
            "wealthThreshold": player.get("wealthRankingThreshold"),
            "nextWealthObjective": player.get("nextWealthObjective"),
            "honor": player.get("honorScore"),
            "honorRank": player.get("honorRank"),
            "honorThreshold": player.get("honorRankingThreshold"),
            "nextHonorObjective": player.get("nextHonorObjective"),
        },
        "cityLimit": {
            "current": player.get("currentCityCount"),
            "max": player.get("maxCityCount"),
        },
        "unreadMessages": gs.get("unreadMessages", 0),
        "endedQuests": ended_quests,
        "pendingActions": pending,
        "nearestEndDate": min((a["endDate"] for a in pending if a.get("endDate")), default=None),
        "heroes": heroes,
        "cities": cities,
        "npcZones": npc_zones,
    }

    summary["guidance"] = build_guidance(gs, heroes, cities)

    if extra:
        summary["extraContent"] = extra

    return summary


# ── Actionable guidance ───────────────────────────────────────────────────────

# Buildings sorted by strategic priority (lower = more important)
_BUILDING_PRIORITY = [
    ("TAVERN",),
    ("TOWN_HALL", "CITY_HALL", "CAPITOL"),
    ("RECRUIT",),           # matches RECRUIT_T1, RECRUIT_T2P, etc.
    ("MARKETPLACE",),
    ("FORT", "CITADEL", "CASTLE"),
    ("MAGIC_GUILD",),
    ("BLACKSMITH",),
    ("RESSOURCE_SILO", "FARMS"),
]

def _building_priority_rank(tag: str) -> int:
    tag = tag or ""
    for rank, keywords in enumerate(_BUILDING_PRIORITY):
        if any(kw in tag for kw in keywords):
            return rank
    return len(_BUILDING_PRIORITY)

def _building_priority_label(tag: str) -> str:
    rank = _building_priority_rank(tag)
    if rank <= 3:
        return "HIGH"
    if rank <= 5:
        return "MED"
    return "LOW"


def build_guidance(gs: dict, heroes: list, cities: list) -> dict:
    """Pre-compute actionable recommendations from current game state."""
    counter_map = {"INFANTRY": "SHOOTER", "CAVALRY": "INFANTRY", "SHOOTER": "CAVALRY"}

    idle_heroes = [h for h in heroes if h["idle"]]
    heroes_no_troops = [h for h in idle_heroes if h["totalPower"] == 0]
    total_idle_power = sum(h["totalPower"] for h in idle_heroes)

    # ── 1. Liberation candidates ──────────────────────────────────────────────
    liberate_candidates = []
    for city in cities:
        garrison_power = sum((s["power"] or 0) * s["qty"] for s in city["garrison"])
        city_hero_power = sum(h["totalPower"] for h in idle_heroes if h["regionId"] == city["regionId"])
        available = garrison_power + city_hero_power

        for bld in city["liberateBuildings"]:
            npc_pw = bld["npcPower"] or 0
            feasible = available > npc_pw
            liberate_candidates.append({
                "cityName": city["name"],
                "regionId": city["regionId"],
                "buildingId": bld["buildingId"],
                "buildingType": bld["buildingType"],
                "npcPower": npc_pw,
                "npcStacks": bld["npcStacks"],
                "availablePower": available,
                "feasible": feasible,
                "action": "READY — run battle sim then liberate" if feasible else "WAIT — need more troops",
            })

    # ── 2. Building queue guidance ────────────────────────────────────────────
    build_guidance_list = []
    for city in cities:
        res = city["resources"]
        res_max = city.get("resourcesMax", {})
        queue_idle = len(city["buildingQueue"]) < 4

        # Detect buildings whose cost exceeds warehouse max capacity (can never be afforded without upgrading storage)
        capacity_blocked_high = []
        for b in city["buildableBuildings"]:
            if _building_priority_label(b["buildingType"]) != "HIGH":
                continue
            cap_issues = {}
            for rtype, cost_key in [("WOOD", "woodCost"), ("ORE", "oreCost")]:
                max_cap = res_max.get(rtype)
                if max_cap and b[cost_key] > max_cap:
                    cap_issues[rtype] = {"need": b[cost_key], "maxCapacity": max_cap}
            if cap_issues:
                capacity_blocked_high.append({
                    "buildingType": b["buildingType"],
                    "buildingId": b["buildingId"],
                    "capacityIssues": cap_issues,
                })

        silo_unblocks = [b["buildingType"] for b in capacity_blocked_high] if capacity_blocked_high else []

        affordable_raw = [b for b in city["buildableBuildings"] if b["resourcesSufficient"]]
        affordable = []
        for b in affordable_raw:
            label = _building_priority_label(b["buildingType"])
            # Elevate RESSOURCE_SILO / FARMS to HIGH if it unblocks a high-priority building
            is_storage = any(kw in (b["buildingType"] or "") for kw in ("RESSOURCE_SILO", "FARMS"))
            if is_storage and silo_unblocks:
                label = "HIGH"
            affordable.append({**b, "priorityLabel": label, "unblocks": silo_unblocks if is_storage and silo_unblocks else []})
        affordable.sort(key=lambda b: (0 if b["priorityLabel"] == "HIGH" else 1 if b["priorityLabel"] == "MED" else 2, _building_priority_rank(b["buildingType"])))

        need_resources = []
        for b in city["buildableBuildings"]:
            if not b["resourcesSufficient"]:
                gap = {
                    rtype: b[cost_key] - (res.get(rtype) or 0)
                    for rtype, cost_key in [
                        ("GOLD", "goldCost"), ("WOOD", "woodCost"), ("ORE", "oreCost"),
                        ("CRYSTAL", "crystalCost"), ("MERCURY", "mercuryCost"),
                        ("SULFUR", "sulfurCost"), ("GEM", "gemCost"),
                    ]
                    if b.get(cost_key, 0) > (res.get(rtype) or 0)
                }
                need_resources.append({
                    **b,
                    "priorityLabel": _building_priority_label(b["buildingType"]),
                    "resourceGap": gap,
                })
        need_resources.sort(key=lambda b: _building_priority_rank(b["buildingType"]))

        high_affordable = [b for b in affordable if b["priorityLabel"] == "HIGH"]
        top = high_affordable[0] if high_affordable else None
        if queue_idle and top:
            top_note = f" (解锁: {', '.join(top['unblocks'])})" if top.get("unblocks") else ""
            action_str = f"BUILD NOW — {top['buildingType']}{top_note}"
        elif queue_idle and affordable:
            action_str = "BUILD NOW (only low-priority available)"
        elif not queue_idle:
            action_str = "QUEUE BUSY"
        else:
            action_str = "NO AFFORDABLE BUILDINGS"

        build_guidance_list.append({
            "cityName": city["name"],
            "regionId": city["regionId"],
            "queueIdle": queue_idle,
            "capacityBlockedHigh": capacity_blocked_high,
            "action": action_str,
            "affordable": affordable,
            "needResources": need_resources,
        })

    # ── 3. NPC zone attack guidance ───────────────────────────────────────────
    attack_zones = []
    for z in gs.get("zones", []):
        npc_pw = z.get("npcPower") or 0
        if npc_pw == 0:
            continue
        comp = z.get("npcComposition") or {}
        dominant = max(comp, key=comp.get) if comp else None
        counter = counter_map.get(dominant)
        has_counter = any(
            any(s.get("type") == counter for s in h["troops"])
            for h in idle_heroes
        ) if counter and idle_heroes else False
        attack_zones.append({
            "zoneId": z.get("id"),
            "regionId": z.get("regionId"),
            "npcPower": npc_pw,
            "npcComposition": comp,
            "dominantType": dominant,
            "counterType": counter,
            "hasCounterTroops": has_counter,
            "npcStacks": [
                {"type": s.get("unitEntityType"), "power": s.get("unitEntityPower"), "qty": s.get("quantity")}
                for s in z.get("npcStacks", [])
            ],
            "feasible": total_idle_power > 0,
        })
    attack_zones.sort(key=lambda z: z["npcPower"])

    # ── 4. Mine upgrade opportunities ─────────────────────────────────────────
    mine_ops = []
    for z in gs.get("zones", []):
        mine = z.get("mine")
        if not mine:
            continue
        npc_pw = z.get("npcPower") or 0
        upgrade_lvl = mine.get("upgradeLevel", 0)
        improve_lvl = mine.get("improveLevel", 0)
        # IMPROVE requires improveLevel == upgradeLevel - 1 (strict equality)
        improve_available = improve_lvl == upgrade_lvl - 1
        # If improveLevel is further behind, Downgrade is needed first
        downgrade_needed = improve_lvl < upgrade_lvl - 1
        upgrade_blocked = npc_pw > 0
        if improve_available or downgrade_needed or not upgrade_blocked:
            if improve_available:
                action = "IMPROVE MINE — send empty hero" if heroes_no_troops else "NEED EMPTY HERO"
            elif downgrade_needed:
                action = f"DOWNGRADE NEEDED (improveLevel={improve_lvl} too far behind upgradeLevel={upgrade_lvl})"
            elif upgrade_blocked:
                action = "BLOCKED BY NPC"
            else:
                action = "ALREADY AT MAX IMPROVE"
            mine_ops.append({
                "zoneId": z.get("id"),
                "mineType": mine.get("ressourceEntityTagName"),
                "upgradeLevel": upgrade_lvl,
                "improveLevel": improve_lvl,
                "improveAvailable": improve_available,
                "downgradeNeeded": downgrade_needed,
                "upgradeBlocked": upgrade_blocked,
                "canActNow": improve_available and len(heroes_no_troops) > 0 and not upgrade_blocked,
                "action": action,
            })

    # ── 5. Ready quests ───────────────────────────────────────────────────────
    ready_quests = [
        {"questId": q.get("id"), "title": q.get("title"), "targetId": q.get("targetId")}
        for q in gs.get("quests", [])
        if q.get("status") == "ended"
    ]

    return {
        "idleHeroes": [
            {"id": h["id"], "name": h["name"], "regionId": h["regionId"],
             "totalPower": h["totalPower"], "hasTroops": h["totalPower"] > 0}
            for h in idle_heroes
        ],
        "liberateCandidates": liberate_candidates,
        "buildingGuidance": build_guidance_list,
        "attackZones": attack_zones,
        "mineOpportunities": mine_ops,
        "readyQuests": ready_quests,
    }


# ── Text summary renderer ─────────────────────────────────────────────────────

def _mins(secs: int) -> str:
    if secs < 120:
        return f"{secs}秒"
    if secs < 3600:
        return f"{secs // 60}分钟"
    return f"{secs // 3600}小时{(secs % 3600) // 60}分"


def _stack_str(s: dict) -> str:
    return f"{s['type']}×{s['qty']}(pw{s['power']})"


def format_state_text(summary: dict, extra: dict = None) -> str:
    lines = []
    now_str = time.strftime("%H:%M:%S")

    # ── 头部 ─────────────────────────────────────────────────────────────────
    sc = summary["scores"]
    wealth_rank = f"#{sc['wealthRank']}" if sc['wealthRank'] else "未上榜"
    lines += [
        f"=== MMHK 状态快照 @ {now_str} ===",
        f"分数: 统治#{sc['dominationRank']}({sc['domination']}) | 财富{wealth_rank}({sc['wealth']}) | 荣誉#{sc['honorRank']}({sc['honor']})",
    ]
    if summary.get("unreadMessages"):
        lines.append(f"未读消息: {summary['unreadMessages']}条")

    # ── 进行中动作 ────────────────────────────────────────────────────────────
    pending = summary.get("pendingActions", [])
    if pending:
        lines.append("\n[进行中动作]")
        for a in pending:
            lines.append(f"  - {a['type']} — 剩余{_mins(a['endsInSecs'])} (endDate={a['endDate']})")
    else:
        lines.append("\n[进行中动作] 无")

    # ── 英雄 ─────────────────────────────────────────────────────────────────
    lines.append("\n[英雄]")
    for h in summary["heroes"]:
        status = "空闲" if h["idle"] else "忙碌"
        troop_str = " | ".join(_stack_str(s) for s in h["troops"]) if h["troops"] else "无部队"
        xp_note = f" ★{h['xpPoints']}技能点" if h.get("xpPoints") else ""
        lines.append(
            f"  {h['name']} (id={h['id']}) Lv{h['level']} ATK/DEF={h['attack']}/{h['defense']}"
            f" @ regionId={h['regionId']} [{status}] 战力{h['totalPower']}{xp_note}"
        )
        lines.append(f"    部队: {troop_str}")

    # ── 城市 ─────────────────────────────────────────────────────────────────
    lines.append("\n[城市]")
    for c in summary["cities"]:
        res = c["resources"]
        inc = c["income"]
        res_str = f"金{int(res.get('GOLD',0))} 木{res.get('WOOD',0):.1f} 矿{res.get('ORE',0):.1f}"
        rare_parts = [f"{k}{res[k]:.1f}" for k in ("MERCURY","CRYSTAL","SULFUR","GEM") if (res.get(k) or 0) > 0]
        if rare_parts:
            res_str += " | " + " ".join(rare_parts)
        inc_str = f"金+{inc.get('GOLD',0)} 木+{inc.get('WOOD',0):.1f} 矿+{inc.get('ORE',0):.1f}"
        lines.append(f"  {c['name']} (regionId={c['regionId']})")
        lines.append(f"    资源: {res_str} | 收入: {inc_str}")
        if c["garrison"]:
            gar = " | ".join(_stack_str(s) for s in c["garrison"])
            lines.append(f"    驻军: {gar}")
        q = c["buildingQueue"]
        bq_action = c.get("currentBuildingAction")
        if q:
            queue_names = [item.get("name", f"id={item.get('id')}") for item in q]
            if bq_action:
                end_secs = max(0, bq_action["endDate"] - int(time.time()))
                lines.append(f"    建筑队列({len(q)}/4): 建造中[{queue_names[0]}] 剩余{_mins(end_secs)}" + (f" | 排队: {', '.join(queue_names[1:])}" if len(queue_names) > 1 else ""))
            else:
                lines.append(f"    建筑队列({len(q)}/4): {', '.join(queue_names)}")
        else:
            lines.append("    建筑队列: 空闲(0/4)")

    # ══════════════════════════════════════════════════════════════════════════
    lines.append("\n=== GUIDANCE ===")

    g = summary.get("guidance", {})

    # ── 解放建筑 ──────────────────────────────────────────────────────────────
    candidates = g.get("liberateCandidates", [])
    lines.append("\n[待解放建筑]")
    if candidates:
        for b in candidates:
            npc_stacks = " + ".join(_stack_str(s) for s in b["npcStacks"])
            lines.append(
                f"  - {b['buildingType']} (buildingId={b['buildingId']}) @ {b['cityName']}(regionId={b['regionId']})"
            )
            lines.append(f"    NPC战力={b['npcPower']} [{npc_stacks}]")
            lines.append(f"    我方可用={b['availablePower']} → {b['action']}")
    else:
        lines.append("  无")

    # ── 建筑队列指引 ──────────────────────────────────────────────────────────
    lines.append("\n[建筑队列指引]")
    for bg in g.get("buildingGuidance", []):
        lines.append(f"  {bg['cityName']}(regionId={bg['regionId']}): {bg['action']}")
        if bg.get("capacityBlockedHigh"):
            for cb in bg["capacityBlockedHigh"]:
                issues = " ".join(f"{k}需{v['need']}上限{v['maxCapacity']}" for k, v in cb["capacityIssues"].items())
                lines.append(f"    ⚠ 容量不足: {cb['buildingType']} — {issues} (需升级仓库)")
        for b in bg.get("affordable", []):
            label = b.get("priorityLabel", "?")
            unblocks = f" → 解锁: {', '.join(b['unblocks'])}" if b.get("unblocks") else ""
            lines.append(
                f"    · [{label}] {b['buildingType']} (id={b['buildingId']}) "
                f"金{b['goldCost']} 木{b['woodCost']} 矿{b['oreCost']} 耗时{_mins(b['durationSecs'])}{unblocks}"
            )
        for b in bg.get("needResources", []):
            label = b.get("priorityLabel", "?")
            gap_str = " ".join(f"{k}-{v:.1f}" for k, v in b["resourceGap"].items())
            lines.append(
                f"    · [{label}][缺] {b['buildingType']} (id={b['buildingId']}) 差: {gap_str}"
            )

    # ── NPC区域 ───────────────────────────────────────────────────────────────
    attack_zones = g.get("attackZones", [])
    lines.append(f"\n[NPC区域攻击 ({len(attack_zones)}个, 按战力升序, 显示前15)]")
    for z in attack_zones[:15]:
        comp = z.get("npcComposition") or {}
        comp_str = " ".join(f"{k[:3]}{v}%" for k, v in comp.items() if v)
        counter_note = f"→带{z['counterType']}反制" if z.get("counterType") else ""
        has_note = "[有反制兵]" if z.get("hasCounterTroops") else "[无反制兵]"
        stacks_str = " + ".join(_stack_str(s) for s in z.get("npcStacks", []))
        lines.append(
            f"  Zone{z['zoneId']} @ regionId={z['regionId']} npc={z['npcPower']} "
            f"{comp_str} {counter_note} {has_note}"
        )
        lines.append(f"    敌方兵团: {stacks_str}")

    # ── 矿点 ─────────────────────────────────────────────────────────────────
    mines = g.get("mineOpportunities", [])
    lines.append(f"\n[矿点机会 ({len(mines)}个)]")
    if mines:
        for m in mines:
            lines.append(
                f"  Zone{m['zoneId']} {m['mineType'] or '?'}矿 "
                f"升级{m['upgradeLevel']}/改善{m['improveLevel']} "
                f"canActNow={m['canActNow']} → {m['action']}"
            )
    else:
        lines.append("  无")

    # ── 任务 ─────────────────────────────────────────────────────────────────
    ready = g.get("readyQuests", [])
    lines.append("\n[可领取任务]")
    if ready:
        for q in ready:
            lines.append(f"  - questId={q['questId']} {q['title']} (targetId={q['targetId']})")
    else:
        lines.append("  无")

    # ── 酒馆 ─────────────────────────────────────────────────────────────────
    if extra and extra.get("TavernFrame"):
        tavern = extra["TavernFrame"]
        heroes_available = tavern.get("heroList") or tavern.get("heroes") or []
        if heroes_available:
            lines.append("\n[酒馆英雄]")
            for th in heroes_available:
                lines.append(
                    f"  - id={th.get('id')} {th.get('name')} Lv{th.get('level')} "
                    f"({th.get('factionName','?')}) 价格={th.get('goldCost',th.get('cost','?'))}"
                )

    # ── 未读消息 ──────────────────────────────────────────────────────────────
    if extra and extra.get("MessageBoxFrame"):
        msgs = extra["MessageBoxFrame"]
        msg_list = msgs.get("receivedMessageList") or msgs.get("messageList") or msgs.get("messages") or []
        if msg_list:
            lines.append("\n[未读消息]")
            for m in msg_list[:5]:
                lines.append(f"  - id={m.get('id')} [{m.get('type','?')}] {m.get('title','(无标题)')}")

    return "\n".join(lines)


# ── Battle simulation ─────────────────────────────────────────────────────────

def run_battle_sim(attacker_stacks: list, defender_stacks: list, hero_attack: int = 0) -> dict:
    """Run battle_simulator.py. Returns {wins, honor, output}."""
    sim_input = {
        "attacker": [{"type": s["type"], "power": s["power"], "qty": s["qty"]} for s in attacker_stacks],
        "defender": [{"type": s["type"], "power": s["power"], "qty": s["qty"]} for s in defender_stacks],
        "hero": {"attack": hero_attack},
    }
    sim_path = SKILL_DIR / "battle_simulator.py"
    proc = subprocess.run(
        ["python3", str(sim_path), json.dumps(sim_input)],
        capture_output=True, text=True, timeout=10,
    )
    output = (proc.stdout + proc.stderr).strip()

    wins = "ATTACKER WINS" in output

    # Extract honor value from output
    honor = None
    for line in output.splitlines():
        if "Honor:" in line:
            try:
                honor = float(line.split("Honor:")[1].split()[0])
            except (IndexError, ValueError):
                pass

    return {"wins": wins, "honor": honor, "output": output}


# ── Action execution ──────────────────────────────────────────────────────────

def exec_actions(client: GameClient, actions: list) -> dict:
    """
    Execute a list of action specs with battle-sim gate for combat actions.

    Each action spec:
      {
        "desc": "human label",
        "type": "addAction",
        "params": { ... },
        "isCombatAction": false,
        "attackerStacks": [],   // if isCombatAction
        "defenderStacks": [],   // if isCombatAction
        "heroAttack": 0         // if isCombatAction
      }

    Returns summary dict with per-action results and earliest endDate.
    """
    results = []
    end_dates = []

    for spec in actions:
        desc = spec.get("desc", "?")
        action_type = spec.get("type", "addAction")
        params = spec.get("params", {})
        result_entry = {"desc": desc, "ok": False}

        # Combat actions: gate on battle simulator
        if spec.get("isCombatAction"):
            atk = spec.get("attackerStacks", [])
            def_ = spec.get("defenderStacks", [])
            hero_atk = spec.get("heroAttack", 0)

            if not atk or not def_:
                result_entry["error"] = "missing_stack_data"
                result_entry["simOutput"] = "No stack data provided for combat action."
                results.append(result_entry)
                continue

            sim = run_battle_sim(atk, def_, hero_atk)
            result_entry["simWins"] = sim["wins"]
            result_entry["simHonor"] = sim["honor"]
            result_entry["simOutput"] = sim["output"]

            if not sim["wins"]:
                result_entry["error"] = "battle_sim_loss"
                results.append(result_entry)
                continue

        # Execute
        api_result = client.action(action_type, params)
        result_entry["ok"] = api_result.get("ok", False)

        if api_result.get("ok"):
            data = api_result.get("data", {})
            end_date = data.get("endDate")
            if end_date:
                result_entry["endDate"] = end_date
                result_entry["endsInSecs"] = max(0, end_date - int(time.time()))
                end_dates.append(end_date)
        else:
            err = api_result.get("error", {})
            result_entry["error"] = err.get("code", "UNKNOWN")
            result_entry["hint"] = err.get("hint") or err.get("message", "")

        results.append(result_entry)
        time.sleep(1)  # Brief pause between actions

    return {
        "results": results,
        "nearestEndDate": min(end_dates) if end_dates else None,
        "secsUntilNearest": max(0, min(end_dates) - int(time.time())) if end_dates else None,
    }


# ── CLI commands ──────────────────────────────────────────────────────────────

def cmd_worlds(player: str):
    client = GameClient(player)
    print(json.dumps(client.worlds(), ensure_ascii=False))


def cmd_login(player: str, world_id: int = None):
    client = GameClient(player)
    result = client.login(world_id)
    print(json.dumps(result, ensure_ascii=False))


def cmd_register(player: str, faction_id: int, world_id: int = None):
    client = GameClient(player)
    result = client.register(faction_id, world_id)
    print(json.dumps(result, ensure_ascii=False))


def cmd_state(player: str):
    client = GameClient(player)

    gs_result = client.game_state()
    if not gs_result.get("ok"):
        print(json.dumps(gs_result, ensure_ascii=False))
        return

    gs = gs_result["data"]
    extra = {}

    # Pre-fetch MessageBoxFrame if unread messages exist
    if gs.get("unreadMessages", 0) > 0:
        r = client.action("getContent", {"elParamList": ["MessageBoxFrame"]})
        if r.get("ok"):
            extra["MessageBoxFrame"] = r.get("data", {}).get("MessageBoxFrame", {})

    # Pre-fetch TavernFrame if any hero is idle and there's a city
    idle = any(h.get("_current_slaveActionId") is None for h in gs.get("heroes", []))
    cities = gs.get("cities", [])
    if idle and cities:
        region_id = cities[0].get("regionId")
        if region_id:
            r = client.action("getContent", {
                "elParamList": [{"elementType": "TavernFrame", "elementId": region_id}]
            })
            if r.get("ok"):
                extra["TavernFrame"] = r.get("data", {}).get("TavernFrame", {})

    extra = extra or None
    summary = format_state(gs, extra)
    print(format_state_text(summary, extra))


def cmd_exec(player: str, actions_json: str):
    actions = json.loads(actions_json)
    client = GameClient(player)
    result = exec_actions(client, actions)
    print(json.dumps({"ok": True, "data": result}, ensure_ascii=False))


def cmd_content(player: str, el_param_list_json: str):
    client = GameClient(player)
    el_param_list = json.loads(el_param_list_json)
    result = client.action("getContent", {"elParamList": el_param_list})
    print(json.dumps(result, ensure_ascii=False))


def cmd_wait(seconds: int):
    end = time.time() + seconds
    while time.time() < end:
        remaining = int(end - time.time())
        print(f"Waiting... {remaining}s remaining", file=sys.stderr, flush=True)
        time.sleep(min(30, remaining))
    print(json.dumps({"ok": True, "data": {"waited": seconds}}))


def cmd_sim(attacker_json: str, defender_json: str, hero_attack: int = 0):
    """Direct battle simulation for testing."""
    atk = json.loads(attacker_json)
    def_ = json.loads(defender_json)
    result = run_battle_sim(atk, def_, hero_attack)
    print(result["output"])
    print(json.dumps({"wins": result["wins"], "honor": result["honor"]}))


# ── Entry point ───────────────────────────────────────────────────────────────

def main():
    args = sys.argv[1:]

    if len(args) < 2:
        print(__doc__)
        sys.exit(1)

    player = args[0]
    cmd = args[1]

    try:
        if cmd == "base":
            print(base_url())

        elif cmd == "worlds":
            cmd_worlds(player)

        elif cmd == "login":
            world_id = int(args[2]) if len(args) > 2 else None
            cmd_login(player, world_id)

        elif cmd == "register":
            faction_id = int(args[2]) if len(args) > 2 else 1
            world_id = int(args[3]) if len(args) > 3 else None
            cmd_register(player, faction_id, world_id)

        elif cmd == "state":
            cmd_state(player)

        elif cmd == "content":
            if len(args) < 3:
                print(json.dumps({"ok": False, "error": "content requires elParamList JSON as 3rd argument"}))
                sys.exit(1)
            cmd_content(player, args[2])

        elif cmd == "exec":
            if len(args) < 3:
                print(json.dumps({"ok": False, "error": "exec requires actions JSON as 3rd argument"}))
                sys.exit(1)
            cmd_exec(player, args[2])

        elif cmd == "wait":
            seconds = int(args[2]) if len(args) > 2 else 60
            cmd_wait(seconds)

        elif cmd == "sim":
            # agent_loop.py _ sim '<atk_json>' '<def_json>' [hero_attack]
            cmd_sim(args[2], args[3], int(args[4]) if len(args) > 4 else 0)

        else:
            print(json.dumps({"ok": False, "error": f"Unknown command: {cmd}"}))
            sys.exit(1)

    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        print(json.dumps({"ok": False, "error": str(e)}), file=sys.stderr)
        raise


if __name__ == "__main__":
    main()
