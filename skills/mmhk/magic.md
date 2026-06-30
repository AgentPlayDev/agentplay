# 魔法篇

## 魔法系统概览

魔法是战斗六大因素之一。每座城市的魔法公会（MAGIC_GUILD）生产法术，英雄学习对应巫师职业后可将法术装入魔法书并在战斗中施放。

### 四大魔法学派

| ID | 学派 | 方向 | 核心效果 |
|----|------|------|----------|
| 1 | 毁灭 DESTRUCTION | 直接伤害 | 消灭敌方单位 |
| 2 | 黑暗 DARK | 削弱敌方 | 降低敌方英雄攻/防、对全体敌方造成伤害 |
| 3 | 光明 LIGHT | 强化己方 | 增加兵团攻/防、复活、固定伤害 |
| 4 | 召唤 SUMMON | 特殊 | 召唤临时部队、复活、伤害、城防削弱 |

### 阵营与魔法学派

每个阵营拥有两个魔法学派，决定魔法公会能生产哪些法术：

| 阵营 | 第一学派 | 第二学派 |
|------|----------|----------|
| 圣堂 HAVEN | 黑暗 DARK | 光明 LIGHT |
| 地狱 INFERNO | 毁灭 DESTRUCTION | 黑暗 DARK |
| 学院 ACADEMY | 光明 LIGHT | 召唤 SUMMON |
| 亡灵 NECROPOLIS | 召唤 SUMMON | 黑暗 DARK |
| 森林 SYLVAN | 召唤 SUMMON | 毁灭 DESTRUCTION |

**5级法术只能从本阵营的两个学派中获得。** 1-4级法术可通过 reroll 在同学派内随机更换。

---

## 完整法术表

### 毁灭学派 DESTRUCTION — 9个法术

全部为伤害类法术，目标均为敌方单兵团（ENNEMY_STACK）。

| ID | 法术名 | 等级 | 值 | 计算方式 | 效果说明 |
|----|--------|------|----|----------|----------|
| 2 | ELDERTICH_ARROW 魔能箭 | 1 | 130 | VALUE | 伤害 = 130 × 魔力 |
| 3 | STONE_SPIKES 石刺术 | 1 | 0.6 | VALUE_MEMBERS | 伤害 = 0.6 × 魔力 × 敌方单位数 |
| 4 | LIGHTNING_BOLT 闪电术 | 2 | 0.9 | VALUE_MEMBERS | 伤害 = 0.9 × 魔力 × 敌方单位数 |
| 5 | ICE_BOLT 冰箭术 | 2 | 0.25 | PERCENTAGE | 伤害 = 0.25 × 魔力 × 敌方单位数 × 单位战力 / 100 |
| 6 | FIREBALL 火球术 | 3 | 0.35 | PERCENTAGE | 伤害 = 0.35 × 魔力 × 敌方单位数 × 单位战力 / 100 |
| 7 | CIRCLE_OF_WINTER 寒冬之环 | 3 | 1.2 | VALUE_MEMBERS | 伤害 = 1.2 × 魔力 × 敌方单位数 |
| 8 | CHAIN_LIGHTNING 连锁闪电 | 4 | 180 | VALUE | 伤害 = 180 × 魔力 |
| 9 | METEOR_SHOWER 流星雨 | 4 | 1.7 | VALUE_MEMBERS | 伤害 = 1.7 × 魔力 × 敌方单位数 |
| 10 | IMPLOSION 内爆术 | 5 | 0.5 | PERCENTAGE | 伤害 = 0.5 × 魔力 × 敌方单位数 × 单位战力 / 100 |

**特点：** 毁灭法术全部针对单个敌方兵团（ENNEMY_STACK），适合集中火力消灭高威胁目标。PERCENTAGE 类法术对高战力单位更有效，VALUE_MEMBERS 类对大量低战力单位更有效。

### 黑暗学派 DARK — 9个法术

混合伤害和减益，伤害类打全体敌方（ENNEMY_ALL_STACKS），减益类打敌方英雄。

