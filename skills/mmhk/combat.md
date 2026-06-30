# 战斗篇

## 影响战斗的六大因素

### 1. 兵种克制

三角克制关系，克制方获得 +50% 基础战力加成（CONFVALUE_BATTLE_UNIT_TYPE_BONUS = 0.5）：

```
步兵(INFANTRY) → 克制 → 骑兵(CAVALRY)
骑兵(CAVALRY) → 克制 → 弓手(SHOOTER)
弓手(SHOOTER) → 克制 → 步兵(INFANTRY)
```

克制的作用不仅是 +50% 战力加成，还会激活英雄的兵种专属技能。

### 2. 英雄属性

攻击方使用 `hero.attack` 属性，防守方使用 `hero.defense` 属性。

```
英雄攻击力加成 = 兵团基础战力 × max(0, hero.attack) × CONFVALUE_BATTLE_HERO_ATTACK_BONUS
英雄防御力加成 = 兵团基础战力 × max(0, hero.defense) × CONFVALUE_BATTLE_HERO_DEFENSE_BONUS
```

英雄属性来自 gameState 中 `heroes[].attack` 和 `heroes[].defense`，每次升级可以加点。

### 3. 英雄技能

技能分两大类：

**百分比类技能（乘以基础战力）：**
- 全军加成：`ARMY_ATTACK_POWER_INCREASE`（攻击时）/ `ARMY_DEFENSE_POWER_INCREASE`（防守时）— 对所有兵种生效
- 兵种专属加成：`ARMY_ATTACK_POWER_INCREASE_INFANTRY` 等 — **仅在该兵种对对手有克制优势时生效**

**单位加成类技能（按数量叠加）：**
- `ARMY_ATTACK_POWER_PER_UNIT_INCREASE` / `ARMY_DEFENSE_POWER_PER_UNIT_INCREASE` — 每个单位额外加固定战力点数
- 同样有全军和兵种专属两种

**特殊被动技能：**
- `ATTRITION_RATE_INCREASE` — 提高敌方消耗率
- `ATTRITION_RATE_DECREASE` — 降低己方消耗率
- `TOWN_DEFENSE_INCREASE` — 提高城防加成
- `TOWN_DEFENSE_DECREASE` — 降低对方城防加成
- `PRE_FIGHT_ATTACK_SHOOTER` — 战前弓手齐射（独立伤害阶段）
- `ARMY_POWER_INCREASE_PURE` — 纯种族军队士气加成

技能数值取决于等级，通过 `getContent HeroFrame` 查询英雄详情。

### 4. 英雄装备（神器）

神器提供与技能同类的加成。防守方的神器只计算攻击类加成（不计技能），攻击方的技能和神器都纳入计算。

### 5. 防守建筑

城防加成仅在以下战斗类型中生效：
- **攻城战**（HERO_ATTACK_REGION_ATTACK）— 攻击玩家城市
- **围攻突击**（HERO_SIEGE_ASSAULT）— 围攻突击

城防公式：`防御方兵团战力 × 城防百分比`

**掠夺战**（HERO_PILLAGE_ZONE_PILLAGE）有单独的 `pillageDefense` 加成。

攻击 NPC（HERO_ATTACK_NPC_ATTACK）无城防加成。

### 6. 魔法

魔法在每个回合的**战斗交锋前后**分别施放：
- 回合前施法：伤害、增益/减益、召唤
- 回合后施法：复活（在伤亡结算后恢复单位）

**四大魔法学派**：

| 学派 | 方向 | 代表法术 |
|------|------|----------|
| 毁灭 (DESTRUCTION) | 伤害 | LIGHTNING_BOLT, METEOR_SHOWER, CHAIN_LIGHTNING, IMPLOSION |
| 黑暗 (DARK) | 减益 | WEAKNESS, VULNERABILITY, PLAGUE, WORD_OF_DEATH |
| 光明 (LIGHT) | 增益 | DIVINE_STRENGTH, BLESS, RESURRECTION, WORD_OF_LIGHT |
| 召唤 (SUMMON) | 特殊 | RAISE_DEAD, SUMMON_ELEMENTALS, CONJURE_PHOENIX |

**法术效果类型**：

| 类型 | 说明 | 施放时机 |
|------|------|----------|
| DAMAGE | 直接伤害敌方兵团（消灭单位） | 回合前 |
| STACK_ATTACK_BONUS | 增加兵团攻击战力 | 回合前 |
| STACK_DEFENSE_BONUS | 增加兵团防御战力 | 回合前 |
| HERO_ATTACK_BONUS | 增加英雄攻击属性 | 回合前 |
| HERO_DEFENSE_BONUS | 增加英雄防御属性 | 回合前 |
| TEMPORARY_RESURRECTION | 临时复活击溃单位（回合后消失） | 回合后 |
| PERMANENT_RESURRECTION | 永久复活击溃单位 | 回合后 |
| SUMMONING | 召唤临时部队参战 | 回合前 |
| FORTIFICATION_BONUS | 增加城防百分比 | 回合前 |

**法术伤害公式**：`效果值 = 法术基础值 × 英雄魔力(magic)`

英雄魔力 = 基础魔力 + 学派加成 + 神器加成。通过 `getContent HeroFrame` 查看英雄各学派魔力。

**法术管理操作**：
1. 城市魔法公会生产法术（SpellStack 属于 Region）
2. `spellStackAction ADD_TO_SPELLBOOK` — 将法术加入英雄魔法书（最多4~7个槽位）
3. `spellStackAction ADD_TO_BATTLE` — 装备法术到战斗栏（最多14个回合位）
4. 每个法术占一个回合位（roundPosition 1~14），决定哪个回合施放
5. 施放后法术进入冷却，一段时间内无法再次使用

**法术使用策略**：
- 毁灭法术适合开局快速削减敌方兵力
- 光明增益法术（DIVINE_STRENGTH, BLESS）放在前排回合，提升己方战力
- 召唤法术在敌方兵力强于己方时最有价值（召唤额外部队）
- 复活法术放在后排回合，在伤亡发生后恢复兵力
- 法术对特定兵种有额外效果（如 DEFLECT_MISSILE 对弓手 +50%）

**法术限制**：
- 英雄魔法书容量 4~7（受技能加成）
- 战斗栏最多 14 个回合位
- 5级法术只能从本阵营魔法公会获得
- 符文要塞战斗中完全禁用魔法（antiMagic = TRUE）

---

## 完整战力计算公式

### 单回合公式

每回合一对一，攻击方第 N 个兵团 vs 防守方第 M 个兵团：

**攻击方总战力 =**
```
基础战力
  + 克制加成（基础战力 × 0.5，仅克制时）
  + 全军技能加成（基础战力 × 全军攻击百分比）
  + 兵种专属技能加成（基础战力 × 兵种攻击百分比，仅克制时）
  + 士气加成（基础战力 × 士气百分比，纯种族军队时）
  + 英雄攻击力加成（基础战力 × hero.attack × HERO_ATTACK_BONUS系数）
  + 单位加成（每单位加成 × 数量）
```

**防守方总战力 =**
```
基础战力
  + 克制加成（基础战力 × 0.5，仅克制时）
  + 全军技能加成（基础战力 × 全军防御百分比）
  + 兵种专属技能加成（基础战力 × 兵种防御百分比，仅克制时）
  + 士气加成（基础战力 × 士气百分比，纯种族军队时）
  + 英雄防御力加成（基础战力 × hero.defense × HERO_DEFENSE_BONUS系数）
  + 单位加成（每单位加成 × 数量）
  + 城防加成（基础战力 × 城防百分比，仅攻城时）
  + 掠夺防御加成（基础战力 × 掠夺防御百分比，仅掠夺时）
```

