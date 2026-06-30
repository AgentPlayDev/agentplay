#!/usr/bin/env python3
"""
MMHK Battle Simulator
Replicates the game's resolveBattle logic from GameUtils.class.php.

Usage:
    python3 battle_simulator.py  (runs built-in example)

Or import and use programmatically:
    from battle_simulator import simulate_battle, UnitStack
"""

import math
import json
import sys

# --- Game Constants (from heroesweb_conf.confvalue) ---
BATTLE_UNIT_TYPE_BONUS = 0.5       # +50% for type advantage
BATTLE_HERO_ATTACK_BONUS = 0.005   # per attack point
BATTLE_HERO_DEFENSE_BONUS = 0.005  # per defense point
BATTLE_ATTRITION_RATE = 0.3        # 30% of routed units die permanently
NO_BATTLE_ARMY_POWER_RATIO = 7     # defender/attacker ratio threshold

# Type counter: key beats value
TYPE_COUNTER = {
    "INFANTRY": "CAVALRY",
    "CAVALRY": "SHOOTER",
    "SHOOTER": "INFANTRY",
}


class UnitStack:
    def __init__(self, unit_type, unit_power, quantity, name=""):
        self.unit_type = unit_type       # INFANTRY / CAVALRY / SHOOTER
        self.unit_power = unit_power     # power per unit
        self.quantity = quantity          # number of units
        self.name = name or f"{unit_type}(pw={unit_power})"
        self.routed = 0
        self.attrition_lost = 0

    def get_power(self):
        return self.unit_power * self.quantity

    def __repr__(self):
        return f"{self.name} x{self.quantity} (pw={self.unit_power}, type={self.unit_type})"


class HeroStats:
    def __init__(self, attack=0, defense=0, magic=0,
                 skill_attack_pct=0, skill_defense_pct=0,
                 skill_attack_infantry_pct=0, skill_attack_cavalry_pct=0, skill_attack_shooter_pct=0,
                 skill_defense_infantry_pct=0, skill_defense_cavalry_pct=0, skill_defense_shooter_pct=0,
                 skill_attack_per_unit=0, skill_defense_per_unit=0,
                 skill_attrition_increase=0, skill_attrition_decrease=0,
                 morale_pct=None):
        self.attack = attack
        self.defense = defense
        self.magic = magic
        # Global % bonuses (as decimal, e.g. 0.03 for 3%)
        self.skill_attack_pct = skill_attack_pct / 100 if skill_attack_pct >= 1 else skill_attack_pct
        self.skill_defense_pct = skill_defense_pct / 100 if skill_defense_pct >= 1 else skill_defense_pct
        # Type-specific % bonuses (only apply when having type advantage)
        self.skill_attack_type = {
            "INFANTRY": skill_attack_infantry_pct / 100 if skill_attack_infantry_pct >= 1 else skill_attack_infantry_pct,
            "CAVALRY": skill_attack_cavalry_pct / 100 if skill_attack_cavalry_pct >= 1 else skill_attack_cavalry_pct,
            "SHOOTER": skill_attack_shooter_pct / 100 if skill_attack_shooter_pct >= 1 else skill_attack_shooter_pct,
        }
        self.skill_defense_type = {
            "INFANTRY": skill_defense_infantry_pct / 100 if skill_defense_infantry_pct >= 1 else skill_defense_infantry_pct,
            "CAVALRY": skill_defense_cavalry_pct / 100 if skill_defense_cavalry_pct >= 1 else skill_defense_cavalry_pct,
            "SHOOTER": skill_defense_shooter_pct / 100 if skill_defense_shooter_pct >= 1 else skill_defense_shooter_pct,
        }
        # Per-unit flat bonuses
        self.skill_attack_per_unit = skill_attack_per_unit
        self.skill_defense_per_unit = skill_defense_per_unit
        # Attrition modifiers (as decimal)
        self.skill_attrition_increase = skill_attrition_increase / 100 if skill_attrition_increase > 1 else skill_attrition_increase
        self.skill_attrition_decrease = skill_attrition_decrease / 100 if skill_attrition_decrease > 1 else skill_attrition_decrease
        # Morale (pure faction army bonus)
        self.morale_pct = morale_pct


def has_type_advantage(attacker_type, defender_type):
    return TYPE_COUNTER.get(attacker_type) == defender_type