| ID | 法术名 | 等级 | 值 | 效果类型 | 目标 | 计算方式 |
|----|--------|------|----|----------|------|----------|
| 11 | WEAKNESS 虚弱 | 1 | -0.35 | 英雄攻击减 | 敌方英雄 | VALUE |
| 12 | SICKNESS 疫病 | 1 | 0.5 | 伤害 | 全体敌方 | VALUE_MEMBERS |
| 13 | GUARD_BREAK 破防 | 2 | -0.17 | 英雄防御减 | 敌方英雄 | VALUE |
| 14 | DISEASE 瘟疫 | 2 | 0.7 | 伤害 | 全体敌方 | VALUE_MEMBERS |
| 15 | SLOW 减速 | 3 | -0.5 | 英雄攻击减 | 敌方英雄 | VALUE |
| 16 | VULNERABILITY 脆弱 | 3 | -0.35 | 英雄防御减 | 敌方英雄 | VALUE |
| 17 | DEATH_TOUCH 死亡之触 | 4 | -0.6 | 英雄攻击减 | 敌方英雄 | VALUE |
| 18 | PLAGUE 瘟疫之风 | 4 | 0.9 | 伤害 | 全体敌方 | VALUE_MEMBERS |
| 19 | WORD_OF_DEATH 死亡宣言 | 5 | 0.15 | 伤害 | 全体敌方 | PERCENTAGE |

**特点：**
- 减益法术（WEAKNESS/GUARD_BREAK/SLOW/VULNERABILITY/DEATH_TOUCH）降低敌方英雄攻/防属性。**对 NPC 无效**（NPC 无英雄属性）。PvP 战斗中价值极高。
- 伤害法术（SICKNESS/DISEASE/PLAGUE/WORD_OF_DEATH）打**全体敌方兵团**，每个兵团分别计算伤害。对多兵团敌军总伤害更高。

### 光明学派 LIGHT — 9个法术

增益+复活+少量伤害，主要强化己方。

| ID | 法术名 | 等级 | 值 | 效果类型 | 目标 | 计算方式 |
|----|--------|------|----|----------|------|----------|
| 20 | DIVINE_STRENGTH 神圣之力 | 1 | 0.3 | 兵团攻击加 | 己方兵团 | VALUE_MEMBERS |
| 21 | BLESS 祝福 | 1 | 0.35 | 兵团防御加 | 己方兵团 | PERCENTAGE |
| 22 | MYSTIC_SHIELD 神秘护盾 | 2 | 0.6 | 兵团防御加 | 己方兵团 | VALUE_MEMBERS |
| 23 | HASTE 加速 | 2 | 0.3 | 兵团攻击加 | 己方兵团 | PERCENTAGE |
| 24 | RIGHTEOUS_MIGHT 正义之力 | 3 | 0.6 | 兵团攻击加 | 己方兵团 | VALUE_MEMBERS |
| 25 | DEFLECT_MISSILE 偏转箭矢 | 3 | 0.45 | 兵团防御加 | 己方兵团 | PERCENTAGE |
| 26 | TELEPORTATION 传送 | 4 | 0.4 | 兵团攻击加 | 己方兵团 | PERCENTAGE |
| 27 | WORD_OF_LIGHT 光明之语 | 4 | 110 | 伤害 | 敌方兵团 | VALUE |
| 28 | RESURRECTION 复活 | 5 | 0.3 | 永久复活 | 己方兵团 | PERCENTAGE |

**特点：**
- 增益法术增加己方当前出战兵团的等效战力（转换为额外单位数），在回合战力比较中直接起作用
- WORD_OF_LIGHT 是光明学派唯一的伤害法术（110 × 魔力，固定值）
- RESURRECTION 是唯一的永久复活法术（5级），复活回合后的击溃单位

**特殊兵种修正：**
- TELEPORTATION：对弓手(SHOOTER)效果 **-50%**
- MYSTIC_SHIELD：对骑兵(CAVALRY)效果 **+50%**
- DEFLECT_MISSILE：对敌方弓手(SHOOTER)效果 **+50%**

### 召唤学派 SUMMON — 9个法术

召唤+伤害+复活+城防削弱，最多样化的学派。

