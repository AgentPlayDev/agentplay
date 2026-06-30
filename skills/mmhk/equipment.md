# 装备组合指南

## 基础规则

- 每个英雄有 8 个装备槽：右手 / 左手 / 头盔 / 胸甲 / 鞋子 / 斗篷 / 戒指 / 项链
- 每个部位只能装备 1 件
- 装备等级 = 所有效果等级之和（如一件装备有 3 个效果分别 lvl2+lvl3+lvl2 = 7 级）
- **世袭装备等级 = 0**，不消耗英雄等级
- 已装备的装备等级总和不能超过英雄等级（英雄最高 40 级）
- 装备不限种族，任何英雄可穿任何装备
- 装备通过 `getContent HeroFrame` 获取，用 `tagName` 字段识别

## 效果体系

同一种效果在多件不同部位的装备上可以叠加。

### 攻击效果

| 效果 | 类型 | lvl1 / lvl2 / lvl3 | 作用范围 |
|---|---|---|---|
| 步兵单兵攻击 | 加值 | +5 / +10 / +15 | 仅步兵，每个步兵都加 |
| 骑兵单兵攻击 | 加值 | +5 / +10 / +15 | 仅骑兵（仅 1 件装备有） |
| 远程单兵攻击 | 加值 | +5 / +10 / +15 | 仅远程（无装备提供此效果） |
| 英雄攻击 + | 加值 | +2 / +4 / +6 | 英雄统帅，所有兵种受益 |
| 英雄攻击 % | 百分比 | +4% / +8% / +12% | 英雄统帅，所有兵种受益 |

### 防御效果

| 效果 | 类型 | lvl1 / lvl2 / lvl3 | 作用范围 |
|---|---|---|---|
| 通用单兵防御 | 加值 | +5 / +10 / +15 | 所有兵种，每个士兵都加 |
| 步兵单兵防御 | 加值 | +3 / +6 / +9 | 仅步兵（仅 1 件装备有） |
| 英雄防御 + | 加值 | +2 / +4 / +6 | 英雄统帅，所有兵种受益 |
| 英雄防御 % | 百分比 | +4% / +8% / +12% | 英雄统帅，所有兵种受益 |

### 法术效果

| 效果 | lvl1 / lvl2 / lvl3 |
|---|---|
| 步兵法术效率 | +6% / +12% / +18% |
| 骑兵法术效率 | +6% / +12% / +18% |
| 远程法术效率 | +6% / +12% / +18% |
| 英雄魔法 + | +2 / +4 / +6 |
| 英雄魔法 % | +4% / +8% / +12% |
| 各学派法术（黑暗/光明/毁灭/召唤） | 按级别和子效果各不相同 |

### 经济效果

| 效果 | lvl1 / lvl2 / lvl3 |
|---|---|
| 黄金/木材/铁矿/水银收入 | +4% / +8% / +12% |
| 水晶/硫磺/宝石收入 | +4% / +8% / +12% |
| NPC 普通卖价提升 | +6% / +12% / +18% |
| NPC 普通买价折扣 | +6% / +12% / +18% |

---

## 推荐装备组合

### 组合 1：步兵单兵攻击流 — 最大 +70（消耗 38/40 级，6 件）

每个步兵攻击力 +70，装备中最强的单一效果。**装备系统对三兵种非均衡设计**：步兵多件可堆叠到 +70，骑兵仅 1 件 +15 封顶，弓手词条存在但 0 装备提供——这让步兵海在装备生态上 S 级首选。但骑兵海仍成立（A 级），靠 SPELL 层的 MYSTIC_SHIELD 对 CAV +50% 防御超模补偿装备弱势。搭配领袖通用技能"高谈阔论"(+15/兵，所有兵种) + 光明巫师 VALUE_MEMBERS 增益法术 = 完整兵海流派。第一赛季弓手海因核心血统能力 PRE_FIGHT_ATTACK_SHOOTER 失效（需上一世界 Tear War 传承），D 级不推荐。三流派的数量回本曲线、成立条件、天敌反制详见 $SKILL_DIR/combat.md「弱兵战术：兵海流派」。

| 部位 | tagName | 等级 | 加成 |
|---|---|---:|---:|
| 右手 | RADIAN_ROD_OF_DARKNESS_INFERNO_LVL7 | 7 | +10 |
| 头盔 | RADIANT_CROWN_HAVEN_LVL3 | 3 | +10 |
| 胸甲 | BALANCED_BREASTPLATE_OF_THE_OWL_LVL7 | 8 | +15 |
| 鞋子 | GREEN_FOOTPADS_OF_THE_SUN_LVL7 | 7 | +10 |
| 斗篷 | BRILLIANT_CAPE_OF_THE_SHREWD_HAVEN_LVL6 | 6 | +10 |
| 项链 | POWERFUL_NECKLACE_OF_DARKNESS_HAVEN_LVL7 | 7 | +15 |

左手和戒指空闲（2 级余量），可补其他效果。

### 组合 2：英雄攻击 % 流 — 最大 +60%（消耗 28/40 级，6 件）

提升英雄攻击力百分比，对所有兵种有效。适合斗士职业英雄。

| 部位 | tagName | 等级 | 加成 |
|---|---|---:|---:|
| 右手 | RADIANT_STAFF_OF_DESTRUCTION_INFERNO_LVL7 | 7 | +12% |
| 左手 | RADIANT_SHIELD_OF_THE_SUN_LVL10 [世袭] | **0** | +12% |
| 头盔 | POWERFUL_HELMET_OF_DESTRUCTION_INFERNO_LVL7 | 7 | +8% |
| 鞋子 | STREETDOGG_S_LUCKY_SOCKS_LVL4 | 4 | +8% |
| 戒指 | POWERFUL_RING_OF_THE_MIGHT_HAVEN_LVL7 | 7 | +8% |
| 项链 | AMULET_LVL2 | 3 | +12% |

胸甲和斗篷空闲（12 级余量），可补英雄攻击 + 或兵种法术。

### 组合 3：英雄防御 % 流 — 最大 +60%（消耗 25/40 级，5 件）