def simulate_battle(attacker_stacks, defender_stacks,
                    attacker_hero=None, defender_hero=None,
                    city_defense_pct=0, pillage_defense_pct=0,
                    action_type="HERO_ATTACK_NPC", verbose=True):
    """
    Simulate a full battle.

    Args:
        attacker_stacks: list of UnitStack (ordered by position, first fights first)
        defender_stacks: list of UnitStack (will be sorted by power descending)
        attacker_hero: HeroStats or None (NPC has no hero)
        defender_hero: HeroStats or None (NPC has no hero)
        city_defense_pct: city defense bonus % (only for ATTACK_REGION/SIEGE_ASSAULT)
        pillage_defense_pct: pillage defense % (only for PILLAGE)
        action_type: battle type string
        verbose: print round details

    Returns:
        dict with battle results
    """
    if not attacker_hero:
        attacker_hero = HeroStats()
    if not defender_hero:
        defender_hero = HeroStats()

    # Deep copy stacks
    atk_stacks = [UnitStack(s.unit_type, s.unit_power, s.quantity, s.name) for s in attacker_stacks]
    def_stacks = [UnitStack(s.unit_type, s.unit_power, s.quantity, s.name) for s in defender_stacks]

    # Sort defender by power descending (game logic)
    def_stacks.sort(key=lambda s: s.get_power(), reverse=True)

    # Check no-battle condition
    atk_total_base = sum(s.get_power() for s in atk_stacks)
    def_total_base = sum(s.get_power() for s in def_stacks)

    if atk_total_base == 0:
        return {"attacker_wins": False, "reason": "no_army"}

    if def_total_base / atk_total_base >= NO_BATTLE_ARMY_POWER_RATIO:
        if verbose:
            print(f"NO BATTLE: defender power ({def_total_base}) / attacker power ({atk_total_base}) = {def_total_base/atk_total_base:.1f} >= {NO_BATTLE_ARMY_POWER_RATIO}")
        return {"attacker_wins": False, "reason": "no_battle", "ratio": def_total_base / atk_total_base}

    is_city_battle = action_type in ("HERO_ATTACK_REGION_ATTACK", "HERO_SIEGE_ASSAULT")
    is_pillage = action_type == "HERO_PILLAGE_ZONE_PILLAGE"

    atk_idx = 0
    def_idx = 0
    rounds = []
    round_num = 0

    if verbose:
        print("=" * 60)
        print("BATTLE START")
        print(f"  Attacker: {atk_total_base} base power, hero atk={attacker_hero.attack}")
        for s in atk_stacks:
            print(f"    [{s.unit_type}] {s.name} x{s.quantity} (pw={s.unit_power}, total={s.get_power()})")
        print(f"  Defender: {def_total_base} base power, hero def={defender_hero.defense}")
        for s in def_stacks:
            print(f"    [{s.unit_type}] {s.name} x{s.quantity} (pw={s.unit_power}, total={s.get_power()})")
        print("=" * 60)

    while atk_idx < len(atk_stacks) and def_idx < len(def_stacks):
        atk_stack = atk_stacks[atk_idx]
        def_stack = def_stacks[def_idx]

        if atk_stack.quantity <= 0:
            atk_idx += 1
            continue
        if def_stack.quantity <= 0:
            def_idx += 1
            continue

        round_num += 1
        round_info = {"round": round_num}

        atk_base = atk_stack.get_power()
        def_base = def_stack.get_power()

        # Type advantage
        atk_has_advantage = has_type_advantage(atk_stack.unit_type, def_stack.unit_type)
        def_has_advantage = has_type_advantage(def_stack.unit_type, atk_stack.unit_type)

        # --- Attacker bonuses ---
        atk_type_bonus = atk_base * BATTLE_UNIT_TYPE_BONUS if atk_has_advantage else 0
        atk_skill_global = atk_base * attacker_hero.skill_attack_pct
        atk_skill_type = 0
        if atk_has_advantage:
            atk_skill_type = atk_base * attacker_hero.skill_attack_type.get(atk_stack.unit_type, 0)
        atk_hero_bonus = atk_base * max(0, attacker_hero.attack) * BATTLE_HERO_ATTACK_BONUS
        atk_per_unit = attacker_hero.skill_attack_per_unit * atk_stack.quantity

        atk_total_bonus = math.floor(atk_type_bonus + atk_skill_global + atk_skill_type + atk_hero_bonus) + atk_per_unit
        atk_total = atk_base + atk_total_bonus

        # --- Defender bonuses ---
        def_type_bonus = def_base * BATTLE_UNIT_TYPE_BONUS if def_has_advantage else 0
        def_skill_global = def_base * defender_hero.skill_defense_pct
        def_skill_type = 0
        if def_has_advantage:
            def_skill_type = def_base * defender_hero.skill_defense_type.get(def_stack.unit_type, 0)
        def_hero_bonus = def_base * max(0, defender_hero.defense) * BATTLE_HERO_DEFENSE_BONUS
        def_per_unit = defender_hero.skill_defense_per_unit * def_stack.quantity

        def_city_bonus = def_base * city_defense_pct / 100 if is_city_battle else 0
        def_pillage_bonus = def_base * pillage_defense_pct / 100 if is_pillage else 0

        def_total_bonus = math.floor(def_type_bonus + def_skill_global + def_skill_type + def_hero_bonus + def_city_bonus + def_pillage_bonus) + def_per_unit
        def_total = def_base + def_total_bonus

        # --- Round result ---
        attacker_wins_round = atk_total >= def_total
        overrun = False
        atk_routed = 0
        def_routed = 0

        if attacker_wins_round:
            diff = atk_total - def_total
            if diff > atk_base:
                overrun = True
                atk_routed = 0
            else:
                atk_routed = math.floor((def_base + def_total_bonus - atk_total_bonus) / atk_stack.unit_power)
                atk_routed = max(0, min(atk_routed, atk_stack.quantity))
            def_routed = def_stack.quantity  # full defender stack routed
        else:
            diff = def_total - atk_total
            if diff > def_base:
                overrun = True
                def_routed = 0
            else:
                def_routed = math.floor((atk_base + atk_total_bonus - def_total_bonus) / def_stack.unit_power)
                def_routed = max(0, min(def_routed, def_stack.quantity))
            atk_routed = atk_stack.quantity  # full attacker stack routed

        # Apply attrition
        atk_attrition_rate = BATTLE_ATTRITION_RATE + defender_hero.skill_attrition_increase - attacker_hero.skill_attrition_decrease
        def_attrition_rate = BATTLE_ATTRITION_RATE + attacker_hero.skill_attrition_increase - defender_hero.skill_attrition_decrease

        atk_attrition = 0
        if atk_routed > 0:
            atk_attrition_points = atk_routed * atk_attrition_rate * 100
            atk_attrition = math.floor(atk_attrition_points / 100)
            if atk_attrition_points > 0 and atk_attrition == 0:
                atk_attrition = 1

        def_attrition = 0
        if def_routed > 0:
            def_attrition_points = def_routed * def_attrition_rate * 100
            def_attrition = math.floor(def_attrition_points / 100)
            if def_attrition_points > 0 and def_attrition == 0:
                def_attrition = 1

        # Update quantities: reduce by routed (not attrition) for combat purposes
        # Routed units can't fight in subsequent rounds; attrition determines permanent loss after battle
        if attacker_wins_round:
            atk_stack.quantity -= atk_routed  # routed units removed from combat
            atk_stack.routed += atk_routed
            atk_stack.attrition_lost += atk_attrition
            def_stack.quantity = 0
            def_stack.routed += def_routed
            def_stack.attrition_lost += def_attrition
            if not overrun:
                atk_idx += 1 if atk_stack.quantity <= 0 else 0
            def_idx += 1
        else:
            def_stack.quantity -= def_routed  # routed units removed from combat
            def_stack.routed += def_routed
            def_stack.attrition_lost += def_attrition
            atk_stack.quantity = 0
            atk_stack.routed += atk_routed
            atk_stack.attrition_lost += atk_attrition
            atk_idx += 1
            if not overrun:
                def_idx += 1 if def_stack.quantity <= 0 else 0

        round_info.update({
            "attacker": f"{atk_stack.name} x{atk_stack.quantity + (atk_attrition if attacker_wins_round else atk_routed)}",
            "defender": f"{def_stack.name} x{def_stack.quantity + (def_attrition if not attacker_wins_round else def_routed)}",
            "atk_base": atk_base, "atk_bonus": atk_total_bonus, "atk_total": atk_total,
            "def_base": def_base, "def_bonus": def_total_bonus, "def_total": def_total,
            "atk_type_adv": atk_has_advantage, "def_type_adv": def_has_advantage,
            "attacker_wins": attacker_wins_round, "overrun": overrun,
            "atk_routed": atk_routed, "def_routed": def_routed,
            "atk_attrition": atk_attrition, "def_attrition": def_attrition,
        })
        rounds.append(round_info)

        if verbose:
            winner = "ATK" if attacker_wins_round else "DEF"
            ov = " OVERRUN!" if overrun else ""
            type_info = ""
            if atk_has_advantage:
                type_info = f" [{atk_stack.unit_type}>{def_stack.unit_type}]"
            elif def_has_advantage:
                type_info = f" [{def_stack.unit_type}>{atk_stack.unit_type}]"
            print(f"\nRound {round_num}:{type_info}")
            print(f"  ATK: {atk_stack.name} base={atk_base} +bonus={atk_total_bonus} = {atk_total}")
            print(f"  DEF: {def_stack.name} base={def_base} +bonus={def_total_bonus} = {def_total}")
            print(f"  => {winner} wins{ov}")
            if atk_routed > 0:
                print(f"     ATK routed={atk_routed}, permanent loss={atk_attrition}")
            if def_routed > 0:
                print(f"     DEF routed={def_routed}, permanent loss={def_attrition}")

    # Restore final quantities: during combat quantity tracks "available for combat" (original - routed),
    # but final surviving = original - attrition_lost
    # For attackers: routed units partially recover (only attrition is permanent loss)
    for s in atk_stacks:
        original = s.quantity + s.routed
        s.quantity = max(0, original - s.attrition_lost)
    # For defenders (NPC): routed units are fully destroyed (no attrition recovery)
    # In PvP, defenders also recover, but vs NPC they don't
    # We keep defender quantities as-is (already reduced by routed during combat)

    # Final result
    atk_surviving = sum(s.quantity for s in atk_stacks if s.quantity > 0)
    def_surviving = sum(s.quantity for s in def_stacks if s.quantity > 0)
    attacker_wins = atk_surviving > 0 and def_surviving == 0

    # Honor / XP calculation
    honor = def_total_base / atk_total_base if atk_total_base > 0 else 0
    honor_modifier = honor - 1

    if verbose:
        print("\n" + "=" * 60)
        print(f"RESULT: {'ATTACKER WINS' if attacker_wins else 'DEFENDER WINS'}")
        print(f"  Attacker survivors:")
        for s in atk_stacks:
            orig = s.quantity + s.attrition_lost
            if s.quantity > 0:
                print(f"    {s.name}: {orig} -> {s.quantity} (lost {s.attrition_lost})")
            else:
                print(f"    {s.name}: {orig} -> 0 (lost {s.attrition_lost})")
        print(f"  Defender survivors:")
        for s in def_stacks:
            orig = s.quantity + s.attrition_lost
            if s.quantity > 0:
                print(f"    {s.name}: {orig} -> {s.quantity} (lost {s.attrition_lost})")
            else:
                print(f"    {s.name}: {orig} -> 0 (lost {s.attrition_lost})")
        if not any(s.quantity > 0 for s in def_stacks):
            print(f"    (all destroyed)")
        print(f"\n  Honor: {honor:.3f} (modifier: {honor_modifier:+.3f})")
        print(f"  Total rounds: {round_num}")

        # XP optimization advice
        if attacker_wins:
            if honor < 0.5:
                ideal_power = math.ceil(def_total_base * 1.3)
                excess = atk_total_base - ideal_power
                print(f"\n  ⚠ XP WARNING: Honor {honor:.2f} is very low. You are bringing {atk_total_base} power vs {def_total_base} enemy.")
                print(f"    XP modifier: {honor_modifier:+.0%} (up to -85% XP penalty)")
                print(f"    SUGGESTION: Only bring ~{ideal_power} power (reduce by ~{excess}). Use SPLIT to leave excess troops in garrison.")
                print(f"    Target honor ~1.0 for maximum XP gain.")
            elif honor < 0.8:
                ideal_power = math.ceil(def_total_base * 1.3)
                print(f"\n  ⚠ XP NOTE: Honor {honor:.2f} means reduced XP ({honor_modifier:+.0%}).")
                print(f"    Consider bringing ~{ideal_power} power instead of {atk_total_base} for better XP.")
            elif honor >= 1.0:
                print(f"\n  ✓ EXCELLENT: Honor {honor:.2f} — maximum XP bonus ({honor_modifier:+.0%})!")
        print("=" * 60)

    return {
        "attacker_wins": attacker_wins,
        "rounds": rounds,
        "total_rounds": round_num,
        "attacker_survivors": [(s.name, s.quantity, s.attrition_lost) for s in atk_stacks],
        "defender_survivors": [(s.name, s.quantity, s.attrition_lost) for s in def_stacks],
        "honor": honor,
        "honor_modifier": honor_modifier,
        "atk_total_base": atk_total_base,
        "def_total_base": def_total_base,
    }