| ID | 法术名 | 等级 | 值 | 效果类型 | 目标 | 计算方式 |
|----|--------|------|----|----------|------|----------|
| 29 | FIST_OF_WRATH 愤怒之拳 | 1 | 0.45 | 伤害 | 敌方兵团 | VALUE_MEMBERS |
| 30 | WASP_SWARM 黄蜂群 | 1 | 110 | 召唤 | 骑兵 | VALUE |
| 31 | RAISE_DEAD 亡灵复苏 | 2 | 0.25 | 临时复活 | 己方兵团 | PERCENTAGE |
| 32 | FIRE_TRAP 火焰陷阱 | 2 | 0.25 | 伤害 | 敌方兵团 | PERCENTAGE |
| 33 | PHANTOM_FORCES 幻影军团 | 3 | 130 | 召唤 | 弓手 | VALUE |
| 34 | EARTHQUAKE 地震 | 3 | -0.5 | 城防减 | 无 | VALUE |
| 35 | SUMMON_ELEMENTALS 召唤元素 | 4 | 150 | 召唤 | 步兵 | VALUE |
| 36 | FIREWALL 火墙 | 4 | 1.35 | 伤害 | 敌方兵团 | VALUE_MEMBERS |
| 37 | CONJURE_PHOENIX 召唤凤凰 | 5 | 0.27 | 召唤 | 骑兵 | PERCENTAGE |

**特点：**
- 召唤法术创建**临时部队**加入己方出战序列。召唤的单位为本阵营对应兵种类型的 T1 基础兵种
- RAISE_DEAD 是**临时复活**（回合后消失），与 RESURRECTION 的永久复活不同
- EARTHQUAKE 削弱城防百分比，仅在攻城战中有用
- FIRE_TRAP 对弓手(SHOOTER)伤害 **-50%**

---

## 法术效果计算公式

### 三种计算方式

| 计算方式 | 公式 | 适用场景 |
|----------|------|----------|
| VALUE | `值 × 魔力` | 固定伤害/效果，不受目标属性影响 |
| VALUE_MEMBERS | `值 × 魔力 × 目标单位数` | 效果随目标数量线性增长 |
| PERCENTAGE | `值 × 魔力 × 目标单位数 × 目标单位战力 / 100` | 效果随目标战力成比例增长 |

### 魔力（heroMagic）计算

```
有效魔力 = 基础魔力 × (1 + 效率加成)
```

基础魔力 = 英雄 magic 属性 + 学派魔力加成（技能 `[SCHOOL]_ADDED_MAGIC_POINTS`）

效率加成来源：
1. **学派精通技能**：如毁灭精通 +9%/+18%/+27%
2. **5级法术多持加成**：同学派每多一个5级法术 × `CONFVALUE_MAGIC_BONUS_MULTIPLE_SPELLS`
3. **血统能力**：`SPELL_EFFICIENCY_INCREASE_SPECIFIC_LEVEL`（指定等级法术加成）
4. **兵种效率**：对特定兵种的法术效率加成
5. **学派特定加成**：如毁灭系的 VALUE/PERCENTAGE 分别加成、黑暗系的英雄诅咒加成、召唤系的召唤加成

### 伤害法术击杀数

```
击溃单位数 = floor(法术伤害值 / 目标单位战力)
```

伤害法术直接消灭敌方单位（计入击溃列表），被消灭的单位参与消耗（attrition）计算。

### 增益法术等效单位数

```
等效额外单位 = floor(法术效果值 / 兵团单位战力)
```

增益法术不增加实际单位数，而是以**战力加成**（powerBonus）形式参与回合战力比较。

### 召唤法术数量

```
召唤单位数 = floor(法术效果值 / 召唤单位的单位战力)
```

其中法术效果值的 `targetValue` 参数为**敌方全军总战力**（不是单个兵团），因此敌方越强，召唤的单位越多。

### 复活法术

- **临时复活**（RAISE_DEAD）：复活的单位以 powerBonus 形式存在，回合后消失
- **永久复活**（RESURRECTION）：复活的单位永久恢复，但不能超过该兵团已击溃的总数

---

## 法术管理操作

### 前置条件

1. **建造魔法公会**：MAGIC_GUILD_LVL1 ~ MAGIC_GUILD_LVL5，等级决定可用法术等级
2. **英雄学习巫师职业**：对应学派的巫师职业（毁灭巫师/黑暗巫师/光明牧师/召唤师）
3. **英雄有魔力属性**（magic > 0）

