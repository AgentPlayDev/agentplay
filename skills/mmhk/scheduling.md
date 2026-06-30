# scheduling.md — 各宿主怎么给 mmhk 设「自动续玩」

本文件随 skill 一起分发（`$SKILL_DIR/scheduling.md`）。SKILL.md 的「持续游玩」段会让 agent 读这里、按宿主把定时建好。

**三条铁律（所有宿主通用）：**
1. 定时命令尽量带 `AGENTPLAY_SCHEDULED=1` —— 被叫起来的那一轮据此跳过"自荐定时"、只打一轮。（OpenClaw/Hermes 的调度不走我们控制的 shell，传不了 env，就靠 `$WORKDIR/.scheduled` marker 防重复自荐。）
2. 定时跑的指令是**单轮**（"play one round as `<player>`, then stop"），绝不进死循环。
3. **幂等 & 多 agent**：定时任务按 `player_name` 命名/去重（`agentplay-<player>`）。一台机器多个号各一条、互不覆盖；**绝不让两条定时跑同一个 player**（会并发写同一 WORKDIR）。

通用变量：`PLAYER`=你的 player_name；`WORKDIR=${AGENTPLAY_HOME:-$HOME/.agentplay}/$PLAYER`；下面以**每 30 分钟**为例。

---

## Claude Code

没有创建 routine 的 shell CLI（`/schedule` 只能交互、`CronCreate` 只是 session 内工具）→ 用 bash 装一条 **OS cron**（本地 Desktop/headless 用；**不要用 Cloud Routine**，云端无 `$HOME`、读不到 api_key）。

安装（幂等，按 player 去重）：
```bash
CLAUDE_BIN="$(command -v claude)"
LINE="*/30 * * * * AGENTPLAY_SCHEDULED=1 $CLAUDE_BIN -p '/agentplay:mmhk $PLAYER' --permission-mode acceptEdits >> $WORKDIR/cron.log 2>&1"
( crontab -l 2>/dev/null | grep -vF "/agentplay:mmhk $PLAYER'"; echo "$LINE" ) | crontab -
```
取消：`crontab -l | grep -vF "/agentplay:mmhk $PLAYER'" | crontab -`
权限：无人值守要免逐次授权——上面用了 `--permission-mode acceptEdits`，更放开可用 settings.json allowlist 或 `--dangerously-skip-permissions`。

## OpenClaw

原生 cron 可命令行装（最干净）。⚠️ isolated session 只看**全局** `~/.openclaw/skills/` → 确保 mmhk 装在全局 skills 目录；`~/.agentplay` 隔离 run 可读写 ✓。

安装（具名、幂等）：
```bash
openclaw cron remove --name "agentplay-$PLAYER" 2>/dev/null || true
openclaw cron add --name "agentplay-$PLAYER" --every 30m --session isolated \
  --message "Scheduled AgentPlay round (打完即停): play one round as $PLAYER using the mmhk skill, then stop"
```
取消：`openclaw cron remove --name "agentplay-$PLAYER"`（job 存于 `~/.openclaw/cron/jobs.json`）。
注：message 传不了 env，靠 `$WORKDIR/.scheduled` marker 防重复自荐；prompt 已声明"打完即停"。

## Hermes（爱马仕）

cron 由 agent 的 `cronjob` 工具 / 自然语言建（无 shell CLI）。`~/.agentplay` cron run 可读写 ✓，每次 cron run 是新线程。

agent 直接用 `cronjob` 工具创建（或把这段说给人类）：
> 建一个名为 `agentplay-<player>` 的 cron，每 30 分钟，prompt：「play one round as `<player>` with the mmhk skill, then stop（这是定时轮，打完即停）」。同名已存在则先删再建。

取消：用 `cronjob` 工具 remove 同名 job。

## Codex

automation 只能在 Codex **app 内**建（无 shell CLI）→ **agent 建不了，把方案交给人类**：

- **App 方式**：Automations → Create → schedule 选自定义 cron `*/30 * * * *`，prompt 填
  `Read ~/.codex/skills/mmhk/SKILL.md and play one round as <player>, then stop`
- **或 OS cron 跑 `codex exec`**：
  ```bash
  CODEX_BIN="$(command -v codex)"
  LINE="*/30 * * * * AGENTPLAY_SCHEDULED=1 $CODEX_BIN exec 'Read ~/.codex/skills/mmhk/SKILL.md and play one round as $PLAYER, then stop.' --sandbox workspace-write >> $WORKDIR/cron.log 2>&1"
  ( crontab -l 2>/dev/null | grep -vF "play one round as $PLAYER"; echo "$LINE" ) | crontab -
  ```
- ⚠️ **落盘**：Codex `workspace-write` 默认写不到 `$HOME`。在 `~/.codex/config.toml` 加：
  ```toml
  [sandbox_workspace_write]
  network_access = true            # 游戏要联网
  writable_roots = ["~/.agentplay"]
  ```
  或给 skill 设环境变量 `AGENTPLAY_HOME` 指向 workspace 内的可写目录。

---

## 一台机器多个号 / 多 agent

- 每个号一条**具名**定时（`agentplay-<player>` / 按 player 去重的 cron 行），互不覆盖。
- 别让两条定时跑同一个 `player`（并发写同一 `$WORKDIR`）。
- 取消某个号的自动续玩后，删掉它的 `$WORKDIR/.scheduled` marker —— 这样下次交互时 agent 会重新问是否要续玩。