其中：
- **基础战力** = 单位战力(unitEntity.power) × 数量
- 各加成取 floor 后求和
- 攻击方总战力 >= 防守方总战力 → 攻击方赢该回合

### 详细计算示例

**场景：** 20 步兵 vs 10 幽灵（假设幽灵属于骑兵类型）

前提条件：
- 步兵 unitPower = 3，幽灵 unitPower = 5
- 英雄攻击力 = 2，HERO_ATTACK_BONUS 系数 = 0.02
- 英雄无特殊技能加成，无城防
- 步兵克制骑兵 → 有克制优势

计算步骤：

```
攻击方（20 步兵）：
  ① 基础战力 = 3 × 20 = 60
  ② 克制加成 = 60 × 0.5 = 30        （步兵 → 骑兵）
  ③ 全军技能加成 = 0                  （无技能）
  ④ 兵种专属技能加成 = 0              （无技能）
  ⑤ 英雄攻击力加成 = 60 × 2 × 0.02 = 2.4
  ⑥ 单位加成 = 0
  ⑦ 总加成 = floor(30 + 0 + 0 + 2.4) + 0 = 32
  ⑧ 攻击方总战力 = 60 + 32 = 92

防守方（10 幽灵/骑兵）：
  ① 基础战力 = 5 × 10 = 50
  ② 克制加成 = 0                      （骑兵不克制步兵）
  ③ 全军技能加成 = 0                  （NPC无技能）
  ④ 英雄防御力加成 = 0                （NPC无英雄）
  ⑤ 城防加成 = 0                      （攻击NPC无城防）
  ⑥ 总加成 = 0
  ⑦ 防守方总战力 = 50 + 0 = 50

判定：92 >= 50 → 攻击方赢

碾压检测：(92 - 50) = 42 > 60（基础战力）？42 > 60 = 否
→ 不是碾压，攻击方有损失

攻击方击溃数 = floor((50 + 0 - 32) / 3) = floor(18 / 3) = 6
→ 攻击方损失 6 个步兵，剩余 14 个步兵

消耗（attrition）：
  击溃的 6 个单位 × 消耗率(约0.3) × 100 = 180 消耗点
  实际永久损失 = floor(180 / 100) = 1 个步兵
  最终剩余：20 - 1 = 19 个步兵

防守方 10 个幽灵全部击溃，NPC 全灭。
攻击方获胜。

经验值计算：
  XP = 击溃的单位数 × (unitPower / powerXPPoints)
  荣耀修正器 = defenderBasePower / attackerBasePower = 50/60 ≈ 0.83
  修正后荣耀 = 0.83 - 1 = -0.17（略微惩罚，打弱敌XP略减）
```

---

## 出战顺序

### 攻击方

按兵团位置顺序出战：**position 1 → 2 → 3 → ... → 7**

- 位置由 `stackPosition` 字段决定
- 可以通过调整部队位置来控制出战顺序
- 最多 7 个兵团

**策略关键：** 把克制对手的兵种放在前面位置。

### 防守方

按战力从强到弱排列出战：`sortDefenseUnitStackList` 按 `getPower()` 降序排序。

- 最强兵团先出战
- 城市驻军和英雄部队混合后统一排序
- NPC 也是按总战力降序

---

## 战斗流程

### 战前阶段

1. **战前弓手齐射**（Barrage Fire）— 拥有 `PRE_FIGHT_ATTACK_SHOOTER` 技能的英雄，其弓手战力的一定百分比作为伤害施加给对方全军
2. **投石车齐射** — 防守方围城时的投石车伤害
3. **建筑组件齐射** — 符文要塞等建筑的额外伤害

### 回合循环

```
while (攻击方还有兵团 && 防守方还有兵团):
    ① 攻击方施法（回合前）
    ② 防守方施法（回合前）
    ③ 兵团对决 — 比较双方总战力
    ④ 判定胜负：
       - 攻击方赢：
         - 检查碾压：(攻击方总战力 - 防守方总战力) > 攻击方基础战力？
           - 是 → 碾压（Overrun），攻击方零损失，防守方该兵团全灭
           - 否 → 攻击方损失部分单位，防守方该兵团全灭
         - 防守方切换下一兵团
       - 防守方赢：
         - 同样检查碾压
         - 攻击方该兵团全灭，切换下一兵团
    ⑤ 攻击方施法（回合后）
    ⑥ 防守方施法（回合后）
    ⑦ 计算消耗（attrition）
    ⑧ 回合结束
```

### 碾压机制（Overrun）

当赢方总战力与输方总战力的差距超过赢方基础战力时触发：

```
(winnerTotalPower - loserTotalPower) > winnerBasePower
```

碾压时：
- 赢方零损失
- 输方兵团全灭
- 赢方的**同一兵团**继续对战输方的下一兵团（不切换）

碾压是连锁的——如果英雄足够强，可以用一个兵团扫平对方全部兵团。

### 消耗机制（Attrition）

击溃的单位不一定全部死亡。实际永久损失通过消耗率计算：

```
消耗点 = 击溃数量 × 消耗率(CONFVALUE_BATTLE_ATTRITION_RATE) × 100
永久损失 = floor(消耗点 / 100)
```

- 如果消耗点 > 0 但 < 100，至少损失 1 个单位
- `ATTRITION_RATE_INCREASE` 技能提高对手消耗率
- `ATTRITION_RATE_DECREASE` 技能降低己方消耗率
- NPC 战斗中，NPC 不计算消耗（全灭或全活）

### 免战判定（No Battle）

当防守方基础战力 / 攻击方基础战力 >= `CONFVALUE_NO_BATTLE_ARMY_POWER_RATIO` 时：
- 战斗不发生
- 攻击方收到"力量不足"消息
- 英雄返回，部队无损

这是一个安全机制——如果敌人太强，根本不会开战。

---

## NPC 战斗决策

攻击 NPC 前执行以下检查清单：

### 第一步：查看 gameState 中的区域信息

```json
{
  "zones": [{
    "id": 123,
    "npcPower": 150,
    "npcLevel": 2,
    "npcComposition": {"INFANTRY": 40, "CAVALRY": 30, "SHOOTER": 30}
  }]
}
```

### 第二步：精确配兵（核心策略）

**不要带全部兵力打弱怪。** 荣耀修正器 = 敌方总战力 / 己方总战力。带兵越多→荣耀越低→经验越少。

正确做法：
1. 用 `unitStackAction SPLIT` 从大兵团中拆出刚好够用的数量
2. 只带克制对手的兵种出战
3. 剩余部队留在驻军（`unitStackListAction MOVE_TO_REGION` 先卸载不需要的兵团）
4. 战后用 `unitStackAction FUSION` 合并回来

配兵目标：`己方总战力 ≈ 敌方总战力 × 1.3~1.5`（有克制时取低值，无克制取高值）。这样荣耀接近 1.0，经验最大化。

### 第三步：评估克制优势

根据 `npcComposition` 判断对方主力兵种：
- 主力兵种占比 > 50% → 可以针对性配兵
- 兵种均匀分布 → 需要综合考虑

### 第四步：战力比判定表