def quick_estimate(atk_power, def_power, atk_type=None, def_type=None,
                   hero_attack=0, hero_defense=0):
    """
    Quick power estimate without full simulation.
    Returns estimated outcome string.
    """
    atk_bonus = 0
    def_bonus = 0

    if atk_type and def_type:
        if has_type_advantage(atk_type, def_type):
            atk_bonus += atk_power * BATTLE_UNIT_TYPE_BONUS

    atk_bonus += atk_power * max(0, hero_attack) * BATTLE_HERO_ATTACK_BONUS
    def_bonus += def_power * max(0, hero_defense) * BATTLE_HERO_DEFENSE_BONUS

    atk_total = atk_power + atk_bonus
    def_total = def_power + def_bonus

    if atk_total >= def_total:
        if (atk_total - def_total) > atk_power:
            return "OVERRUN (zero loss)"
        ratio = def_total / atk_total if atk_total > 0 else 0
        if ratio < 0.5:
            return "EASY WIN (minimal loss)"
        elif ratio < 0.8:
            return "WIN (moderate loss)"
        else:
            return "CLOSE WIN (heavy loss)"
    else:
        return "LOSE"


def parse_cli_input(data):
    """
    Parse JSON input from command line.

    Full simulation format:
    {
      "attacker": [{"type":"INFANTRY","power":71,"qty":50,"name":"Imp"}, ...],
      "defender": [{"type":"SHOOTER","power":410,"qty":5}, ...],
      "hero": {"attack":5, "defense":3, "skill_attack_pct":3, "skill_attack_cavalry_pct":15},
      "defenderHero": {"defense":2},
      "cityDefense": 0,
      "actionType": "HERO_ATTACK_NPC"
    }

    Quick estimate format:
    {
      "quick": true,
      "atkPower": 8000,
      "defPower": 3000,
      "atkType": "CAVALRY",
      "defType": "SHOOTER",
      "heroAttack": 5
    }
    """
    if data.get("quick"):
        result = quick_estimate(
            data["atkPower"], data["defPower"],
            data.get("atkType"), data.get("defType"),
            data.get("heroAttack", 0), data.get("heroDefense", 0)
        )
        print(result)
        return

    atk_stacks = [UnitStack(s["type"], s["power"], s["qty"], s.get("name", ""))
                  for s in data["attacker"]]
    def_stacks = [UnitStack(s["type"], s["power"], s["qty"], s.get("name", ""))
                  for s in data["defender"]]

    hero_data = data.get("hero", {})
    atk_hero = HeroStats(**hero_data) if hero_data else None

    def_hero_data = data.get("defenderHero", {})
    def_hero = HeroStats(**def_hero_data) if def_hero_data else None

    simulate_battle(
        atk_stacks, def_stacks,
        attacker_hero=atk_hero, defender_hero=def_hero,
        city_defense_pct=data.get("cityDefense", 0),
        pillage_defense_pct=data.get("pillageDefense", 0),
        action_type=data.get("actionType", "HERO_ATTACK_NPC"),
    )


if __name__ == "__main__":
    if len(sys.argv) > 1:
        parse_cli_input(json.loads(sys.argv[1]))
    else:
        print("Usage: python3 battle_simulator.py '<JSON>'")
        print()
        print("Examples:")
        print()
        print("Quick estimate:")
        print("""  python3 battle_simulator.py '{"quick":true,"atkPower":8000,"defPower":3000,"atkType":"CAVALRY","defType":"SHOOTER","heroAttack":5}'""")
        print()
        print("Full simulation:")
        print("""  python3 battle_simulator.py '{"attacker":[{"type":"CAVALRY","power":370,"qty":15,"name":"Hell Hound"}],"defender":[{"type":"SHOOTER","power":410,"qty":5,"name":"Gnome Shooter"}],"hero":{"attack":5}}'""")
