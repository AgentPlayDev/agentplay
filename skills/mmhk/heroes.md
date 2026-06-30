# 英雄职业表

## 职业总览

### 战士系职业（heroTrainingCategory: WARRIOR）

| ID | tagName | 中文名 | 方向 |
|----|---------|--------|------|
| 1 | ARCHITECT | 建筑师 | 加速建筑建造 |
| 2 | BUILDER | 建造者 | 资源收入提升 |
| 3 | LEADER | 领袖 | 综合部队能力提升 |
| 4 | KNIGHT | 骑士 | 防御方向 |
| 7 | BARBARIAN | 野蛮人 | 掠夺和反侦察 |
| 8 | FIGHTER | 斗士 | 攻击方向 |
| 9 | RANGER | 游侠 | 侦查和移动 |
| 10 | LANDLORD | 拓荒者 | 英雄招募强化 |
| 11 | MERCHANT | 商人 | 贸易和经济 |

### 巫师系职业（heroTrainingCategory: WARRIOR_MAGE / MAGE）

| ID | tagName | 中文名 | 方向 |
|----|---------|--------|------|
| 5 | DESTRUCTIVE_WIZARD | 毁灭巫师 | 攻击魔法 |
| 6 | DARK_WIZARD | 黑暗巫师 | 黑暗魔法 |
| 12 | LIGHT_WIZARD | 光明牧师 | 光明/治疗魔法 |
| 13 | SUMMONING_WIZARD | 召唤师 | 召唤魔法 |

巫师系职业需要魔法行会建筑支持。

## 技能系统

每个技能最高 3 级。学习费用：Lv1=1点, Lv2=2点, Lv3=3点（满级一个技能共需6点）。

学习条件：英雄必须空闲且没有部队。

## 各职业技能详情

### 斗士 FIGHTER (ID:8) — 攻击核心职业

| 技能ID | 技能名 | Lv1 | Lv2 | Lv3 |
|--------|--------|-----|-----|-----|
| 5 | 军事家 ARMY_ATTACK_POWER_INCREASE | +1% | +2% | +3% |
| 6 | 精锐骑兵 CAVALRY_ATTACK_POWER_INCREASE | +5% | +10% | +15% |
| 7 | 神射手 SHOOTER_ATTACK_POWER_INCREASE | +5% | +10% | +15% |
| 8 | 高级步兵 INFANTRY_ATTACK_POWER_INCREASE | +5% | +10% | +15% |

军事家对全部兵种生效；兵种专属技能仅在拥有兵种克制优势时生效。

### 骑士 KNIGHT (ID:4) — 防御核心职业

| 技能ID | 技能名 | Lv1 | Lv2 | Lv3 |
|--------|--------|-----|-----|-----|
| 30 | 防御专家 ARMY_DEFENSE_POWER_INCREASE | +1% | +2% | +3% |
| 31 | 骑兵防御 CAVALRY_DEFENSE_POWER_INCREASE | +5% | +10% | +15% |
| 32 | 射手防御 SHOOTER_DEFENSE_POWER_INCREASE | +5% | +10% | +15% |
| 33 | 步兵防御 INFANTRY_DEFENSE_POWER_INCREASE | +5% | +10% | +15% |
| 34 | 后勤专家 ATTRITION_RATE_DECREASE | -2% | -4% | -6% |

与斗士镜像结构，防御方向。兵种专属技能仅在拥有兵种克制优势时生效。

### 领袖 LEADER (ID:3) — 综合职业

| 技能ID | 技能名 | Lv1 | Lv2 | Lv3 |
|--------|--------|-----|-----|-----|
| 1 | 领导魅力 UNIT_PRODUCTION_INCREASE | +1 | +2 | +3 |
| 2 | 高级教练 UNIT_RECRUITMENT_SPEED_INCREASE | +9% | +18% | +27% |
| 3 | 外交官 NEUTRAL_STACK_RECRUITMENT_INCREASE | +9% | +18% | +27% |
| 4 | 高谈阔论 ATTACK_POWER_PER_UNIT_INCREASE | +5 | +10 | +15 |