| 部位 | tagName | 等级 | 加成 |
|---|---|---:|---:|
| 左手 | BALANCED_SHIELD_OF_THE_MIGHT_SYLVAN_LVL7 | 7 | +12% |
| 胸甲 | RADIAN_LEATHER_JACKET_LVL4 | 4 | +12% |
| 斗篷 | POWERFUL_CLOAK_OF_THE_MIGHT_HAVEN_LVL6 | 6 | +12% |
| 戒指 | CORRUPTED_RING_OF_STONE_HAVEN_LVL8 | 8 | +12% |
| 项链 | POWERFUL_AMULET_OF_STONE_LVL10 [世袭] | **0** | +12% |

右手/头盔/鞋子空闲（15 级余量），可补英雄防御 + 或其他。

### 组合 4：召唤法术·3 级 — 最大 +84%（消耗 38/40 级，6 件）

所有单效果中百分比最高的组合。适合召唤师英雄。

| 部位 | tagName | 等级 | 加成 |
|---|---|---:|---:|
| 右手 | HOWLING_STAFF_OF_DARKNESS_NECROPOLIS_LVL8 | 8 | +18% |
| 左手 | CORRUPTED_FIGURINE_OF_THE_OUTER_WORLD_NECROPOLIS_LVL7 | 6 | +12% |
| 鞋子 | HOWLING_SABATONS_OF_DARKNESS_NECROPOLIS_LVL7 | 7 | +12% |
| 斗篷 | BRILLIANT_BAG_OF_THE_OUTER_WORLD_ACADEMY_LVL7 | 7 | +18% |
| 戒指 | BRILLIANT_RING_OF_THE_WISE_ACADEMY_LVL6 | 6 | +12% |
| 项链 | HOWLING_CHARM_ACADEMY_LVL4 | 4 | +12% |

### 组合 5：骑兵法术效率 — 最大 +66%（消耗 27/40 级，仅 4 件）

仅 4 件装备就能堆到 +66%，剩余等级和槽位可补英雄攻击。

| 部位 | tagName | 等级 | 加成 |
|---|---|---:|---:|
| 右手 | HOWLING_BOOK_OF_THE_LIGHT_ACADEMY_LVL7 | 7 | +18% |
| 鞋子 | SOLID_SLIPPERS_OF_THE_MIGHT_LVL7 | 7 | +18% |
| 斗篷 | BRILLIANT_BAG_OF_THE_OUTER_WORLD_ACADEMY_LVL7 | 7 | +12% |
| 戒指 | BRILLIANT_RING_OF_THE_WISE_ACADEMY_LVL6 | 6 | +18% |

### 组合 6：黑暗法术·3 级 — 最大 +60%（消耗 34/40 级，5 件）

适合黑暗巫师英雄。

| 部位 | tagName | 等级 | 加成 |
|---|---|---:|---:|
| 右手 | HOWLING_STAFF_OF_DARKNESS_NECROPOLIS_LVL8 | 8 | +12% |
| 左手 | CORRUPTED_SHIELD_OF_THE_SUN_INFERNO_LVL4 | 4 | +6% |
| 头盔 | CORRUPTED_HELMET_OF_THE_SUN_INFERNO_LVL8 | 8 | +18% |
| 胸甲 | HOWLING_WRATH_OF_THE_OUTER_WORLD_NECROPOLIS_LVL7 | 7 | +12% |
| 项链 | CORRUPTED_TALISMAN_OF_THE_MIGHT_INFERNO_LVL7 | 7 | +12% |

### 组合 7：黄金收入流 — 最大 +40%（消耗 19/40 级，5 件）

经济型英雄专用，搭配建造者职业的掘金者技能。

| 部位 | tagName | 等级 | 加成 |
|---|---|---:|---:|
| 右手 | SOLID_STICK_ACADEMY_LVL3 | 3 | +8% |
| 头盔 | RADIANT_HELMET_OF_INTELLIGENCE_SYLVAN_LVL7 | 7 | +8% |
| 胸甲 | HARNESS_LVL1 | 1 | +4% |
| 戒指 | CORRUPTED_RING_OF_STONE_HAVEN_LVL8 | 8 | +8% |
| 项链 | POWERFUL_AMULET_OF_STONE_LVL9 [世袭] | **0** | +12% |

仅消耗 19 级，剩余 21 级可搭配木材/铁矿收入装备。

### 组合 8：铁矿收入流 — 最大 +52%（消耗 28/40 级，5 件）

| 部位 | tagName | 等级 | 加成 |
|---|---|---:|---:|
| 头盔 | CIRCLET_OF_PROSPERITY_LVL8 | 8 | +12% |
| 胸甲 | SOLID_BREASTPLATE_OF_STONE_SYLVAN_LVL7 | 7 | +8% |
| 鞋子 | SOLID_SLIPPERS_OF_THE_MIGHT_LVL7 | 7 | +12% |
| 斗篷 | GREEN_COAT_OF_THE_SUN_SYLVAN_LVL6 | 6 | +8% |
| 戒指 | GENEROUS_RING_OF_SHREWDNESS_LVL10 [世袭] | **0** | +12% |

### 组合 9：NPC 普通卖价 — 最大 +78%（消耗 22/40 级，5 件）

搭配商人职业，卖资源利润极高。

| 部位 | tagName | 等级 | 加成 |
|---|---|---:|---:|
| 右手 | WHIP_LVL2 | 2 | +12% |
| 胸甲 | SOLID_BREASTPLATE_OF_STONE_SYLVAN_LVL7 | 7 | +18% |
| 斗篷 | BRILLIANT_CAPE_OF_THE_SHREWD_HAVEN_LVL6 | 6 | +18% |
| 戒指 | GENEROUS_RING_OF_SHREWDNESS_LVL7 [世袭] | **0** | +18% |
| 项链 | SHINING_CHAPLET_OF_THE_OUTER_WORLD_ACADEMY_LVL7 | 7 | +12% |

### 组合 10：部队侦查等级 — 最大 +39（消耗 27/40 级，6 件）

搭配游侠职业的侦察大师技能。