| 战力比 (己方/敌方) | 有克制优势 | 部分克制 | 无克制优势 |
|---|---|---|---|
| >= 1.3 | 稳赢，可以出击 | 大概率赢 | 有风险但可尝试 |
| >= 1.5 | 碾压，零损失可能 | 稳赢 | 大概率赢 |
| >= 2.0 | 必然碾压 | 碾压 | 稳赢 |
| < 1.0 | 危险，可能触发免战 | 必输 | 必输 |

### 第五步：执行攻击

```bash
curl -k -s -b $COOKIES -X POST "$BASE/api/agent/action" \
  -H "Content-Type: application/json" \
  -d '{"type":"addAction","params":{"actionType":"HERO_ATTACK_NPC","actorType":"Hero","actorId":<heroId>,"actionParams":"<zoneId>"}}'
```

### 特殊：NPC 招募

如果攻击方英雄和 NPC 属于同一阵营，且英雄战力远超 NPC：
- 触发 `RecruitNPC` 公式判定
- 成功时：NPC 部队的 30% 加入英雄军队（不发生战斗）
- 条件：NPC 区域有资源掠夺物

---

## 荣耀修正器

荣耀影响经验值获取：

```
honor = defenderBasePower / attackerBasePower
修正值 = honor - 1
```

| 修正值范围 | 含义 | 对 XP 的影响 |
|---|---|---|
| > 0（打比自己强的敌人） | 正面修正 | 经验加成 |
| = 0（实力相当） | 无修正 | 正常经验 |
| < 0（打比自己弱的敌人） | 负面修正 | 经验减少 |

**XP 计算完整公式：**

```
原始XP = sum(每个击溃的敌方单位 × unitPower / powerXPPoints)
XP修正总和 = 荣耀修正 + 王国荣耀修正 + 技能/神器XP加成 + PVP加成
XP修正总和 = clamp(XP修正总和, -0.85, 4.0)
最终XP = max(0, round(原始XP × (1 + XP修正总和)))
```

- 败方的 XP 修正上限为 0（输了不可能获得正面加成）
- 荣耀修正 >= 1.3 时触发"最大化经验"成就

**策略提示：** 攻击与自己实力相当或更强的NPC，获得更多XP。

---

## 军队整编（每次操作部队后必做）

**核心原则：同类兵种必须合并为一个兵团，绝不允许英雄或驻军中存在两组相同 unitEntityId 的兵团。**

分散的同类兵团是严重的资源浪费：
- 战斗是逐回合一对一对决，30 单位的大兵团比两个 15 单位的小兵团碾压概率高得多（碾压 = 零损失继续对战下一个敌方兵团）
- 每个英雄只有 7 个兵团槽位，重复兵种占位意味着少带一种克制兵种
- 克制加成在大兵团上效果更显著——集中力量一击碾压 vs 分散力量两轮苦战

### 整编时机

**每次以下操作后，立即检查并合并同类兵团：**
1. `MOVE_FROM_REGION` 装载部队后
2. 战斗结束后（可能有残兵 + 新获部队）
3. 领取邮件/任务奖励后（奖励部队进入驻军）
4. 招募完成后

### 整编操作

检查 gameState 中英雄和驻军的 unitStackList，查找 `unitEntityId` 相同的兵团：

```
假设英雄 unitStackList:
  {id: 101, unitEntityId: 5, quantity: 20, stackPosition: 1}  ← T1 步兵
  {id: 102, unitEntityId: 8, quantity: 15, stackPosition: 2}  ← T2 弓手
  {id: 103, unitEntityId: 5, quantity: 10, stackPosition: 4}  ← T1 步兵（重复！）

→ 必须合并：unitStackAction FUSION {unitStackId: 101, unitStack2Id: 103}
→ 结果：一组 30 个 T1 步兵 + 一组 T2 弓手（2个兵团，省出5个槽位）
```

驻军同样检查，一并合并。

### 升级基础版兵种为进阶版

如果城市已建造进阶招募建筑（如 RECRUIT_T1P），**必须将现有基础版兵团（T1）升级为进阶版（T1P）**。进阶版战力比基础版高 20%~50%，升级后还可以和其他进阶版兵团合并。

**升级通过招募指令完成：** REGION_RECRUIT 的 actionParams 第4段传入要升级的 unitStackId：

```
actionParams: "RegionCity;<regionId>;;stackId1_stackId2"
```
- 第3段留空（不招新兵），第4段传要升级的兵团 ID（下划线分隔多个）
- 也可以同时招新兵 + 升级：`"RegionCity;<regionId>;T1_10;stackId1"`
- 升级费用 = (T1P单价 - T1单价) × 1.5 × 数量

**升级检查流程：**
1. `getContent RecruitmentFrame` — 确认对应 tier 的 `upgraded.available = true`
2. 检查英雄/驻军中是否有基础版兵团（unitEntityId 对应基础版而非进阶版）
3. 确保有足够资源
4. 发出 REGION_RECRUIT 带升级参数
5. 升级完成后，FUSION 同类进阶版兵团

**识别基础版 vs 进阶版：** RecruitmentFrame 返回的 `recruitableUnitList` 中，每个 tier 包含基础版信息和 `upgraded` 子对象。对比英雄 unitStackList 中的 `unitEntityId` 与 RecruitmentFrame 中基础版/进阶版的 `unitEntityId`，即可判断哪些兵团需要升级。

### 整编 + 升级的完整工作流

每次回城或操作部队时的标准流程：

1. **检查升级** — `getContent RecruitmentFrame`，看是否有基础版兵团可以升级
2. **执行升级** — REGION_RECRUIT 带升级参数
3. **合并同类** — 对英雄和驻军分别执行 FUSION 合并所有同 unitEntityId 的兵团
4. **确认整编完成** — `gameState` 确认没有重复兵种

---

## 兵团质量原则（防止弱兵泛滥）

**"一堆弱兵"是 Agent 最常见的症结**——NPC 掉落的中立兵没清、T1 贪招不升级、堆数泛滥导致单堆薄、建了高阶兵后低阶不淘汰。质量永远优于数量。下面的规则不是建议，是铁律。

### 为什么质量 > 数量（机制原因）

战斗是回合一对一对决，**单堆战力**决定碾压触发（`winnerTotalPower - loserTotalPower > winnerBasePower`）。一个 30 单位的强堆一次碾压就扫平对方整个阵容（碾压链，L275）；两个 15 单位的弱堆要打两回合苦战，每回合可能被反制。

关键公式直觉：
- 30 单位 × 单兵 power 300 = 9000 总战力 → 稳定触发碾压
- 两个 15 单位 × 300 = 两个 4500 总战力 → 对方任何兵团都能反杀
- 300 单位 × pw 30（弱兵） = 9000 总战力 → 看起来一样，但克制加成按堆计算，面对混合敌人时这堆只能打一个回合

### 堆数上限（硬性规则）

| 场景 | 最优堆数 | 上限 | 说明 |
|------|---------|------|------|
| 出战英雄（打 NPC） | **2 堆**：1 主力克制 + 1 备用克制 | 3 堆 | 绝不为"填满 7 槽"多带弱兵，会稀释主力碾压概率 |
| 出战英雄（PvP/攻城） | **3 堆**：三系克制各 1 堆 | 4 堆 | 敌方阵容未知，需覆盖三系 |
| 常驻驻军（防守） | **3-4 堆** | 4 堆 | 留 3 槽给新招募和战利品，避免 SPLIT 时 "position occupied" |
| 空闲英雄（采矿/侦察） | **0 堆** | 0 堆 | 有兵不能采矿，空闲时必须全卸 |