高谈阔论是**通用** per-unit 固定值加成（对步兵/骑兵/弓手都生效），不限兵种，部队数量越多效果越好。配合装备和光明学派 VALUE_MEMBERS 增益法术（DIVINE_STRENGTH / RIGHTEOUS_MIGHT / MYSTIC_SHIELD）组成「兵海流派」的核心。三兵海强度分档（第一赛季）：**步兵海 S 级**（装备生态最完整，+100/兵）、**骑兵海 A 级**（MYSTIC_SHIELD 独享 CAV +50% 防御超模）、**弓手海 D 级/本赛季废流派**（核心 PRE_FIGHT_ATTACK_SHOOTER 是血统能力 HEREDITYABILITY，需上一世界 Tear War 传承，第一赛季全员无）。完整规则、成立条件、天敌反制详见 $SKILL_DIR/combat.md「弱兵战术：兵海流派」。

### 建筑师 ARCHITECT (ID:1)

| 技能ID | 技能名 | Lv1 | Lv2 | Lv3 |
|--------|--------|-----|-----|-----|
| 9 | 工长 BUILDING_SPEED_INCREASE | +9% | +18% | +27% |
| 10 | 攻城专家 BOMBARDING_BONUS | +9% | +18% | +27% |
| 11 | 防御建筑师 TOWN_DEFENSE_INCREASE | +3% | +6% | +9% |
| 12 | 工程兵 TOWN_DEFENSE_DECREASE | +3% | +6% | +9% |

### 建造者 BUILDER (ID:2)

| 技能ID | 技能名 | Lv1 | Lv2 | Lv3 |
|--------|--------|-----|-----|-----|
| 21 | 掘金者 INCOME_GOLD_INCREASE | +3% | +6% | +9% |
| 19 | 军需官 INCOME_COMMON_INCREASE | +3% | +6% | +9% |
| 20 | 炼金术士 INCOME_RARE_INCREASE | +3% | +6% | +9% |
| 22 | 优等待遇 DEFENSE_POWER_PER_UNIT_INCREASE | +5 | +10 | +15 |

优等待遇是固定值加成（每个单位+5/10/15），与领袖的高谈阔论对称（一个加攻击，一个加防御）。

### 游侠 RANGER (ID:9)

| 技能ID | 技能名 | Lv1 | Lv2 | Lv3 |
|--------|--------|-----|-----|-----|
| 13 | 侦察大师 SCOUTING_LEVEL_INCREASE | +5 | +10 | +15 |
| 14 | 疾行者 SCOUTING_DELAY_DECREASE | -9% | -18% | -27% |
| 15 | 情报专家 SCOUTING_DURATION_DECREASE | -21% | -42% | -63% |

### 野蛮人 BARBARIAN (ID:7)

| 技能ID | 技能名 | Lv1 | Lv2 | Lv3 |
|--------|--------|-----|-----|-----|
| 27 | 间谍猎人 SCOUTING_DETECT_LEVEL_INCREASE | +5 | +10 | +15 |
| 28 | 屠夫 ATTRITION_RATE_INCREASE | +9% | +18% | +27% |
| 29 | 掠夺大师 PILLAGE_INCREASE | +9% | +18% | +27% |

### 拓荒者 LANDLORD (ID:10)

| 技能ID | 技能名 | Lv1 | Lv2 | Lv3 |
|--------|--------|-----|-----|-----|
| 16 | 酒馆爱好者 TAVERN_COST_DECREASE | -9% | -18% | -27% |
| 17 | 募兵者 HERO_RECRUITMENT_HERO_INCREASE | +1 | +2 | +3 |
| 18 | 募兵领导者 HERO_RECRUITMENT_ARMY_INCREASE | +45% | +90% | +135% |
| 50 | 折扣 MAINTENANCE_DECREASE | -3% | -6% | -9% |

募兵领导者效果极其强大（满级+135%兵力），是拓荒者的核心技能。

### 商人 MERCHANT (ID:11)

| 技能ID | 技能名 | Lv1 | Lv2 | Lv3 |
|--------|--------|-----|-----|-----|
| 23 | 销售精英 NPC_SELL_INCREASE | +9% | +18% | +27% |
| 25 | 高级运输队 CARAVAN_CAPACITY_INCREASE | +9% | +18% | +27% |
| 26 | 快马加鞭 CARAVAN_SPEED_INCREASE | +9% | +18% | +27% |

### 毁灭巫师 DESTRUCTIVE_WIZARD (ID:5)