| 部位 | tagName | 等级 | 加成 |
|---|---|---:|---:|
| 左手 | QUIVER_SYLVAN_LVL2 | 2 | +6 |
| 头盔 | GREEN_HELMET_LVL4 | 4 | +6 |
| 胸甲 | GREEN_HARNESS_LVL6 | 6 | +9 |
| 鞋子 | GREEN_FOOTPADS_OF_THE_SUN_LVL7 | 7 | +9 |
| 斗篷 | GREEN_COAT_OF_THE_SUN_SYLVAN_LVL6 | 6 | +3 |
| 项链 | MEDALLION_LVL2 | 2 | +6 |

### 组合 11：战斗经验流 — 最大 +42%（消耗 26/40 级，5 件）

快速升级英雄，前中期非常实用。

| 部位 | tagName | 等级 | 加成 |
|---|---|---:|---:|
| 左手 | RADIANT_SHIELD_OF_THE_SUN_LVL7 [世袭] | **0** | +9% |
| 头盔 | RADIANT_HELMET_OF_INTELLIGENCE_SYLVAN_LVL7 | 7 | +9% |
| 胸甲 | ARTURCHIX_S_USED_BATTLE_CHEST_LVL8 | 8 | +9% |
| 鞋子 | STREETDOGG_S_LUCKY_SOCKS_LVL4 | 4 | +6% |
| 斗篷 | RADIANT_RUCKSACK_OF_THE_SUN_HAVEN_LVL7 | 7 | +9% |

### 组合 12：步兵法术效率 — 最大 +42%（消耗 13/40 级，仅 3 件）

性价比极高，仅 13 级就能达到 +42%，剩余 27 级自由分配。

| 部位 | tagName | 等级 | 加成 |
|---|---|---:|---:|
| 右手 | EXPLOSIVE_SWORD_SYLVAN_LVL3 | 3 | +12% |
| 胸甲 | DUSTY_TOGA_OF_THE_OUTER_WORLD_ACADEMY_LVL7 | 7 | +18% |
| 项链 | DUSTY_CHARM_NECROPOLIS_LVL3 | 3 | +12% |

### 组合 13：远程法术效率 — 最大 +36%（消耗 14/40 级，3 件）

| 部位 | tagName | 等级 | 加成 |
|---|---|---:|---:|
| 右手 | DUSTY_WAND_OF_THE_OUTER_WORLD_ACADEMY_LVL6 | 6 | +6% |
| 头盔 | HAT_LVL2 | 2 | +12% |
| 胸甲 | DUSTY_ARMOR_LVL6 | 6 | +18% |

---

## 混合装备方案

### 方案 A：步兵战斗英雄（攻防兼顾）

步兵单兵攻击 3 件（+35）+ 英雄攻击 % 3 件（+28%）+ 通用单兵防御 1 件（+10）

| 部位 | tagName | 等级 | 主效果 |
|---|---|---:|---|
| 右手 | RADIAN_ROD_OF_DARKNESS_INFERNO_LVL7 | 7 | 步兵单兵攻击 +10 |
| 左手 | RADIANT_SHIELD_OF_THE_SUN_LVL10 [世袭] | **0** | 英雄攻击 % +12% |
| 头盔 | RADIANT_CROWN_HAVEN_LVL3 | 3 | 步兵单兵攻击 +10 |
| 鞋子 | STREETDOGG_S_LUCKY_SOCKS_LVL4 | 4 | 英雄攻击 % +8% |
| 斗篷 | RADIANT_RUCKSACK_OF_THE_SUN_HAVEN_LVL7 | 7 | 通用单兵防御 +10 |
| 戒指 | POWERFUL_RING_OF_THE_MIGHT_HAVEN_LVL7 | 7 | 英雄攻击 % +8% |
| 项链 | POWERFUL_NECKLACE_OF_DARKNESS_HAVEN_LVL7 | 7 | 步兵单兵攻击 +15 |

总等级 35/40。效果：步兵单兵攻击 +35 / 英雄攻击 % +28% / 通用单兵防御 +10

### 方案 B：经济混搭（多资源同时堆）

| 部位 | tagName | 等级 | 效果 |
|---|---|---:|---|
| 右手 | SOLID_STICK_ACADEMY_LVL3 | 3 | 黄金 +8% |
| 左手 | TOOLBAG_SYLVAN_LVL2 | 2 | 木材 +8% |
| 头盔 | CIRCLET_OF_PROSPERITY_LVL8 | 8 | 黄金 +8% / 木材 +12% / 铁矿 +12% |
| 胸甲 | GREEN_HARNESS_LVL6 | 6 | 宝石 +12% |
| 斗篷 | GREEN_COAT_OF_THE_SUN_SYLVAN_LVL6 | 6 | 铁矿 +8% |
| 戒指 | GENEROUS_RING_OF_SHREWDNESS_LVL10 [世袭] | **0** | 木材 +12% / 铁矿 +12% |
| 项链 | POWERFUL_AMULET_OF_STONE_LVL10 [世袭] | **0** | 黄金 +12% |

总等级 25/40。效果：黄金 +28% / 木材 +32% / 铁矿 +32% / 宝石 +12%

---

## 效果极限值速查表

| 排名 | 效果 | 最大值 | 件数 | 消耗等级 |
|---:|---|---:|---:|---:|
| 1 | 召唤法术·3 级 | +84% | 6 | 38/40 |
| 2 | NPC 普通卖价 | +78% | 5 | 22/40 |
| 3 | **步兵单兵攻击** | **+70** | 6 | 38/40 |
| 4 | 骑兵法术效率 | +66% | 4 | 27/40 |
| 5 | 英雄攻击 % | +60% | 6 | 28/40 |
| 6 | 英雄防御 % | +60% | 5 | 25/40 |
| 7 | 黑暗法术·3 级 | +60% | 5 | 34/40 |
| 8 | 召唤法术·1 级 | +54% | 3 | 17/40 |
| 9 | 铁矿收入 | +52% | 5 | 28/40 |
| 10 | 战斗经验 % | +42% | 5 | 26/40 |
| 11 | 步兵法术效率 | +42% | 3 | 13/40 |
| 12 | 毁灭法术·2 级 | +42% | 3 | 18/40 |
| 13 | 黄金收入 | +40% | 5 | 19/40 |
| 14 | 部队侦查等级 | +39 | 6 | 27/40 |
| 15 | 远程法术效率 | +36% | 3 | 14/40 |
| 16 | 木材收入 | +36% | 4 | 13/40 |
| 17 | 宝石收入 | +32% | 4 | 22/40 |
| 18 | 英雄攻击 + | +28 | 6 | 40/40 |
| 19 | 英雄防御 + | +28 | 6 | 34/40 |
| 20 | 通用单兵防御 | +15 | 2 | 11/40 |
| 21 | 骑兵单兵攻击 | +10 | 1 | 4/40 |
| 22 | 步兵单兵防御 | +6 | 1 | 6/40 |