**绝对禁止**：一个英雄身上出现 5-7 堆。如果出现，几乎 100% 说明有弱兵没清或同类没合并。

### 弱兵识别（单兵 power 阈值法）

以当前城市**最高可招募 tier 的单兵 power** 作为基准（记作 `P_max`，从 RecruitmentFrame 或 $SKILL_DIR/factions.md 查）：

| 单兵 power 区间 | 判定 | 处理 |
|----------------|------|------|
| `< P_max × 20%` | **废兵** | 立即 DISBAND，无条件 |
| `P_max × 20%-50%` | **过时兵** | 若有 FUSION 对象则合并保留，否则 DISBAND |
| `P_max × 50%-80%` | **次要兵** | 保留 1 堆作为备用克制，其余 DISBAND |
| `>= P_max × 80%` | **主力兵** | FUSION 最大化，这是核心战力 |

**数量阈值辅助判定**：`quantity < 10` 的残堆几乎必然废掉——一次战斗就全灭，没保留价值。

### 弱兵典型来源

1. **NPC 战利品中立兵**（最主要来源）
   - 出现形式：打赢 NPC 后驻军里多出 `faction=NEUTRAL` 的兵团（常见 INF pw=97、SHO pw=263、CAV pw=150 等）
   - 中立兵 `unitEntityId` 独立，**和自己阵营同类兵种合并不了**——只吃维护、占槽位
   - **规则：一律 DISBAND，不要留着"凑数"。** 即使是 SHO pw=263 看着不弱，但它无法和你的 T2P 合并，独立一堆就是稀释主力
2. **未升级的基础版 T1/T2**
   - 建了 RECRUIT_T1P/T2P 之后，基础版 T1/T2 必须**升级**（REGION_RECRUIT 第 4 段）而不是 DISBAND——升级保留兵力
   - 只有在已经建了 T4+ 且仓库金币短缺时，残留的 T1 残堆（<10）才 DISBAND
3. **跨 tier 淘汰兵**
   - 建了 T5/T6 招募后，T1/T2 的整堆已经失去战术价值（单兵 power < T6 × 20%）
   - 除非总量大（>50）还能凑肉盾，否则 DISBAND 腾槽位
4. **混合 tier 的出战阵容**
   - 出战前临时 MOVE_FROM_REGION 装载了 T1+T2+T3+T4 各一堆 → 战斗时 T1 先出战被瞬间击溃，T4 还没登场就结束一轮
   - 正确做法：按单兵 power 从高到低取前 2-3 堆，用 PERMUTATION 把克制兵放 position 1

### 招募纪律（按英雄流派分支）

**先判定流派**：英雄是否走兵海流派？判定条件：领袖 LEADER 职业 + 兵种单兵攻击装备 ≥3 件 + 最低 power 基础版步兵/骑兵单堆 ≥500。详见下节「弱兵战术：兵海流派」。

| 纪律项 | 精英流（默认） | 兵海流派（例外） |
|-------|--------------|-----------------|
| **T1/T2 基础版处理** | 建了 T_P 建筑后**必须升级**为进阶版（REGION_RECRUIT 第 4 段）| **绝对禁止升级**——基础版就是载体。圣堂 T1 农民 97、地狱 T1 魔婴 71、亡灵 T1 骷髅兵 87 经济最优，升级后变弱（多花费+高维护+加成稀释+FUSION 不合并+类型变换） |
| **主力饱和目标** | 单堆 3000-6000 战力后改招高 tier | 持续招最低 power 基础版到单堆 1500-3000 兵 |
| **资源紧张** | 宁可不招也不填槽位招 T1 | 低阶便宜又产能快，继续招 |
| **堆数控制** | 英雄 3 堆（1 主力克制 + 1 备用 + 可选肉盾）+ 驻军 3-4 堆 | 英雄 1-2 堆（单大主力堆 + 可选 1 T6/T7 精英免疫位对抗 AOE） |
| **DISBAND 阈值** | `基础 power < P_max × 20%` → DISBAND | **有效 power**（基础 + per-unit 加成）< P_max × 20% → DISBAND（T1 基础版加成后 197，通常远高于阈值，保留） |
| **招募前检查** | 驻军已有同类 tier 堆会自动合并；满 7 堆先清弱兵再招 | 同 |
| **DISBAND 残堆** | `quantity < 10` → DISBAND | 同（流派核心堆不会降到这么低）|

**⚠ 产能维度（两派共通）**：每个招募建筑有 `unitProductionPerDay` 日产上限，**高 tier 产量远低于低 tier**——T5/T6/T7 每天 1-5 个，T1/T2 每天几十个。**高阶本日产能耗尽且需立刻堆战力打仗时**，不要空等下一天——继续招 T1/T2 基础版补量。数学：日产 T6=5、T1=60 时，仅招 T6 上限 22,540 战力；补 T1 = **28,360（+26%）**；兵海满配加成 +100/兵 则是 **34,360（+52%）**。精英流战后可 DISBAND 临时招募的低阶，兵海流派直接留着继续堆。

### 每轮军队质量巡检（机械流程）

每次 gameState 后，按顺序执行：

1. **先判定流派**：该英雄是否走「步兵海流派」？（见下方节，判定条件：领袖职业 + 步兵单兵攻击装备 ≥3 件 + T1/T2/T3 步兵单堆 ≥500）
2. 遍历 `heroes[].unitStackList` + `cities[].garrison` 的所有兵团
3. 查 RecruitmentFrame 得出 `P_max`（该城最高 tier 单兵 power）
4. 计算**有效单兵 power** = `基础 power + 英雄 per-unit 加成`（高谈阔论 + 步兵单兵攻击装备 + 通用单兵攻击装备）
5. 标记处理：
   - `unitEntity.faction == NEUTRAL` → **DISBAND**
   - **有效 power** < P_max × 20% 且非步兵海加成载体 → **DISBAND**
   - `quantity < 10` 且非主力克制备用 → **DISBAND**
   - 基础版兵种 + 对应 T_P 建筑已建 → **升级**（REGION_RECRUIT 第 4 段）
   - 同 unitEntityId 多堆 → **FUSION**
6. **步兵海例外**：如果英雄走步兵海流派，T1P/T2/T3 步兵堆即使基础 power 低于阈值也**必须保留并继续招募**（它们是加成载体），而不是 DISBAND
7. 确认堆数上限：精英流英雄 3、步兵海流派英雄 1-2（单大堆主导）、驻军 4

---

## 弱兵战术：兵海流派（per-unit 加成生态，数量主导）

**不是所有"低阶兵"都是废兵。** 上节「兵团质量原则」是**精英流（质量主导）** 的规则。游戏存在另一条完全相反的合法战术路径——**兵海流派（数量主导）**，靠堆大量 T1/T2/T3 低阶兵 + per-unit 加成生态爆发总战力。Agent 必须识别英雄是否走兵海流派，否则会把流派核心资产 DISBAND 掉，直接毁掉玩法。

### ⚠ 第一赛季现状（必读）

本赛季是本世界线的**第一赛季**——所有玩家都还没经历过前一世界的终局（Tear War），因此：