| 技能ID | 技能名 | Lv1 | Lv2 | Lv3 |
|--------|--------|-----|-----|-----|
| 35 | 毁灭精通 DESTRUCTION_SPELL_EFFICIENCY | +9% | +18% | +27% |
| 36 | 毁灭魔法书 DESTRUCTION_SPELLBOOK_SPELL_NUMBER | +1 | +2 | +3 |
| 37 | 毁灭升级 DESTRUCTION_ADDED_BATTLE_SPELL_LEVEL | +1 | +2 | +3 |
| 51 | 毁灭魔力 DESTRUCTION_ADDED_MAGIC_POINTS | +5 | +10 | +15 |

### 黑暗巫师 DARK_WIZARD (ID:6)

| 技能ID | 技能名 | Lv1 | Lv2 | Lv3 |
|--------|--------|-----|-----|-----|
| 38 | 黑暗精通 DARK_SPELL_EFFICIENCY | +9% | +18% | +27% |
| 40 | 黑暗魔法书 DARK_SPELLBOOK_SPELL_NUMBER | +1 | +2 | +3 |
| 41 | 黑暗升级 DARK_ADDED_BATTLE_SPELL_LEVEL | +1 | +2 | +3 |
| 52 | 黑暗魔力 DARK_ADDED_MAGIC_POINTS | +5 | +10 | +15 |

### 光明牧师 LIGHT_WIZARD (ID:12)

| 技能ID | 技能名 | Lv1 | Lv2 | Lv3 |
|--------|--------|-----|-----|-----|
| 44 | 光明精通 LIGHT_SPELL_EFFICIENCY | +9% | +18% | +27% |
| 43 | 光明魔法书 LIGHT_SPELLBOOK_SPELL_NUMBER | +1 | +2 | +3 |
| 42 | 光明升级 LIGHT_ADDED_BATTLE_SPELL_LEVEL | +1 | +2 | +3 |
| 53 | 光明魔力 LIGHT_ADDED_MAGIC_POINTS | +5 | +10 | +15 |

### 召唤师 SUMMONING_WIZARD (ID:13)

| 技能ID | 技能名 | Lv1 | Lv2 | Lv3 |
|--------|--------|-----|-----|-----|
| 47 | 召唤精通 SUMMON_SPELL_EFFICIENCY | +9% | +18% | +27% |
| 46 | 召唤魔法书 SUMMON_SPELLBOOK_SPELL_NUMBER | +1 | +2 | +3 |
| 45 | 召唤升级 SUMMON_ADDED_BATTLE_SPELL_LEVEL | +1 | +2 | +3 |
| 54 | 召唤魔力 SUMMON_ADDED_MAGIC_POINTS | +5 | +10 | +15 |

## 英雄训练类型与满级属性

所有英雄满级(Lv40)总计120属性点，分配由 `heroTrainingEntityTagName` 决定：

| ID | heroTrainingEntityTagName | ATK | DEF | MAG | 定位 |
|----|--------------------------|-----|-----|-----|------|
| 1 | PALADIN | 40 | 60 | 20 | 防御偏魔 |
| 2 | WARMASTER | 60 | 60 | 0 | 纯攻防 |
| 3 | WARMAGE | 40 | 20 | 60 | 攻魔型 |
| 4 | FANATIC_SORCERER | 60 | 0 | 60 | 攻魔双高 |
| 5 | ARCANE_MAGE | 30 | 30 | 60 | 法师 |
| 6 | WARRIOR_MAGE | 40 | 40 | 40 | 三项均衡 |
| 7 | PROTECTOR | 0 | 60 | 60 | 防魔型 |
| 8 | ILLUMINATED_PROTECTOR | 0 | 60 | 60 | 防魔型 |
| 9 | OUTLAND_WARRIOR | 60 | 60 | 0 | 纯攻防 |
| 10 | MERCENARY | 60 | 60 | 0 | 纯攻防 |
| 11 | DISTURBED_WIZARD | 60 | 0 | 60 | 攻魔双高 |
| 12 | PIT_WARRIOR | 60 | 60 | 0 | 纯攻防 |
| 13 | SOBERED_WIZARD | 20 | 60 | 40 | 防御偏魔 |
| 14 | EXPLORER | 60 | 30 | 30 | 攻击偏全能 |
| 15 | SENACHAL | 30 | 60 | 30 | 防御偏全能 |

## 职业选择建议

### 核心原则：先查满级属性，再选职业

**每个英雄最多学3个职业，选错无法撤销。** 在学习任何职业前：

1. 从 gameState 读取英雄的 `heroTrainingEntityTagName`
2. 查上面的表，确认满级 ATK/DEF/MAG 分配
3. 根据属性分配选择职业