## 装备选择决策树

```
英雄职业是什么？
├── 斗士/骑士 → 步兵单兵攻击流(+70) 或 英雄攻击/防御 % 流(+60%)
├── 领袖 → 步兵单兵攻击流(+70) + 兵种法术(+42%)
├── 召唤师 → 召唤法术·3 级流(+84%)
├── 黑暗巫师 → 黑暗法术·3 级流(+60%)
├── 毁灭巫师 → 毁灭法术·2 级流(+42%)
├── 建造者 → 黄金收入流(+40%) + 资源收入
├── 商人 → NPC 卖价流(+78%)
├── 游侠 → 部队侦查流(+39)
└── 升级中 → 战斗经验流(+42%)
```

---

## 完整装备效果列表

> 效果数值查询规则：每个效果有 lvl1/lvl2/lvl3 三档，数值见下方效果数值速查表。
> 来源缩写：区=区域怪物掉落，排=排名奖励，建=区域建筑掉落，袭=世袭（等级0）。


### 右手（RIGHT_HAND）

| tagName | 来源 | 效果 |
|---|---|---|
| AXE_LVL2 | 排名奖励 | 英雄攻击+ +4 |
| WHIP_LVL2 | 区域掉落 | NPC普通卖价 +12% |
| POWERFUL_ROD_INFERNO_LVL3 | 区域掉落 | 增产T2兵 +2 / 毁灭(伤害值) +3% |
| STICK_ACADEMY_LVL2 | 区域掉落 | 召唤(召唤) +6% |
| SOLID_STICK_ACADEMY_LVL3 | 区域掉落 | 黄金收入 +8% / 召唤·5级 +2% |
| BRILLIANT_WHIP_ACADEMY_LVL3 | 区域掉落 | 光明·2级 +6% / NPC稀有买价折扣 +12% |
| STAFF_NECROPOLIS_LVL2 | 区域掉落 | 黑暗(诅咒) +6% |
| SOLID_BOOK_LVL4 | 区域掉落 | 普通矿建速 +10% / 骑兵法术效率 +12% |
| BRILLIANT_STAFF_OF_THE_SUN_HAVEN_LVL7 | 区域掉落 | 光明(防御) +6% / 黑暗·4级 +6% / 增产T6兵 +1 |
| RADIANT_STAFF_OF_DESTRUCTION_INFERNO_LVL7 | 区域掉落 | 英雄攻击% +12% / 黑暗(伤害) +6% / 毁灭·1级 +18% |
| HOWLING_BOOK_OF_THE_LIGHT_ACADEMY_LVL7 | 区域掉落 | 召唤·5级 +4% / 骑兵法术效率 +18% / 光明(攻击) +6% |
| DUSTY_WAND_OF_THE_OUTER_WORLD_ACADEMY_LVL6 | 区域掉落 | 远程法术效率 +6% / 光明·4级 +6% / 召唤·5级 +6% |
| HOWLING_BOOK_OF_THE_LIGHT_ACADEMY_LVL6 | 区域掉落 | 召唤·1级 +9% / 英雄魔法+ +6 / 光明(攻击) +6% |
| RADIAN_ROD_OF_DARKNESS_INFERNO_LVL7 | 区域掉落 | 步兵单兵攻击 +10 / 毁灭(伤害值) +6% / 黑暗·4级 +9% |
| CORRUPTED_STICK_OF_DARKNESS_NECROPOLIS_LVL7 | 区域掉落 | 黑暗(诅咒) +6% / 召唤·5级 +4% / 黑暗·5级 +6% |
| HOWLING_STAFF_OF_DARKNESS_NECROPOLIS_LVL8 | 区域掉落 | 召唤·3级 +18% / 黑暗(诅咒) +9% / 黑暗·3级 +12% |
| EXPLOSIVE_SWORD_SYLVAN_LVL3 | 区域掉落 | 毁灭(伤害值) +3% / 步兵法术效率 +12% |
| POWERFUL_WHIP_OF_THE_LAND_SYLVAN_LVL8 | 区域掉落 | 英雄攻击+ +6 / 英雄防御+ +6 / 宝石收入 +8% |

### 左手（LEFT_HAND）