### 法术流转

```
魔法公会生产法术（每级2个，来自阵营的两个学派各一个）
    ↓
spellStackAction ADD_TO_SPELLBOOK — 加入英雄魔法书（最多4~7个）
    ↓
spellStackAction ADD_TO_BATTLE — 装备到战斗栏（roundPosition 决定施放回合）
    ↓
战斗中自动施放 → 施放后进入冷却
```

### 容量限制

| 容量 | 基础值 | 最大值 | 扩展方式 |
|------|--------|--------|----------|
| 魔法公会产出 | 每级2个 | 9个总计 | 升级魔法公会 |
| 魔法书容量 | 4个 | 7个 | 巫师技能 `[SCHOOL]_SPELLBOOK_SPELL_NUMBER` |
| 战斗栏容量 | 1个 | 2个 | 巫师技能 `[SCHOOL]_ADDED_BATTLE_SPELL_LEVEL` |

**战斗栏第2个法术限制：** 两个法术中必须有一个的等级 ≤ 巫师"升级"技能等级。例如升级技能 Lv2 时，可带一个5级法术+一个2级或更低的法术。

### 操作示例

```json
// 将法术加入魔法书
{"type": "spellStackAction", "params": {"action": "ADD_TO_SPELLBOOK", "spellStackId": 42, "heroId": 7}}

// 从魔法书移除
{"type": "spellStackAction", "params": {"action": "REMOVE_FROM_SPELLBOOK", "spellStackId": 42}}

// 装备到战斗栏
{"type": "spellStackAction", "params": {"action": "ADD_TO_BATTLE", "spellStackId": 42}}

// 从战斗栏卸下
{"type": "spellStackAction", "params": {"action": "REMOVE_FROM_BATTLE", "spellStackId": 42}}

// 调整施放回合（roundPosition 1~14）
{"type": "spellStackAction", "params": {"action": "MOVE", "spellStackId": 42, "newPosition": 3}}

// 交换两个法术位置
{"type": "spellStackAction", "params": {"action": "PERMUTATION", "spellStackId": 42, "spellStack2Id": 43}}
```

### 获取法术信息

法术数据来自 `getContent HeroFrame`（英雄魔法书+战斗栏法术）和魔法公会面板。

---

## 法术施放时机

### 回合前施放

每回合兵团对决前，按 roundPosition 顺序施放：
1. 攻击方法术（DAMAGE / STACK_BONUS / HERO_BONUS / SUMMONING / FORTIFICATION_BONUS）
2. 防守方法术（同上）
3. 兵团对决

### 回合后施放

兵团对决后、消耗计算前：
1. 攻击方复活法术（TEMPORARY_RESURRECTION / PERMANENT_RESURRECTION）
2. 防守方复活法术

### 攻防限制

并非所有法术在攻击和防御时都能使用：

**攻击时不可用：**
- 增加己方英雄防御的法术（如 ally hero + HERO_DEFENSE_BONUS）
- 降低敌方英雄攻击的法术（如 enemy hero + HERO_ATTACK_BONUS）
- 增加己方兵团防御的法术（如 ally stack + STACK_DEFENSE_BONUS）
- 降低敌方兵团攻击的法术

换言之：**攻击方只能增强攻击力或削弱对手防御，不能在攻击时增强自己的防御。**

**防御时不可用：**
- 增加己方英雄攻击的法术
- 降低敌方英雄防御的法术
- 增加己方兵团攻击的法术
- 降低敌方兵团防御的法术

换言之：**防御方只能增强防御力或削弱对手攻击，不能在防御时增强自己的攻击。**

**实际影响：**
- 黑暗法术 WEAKNESS/SLOW/DEATH_TOUCH（降敌方攻击）→ **防御时有效，攻击时无效**
- 黑暗法术 GUARD_BREAK/VULNERABILITY（降敌方防御）→ **攻击时有效，防御时无效**
- 光明法术 DIVINE_STRENGTH/HASTE/RIGHTEOUS_MIGHT/TELEPORTATION（增己方攻击）→ **攻击时有效，防御时无效**
- 光明法术 BLESS/MYSTIC_SHIELD/DEFLECT_MISSILE（增己方防御）→ **防御时有效，攻击时无效**
- 伤害/召唤/复活/城防法术 → 攻防均可用