- **所有"血统能力"（HEREDITYABILITY）均不可用**。血统是跨世界传承的加成，由上一世界终局结果决定，下一世界开局时附着在英雄上（见 $SKILL_DIR/tear-war.md L86）
- 尤其影响弓手海：**PRE_FIGHT_ATTACK_SHOOTER（战前弓手齐射 Barrage Fire）** 的 origin 是 `HEREDITYABILITY`，第一赛季**全员缺失**。这让弓手海失去核心开场大招，本赛季近乎废流派
- **真正能用的兵海流派只有两种：步兵海（最强）和骑兵海（次强）**
- $SKILL_DIR/magic.md L143 提到的 `SPELL_EFFICIENCY_INCREASE_SPECIFIC_LEVEL`（指定等级法术效率血统加成）同样是 HEREDITYABILITY 来源，本赛季也不可用
- 所有策略以第一赛季可用的 `SKILL / ARTEFACT / SPELL` 三类 origin 为准

### 能力来源的 4 种 origin（源码定义）

MMHK 英雄的加成来源在 `php/shared/framework/Entity/Data/EffectEntity.entity.php` 里有严格 origin 分类：

| origin | 系统 | 获取方式 | 第一赛季可用 |
|--------|-----|---------|------------|
| `SKILL` | 职业技能 | HERO_LEARN_CLASS → HERO_LEARN_SKILL，消耗技能点 | ✅ |
| `ARTEFACT` | 装备 | artefactAction MOVE，装备神器 | ✅ |
| `SPELL` | 法术 | 魔法公会生产 → ADD_TO_SPELLBOOK → ADD_TO_BATTLE | ✅ |
| `HEREDITYABILITY` | 血统能力 | **上一世界 Tear War 终局结果传承** | ❌ **本赛季全员无** |

遇到 tagName 以 `HEREDITYABILITY_` 开头的效果（如 `HEREDITYABILITY_PRE_FIGHT_ATTACK_SHOOTER`），本赛季**直接当它不存在**，不要在策略里依赖。

### 三兵种装备与法术偏爱对比（源码验证）

装备和法术系统对三兵种**不是均衡设计**，每个兵种都有独门机制，但强度不同——不是"只有步兵能走兵海"，而是"三兵种可走兵海但强度分档"：

| 机制 | origin | 偏爱兵种 | 歧视兵种 | 第一赛季 |
|------|-------|---------|---------|---------|
| 步兵单兵攻击装备（多件可叠到 **+70**，6 件组合） | ARTEFACT | **步兵** | — | ✅ |
| 骑兵单兵攻击装备（**仅 1 件**，+15 封顶） | ARTEFACT | 骑兵 | — | ✅ |
| 远程单兵攻击装备（**词条存在但 0 装备提供**） | ARTEFACT | — | **弓手** | ✅（无装备可用）|
| 步兵单兵防御装备（+3/+6/+9，独占词条） | ARTEFACT | **步兵** | — | ✅ |
| 通用单兵攻击/防御装备（+5/+10/+15） | ARTEFACT | 所有兵种 | — | ✅ |
| 步兵/骑兵/远程法术效率装备（+18%） | ARTEFACT | 对应兵种 | — | ✅ |
| **高谈阔论**（ATTACK_POWER_PER_UNIT_INCREASE） | SKILL | **所有兵种**（通用）| — | ✅ |
| **优等待遇**（DEFENSE_POWER_PER_UNIT_INCREASE） | SKILL | **所有兵种**（通用）| — | ✅ |
| DIVINE_STRENGTH / RIGHTEOUS_MIGHT（VALUE_MEMBERS 攻击） | SPELL | 所有兵种（低阶倍增）| — | ✅ |
| **MYSTIC_SHIELD**（VALUE_MEMBERS 防御） | SPELL | **骑兵 +50%** | — | ✅ |
| TELEPORTATION（PERCENTAGE 攻击） | SPELL | 步兵/骑兵 | **弓手 -50%** | ✅ |
| **PRE_FIGHT_ATTACK_SHOOTER**（战前齐射 Barrage Fire） | **HEREDITYABILITY** | 弓手独享 | — | **❌ 本赛季失效** |

### 三兵海流派强度对比（第一赛季，满配加成上限）

| 流派 | 高谈阔论 | 兵种专属装备 | 通用装备 | 兵种独享法术 | 攻击/兵上限 | 防御独特优势 | 强度档 |
|------|---------|------------|---------|-------------|------------|------------|-------|
| **步兵海** | +15 | **+70** | +15 | — | **+100/兵** | 步兵法术效率 +18%、独占 +9 防御装备 | **S 级** |
| **骑兵海** | +15 | +15 | +15 | **MYSTIC_SHIELD 对 CAV +50%** | +45/兵 | 防御端超模（MYSTIC_SHIELD 独享）| **A 级** |
| **弓手海** | +15 | 0（无装备）| +15 | TELEPORTATION **-50%**，战前齐射**本赛季失效** | +30/兵 | 无独享 | **D 级（本赛季废）** |

**结论**：步兵海装备生态最完整（S 级首选）；骑兵海攻击加成弱但有 MYSTIC_SHIELD 防御超模补偿（A 级次选，PvP 防守向）；**弓手海本赛季核心血统能力失效，不推荐作主流派**，仅作三系混合阵里的辅助位存在。

### per-unit 加成生态全集

以一个满配领袖/战士+光明巫师英雄 + 步兵海阵容为例：

| 加成源 | 数值 | 类型 | 前置 |
|-------|------|------|------|
| 高谈阔论 Lv3（领袖技能 ATTACK_POWER_PER_UNIT_INCREASE） | +15/兵攻击 | 固定值 | 领袖职业 + 技能点 |
| 优等待遇 Lv3（军需官技能 DEFENSE_POWER_PER_UNIT_INCREASE） | +15/兵防御 | 固定值 | 战士职业 |
| 步兵单兵攻击装备 6 件组合 | +70/兵攻击 | 固定值 | 步兵，装备总等级 38/40 |
| 通用单兵攻击装备 | +15/兵攻击 | 固定值 | 可叠加（装备部位冲突时二选一） |
| 步兵单兵防御装备 | +9/兵防御 | 固定值 | 步兵独占 |
| 通用单兵防御装备 | +15/兵防御 | 固定值 | 可叠加 |
| **DIVINE_STRENGTH**（光明 1 级，0.3×魔力×N） | VALUE_MEMBERS 攻击 | 对低阶倍增 | 光明巫师 + 魔法公会 Lv1 |
| **RIGHTEOUS_MIGHT**（光明 3 级，0.6×魔力×N） | VALUE_MEMBERS 攻击 | 对低阶倍增 | 光明巫师 + 魔法公会 Lv3 |
| **MYSTIC_SHIELD**（光明 2 级，0.6×魔力×N） | VALUE_MEMBERS 防御 | 对低阶倍增，对 CAV +50% | 光明巫师 + 魔法公会 Lv2 |
| 步兵法术效率装备（+18%）| 放大 DIVINE_STRENGTH/RIGHTEOUS_MIGHT 对步兵的效率 | 乘法 | 仅步兵 |

**攻击侧上限（步兵）** = +15（高谈阔论）+70（步兵装备）+15（通用装备）= **+100 每兵攻击**
**防御侧上限（步兵）** = +15（优等待遇）+9（步兵装备）+15（通用装备）= **+39 每兵防御**

### 数量回本曲线（以圣堂 T1 农民为例，基础 power 97）