| tagName | 来源 | 效果 |
|---|---|---|
| SCALES_HAVEN_LVL2 | 区域掉落 | NPC普通买价折扣 +12% |
| GREEN_SHIELD_INFERNO_LVL3 | 区域掉落 | 侦查·城市 +3 / 增产T3兵 +1 |
| GLOBE_ACADEMY_LVL2 | 区域掉落 | 光明·5级 +4% |
| CANDLE_NECROPOLIS_LVL2 | 区域掉落 | 英雄魔法% +8% |
| CORRUPTED_FIGURINE_OF_THE_OUTER_WORLD_NECROPOLIS_LVL7 | 区域掉落 | 黑暗·1级 +9% / 召唤·3级 +12% / 召唤·4级 +9% |
| GREEN_SHIELD_LVL4 | 区域掉落 | 侦查·部队 +6 / 增产T6兵 +1 |
| SHINING_SHIELD_OF_THE_MIGHT_HAVEN_LVL4 | 区域掉落 | 通用单兵防御 +5 / 增产T3兵 +1 / 英雄攻击% +4% |
| CORRUPTED_SHIELD_OF_THE_SUN_INFERNO_LVL4 | 区域掉落 | 黑暗·3级 +6% / 招募速度T2 +12% / 英雄攻击% +4% |
| CORRUPTED_POWDER_OF_THE_OUTER_WORLD_NECROPOLIS_LVL4 | 区域掉落 | 黑暗·1级 +9% / 黑暗(诅咒) +6% / 召唤·3级 +6% |
| QUIVER_SYLVAN_LVL2 | 区域掉落 | 侦查·部队 +6 |
| RADIANT_TORCH_SYLVAN_LVL4 | 区域掉落 | 骑兵单兵攻击 +10 / 毁灭·2级 +12% |
| TOOLBAG_SYLVAN_LVL2 | 区域掉落 | 木材收入 +8% |
| FIGURINE_SYLVAN_LVL2 | 区域掉落 | 召唤(伤害) +6% |
| EXPLOSIVE_SHIELD_OF_THE_SUN_SYLVAN_LVL7 | 区域掉落 | 毁灭·3级 +12% / 增产T5兵 +2 / 英雄攻击+ +4 |
| GENEROUS_SCALES_OF_THE_OUTER_WORLD_SYLVAN_LVL4 | 区域掉落 | NPC稀有卖价 +6% / 木材收入 +8% / 召唤·3级 +6% |
| BALANCED_SHIELD_OF_THE_MIGHT_SYLVAN_LVL7 | 区域掉落 | 水晶收入 +8% / 英雄防御+ +4 / 英雄防御% +12% |

### 头盔（HEAD）

| tagName | 来源 | 效果 |
|---|---|---|
| HELMET_HAVEN_LVL2 | 区域掉落 | 增产T3兵 +1 |
| RADIANT_CROWN_HAVEN_LVL3 | 区域掉落 | 英雄防御+ +2 / 步兵单兵攻击 +10 |
| FEATHER_INFERNO_LVL2 | 区域掉落 | 侦查·区域 +6 |
| HAT_LVL2 | 区域掉落 | 远程法术效率 +12% |
| CAP_LVL1 | 区域掉落 | 普通矿建速 +5% |
| GREEN_HELMET_LVL4 | 区域掉落 | 侦查·部队 +6 / 战斗经验 +6% |
| POWERFUL_HOOD_OF_DARKNESS_INFERNO_LVL6 | 区域掉落 | 英雄防御+ +2 / 黑暗·4级 +6% / 黑暗·2级 +18% |
| BONNET_LVL3 | 区域掉落 | 稀有矿建速 +15% |
| POWERFUL_HELMET_OF_DESTRUCTION_INFERNO_LVL7 | 区域掉落 | 英雄攻击% +8% / 英雄防御+ +4 / 毁灭·2级 +18% |
| CORRUPTED_HELMET_OF_THE_SUN_INFERNO_LVL8 | 区域掉落 | 黑暗·3级 +18% / 招募速度T6 +9% / 英雄防御+ +4 |
| CIRCLET_OF_PROSPERITY_LVL8 | 排名奖励 | 木材收入 +12% / 铁矿收入 +12% / 黄金收入 +8% |
| RADIANT_HELMET_OF_INTELLIGENCE_SYLVAN_LVL7 | 区域掉落 | 英雄攻击+ +4 / 战斗经验 +9% / 黄金收入 +8% |
| PUMPKIN_HELMET_LVL3 | 区域建筑掉落 | 英雄防御+ +6 |

### 胸甲（CHEST）

| tagName | 来源 | 效果 |
|---|---|---|
| HARNESS_LVL1 | 区域掉落 | 黄金收入 +4% |
| ROBE_LVL2 | 区域掉落 | 步兵法术效率 +12% |
| CLOAK_LVL2 | 区域掉落 | 增产T3兵 +1 |
| SOLID_BREASTPLATE_HAVEN_LVL4 | 区域掉落 | 宝石收入 +8% / 英雄攻击+ +4 |
| WRATH_NECROPOLIS_LVL2 | 区域掉落 | 黑暗·5级 +4% |
| CORRUPTED_PADDED_ARMOR_NECROPOLIS_LVL4 | 区域掉落 | 黑暗(诅咒) +6% / 召唤·1级 +18% |
| HOWLING_ROBE_NECROPOLIS_LVL3 | 区域掉落 | 召唤·5级 +2% / 步兵法术效率 +12% |
| ARMOR_LVL2 | 区域掉落 | 增产T1兵 +4 |
| DUSTY_TOGA_OF_THE_OUTER_WORLD_ACADEMY_LVL7 | 区域掉落 | 步兵法术效率 +18% / 光明·1级 +18% / 召唤(伤害) +6% |
| HOWLING_WRATH_OF_THE_OUTER_WORLD_NECROPOLIS_LVL7 | 区域掉落 | 召唤(召唤) +9% / 黑暗·3级 +12% / 召唤(伤害) +6% |
| RADIAN_LEATHER_JACKET_LVL4 | 区域掉落 | 英雄防御% +12% / 侦查·部队 +3 |
| GREEN_HARNESS_LVL6 | 区域掉落 | 侦查·部队 +9 / 宝石收入 +12% |
| DUSTY_ARMOR_LVL6 | 排名奖励 | 远程法术效率 +18% / 增产T6兵 +1 |
| DUSTY_ARMOR_LVL3 | 区域掉落 | 英雄魔法+ +4 / 增产T2兵 +1 |
| BALANCED_BREASTPLATE_OF_THE_OWL_LVL7 | 区域掉落 | 金矿建速 +10% / 步兵单兵攻击 +15 / 侦查·城市 +9 |
| ARTURCHIX_S_USED_BATTLE_CHEST_LVL8 | 排名奖励 | 英雄攻击+ +6 / 战斗经验 +9% / 英雄防御% +8% |
| SOLID_BREASTPLATE_OF_STONE_SYLVAN_LVL7 | 区域掉落 | NPC普通卖价 +18% / 英雄防御+ +4 / 铁矿收入 +8% |

### 鞋子（FEET）

