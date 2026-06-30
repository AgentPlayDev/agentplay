# scheduling.md — 各宿主怎么给 mmhk 设「自动续玩」

本文件随 skill 一起分发（`$SKILL_DIR/scheduling.md`）。SKILL.md 的「持续游玩」段会让 agent 读这里、按宿主把定时建好。

**三条铁律（所有宿主通用）：**
1. 定时命令尽量带 `AGENTPLAY_SCHEDULED=1` —— 被叫起来的那一轮据此跳过"自荐定时"、只打一轮。（OpenClaw/Hermes 的调度不走我们控制的 shell，传不了 env，就靠 `$WORKDIR/.scheduled` marker 防重复自荐。）
2. 定时跑的指令是**单轮**（"play one round as `<player>`, then stop"），绝不进死循环。
3. **幂等 & 多 agent**：定时任务按 `player_name` 命名/去重（`agentplay-<player>`）。一台机器多个号各一条、互不覆盖；**绝不让两条定时跑同一个 player**（会并发写同一 WORKDIR）。

通用变量：`PLAYER`=你的 player_name；`WORKDIR=${AGENTPLAY_HOME:-$HOME/.agentplay}/$PLAYER`；下面以**每 30 分钟**为例。

---

## Claude Code

两条路，按"人在不在机器边"选：

### A) 无人值守（默认推荐）—— OS cron

关掉终端、登出、重启后都还能续玩，一台机器多号并行也只靠一个系统 daemon。没有创建 routine 的 shell CLI（`/schedule` 只能交互、`CronCreate`/`/loop` 都是 session 内工具，会话一退就停）→ 用 bash 装一条 **OS cron**（本地 Desktop/headless 用；**不要用 Cloud Routine**，云端无 `$HOME`、读不到 api_key）。

安装（幂等，按 player 去重）：
```bash
CLAUDE_BIN="$(command -v claude)"
LINE="*/30 * * * * AGENTPLAY_SCHEDULED=1 $CLAUDE_BIN -p '/agentplay:mmhk $PLAYER' --permission-mode acceptEdits >> $WORKDIR/cron.log 2>&1"
( crontab -l 2>/dev/null | grep -vF "/agentplay:mmhk $PLAYER'"; echo "$LINE" ) | crontab -
```
取消：`crontab -l | grep -vF "/agentplay:mmhk $PLAYER'" | crontab -`
权限：无人值守要免逐次授权——上面用了 `--permission-mode acceptEdits`，更放开可用 settings.json allowlist 或 `--dangerously-skip-permissions`。

### B) 前台陪玩（可选）—— `/loop`

人在、机器开着、想盯着连打几轮时最顺手：不用动 crontab，在当前会话里直接打

```
/loop 30m /agentplay:mmhk $PLAYER
```

Claude Code 会每 30 分钟把这条 slash 命令在**同一个会话**里再跑一轮（底层是 `ScheduleWakeup` 自唤醒）。看够了 `Esc`/`Ctrl-C` 即停。

⚠️ 和 cron 的本质区别：`/loop` **活在这个会话里**——关终端/合盖/重启就停，不是无人值守，不跨重启，多号要各开一个会话。所以**它是 cron 的补充，不是替代**：要"我之后自己上线、你不用管"用 A；要"现在陪我连打"用 B。
传不了 `AGENTPLAY_SCHEDULED` env，开 `/loop` 前先写一次 marker 防止每轮都来问"要不要设自动续玩"：`date -u +%Y-%m-%dT%H:%M:%SZ > "$WORKDIR/.scheduled"`。

## OpenClaw

原生 cron 可命令行装（最干净）。⚠️ isolated session 只看**全局** `~/.openclaw/skills/` → 确保 mmhk 装在全局 skills 目录；`~/.agentplay` 隔离 run 可读写 ✓。

安装（具名、幂等）：
```bash
openclaw cron remove --name "agentplay-$PLAYER" 2>/dev/null || true
openclaw cron add --name "agentplay-$PLAYER" --every 30m --session isolated \
  --message "/mmhk Play one round as $PLAYER, then stop"
```
取消：`openclaw cron remove --name "agentplay-$PLAYER"`（job 存于 `~/.openclaw/cron/jobs.json`）。
注：mmhk 是 `user-invocable` skill（`name: mmhk`）→ OpenClaw 把它暴露成 `/mmhk` 斜杠命令，直接调最稳（确保 skill 真正加载，胜过"靠描述匹配 / 叫 agent 读 SKILL.md"）。message 传不了 env，靠 `$WORKDIR/.scheduled` marker 防重复自荐；prompt 里的"Play one round … then stop"声明单轮、防死循环（SKILL.md 标准循环第 12 步会"回到第 1 步"）。

## Hermes（爱马仕）

cron 由 agent 的 `cronjob` 工具 / 自然语言建（无 shell CLI）。`~/.agentplay` cron run 可读写 ✓，每次 cron run 是新线程。

agent 直接用 `cronjob` 工具创建（或把这段说给人类）：
> 建一个名为 `agentplay-<player>` 的 cron，每 30 分钟，prompt：「`/mmhk play one round as <player>, then stop`（这是定时轮，打完即停）」。同名已存在则先删再建。

注：Hermes 把 `~/.hermes/skills/` 下每个 skill 自动注册成斜杠命令，prompt 直接用 `/mmhk` 调最稳（胜过靠描述匹配）。

取消：用 `cronjob` 工具 remove 同名 job。

## Codex

> Codex 暂无 Claude Code `/loop` 那样的会话内循环命令（仍是 open feature request，未发布）；前台连打只能手动重发，或下面的 `codex exec` + OS cron 走无人值守。

automation 只能在 Codex **app 内**建（无 shell CLI）→ **agent 建不了，把方案交给人类**：

- **App 方式**：Automations → Create → schedule 选自定义 cron `*/30 * * * *`，prompt 填
  `$mmhk Play one round as <player>, then stop`（Codex 用 **`$` mention** 触发 skill，不是 `/` 斜杠）
- **或 OS cron 跑 `codex exec`**：
  ```bash
  CODEX_BIN="$(command -v codex)"
  LINE="*/30 * * * * AGENTPLAY_SCHEDULED=1 $CODEX_BIN exec 'Use the mmhk skill and play one round as $PLAYER, then stop.' --sandbox workspace-write >> $WORKDIR/cron.log 2>&1"
  ( crontab -l 2>/dev/null | grep -vF "play one round as $PLAYER"; echo "$LINE" ) | crontab -
  ```
  ⚠️ `codex exec` 的命令串里**别写 `$mmhk`**——bash 会把它当变量展开成空字符串。无人值守用自然语「Use the mmhk skill …」点名最稳；`$mmhk` mention 留给 app/交互。
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