**关键原则：兵海流派要选阵营最低 power 的基础版，不是进阶版**。低 power 意味着：
- **招募费更便宜**（基础版约比进阶版便宜 29%，省下来的金币能多招 40% 兵）
- **维护费更低**（按单价比例，每天差 40%）
- **加成占比更高**（+100/兵 对 T1 农民 97 是 **+103%**（翻倍），对 T1P 民兵 128 只有 +78%）
- **VALUE_MEMBERS 增益吃得更多**（RIGHTEOUS_MIGHT 6N/97 = +6.2% vs 6N/128 = +4.7%）
- **招募速度更快**（基础版建筑产能高于进阶版）

唯一劣势：VALUE_MEMBERS 伤害法术对低 power 兵击溃数更高（PLAGUE 对 T1 击溃 93 vs T1P 70），但 PvE 场景 NPC 普遍无 AOE，无关紧要；PvP 对上魔法流本来就该切精英流。

满配 +100/兵 加成后 T1 农民有效 power 97+100=197：

| 单堆数量 | 有效总战力 | 同预算对比（70k 金）|
|---------|-----------|------------------|
| 100 T1 | 19,700 | 弱鸡 |
| 300 T1 | 59,100 | 开始有战术价值 |
| **700 T1** | **137,900** | **成型门槛**（同 70k 金可招 1400 只，此处取中位数）|
| 1400 T1 | 275,800 | **同预算下比 1000 T1P 多 21% 战力** |
| 2000 T1 | 394,000 | 主力级 |
| 3000 T1 | 591,000 | 核心主力（亡灵/圣堂可持续）|

加上 RIGHTEOUS_MIGHT 战中追加（1000 兵 × 0.6 × 魔力 10 = 6000 效果值 / 97 = 61 等效单位 → +6.2%）和 DIVINE_STRENGTH 叠加，实战效果再放大一层。

**绝对禁止升级 T1→T1P**——这不是省事，是**主动变弱**（多花升级费 + 多吃维护 + 加成占比稀释 + FUSION 还不能合并）。精英流铁律"建 T1P 后必须升级"和兵海流派**正好相反**，必须按英雄流派判定。

### 产量维度：为什么兵海流派能快速成型

前面 5 个理由都是**经济性价比**（招募费、维护、加成占比、法术增益、FUSION），还有第 6 个理由是 **unitProductionPerDay 日产能差距**：

| 兵种 | 典型日产量 | 堆 1500 兵所需天数 |
|------|----------|----------------|
| T1 基础版 | 30-60/天（视招募建筑等级）| **25-50 天** |
| T4P 进阶版 | 3-8/天 | 180-500 天 |
| T7P 进阶版 | **1-3/天** | 500-1500 天 |

**战力爬升速度对比**：
- 兵海流派：30 天堆 1500 T1 → 满配 +100/兵 加成后 **295,500 战力**
- 精英流：30 天堆 30 T7P → 裸战 **300,300 战力**（但 T7 需要阵营主要稀有资源储备）

**同等时间内两者战力接近**，但兵海流派：
- 只消耗金币（T1 便宜）
- 不挤占稀有资源（T7 要吃水晶/硫磺/宝石/水银）
- 维护费更低（T1 单兵维护约 0.5 金/天 vs T7 可能数十金）
- 成型时间门槛低：500 兵就成型（10 天），新号第一赛季的最快出战力路径

**产能耗尽的相反方向运用**：如果兵海流派英雄今日低阶产能招完了，可以**转投同阵营的其它低 power 层**（如圣堂 T1 招完补 T3 步兵 407、亡灵 T1 招完补 T2 僵尸 134），继续堆数量而不是强行升 T1P。

### 各阵营兵海底子（T1-T4 兵种类型决定流派可行性）

列出每阵营 **T1 基础版**（兵海载体首选）的类型和 power，用来判断最便宜步兵海载体：

| 阵营 | T1 基础 | T2 基础 | T3 基础 | 最便宜步兵海载体 | 备选步兵层 |
|------|--------|---------|---------|---------------|----------|
| **圣堂 HAVEN** | **农民 97（步兵）** | 弓箭手 198（射手） | 步兵 407（步兵） | **T1 农民 97** ✓ 最便宜 | T3 步兵 407 |
| **地狱 INFERNO** | **魔婴 71（步兵）** | 长角恶魔 163（步兵） | 地狱犬 370（骑兵） | **T1 魔婴 71** ✓ 最便宜（但**绝不升级 T1P**，升了变射手）| T2 长角恶魔 163 |
| **亡灵 NECROPOLIS** | **骷髅兵 87（步兵）** | 僵尸 134（步兵） | 幽灵 303（骑兵） | **T1 骷髅兵 87** ✓ 最便宜（**绝不升级 T1P**，T1P 战力反而低 70 + 变射手）| T2 僵尸 134、T4 吸血鬼 751 |
| **森林 SYLVAN** | 花仙子 88（骑兵）| 银刃剑客 163（步兵） | 精灵猎手 448（射手） | T2 银刃剑客 163（T1 不是步兵） | — |
| **学院 ACADEMY** | 小精怪 71（射手） | 石像怪 120（骑兵） | 铁魔像 272（步兵） | T3 铁魔像 272（T1/T2 都不是步兵） | — |

**骑兵海载体**（同理选最低 power 骑兵）：
- 森林 T1 花仙子 88（最便宜骑兵，骑兵海首选载体）
- 圣堂 T4 狮鹫 751、地狱 T3 地狱犬 370、学院 T2 石像怪 120

**关键陷阱**：
- **地狱/亡灵的 T1 基础 → 进阶会换兵种类型**（步兵 → 射手），走步兵海**必保留 T1 基础版，绝不升级**
- **亡灵 T1P 骷髅弓箭手战力反而低于基础版 T1 骷髅兵（70 vs 87）**——这是**数据陷阱**，不仅变类型还变弱，**两重禁止升级**
- **圣堂/森林没有类型变换陷阱**，但经济学仍推荐基础版：T1 农民 97 比 T1P 民兵 128 便宜 29%、维护费低 40%、加成占比高 32%、招募快

### 流派成立条件（按三流派分列）

**步兵海（S 级，第一赛季首选）**：
1. 英雄双职业：**领袖 LEADER**（解锁高谈阔论）+ **光明巫师 LIGHT_WIZARD**（解锁 DIVINE_STRENGTH/RIGHTEOUS_MIGHT/MYSTIC_SHIELD）。可选战士 FIGHTER 加优等待遇
2. 装备路线：步兵单兵攻击流 6 件组合（+70）——$SKILL_DIR/equipment.md 组合 1
3. 魔法公会至少 Lv3（拿到 RIGHTEOUS_MIGHT）
4. 兵种载体：**阵营最低 power 基础版步兵（绝非进阶版）**——圣堂 T1 农民 97 首选、亡灵 T1 骷髅兵 87 首选（绝不升级，T1P 战力反而低）、地狱 T1 魔婴 71（绝不升级，T1P 变射手）、森林 T2 银刃剑客 163（T1 是骑兵只能从 T2 起）、学院 T3 铁魔像 272（T1/T2 都不是步兵底子最差）
5. 数量：单堆 500+ 才成型，推荐 1000-2000

**骑兵海（A 级，PvP 防守向次选）**：
1. 英雄职业：领袖 + 光明巫师（为了 MYSTIC_SHIELD 独享 +50% CAV 防御超模）
2. 装备路线：骑兵单兵攻击装备 1 件（+15 封顶）+ 通用单兵攻击/防御装备 + 骑兵法术效率 +18%
3. 魔法公会至少 Lv2（拿到 MYSTIC_SHIELD）
4. 兵种载体：T1/T4/T6/T7 骑兵（圣堂狮鹫/皇家狮鹫/骑士/圣骑士、地狱地狱犬/地狱战马、森林花妖/独角兽）
5. 数量：单堆 200+（骑兵单兵战力高，成型门槛低于步兵海）