| tagName | 来源 | 效果 |
|---|---|---|
| SOLID_STOMPERS_LVL4 | 区域掉落 | 木材收入 +4% / 招募速度T3 +12% |
| HOWLING_SABATONS_OF_DARKNESS_NECROPOLIS_LVL7 | 区域掉落 | 召唤·3级 +12% / 召唤·1级 +27% / 黑暗·1级 +18% |
| EXPLOSIVE_STOMPERS_OF_DESTRUCTION_INFERNO_LVL6 | 区域掉落 | 毁灭·3级 +6% / 增产T2兵 +2 / 毁灭(伤害值) +9% |
| CORRUPTED_STOMPERS_OF_THE_OUTER_WORLD_NECROPOLIS_LVL7 | 区域掉落 | 黑暗(伤害) +6% / 增产T6兵 +1 / 召唤·3级 +12% |
| HOWLING_CLOG_OF_THE_MIGHT_NECROPOLIS_LVL6 | 区域掉落 | 召唤(召唤) +3% / 黑暗(诅咒) +6% / 招募速度T2 +18% |
| SOLID_SLIPPERS_OF_THE_MIGHT_LVL7 | 区域掉落 | 铁矿收入 +12% / 骑兵法术效率 +18% / 战斗经验 +3% |
| GREEN_FOOTPADS_OF_THE_SUN_LVL7 | 区域掉落 | 侦查·部队 +9 / 水银收入 +8% / 步兵单兵攻击 +10 |
| BRILLIANT_FOOTPADS_OF_THE_OUTER_WORLD_ACADEMY_LVL4 | 区域掉落 | 光明(攻击) +3% / 硫磺收入 +8% / 召唤·5级 +2% |
| STREETDOGG_S_LUCKY_SOCKS_LVL4 | 排名奖励 | 英雄攻击% +8% / 战斗经验 +6% |
| SHINING_SANDALS_OF_THE_MIGHT_SYLVAN_LVL6 | 区域掉落 | 宝石收入 +4% / 步兵单兵防御 +6 / 增产T4兵 +2 |

### 斗篷（CAPE）

| tagName | 来源 | 效果 |
|---|---|---|
| BLANKET_LVL1 | 区域掉落 | 侦查·区域 +3 |
| BLANKET_LVL2 | 区域掉落 | 侦查·城市 +6 |
| LEATHER_JACKET_INFERNO_LVL2 | 区域掉落 | 侦查·城市 +6 |
| RUCKSACK_ACADEMY_LVL2 | 区域掉落 | NPC普通买价折扣 +12% |
| POWERFUL_CLOAK_OF_THE_MIGHT_HAVEN_LVL6 | 区域掉落 | 增产T2兵 +1 / 英雄攻击+ +4 / 英雄防御% +12% |
| RADIANT_RUCKSACK_OF_THE_SUN_HAVEN_LVL7 | 区域掉落 | 步兵单兵攻击 +10 / 通用单兵防御 +10 / 战斗经验 +9% |
| BRILLIANT_CAPE_OF_THE_SHREWD_HAVEN_LVL6 | 区域掉落 | 光明·2级 +6% / 步兵单兵攻击 +10 / NPC普通卖价 +18% |
| BRILLIANT_BAG_OF_THE_OUTER_WORLD_ACADEMY_LVL7 | 区域掉落 | 光明·1级 +18% / 骑兵法术效率 +12% / 召唤·3级 +18% |
| GREEN_MANTLE_SYLVAN_LVL3 | 区域掉落 | 侦查·区域 +6 / NPC稀有卖价 +6% |
| GREEN_COAT_OF_THE_SUN_SYLVAN_LVL6 | 区域掉落 | 侦查·部队 +3 / 铁矿收入 +8% / 增产T5兵 +2 |

### 戒指（RING）

| tagName | 来源 | 效果 |
|---|---|---|
| RING_LVL2 | 区域掉落 | 英雄防御+ +4 |
| RING_LVL1 | 区域掉落 | 金矿建速 +5% |
| RING_HAVEN_LVL2 | 区域掉落 | 宝石收入 +8% |
| POWERFULL_RING_HAVEN_LVL3 | 区域掉落 | 增产T5兵 +1 / 英雄防御+ +2 |
| RING_INFERNO_LVL2 | 区域掉落 | 毁灭·3级 +12% |
| CORRUPTED_RING_INFERNO_LVL4 | 区域掉落 | 黑暗(伤害) +6% / 英雄攻击+ +4 |
| BRILLIANT_RING_OF_THE_WISE_ACADEMY_LVL6 | 区域掉落 | 光明·3级 +6% / 召唤·3级 +12% / 骑兵法术效率 +18% |
| HOWLING_RING_OF_DARKNESS_NECROPOLIS_LVL7 | 区域掉落 | 召唤·3级 +12% / 英雄防御% +8% / 黑暗(伤害) +9% |
| POWERFUL_RING_OF_THE_MIGHT_HAVEN_LVL7 | 区域掉落 | 增产T6兵 +1 / 硫磺收入 +8% / 英雄攻击% +8% |
| CORRUPTED_RING_OF_STONE_HAVEN_LVL8 | 区域掉落 | 黑暗·2级 +18% / 英雄防御% +12% / 黄金收入 +8% |
| RING_OF_THE_DOMINEER_LVL4 | 排名奖励 | 英雄攻击+ +4 / 英雄防御+ +2 / 英雄魔法+ +2 |
| HOWLING_RING_OF_THE_LAND_SYLVAN_LVL7 | 区域掉落 | 召唤·5级 +4% / 木材收入 +8% / 水晶收入 +12% |

### 项链（NECKLACE）