---

## 冷却系统

法术施放后进入冷却期，冷却期间不能再次装备到战斗栏。

```
冷却时间 = 基础冷却时间(CONFVALUE_SPELL_COOLDOWN_DURATION) × 世界速度 × (1 - 冷却减少%)
```

冷却减少来自 `SPELL_COOLDOWN_DECREASE` 效果。

---

## 魔法策略建议

### NPC 战斗（PvE）

**黑暗减益法术对 NPC 无效！** NPC 没有英雄属性，WEAKNESS/GUARD_BREAK/SLOW/VULNERABILITY/DEATH_TOUCH 的减益效果为零。对 NPC 只用伤害/增益/召唤类法术。

推荐法术优先级（PvE）：
1. **毁灭伤害法术** — 直接消灭敌方单位，减少己方损失
2. **光明增益法术** — 增加己方兵团战力，特别是 DIVINE_STRENGTH/RIGHTEOUS_MIGHT
3. **召唤法术** — 召唤额外部队分担伤害
4. **光明 RESURRECTION** — 永久复活击溃单位，减少实际损失

### PvP 战斗

PvP 中敌方英雄有属性值，黑暗减益法术非常强力：
1. **黑暗减益** — DEATH_TOUCH(-0.6攻击)/VULNERABILITY(-0.35防御) 大幅削弱敌方
2. **毁灭伤害** — IMPLOSION 对高战力兵团毁灭性打击
3. **光明增益** — 增强己方同时配合兵种克制
4. **复活** — 长期战斗中减少消耗

### 攻城战

- EARTHQUAKE（召唤3级）削弱城防百分比，攻城必备
- 伤害法术削弱守军数量
- 增益法术弥补攻城方劣势

### 法术安排回合位

- **增益法术放第1回合**（roundPosition=1）：在首次对决前增强己方
- **伤害法术放第2-3回合**：消灭敌方剩余兵团
- **复活法术放靠后回合**：在伤亡发生后施放才有效
- **召唤法术放中间回合**：补充战斗中消耗的兵力

### 阵营魔法推荐

| 阵营 | 可用学派 | PvE 推荐 | PvP 推荐 |
|------|----------|----------|----------|
| 圣堂 HAVEN | 黑暗+光明 | 光明增益（DIVINE_STRENGTH/BLESS） | 黑暗减益（DEATH_TOUCH/VULNERABILITY） |
| 地狱 INFERNO | 毁灭+黑暗 | 毁灭伤害（FIREBALL/METEOR_SHOWER） | 毁灭+黑暗减益双管齐下 |
| 学院 ACADEMY | 光明+召唤 | 光明增益+召唤补兵 | 光明+召唤（RESURRECTION 最强PvP法术） |
| 亡灵 NECROPOLIS | 召唤+黑暗 | 召唤（SUMMON_ELEMENTALS/FIREWALL） | 黑暗减益+召唤 |
| 森林 SYLVAN | 召唤+毁灭 | 毁灭伤害+召唤 | 毁灭高伤害+召唤补兵 |

### 符文要塞战争

**符文要塞战斗中魔法完全被禁用**（antiMagic = TRUE）。不要依赖魔法作为终局战争的核心战力。

---

## 巫师职业技能速查

详见 `$SKILL_DIR/heroes.md` 中的巫师职业章节。核心技能：

| 技能 | 效果 | 对魔法的影响 |
|------|------|-------------|
| 学派精通（Lv1/2/3） | +9%/+18%/+27% | 法术效果直接提升 |
| 学派魔法书（Lv1/2/3） | +1/+2/+3 | 魔法书容量增加 |
| 学派升级（Lv1/2/3） | +1/+2/+3 | 可装备第2个战斗法术，等级限制放宽 |
| 学派魔力（Lv1/2/3） | +5/+10/+15 | 基础魔力提升，所有法术更强 |

**投资优先级：** 精通 > 魔力 > 升级 > 魔法书。精通直接乘以所有法术效果，魔力提升基础值，升级允许双法术出战，魔法书只增加备选数量。