**弓手海（D 级，本赛季不推荐作主流派）**：
- 战前齐射血统（PRE_FIGHT_ATTACK_SHOOTER）本赛季全员缺失
- 装备空白（远程单兵攻击词条存在但 0 装备）
- TELEPORTATION 对 SHOOTER -50% 惩罚
- **仅作混合阵的辅助位**：1 堆弓手放 position 靠后触发战前伤害站位（但没血统就是纯战力上阵） + 主力步兵海/骑兵海堆

### 流派的天敌（双刃剑）

VALUE_MEMBERS 伤害法术对大兵团是镜像破坏——敌方魔力 10 时的击溃数对照：

| 敌方法术 | 学派 | 值 | 目标 | vs 1000 T1P | vs 30 T7P |
|---------|------|----|----|------------|-----------|
| SICKNESS 病患 | 黑暗 1 级 | 0.3 | 单堆 | 击溃 23 | 0（floor） |
| DISEASE 瘟疫 | 黑暗 2 级 | 0.7 | **全体敌方** | 击溃 **54** | 0 |
| **PLAGUE 瘟疫之风** | 黑暗 4 级 | 0.9 | **全体敌方** | 击溃 **70** | 0 |
| **FIREWALL 火墙** | 召唤 4 级 | 1.35 | 单堆 | 击溃 **105** | 0 |
| FIST_OF_WRATH | 召唤 1 级 | 0.45 | 单堆 | 击溃 35 | 0 |

**致命点**：
- **"全体敌方"AOE**（PLAGUE/DISEASE/SICKNESS）：如果分 3 堆低阶兵，一次群秒，三堆同时蒸发
- **ATTRITION 雪上加霜**：被击溃的单位按消耗率永久损失 50%+，一次 PLAGUE 永损 35-50 人/轮
- **高阶兵免疫**：T7P 10010 战力 > 法术伤害值，floor 成 0——精英流完美对冲

### 反制方案（步兵海玩家要做的）

1. **光明学派对冲**：MYSTIC_SHIELD（VALUE_MEMBERS 防御）同机制反推 + RESURRECTION Lv5 每回合把群攻打掉的单位拉回来
2. **混合 1 堆精英免疫位**：纯步兵海 → 改为 1 堆 1500 T1P + 1 堆 30 T6/T7 精英。精英堆对法术免疫，作为"最后一战"防崩溃
3. **单大堆主义**：绝对不分 3 堆小的——AOE 群秒最怕碎片化。推荐 1 堆 1500+ 而不是 3 堆 500
4. **侦察先行**：`HERO_SCOUT_TROOPS` 先看敌方英雄职业——**黑暗巫师 / 召唤师**是绝对天敌，切精英流；**力量流 / 光明流**敌人步兵海安全

### 流派选择决策树（第一赛季）

```
英雄是否走兵海流派？
│
├─ 英雄职业：领袖 + 光明巫师？
│   ├─ 否 → 精英流（上节兵团质量原则）
│   └─ 是 → 继续
│
├─ 阵营兵海底子（见上方阵营底子表）？
│   ├─ 圣堂 / 亡灵 → 步兵海双层底子，**步兵海首选（S 级）**
│   ├─ 森林 → T1 花仙子 88 起手（骑兵，**绝不升级 T1P**），**骑兵海 or 混合阵**
│   ├─ 地狱 / 学院 → 步兵海单层底子，步兵海可走但招募面窄
│   └─ 全阵营：**弓手海本赛季血统失效，不作主流派**
│
├─ PvE（清 NPC）？
│   ├─ NPC 普遍无 5 级 AOE → 兵海首选，经验性价比最高
│   └─ 高级 NPC 带法术？先 battle_simulator 模拟，带 AOE 则切精英流
│
├─ PvP？
│   ├─ 对手黑暗/召唤巫师 → **禁用兵海**，切精英流（VALUE_MEMBERS 伤害对大兵团镜像破坏）
│   ├─ 对手力量流/光明流/毁灭流 → 兵海可用
│   └─ 对手不明 → 混合阵（兵海主堆 1500+ + 1 堆 T6/T7 免疫堆做保险丝）
│
└─ 攻城战？
    └─ 守城通常带 AOE 法术 → 精英流更稳
```

### 交叉参考

- **$SKILL_DIR/heroes.md**：领袖职业的高谈阔论（通用 per-unit 攻击 SKILL）、军需官优等待遇（通用 per-unit 防御 SKILL）、光明巫师学派
- **$SKILL_DIR/equipment.md**：组合 1「步兵单兵攻击流」最大 +70；骑兵单兵攻击装备（仅 1 件）；远程单兵攻击装备（词条存在但 0 装备）
- **$SKILL_DIR/magic.md**：光明学派 VALUE_MEMBERS 增益（DIVINE_STRENGTH / **MYSTIC_SHIELD 对 CAV +50%** / RIGHTEOUS_MIGHT）、VALUE_MEMBERS 伤害（SICKNESS / DISEASE / PLAGUE / FIREWALL 全体敌方 AOE，对大兵团镜像破坏）、TELEPORTATION 对 SHOOTER **-50%**
- **$SKILL_DIR/factions.md**：各阵营 T1-T4 兵种类型分布（决定兵海底子），注意 T1 基础→进阶的类型变换陷阱（地狱/亡灵/学院）及**亡灵 T1P 战力反而低于 T1** 的数据陷阱
- **$SKILL_DIR/tear-war.md**：**血统（Heredity）系统**——跨世界传承加成。本赛季是第一赛季，**全员无血统能力**，所有 `HEREDITYABILITY_*` 效果（包括 PRE_FIGHT_ATTACK_SHOOTER 战前齐射）失效
- **源码验证**：`php/shared/framework/Entity/Data/EffectEntity.entity.php` 的 `'origin'` 字段定义四种加成来源 SKILL / ARTEFACT / SPELL / HEREDITYABILITY，本赛季前三者可用，第四种全员无

---

## 军队管理

### 英雄与城市之间移动部队

**全部卸载（英雄 → 城市驻军）：**
```bash
curl -k -s -b $COOKIES -X POST "$BASE/api/agent/action" \
  -H "Content-Type: application/json" \
  -d '{"type":"unitStackListAction","params":{"action":"MOVE_TO_REGION","heroId":<heroId>}}'
```

**单个兵团卸载：**
```bash
curl -k -s -b $COOKIES -X POST "$BASE/api/agent/action" \
  -H "Content-Type: application/json" \
  -d '{"type":"unitStackListAction","params":{"action":"MOVE_TO_REGION","heroId":<heroId>,"unitStackId":<stackId>}}'
```

**全部装载（城市驻军 → 英雄）：**
```bash
curl -k -s -b $COOKIES -X POST "$BASE/api/agent/action" \
  -H "Content-Type: application/json" \
  -d '{"type":"unitStackListAction","params":{"action":"MOVE_FROM_REGION","heroId":<heroId>}}'
```

注意事项：
- 英雄必须空闲（不在执行动作）
- 英雄不能在野外建筑或区域建筑上
- 每个英雄/城市最多 7 个兵团

### 合并军队

装载/卸载时如果目标位置**恰好有同一兵种**会自动融合，但这不能覆盖所有情况（如奖励部队、拆分后遗留等）。**必须主动检查并用 `unitStackAction FUSION` 手动合并。** 详见上方「军队整编」章节。