| tagName | 来源 | 效果 |
|---|---|---|
| HOWLING_CHARM_ACADEMY_LVL4 | 区域掉落 | 召唤·3级 +12% / 召唤(伤害) +6% |
| DUSTY_CHARM_NECROPOLIS_LVL3 | 区域掉落 | 步兵法术效率 +12% / 召唤(伤害) +3% |
| POWERFUL_NECKLACE_OF_DARKNESS_HAVEN_LVL7 | 区域掉落 | 步兵单兵攻击 +15 / 英雄防御+ +4 / 黑暗(伤害) +6% |
| CORRUPTED_TALISMAN_OF_THE_MIGHT_INFERNO_LVL7 | 区域掉落 | 黑暗·3级 +12% / 黑暗·4级 +9% / 增产T1兵 +4 |
| MEDALLION_LVL2 | 区域掉落 | 侦查·部队 +6 |
| AMULET_LVL2 | 区域掉落 | 英雄攻击% +12% |
| SOLID_NECKLACE_LVL_5 | 区域掉落 | 水晶收入 +8% / 招募速度T6 +9% |
| SOLID_AMULET_OF_THE_LIGHT_HAVEN_LVL7 | 区域掉落 | 黄金收入 +8% / 增产T1兵 +6 / 光明·3级 +12% |
| EXPLOSIVE_AMULET_OF_DESTRUCTION_INFERNO_LVL7 | 区域掉落 | 毁灭·2级 +12% / 招募速度T5 +9% / 毁灭(百分比) +6% |
| SHINING_CHAPLET_OF_THE_OUTER_WORLD_ACADEMY_LVL7 | 区域掉落 | NPC普通卖价 +12% / 光明·2级 +12% / 召唤·2级 +18% |
| HOWLING_CHAPLET_OF_THE_CROWD_ACADEMY_LVL8 | 区域掉落 | 召唤(伤害) +9% / 光明·5级 +6% / 招募英雄折扣 +14% |

### 世袭装备（Heredity — 装备等级=0）

> **Session1 状态：全部未获得。** 游戏内装备 ID 上限为 111，世袭装备实体 ID 从 112 起，当前数据库中无任何玩家持有世袭装备。

| tagName | 部位 | 效果 |
|---|---|---|
| RADIANT_SHIELD_OF_THE_SUN_LVL1 | 左手 | 战斗经验 +3% |
| RADIANT_SHIELD_OF_THE_SUN_LVL2 | 左手 | 战斗经验 +3% / 增产T6兵 +1 |
| RADIANT_SHIELD_OF_THE_SUN_LVL3 | 左手 | 战斗经验 +3% / 增产T6兵 +1 / 英雄攻击% +4% |
| RADIANT_SHIELD_OF_THE_SUN_LVL4 | 左手 | 战斗经验 +6% / 增产T6兵 +1 / 英雄攻击% +4% |
| RADIANT_SHIELD_OF_THE_SUN_LVL5 | 左手 | 战斗经验 +6% / 增产T6兵 +1 / 英雄攻击% +4% |
| RADIANT_SHIELD_OF_THE_SUN_LVL6 | 左手 | 战斗经验 +6% / 增产T6兵 +1 / 英雄攻击% +8% |
| RADIANT_SHIELD_OF_THE_SUN_LVL7 | 左手 | 战斗经验 +9% / 增产T6兵 +1 / 英雄攻击% +4% |
| RADIANT_SHIELD_OF_THE_SUN_LVL8 | 左手 | 战斗经验 +9% / 增产T6兵 +1 / 英雄攻击% +8% |
| RADIANT_SHIELD_OF_THE_SUN_LVL9 | 左手 | 战斗经验 +9% / 增产T6兵 +1 / 英雄攻击% +8% |
| RADIANT_SHIELD_OF_THE_SUN_LVL10 | 左手 | 战斗经验 +9% / 增产T6兵 +1 / 英雄攻击% +12% |
| GENEROUS_RING_OF_SHREWDNESS_LVL1 | 戒指 | NPC普通卖价 +6% |
| GENEROUS_RING_OF_SHREWDNESS_LVL2 | 戒指 | NPC普通卖价 +6% / 木材收入 +4% |
| GENEROUS_RING_OF_SHREWDNESS_LVL3 | 戒指 | NPC普通卖价 +6% / 木材收入 +4% / 铁矿收入 +4% |
| GENEROUS_RING_OF_SHREWDNESS_LVL4 | 戒指 | NPC普通卖价 +12% / 木材收入 +4% / 铁矿收入 +4% |
| GENEROUS_RING_OF_SHREWDNESS_LVL5 | 戒指 | NPC普通卖价 +12% / 木材收入 +8% / 铁矿收入 +4% |
| GENEROUS_RING_OF_SHREWDNESS_LVL6 | 戒指 | NPC普通卖价 +12% / 木材收入 +8% / 铁矿收入 +8% |
| GENEROUS_RING_OF_SHREWDNESS_LVL7 | 戒指 | NPC普通卖价 +18% / 木材收入 +8% / 铁矿收入 +4% |
| GENEROUS_RING_OF_SHREWDNESS_LVL8 | 戒指 | NPC普通卖价 +18% / 木材收入 +8% / 铁矿收入 +8% |
| GENEROUS_RING_OF_SHREWDNESS_LVL9 | 戒指 | NPC普通卖价 +18% / 木材收入 +12% / 铁矿收入 +8% |
| GENEROUS_RING_OF_SHREWDNESS_LVL10 | 戒指 | NPC普通卖价 +18% / 木材收入 +12% / 铁矿收入 +12% |
| POWERFUL_AMULET_OF_STONE_LVL1 | 项链 | 增产T4兵 +1 |
| POWERFUL_AMULET_OF_STONE_LVL2 | 项链 | 增产T4兵 +1 / 黄金收入 +4% |
| POWERFUL_AMULET_OF_STONE_LVL3 | 项链 | 增产T4兵 +1 / 黄金收入 +4% / 英雄防御% +4% |
| POWERFUL_AMULET_OF_STONE_LVL4 | 项链 | 增产T4兵 +2 / 黄金收入 +4% / 英雄防御% +4% |
| POWERFUL_AMULET_OF_STONE_LVL5 | 项链 | 增产T4兵 +2 / 黄金收入 +8% / 英雄防御% +4% |
| POWERFUL_AMULET_OF_STONE_LVL6 | 项链 | 增产T4兵 +2 / 黄金收入 +8% / 英雄防御% +8% |
| POWERFUL_AMULET_OF_STONE_LVL7 | 项链 | 增产T4兵 +2 / 黄金收入 +8% / 英雄防御% +4% |
| POWERFUL_AMULET_OF_STONE_LVL8 | 项链 | 增产T4兵 +2 / 黄金收入 +8% / 英雄防御% +8% |
| POWERFUL_AMULET_OF_STONE_LVL9 | 项链 | 增产T4兵 +2 / 黄金收入 +12% / 英雄防御% +8% |
| POWERFUL_AMULET_OF_STONE_LVL10 | 项链 | 增产T4兵 +2 / 黄金收入 +12% / 英雄防御% +12% |