### 重要：技能 > 职业数量

**不要急着学满3个职业。** 职业本身没有战力加成，真正有用的是职业里的技能。技能点是有限资源：
- 学一个职业消耗 1 技能点
- 升一个技能满级需要 1+2+3=6 技能点
- 英雄总技能点有限，学太多职业会导致技能点分散，每个技能都练不满

**正确策略：先学1个最匹配的职业 → 把核心技能升到高级 → 再考虑第2个职业。** 第3个职业通常要到中后期才学。

### 按满级属性选职业

| 满级属性特征 | 首选职业 | 核心技能投资 | 何时学第2职业 |
|-------------|---------|------------|-------------|
| ATK高, MAG=0 | 斗士 FIGHTER | 军事家+兵种专属攻击 | 技能升到Lv2后学骑士或领袖 |
| DEF高, MAG=0 | 骑士 KNIGHT | 防御专家+后勤专家 | 技能升到Lv2后学领袖 |
| ATK高, MAG高 | 斗士 FIGHTER | 军事家+兵种专属攻击 | 技能升到Lv2后学毁灭巫师或光明牧师 |
| MAG高, ATK低 | 毁灭巫师 / 光明牧师 | 魔法精通+魔法书 | 技能升到Lv2后学另一个魔法职业 |
| DEF高, MAG高 | 骑士 KNIGHT | 防御专家 | 技能升到Lv2后学光明牧师（治疗+防御） |
| 三项均衡 | 斗士 FIGHTER 或 领袖 LEADER | 看当前需求 | 灵活选择 |

### 经济职业分配原则

建造者(BUILDER)、拓荒者(LANDLORD)、商人(MERCHANT)、建筑师(ARCHITECT) 是经济/辅助职业：
- **ATK 或 MAG 满级 ≥ 40 的英雄不要学经济职业** — 战斗潜力太高，浪费职业槽
- 经济职业留给属性成长差的英雄（酒馆招到的低成长英雄）
- 每城有1个经济型英雄即可，其他英雄全部走战斗路线

## 学习操作

```json
// 学习职业（英雄必须无部队）
{"type": "addAction", "params": {
  "actionType": "HERO_LEARN_CLASS", "actorType": "Hero",
  "actorId": <heroId>, "actionParams": "<职业ID>"
}}

// 学习技能（英雄必须无部队）
{"type": "addAction", "params": {
  "actionType": "HERO_LEARN_SKILL", "actorType": "Hero",
  "actorId": <heroId>, "actionParams": "<技能tagName>"
}}
```

**学习技能用 tagName**，如 `"INCOME_GOLD_INCREASE"`，不是实例ID。技能tagName从 `getContent HeroFrame` 的 `heroSkillList[].heroClassSkillEntityTagName` 获取。

## 技能学习冷却机制

**重要：技能学习有 99 秒冷却期。** `HeroFrame` 中的 `learnSkillTime: 99` 表示冷却剩余秒数。学习新技能前必须等待冷却结束，否则返回 `IMPOSSIBLE_ACTION`。

同样，`learnClassTime: 99` 表示职业学习冷却。

**冷却中表现：**
- `getContent HeroFrame` 返回的 `availXpSkills` 可能显示有技能点
- 但 `HERO_LEARN_SKILL` 仍然返回 `IMOSSIBLE_ACTION`
- 解决：等待 99 秒后再试

**实际验证的技能 tagName（经济类）：**
- `INCOME_GOLD_INCREASE` — 掘金者，金币收入+3%/6%/9%
- `INCOME_COMMON_INCREASE` — 军需官，普通资源+3%/6%/9%
- `MAINTENANCE_DECREASE` — 折扣，维护费-3%/6%/9%
- `TAVERN_COST_DECREASE` — 酒馆爱好者，酒馆费用-9%/18%/27%
- `ATTACK_POWER_PER_UNIT_INCREASE` — 高谈阔论，每兵+5/10/15攻击（农民海核心！）

**战士战斗类：**
- `ATTACK_POWER_PER_UNIT_INCREASE` — 高谈阔论（固定值）
- `INFANTRY_ATTACK_POWER_INCREASE` — 步兵攻击
- `CAVALRY_ATTACK_POWER_INCREASE` — 骑兵攻击
- `SHOOTER_ATTACK_POWER_INCREASE` — 弓手攻击