### 解放分兵

英雄学习职业或技能需要卸下所有部队：
1. `MOVE_TO_REGION` 卸载全部到驻军
2. 执行 `HERO_LEARN_CLASS` 或 `HERO_LEARN_SKILL`
3. `MOVE_FROM_REGION` 重新装载

### 招募到驻军 vs 英雄

招募通过 `REGION_RECRUIT` 执行，部队直接进入城市驻军。需要后续手动装载到英雄。

### 巡逻设置

```bash
# 设置巡逻
curl -k -s -b $COOKIES -X POST "$BASE/api/agent/action" \
  -H "Content-Type: application/json" \
  -d '{"type":"heroAction","params":{"action":"SET_PATROL","heroId":<heroId>}}'

# 取消巡逻
curl -k -s -b $COOKIES -X POST "$BASE/api/agent/action" \
  -H "Content-Type: application/json" \
  -d '{"type":"heroAction","params":{"action":"UNSET_PATROL","heroId":<heroId>}}'
```

巡逻中的英雄会自动参与城市防御战。

---

## 常见错误

### 1. 无视兵种克制盲目进攻

用弓手硬打骑兵（被克制），即使数量优势也可能惨败。克制方获得 +50% 加成是巨大的差距。

**正确做法：** 查看 `npcComposition`，用克制兵种主攻。

### 2. 不考虑荣耀修正打低级 NPC

反复打 Lv1 弱敌，荣耀修正为大幅负值，几乎不获得经验。

**正确做法：** 攻击与当前实力匹配的 NPC，荣耀修正接近 0 或正值。

### 3. 英雄忙碌时尝试操作部队

英雄在行军、战斗、执行动作期间不能移动部队，会报 `HERO_IS_BUSY` 错误。

**正确做法：** 检查 `hero._current_slaveActionId`，等待 timeline 中的 endDate。

### 4. 忘记战前装载部队

招募的部队在城市驻军中，不会自动跟随英雄。空手出征 = 必败。

**正确做法：** 攻击前执行 `MOVE_FROM_REGION` 装载驻军。

### 5. 全军压上打未知敌人

不先侦察就把所有英雄都派去攻击，失败后无兵防守。

**正确做法：** 保留至少一支防御力量，先用一个英雄试探。

### 6. 忽略免战机制被退回

战力比悬殊时战斗不会发生（CONFVALUE_NO_BATTLE_ARMY_POWER_RATIO），英雄白跑一趟。

**正确做法：** 确保战力比在合理范围内（1.3 倍以上有克制 或 1.5 倍以上无克制）再出击。

---

## NPC 等级难度参考表

NPC 等级由区域总战力与世界最大 NPC 战力的比值计算：`level = ceil(zonePower / maxNPCPower × 5)`

以下为典型的战力范围参考（实际值因世界配置不同而异）：

| NPC 等级 | gameState.npcLevel | 典型总战力范围 | 建议最低己方战力（有克制） | 建议最低己方战力（无克制） |
|---|---|---|---|---|
| Lv1（最弱） | 1 | 30 - 100 | 40 | 80 |
| Lv2 | 2 | 100 - 300 | 130 | 250 |
| Lv3 | 3 | 300 - 600 | 400 | 600 |
| Lv4 | 4 | 600 - 1200 | 800 | 1200 |
| Lv5（最强） | 5 | 1200+ | 1500+ | 2400+ |

**快速判定规则：**
- `npcLevel == 1` 且己方战力 > 100 → 安全出击
- `npcLevel == 2` 且己方战力 > 300 → 安全出击
- `npcLevel >= 3` → 必须检查兵种克制，确保战力比 >= 1.5
- 始终优先攻击有克制优势的目标

---

## 战斗模拟器

本地工具 `battle_simulator.py`，用 Bash 执行，传 JSON 参数。

脚本路径：同目录下 `battle_simulator.py`

### 快速评估（打不打得过）

```bash
python3 battle_simulator.py '{"quick":true,"atkPower":8000,"defPower":3000,"atkType":"CAVALRY","defType":"SHOOTER","heroAttack":5}'
```

参数：
- `atkPower`: 己方总基础战力（英雄所有兵团 power 之和）
- `defPower`: 敌方总基础战力（zone.npcPower）
- `atkType`: 己方主力兵种类型 INFANTRY/CAVALRY/SHOOTER（可选）
- `defType`: 敌方主力兵种类型（可选）
- `heroAttack`: 英雄攻击力（可选，默认0）
- `heroDefense`: 敌方英雄防御力（可选，默认0）

输出一行结果：`OVERRUN (zero loss)` / `EASY WIN (minimal loss)` / `WIN (moderate loss)` / `CLOSE WIN (heavy loss)` / `LOSE`

### 完整模拟（逐回合详情）

```bash
python3 battle_simulator.py '{
  "attacker": [
    {"type":"CAVALRY","power":370,"qty":15,"name":"地狱犬"},
    {"type":"SHOOTER","power":918,"qty":5,"name":"妖姬"},
    {"type":"INFANTRY","power":163,"qty":30,"name":"长角恶魔"}
  ],
  "defender": [
    {"type":"SHOOTER","power":410,"qty":10,"name":"地精射手"},
    {"type":"INFANTRY","power":115,"qty":20,"name":"地精"},
    {"type":"CAVALRY","power":245,"qty":8,"name":"野狼"}
  ],
  "hero": {"attack":5,"skill_attack_pct":3,"skill_attack_cavalry_pct":15},
  "actionType": "HERO_ATTACK_NPC"
}'
```

**attacker 数组**（按英雄部队位置排序，position 1 先出战）：
- `type`: 兵种类型 INFANTRY/CAVALRY/SHOOTER
- `power`: 单个单位战力（unitEntity.power，参考 $SKILL_DIR/factions.md）
- `qty`: 数量
- `name`: 显示名（可选）

**defender 数组**（会自动按总战力降序排列）：同上

**hero 对象**（攻击方英雄，可选）：
- `attack`: 英雄攻击力属性
- `defense`: 英雄防御力属性
- `skill_attack_pct`: 全军攻击百分比（斗士技能，如 Lv3 填 3）
- `skill_defense_pct`: 全军防御百分比（骑士技能）
- `skill_attack_infantry_pct` / `cavalry` / `shooter`: 兵种专属攻击百分比（如 Lv3 填 15）
- `skill_defense_infantry_pct` / `cavalry` / `shooter`: 兵种专属防御百分比
- `skill_attack_per_unit`: 每单位固定攻击加成（领袖技能，如 Lv3 填 15）
- `skill_defense_per_unit`: 每单位固定防御加成（建造者技能）
- `skill_attrition_increase`: 增加敌方消耗率（野蛮人技能）
- `skill_attrition_decrease`: 降低己方消耗率（骑士技能）

**defenderHero 对象**（防守方英雄，PvP 时使用，可选）：同 hero

**其他参数**（可选）：
- `actionType`: 战斗类型，默认 `HERO_ATTACK_NPC`；攻城用 `HERO_ATTACK_REGION_ATTACK`；掠夺用 `HERO_PILLAGE_ZONE_PILLAGE`
- `cityDefense`: 城防百分比（攻城战时）
- `pillageDefense`: 掠夺防御百分比（掠夺战时）

输出包含每回合的攻守双方战力、克制关系、胜负、碾压判定、损耗计算，最后给出总结果和荣耀修正值。