---

## 装备操作 API

### 第一步：查询英雄现有装备

```json
{"type":"getContent","params":{"elementType":"HeroFrame","elementId":<heroId>}}
```

响应中包含三个数组：
- `equipedArtefacts` — 已装备（associated=1，在装备槽上）
- `backpackArtefacts` — 背包中（associated=0，在英雄身上但未装备）
- `regionArtefacts` — 城市仓库中

每个装备对象的关键字段：
```json
{
  "id": 42,                        // 装备实例 ID（操作时用这个）
  "position": 3,                   // 槽位编号（见下表）
  "associated": 1,                 // 1=装备中，0=背包/城市
  "binded": 1,                     // 1=绑定（冷却中或已装备）
  "unbindDate": 1713000000,        // 冷却结束时间戳（Unix）；null=无冷却
  "artefactEntity": {
    "tagName": "SWORD_LVL2",
    "bodyPart": "RIGHT_HAND",      // 必须对应正确槽位才能装备
    "level": 3
  }
}
```

### 第二步：装备到英雄槽位（MOVE）

```json
{
  "type": "artefactAction",
  "params": {
    "action": "MOVE",
    "artefactId": 42,
    "newPosition": 3,
    "newOwnerType": "HeroEquipment",
    "newOwnerId": <heroId>
  }
}
```

**槽位编号（newPosition）：**

| position | 部位 |
|----------|------|
| 1 | HEAD（头盔） |
| 2 | NECKLACE（项链） |
| 3 | RIGHT_HAND（右手） |
| 4 | CHEST（胸甲） |
| 5 | LEFT_HAND（左手） |
| 6 | RING（戒指） |
| 7 | FEET（鞋子） |
| 8 | CAPE（斗篷） |

装备后立即绑定（`binded=1, unbindDate=null`）。

### 从槽位移到背包（开始冷却）

```json
{
  "type": "artefactAction",
  "params": {
    "action": "MOVE",
    "artefactId": 42,
    "newPosition": 9,
    "newOwnerType": "HeroBackpack",
    "newOwnerId": <heroId>
  }
}
```

移到背包后立即进入冷却状态（`unbindDate = now + 86400秒`）。**冷却期间不能再次装备，也不能放入城市。**

背包最多 18 个槽位（position 9–18 均可）。

### 从背包/槽位移到城市仓库

只有冷却结束（`unbindDate < now` 或 `unbindDate=null`）才可以放入城市。

```json
{
  "type": "artefactAction",
  "params": {
    "action": "MOVE",
    "artefactId": 42,
    "newPosition": 1,
    "newOwnerType": "Region",
    "newOwnerId": <regionId>
  }
}
```

城市仓库最多 9 个槽位。

### 交换两件装备位置（PERMUTATION）

在英雄两个槽位之间、槽位与背包之间互换：

```json
{
  "type": "artefactAction",
  "params": {
    "action": "PERMUTATION",
    "artefactId": 42,
    "artefact2Id": 43
  }
}
```

---

## 为什么装不上装备

| 错误原因 | 说明 | 解决方法 |
|----------|------|----------|
| `isBinded` — 冷却中 | 装备从英雄槽移到背包后 24h 内无法再装备或放入城市 | 检查 `unbindDate`，等冷却结束 |
| 部位不匹配 | `bodyPart`（如 RIGHT_HAND）与目标槽位（position 3）不对应 | 确认目标 position 对应正确的 bodyPart |
| 英雄等级不足 | `已装备等级总和 + 新装备等级 > 英雄等级` | 选择等级更低的装备，或先卸掉其他装备 |
| 槽位已占用 | 目标 position 已经有其他装备 | 先卸掉该槽位的装备，或用 PERMUTATION 换位 |
| 英雄状态异常 | 英雄被俘/受伤/围城/忙碌时，不能在城市与英雄之间转移装备 | 等英雄恢复空闲状态 |
| 套装冲突 | 英雄已装备某套装的件数后，不能再装来自其他套装的装备 | 同一英雄只能穿同一套装的件数 |
| 主英雄不能穿套装 | 主英雄（isMainHero=true）不能装备套装类装备 | 改用非套装装备 |

---

## 装备管理实战流程

### 场景：把城市仓库里的装备装给英雄

1. `getContent HeroFrame <heroId>` — 查看 `regionArtefacts`，找到装备的 `id` 和 `artefactEntity.bodyPart`
2. 确认英雄等级够用：`已装等级总和 + 新装备等级 ≤ hero._level`
3. 确认目标槽位未被占用（`equipedArtefacts` 中对应 position 无装备）
4. `artefactAction MOVE` — `newOwnerType=HeroEquipment`，`newOwnerId=heroId`，`newPosition`=对应槽位

### 场景：把英雄装备换到另一个英雄

1. 先从英雄A槽位 MOVE 到背包（开始24h冷却）
2. 等 `unbindDate` 过期后（检查时间戳），再 MOVE 到城市仓库
3. 再从城市仓库 MOVE 到英雄B的槽位

**注意：** 如果两个英雄在同一城市，可以先移到城市仓库（不经过背包），跳过冷却直接给另一个英雄装备——但必须先经过背包冷却才能进城市。

实际上，从装备槽→背包会触发冷却，冷却中不能进城市；冷却结束后可以进城市，进城市后再给其他英雄就没有冷却了。

### 场景：检查装备是否在冷却

```python
import time
unbind_ts = artefact.get('unbindDate')  # Unix 时间戳或 None
if unbind_ts and unbind_ts > time.time():
    remaining = int(unbind_ts - time.time())
    print(f"冷却中，还需等待 {remaining//3600}h {(remaining%3600)//60}m")
else:
    print("冷却结束，可以移动")
```
