# 财富篇

## 资源类型与价值

游戏共有 7 种资源，分为三大类：

| ID | 资源 | 类型 | 基础价值 (goldValue) | NPC买入价(你卖出) | NPC卖出价(你买入) |
|----|------|------|---------------------|-------------------|-------------------|
| 1 | 金币 GOLD | 货币 | 1 | — | — |
| 2 | 木材 WOOD | 普通 COMMON | 1000 | ~500金/个 | ~2000金/个 |
| 3 | 矿石 ORE | 普通 COMMON | 1000 | ~500金/个 | ~2000金/个 |
| 4 | 水银 MERCURY | 稀有 RARE | 2000 | ~1000金/个 | ~4000金/个 |
| 5 | 水晶 CRYSTAL | 稀有 RARE | 2000 | ~1000金/个 | ~4000金/个 |
| 6 | 硫磺 SULFUR | 稀有 RARE | 2000 | ~1000金/个 | ~4000金/个 |
| 7 | 宝石 GEM | 稀有 RARE | 2000 | ~1000金/个 | ~4000金/个 |

**实际价值比**（换算到金币的真实成本）：
- 普通资源（木材、矿石）：基础价值 1000（NPC买入~500金，卖出~2000金）
- 稀有资源（水银、水晶、硫磺、宝石）：基础价值 2000（NPC买入~1000金，卖出~4000金）

**NPC价格公式**：
- NPC买入价（你卖给商人）= `goldValue / 2`（基础价值的一半）
- NPC卖出价（你从商人买）= `goldValue * 2`（基础价值的两倍）
- 买卖差价 = 4 倍（卖出价是买入价的 4 倍）

## 阵营主要稀有资源

每个阵营有其对应的主要稀有资源，该阵营建筑升级主要消耗该资源：

| 阵营 | 主要稀有资源 | 次要稀有资源 | 说明 |
|------|-------------|-------------|------|
| 圣堂 HAVEN | 水晶 CRYSTAL | 宝石 GEM | 大部分兵种和建筑需要水晶，T6/T6P 需要宝石 |
| 地狱 INFERNO | 硫磺 SULFUR | 水晶 CRYSTAL | 大部分需要硫磺，T6/T6P 需要水晶 |
| 学院 ACADEMY | 宝石 GEM | 水银 MERCURY | 大部分需要宝石，T6/T6P 需要水银 |
| 亡灵 NECROPOLIS | 水银 MERCURY | 硫磺 SULFUR | 大部分需要水银，T6/T6P 需要硫磺 |

### 兵种招募的资源需求规律（按 tier）

| Tier | 金币 | 普通资源（木/矿石/水银）| 主要稀有资源 | 次要稀有资源 |
|------|------|----------------------|------------|------------|
| T1 | ✓（便宜）| — | — | — |
| T2 | ✓ | ✓ 少量 | — | — |
| T3 | ✓ | ✓ | — | — |
| T4 | ✓ | ✓ | — | — |
| **T5** | ✓ | ✓ | **✓ 少量** | — |
| **T6/T6P** | ✓ | ✓ | — | **✓ 需要（中等）** |
| **T7/T7P** | **✗ 不要金币** | — | **✓ 大量** | — |

两个关键经济转折点：
- **T5 开始吃主要稀有**：没矿的阵营从这层开始卡产能
- **T7 只吃主矿不吃金**：主矿丰富时 T7 变成"免金币生产"，经济模式反转

### 资源综合决策：应该主力招募 T 几？

**根据当前拥有的矿产类型和数量 + 阵营主矿状况，综合决策**。不要无脑追高 tier，要看资源约束：

| 当前资源状况 | 主力 tier 建议 | 理由 |
|------------|-------------|------|
| **无阵营主矿**（新号/新城） | **兵海 T1-T3 基础版** | 绕开稀有瓶颈，只吃金币；搭配 per-unit 加成生态战力不差 |
| 金币足、**1 个阵营主矿** | T4 主力 + 少量 T5 | 主矿产量不足支撑 T5 海量，T6/T7 还早 |
| 金币足、**2 个主矿 + 次要稀有矿** | **T5 主力 + 少量 T6** | 主矿供 T5，次要稀有矿供 T6 做决胜位 |
| 金币足、**3+ 主矿 + 充足次要稀有** | **T6 主力，T7 备用** | T6 吃金 + 次要稀有双重消耗，成本稳定；T7 产能有限当决胜位 |
| **3+ 主矿、金币紧缺** | **T7 全力** | T7 不吃金，主矿丰富时 T7 变成经济最优解；T6 反而吃金币雪上加霜 |
| 主矿 1-2 个但金币短缺 | 兵海 T1-T3 应急 | 既缺金又缺稀有时，兵海是唯一出路 |

### 双重资源瓶颈：兵种 vs 建筑（优先级规则）

阵营主矿（水晶/硫磺/宝石/水银）中后期有**双重消耗**：

1. **建筑消耗**：MAGIC_GUILD_LVL3+、RECRUIT_T6/T7 建造 → **一次性大量**主矿
2. **兵种消耗**：T5（少量）、T6（吃次要）、T7（大量主矿）→ **持续性**消耗

**主矿不够两边用时，建筑优先于兵种**：
- 建筑是**永久加成**（放大所有战力，技能效率、招募速度、魔力等）
- 兵种是**消耗品**（一次战败就损失 10%+）
- 建 MAGIC_GUILD_LVL3 一次投入让之后所有 VALUE_MEMBERS 增益永久强化，ROI 远大于当场招一堆 T6

判定流程：
```
是否有 MAGIC_GUILD_LVL3+ / RECRUIT_T7 等关键建筑可建？
├─ 是 → 先囤主矿建建筑，暂停招 T6/T7
└─ 否 → 继续招 T6/T7 消耗主矿
```

### 矿区占领优先级（前期 → 中后期演化）

| 阶段 | 抢矿优先级 |
|------|-----------|
| 前期（1-2 城） | **金矿 >> 普通矿（木/矿石）>> 稀有矿** —— 金币是一切基础，兵海和 T1-T4 不吃稀有 |
| 中期（2-4 城） | **金矿 + 阵营主矿 > 次要稀有 > 普通矿** —— 开始需要主矿建 MAGIC_GUILD 和招 T5 |
| 后期（4+ 城） | **阵营主矿 >> 金矿 > 其它** —— T7 海吃主矿，金矿反而够用 |

开新城选址见 $SKILL_DIR/territory.md，铁律："金矿决定一切"仅适用前中期，后期应转为"主矿决定一切"。

### 流派与资源的匹配

| 流派 | 资源依赖 | 适合条件 |
|------|---------|---------|
| **兵海流派** | 只要金币 + 普通资源 | 主矿少/新号/新城；最低资源门槛的出战力路径 |
| **精英流 T4-T5** | 金币 + 主矿（少量）| 有 1-2 主矿的中期标配 |
| **精英流 T6** | 金币 + 次要稀有矿 | 有次要稀有矿（阵营 ↔ 阵营交换后拿的矿，或开城抢） |
| **精英流 T7** | **只要主矿（大量）** | 3+ 主矿 + 金币紧缺时最优（金币压力转成主矿压力） |

**关键洞察**：**资源充裕度决定流派**，不是英雄职业决定流派。
- 有 3+ 主矿 → T7 经济最优，精英流
- 无主矿 → 兵海最优，不看职业
- 职业 + 装备 + 法术只是在资源允许的流派里做"加速器"

## 金币收入

### 市政大厅等级与金币收入

市政大厅（Village Hall 系列）是唯一决定金币存储上限和基础金币收入的城市建筑：

| 建筑 | 每日金币收入 | 金币存储上限 |
|------|-------------|-------------|
| VILLAGE_HALL（村庄大厅） | 2,000 | 30,000 |
| TOWN_HALL（城镇大厅） | 4,000 | 60,000 |
| CITY_HALL（城市大厅） | 7,000 | 150,000 |
| CAPITOL（议会大厦） | 13,000 | 500,000 |

### 金矿收入

金矿每升一级增加 2,000 金/天。

### 总金币收入公式

```
每日金币总收入 = 市政大厅收入 + 金矿等级 * 2000 + 金矿强化加成 + 英雄效果加成
```

## 维护费机制（Maintenance，兵多了会逃跑）

**维护费是每座城市独立计算**——不是全账号总收支。每座城市都有自己的"军队支撑上限 `citySupportCapacity`"，超过后指数级征税，一旦 **金币净收入 ≤ 0** 且 **金库见底**，部队每小时 10% 按堆向上取整永久逃跑。Agent 最常见的死法是往新城搬驻军不看收入，直接破产损兵。

### 关键机制（源码验证）

从 `Region.class.php:2887-3020` 的 `computeMaintenanceCost` / `updateRegionMaintenance` 梳理：

```
maintenanceRatio = regionArmyPower / citySupportCapacity
maintenanceTaxRate = getMaintenanceTaxRate(maintenanceRatio)   # 公式：比值越大，税率越高（非线性）
maintenanceGoldCost = goldIncome * maintenanceTaxRate
netGoldIncome = goldIncome - maintenanceGoldCost
```

- `regionArmyPower` = **城市驻军总 power + 该城市境内所有英雄携带部队的总 power**（英雄在城内就算这座城的维护负担！）
- `citySupportCapacity` = 城市建筑提供的军队上限（市政大厅、军营、城堡等建筑加成）
- 减免：`MAINTENANCE_DECREASE` 英雄技能/装备 -3%/6%/9%，**封顶 60% 减免**

### 逃跑触发条件（三个全中才逃）

```
if (cityGoldIncome ≤ 0)           # 金收入不正
   && (cityGoldStock == 0)        # 金库见底
   && (now > maintenanceNextCheckDate)   # 到了检查点
{
   for each unitStack in (城市驻军 + 城内英雄携带部队):
       unitsLost = ceil(quantity × CONFVALUE_MAINTENANCE_UNIT_DISBAND_RATE / 100)
                 = ceil(quantity × 10%)
       stack.quantity -= unitsLost
   玩家统治力分 -= 总 powerLost   # 排名也被打击
   发送 TYPE_MAINTENANCE 消息
   下次检查 = now + 3600s（1 小时）
}
```

**关键数值**：
- `CONFVALUE_MAINTENANCE_UNIT_DISBAND_RATE = 10` → 每次检查逃跑 **10%**
- `CONFVALUE_MAINTENANCE_FREQUENCY = 3600` 秒 → **每小时检查 1 次**（快速世界为 480 秒 / 8 分钟）
- **向上取整**：1 个兵也会逃跑（`ceil(1 × 0.1) = 1`），小堆更惨
- **连续扣 10%**：10 小时后 1000 兵只剩 349 人（0.9^10）
- **统治力同步扣**：逃跑的 powerLost 直接从 dominationScore 减掉——经济崩溃 + 排名下滑

### 决策底线（Agent 每轮必查）

1. **硬底线：任何一座城市 `goldIncome > 0`**（注意是正数，不是 ≥ 0；只要正就完全安全，金库再少都不会逃兵）
2. **新城警戒**：新城初始 `citySupportCapacity` 低 + 金矿收入少（2000-5000/天）→ 只运当前战斗需要的兵力（参考：~30-60k 战力），绝不超过 100k
3. **英雄移动同步算维护**：英雄带兵进城会立即加到该城 `regionArmyPower`，哪怕只路过。打完仗立刻 MOVE 离开或 MOVE_TO_REGION 卸兵
4. **驻军集中原则**：如果有多座城市，**把大部队集中在金矿多、citySupportCapacity 高的主城**，不是分散每城一点

### 应对动作（发现负收入时）

按优先级：

1. **MOVE 英雄离开**：如果英雄带兵在新城，先移到主城。**这是最快的止血**（分钟级生效）
2. **MOVE_TO_REGION 卸到主城驻军**：把新城兵团转到主城驻军（主城支撑上限高）
3. **DISBAND 弱兵**：驻军里的 NEUTRAL 战利品、quantity<10 的残堆、低阶过时兵一律 DISBAND
4. **CARAVAN_DELIVERY 应急运金**：主城向危机城市运一波金币，填金库避免见底触发逃跑（治标不治本，但争取时间）
5. **市场应急卖资源**：`marketPlaceAction SELL_NPC` 把非金资源卖给 NPC 换金（差价大但救急）
6. **最后手段**：直接 `GIVE_CITY` 把撑不起来的新城送给联盟友军

### 与兵海流派的关系

兵海流派看似吃很多维护（1500 T1 x 0.5 金/天 = 750 金/天），但因为：
- 集中在主城（高 citySupportCapacity）
- 低阶单兵维护费 ≈ 0.5 金/天（高阶 T7 可能数十金/天）
- 招募纪律明确"一个英雄主堆制"——不会分散到每个新城

所以兵海流派反而比分散配置 T5/T6 的精英流在维护费上更轻。

## 矿产升级

### 产量公式

```
production = base × upgradeLevel × (1 + 0.05 × improveLevel)
```

矿产有两个独立等级属性：
- **upgradeLevel** — 矿的基础等级（由 mineEntity 决定），范围 1~10
- **improveLevel** — 强化等级（存储在 Mine 上），范围 0~upgradeLevel-1

### 每级增量（base 值）

| 资源类型 | base（每日基础产量/级） |
|---------|---------------------|
| 金币 | 2,000/天 |
| 普通资源（木材/矿石） | 2/天 |
| 稀有资源（水银/水晶/硫磺/宝石） | 1/天 |

### 三种矿产操作

| 操作 | 效果 | 代价 | 需要英雄 |
|------|------|------|---------|
| **Upgrade（升级）** | upgradeLevel +1 | 消耗金币，需要英雄 | 是 |
| **Improve（强化）** | upgradeLevel +1 **且** improveLevel +1 | 消耗金币，需要英雄，**停产** | 是 |
| **Downgrade（降级）** | upgradeLevel 降至 improveLevel+1 | 耗时 9000 秒（2.5h） | 否 |

关键约束：
- Improve 只在 `improveLevel == upgradeLevel - 1` 时可用（必须追平才能强化）
- Upgrade 后 improveLevel 不变，导致 `improveLevel < upgradeLevel - 1`，无法再 Improve
- Downgrade 把 upgradeLevel 退回到 `improveLevel + 1`，重新满足 Improve 条件

### 什么时候该升级矿产

**矿产升级用英雄执行，和城市建筑队列互不冲突。** 英雄空闲时应优先考虑升矿，因为投资回报率极高：

| 矿类型 | 升级收益 | 大约金币成本 | 回本天数 |
|--------|---------|------------|---------|
| 金矿 Lv1→2 | +2,000 金/天 | ~3,000 金 | **1.5 天** |
| 金矿 Lv2→3 | +2,000 金/天 | ~5,000 金 | 2.5 天 |
| 普通矿 Lv1→2 | +2/天 | ~3,000 金 | — |
| 稀有矿 Lv1→2 | +1/天 | ~3,000 金 | — |

**英雄空闲时的优先级**：
1. 解放城内建筑（如有未解放的）
2. 攻击 NPC 区域扩张领土
3. **升级金矿**（ROI 最高，1-3 天回本）
4. 升级其他矿产
5. 学习技能/职业
6. 建造/升级野外建筑

**关键原则：英雄升矿不占用建筑队列。** 城市可以同时在建造 TOWN_HALL，而英雄去升矿。两条线并行 = 收入双倍增长。

### Improve vs Upgrade：始终用 Improve

执行矿产升级时，用 IMPROVE_MINE 而非 UPGRADE_MINE。Improve 同时提升 upgradeLevel 和 improveLevel，效果严格优于 Upgrade。

**产量对比（金矿为例）：**

| upgradeLevel | 纯 Upgrade (I=0) | 全 Improve (I=L-1) | 差距 |
|-------------|------------------|-------------------|------|
| 1 | 2,000 | 2,000 | — |
| 2 | 4,000 | 4,200 | +5% |
| 5 | 10,000 | 12,000 | +20% |
| 10 | 20,000 | 29,000 | **+45%** |

**正确的升级路线：**

```
初始: upgradeLevel=1, improveLevel=0 → 满足 Improve 条件 (0 == 1-1)
  ↓ Improve
upgradeLevel=2, improveLevel=1 → 满足 Improve 条件 (1 == 2-1)
  ↓ Improve
upgradeLevel=3, improveLevel=2 → 满足 Improve 条件 (2 == 3-1)
  ↓ ...一路 Improve...
upgradeLevel=10, improveLevel=9 → 满级，产量最大化
```

**硬上限**：矿产最高 upgradeLevel=10，达到后 IMPROVE_MINE 和 UPGRADE_MINE 均返回 IMPOSSIBLE_ACTION。

**永远不要用 UPGRADE_MINE**，因为：
1. IMPROVE_MINE 给你 UPGRADE 的全部收益（upgradeLevel +1）外加额外 +5% 产出加成
2. UPGRADE 后 improveLevel 落后，你必须 Downgrade（浪费 2.5h）再 Improve 来补救
3. IMPROVE 唯一的额外代价是强化期间停产，但这是临时的，+5%/级加成是永久的

**仅有的例外**：矿即将被敌人夺走，此时停产做 Improve 不如快速 Upgrade 多产一点资源。

### Downgrade 用法

Downgrade 用于纠正误操作——如果不小心用了 Upgrade 跳过了 Improve，可以降级回去重新 Improve。

- 不需要英雄，不需要金币
- 耗时 9000 秒（2.5 小时，受世界速度调整）
- 降级期间矿产正常产出

### 操作方式

**强化矿产（始终使用这个）：**
```json
{"type": "addAction", "params": {
  "actionType": "IMPROVE_MINE",
  "actorType": "Hero",
  "actorId": <heroId>,
  "actionParams": "<zoneId>;<速度>"
}}
```

**升级矿产（仅在矿即将被敌人夺走时使用）：**
```json
{"type": "addAction", "params": {
  "actionType": "UPGRADE_MINE",
  "actorType": "Hero",
  "actorId": <heroId>,
  "actionParams": "<zoneId>;<速度>"
}}
```

**降级矿产（纠错用）：**
```json
{"type": "addAction", "params": {
  "actionType": "DOWNGRADE_MINE",
  "actorType": "Region",
  "actorId": <regionId>,
  "actionParams": "<zoneId>"
}}
```

zoneId 从 gameState 的 `zones[].id`（已占领且有 mine 的 zone）获取。速度参数同 BUILD_CITYBUILDING。Downgrade 的 actorType 是 Region 而非 Hero，无需英雄参与。

### 升级条件

- 英雄必须在该矿所在区域（Upgrade/Improve）
- 英雄必须空闲
- **英雄必须无部队**（Upgrade/Improve 均要求）
- 需要消耗金币（随等级递增）
- 升级和强化都需要时间，受英雄建筑师技能（BUILDING_SPEED_INCREASE）加速
- Improve 期间矿产停止生产

**IMPROVE_MINE vs UPGRADE_MINE 费用对比**：两者均只消耗黄金。IMPROVE_MINE 费用**高于** UPGRADE_MINE（因为 Improve 效果更好）。如果 IMPROVE_MINE 报 `NOT_ENOUGH_RESOURCES` 错误，通常是因为金币不足（不是缺少木材/矿石），可以先等待金币积累再 Improve。**不建议用 UPGRADE_MINE 代替再做 Downgrade 补救**：Downgrade 会短暂降低矿产等级（升级到Lv3的矿暂时退回Lv2），而 IMPROVE 期间停产，双重损失的代价远超 IMPROVE 带来的 +5% 收益，前期尤其得不偿失。

**前期黄金策略（重要）**：
- 招募 T1~T5 **只需黄金**；矿产升级/强化**只需黄金**；建造 T1~T5 招募建筑**只需黄金+少量木/矿**
- **卖出非阵营稀有资源**换取黄金——NPC 收购约 1000 金/个（详见下方"NPC商人交易"）
- **果断买入缺口木材/矿石**——建筑差几个就买，不要让建筑队列空转等自然积累
- 黄金是前期发展的核心货币，**资源流动 > 资源囤积**

**带兵英雄如何升矿**：升矿要求英雄身上没有部队，但这不意味着要等打完仗才能升矿。正确做法是先用 `unitStackListAction MOVE_TO_REGION` 把部队卸到城防驻军，升完矿再用 `MOVE_FROM_REGION` 装回来。英雄部队和城防驻军是独立的，互不影响。

## 资源储存上限

### 非金币资源储存

非金币资源的存储上限由**资源仓**（Support 类城市建筑）等级决定：

提升资源储存上限的方式：
1. **升级资源仓** — 最主要的方式，每级大幅提升普通/稀有资源上限
2. **升级市场** — 市场建筑（MarketPlace）也属于 Support 类建筑，但以资源仓为优先
3. **野外建筑** — 部分野外建筑提供 `STORAGE_INCREASE` 效果
4. **英雄技能** — 某些英雄技能提供 `STORAGE_INCREASE` 或特定资源的储存加成

### 金币储存

金币储存由市政大厅等级决定（见上表），最高 CAPITOL = 500,000 金。

### 储存上限公式

```
实际上限 = 基础上限 * (1 + 野外建筑/英雄加成百分比 / 100)
```

## NPC商人交易

### 买卖价差

NPC商人的买卖价差巨大（约 4 倍）：
- 你卖给NPC 1 个木材只能得到 ~500 金
- 你从NPC买 1 个木材需要花 ~2000 金

价差虽大，但**不代表不能买卖**。关键是判断交易是否能加速整体发展节奏。

### 资源交易策略

**1. 卖出非阵营稀有资源（前期重要收入来源）**

前期打 NPC 会掉落各种稀有资源，但你的阵营只需要其中一种。非阵营稀有资源前期用不到，留着只会占储存上限。果断卖掉换金：

| 阵营 | 保留 | 卖出 | 说明 |
|------|------|------|------|
| 圣堂 HAVEN | 水晶 | 水银、硫磺、宝石 | 极少数建筑需要宝石（T6/T6P），前期可先卖 |
| 地狱 INFERNO | 硫磺 | 水银、水晶、宝石 | |
| 学院 ACADEMY | 宝石 | 水银、水晶、硫磺 | |
| 亡灵 NECROPOLIS | 水银 | 水晶、硫磺、宝石 | |

稀有资源 NPC 收购价 ~1000 金/个，比普通资源（500 金/个）更值得卖。**宁愿持有黄金也不要囤用不到的稀有资源。**

**2. 果断买入关键缺口资源**

当建筑只差少量木材或矿石时，**不要干等自然积累**。等待的时间成本远超 NPC 的高价。例如：
- 建筑差 5 木材 → 买入花 10,000 金，但建筑立刻开工，节省数小时等待
- 等自然积累 5 木材 → 以 2 木/天的产量需要 2.5 天，期间建筑队列空转

**原则：如果买入资源能让建筑队列不空转，就值得买。** 建筑队列空闲 = 浪费发展时间，代价比 NPC 高价大得多。

**3. 利用季节波动降低买卖成本**

NPC 价格随季节浮动约 ±20%。如果不急需，等有利季节再交易：
- **卖出**时选资源价格 +20% 的季节（多赚 20%）
- **买入**时选资源价格 -20% 的季节（少花 20%）
- 通过 `MarketPlaceFrame.currentSeason` 和 `resourceCotation` 查看当前季节对各资源的影响
- **但不要为了等季节而让建筑队列空转**——季节优化是锦上添花，不是必须条件

**4. 配合商人职业技能**

学了商人（MERCHANT）职业的英雄有交易加成技能：
- `NPC_BUY_DECREASE` — 降低从 NPC 购买的价格（买入更便宜）
- `NPC_SELL_INCREASE` — 提高卖给 NPC 的价格（卖出更值钱）

**让学了商人职业的英雄驻守在交易量最大的城市**，所有该城的 NPC 买卖都会享受加成。

**MarketPlaceFrame 字段说明（防止混淆）**：
- `resourceBuyPrice`：NPC 购买你的资源的价格（即**你出售给NPC**的价格，约500金/普通资源）
- `resourceSellPrice`：NPC 出售给你的价格（即**你从NPC购买**的价格，约2000金/普通资源）
- 字段名从 NPC 视角命名，容易混淆——记住：你买资源时看 `resourceSellPrice`（高价）

### 季节和日期波动

NPC价格受季节（Season）和日期（Day）影响：
- **季节加成**：每种资源在不同季节有 `+`（+20%）或 `-`（-15%~-25%随机）标记
- **每日加成**：每天有一种资源获得 +15%~+25% 的随机价格加成

通过 `getContent` 获取 `MarketPlaceFrame` 可查看当前实时买卖价格：

```bash
curl -k -s -b $COOKIES -X POST "$BASE/api/agent/action" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "getContent",
    "params": {
      "elParamList": [
        {"elementType": "MarketPlaceFrame", "elementId": <regionId>}
      ]
    }
  }'
```

返回数据包含：
- `resourceBuyPrice` — NPC买入价（你卖出的价格）
- `resourceSellPrice` — NPC卖出价（你购买的价格）
- `goldValue` — 各资源的基础金价
- `auctionOfferList` — 当前拍卖出售列表
- `auctionRequestList` — 当前拍卖求购列表

### NPC交易 API

**卖给NPC（获得金币）**：
```bash
curl -k -s -b $COOKIES -X POST "$BASE/api/agent/action" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "marketPlaceAction",
    "params": {
      "action": "SELL_NPC",
      "regionId": <regionId>,
      "order": {"WOOD": 10, "ORE": 5}
    }
  }'
```

**从NPC购买（消耗金币）**：
```bash
curl -k -s -b $COOKIES -X POST "$BASE/api/agent/action" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "marketPlaceAction",
    "params": {
      "action": "BUY_NPC",
      "regionId": <regionId>,
      "order": {"CRYSTAL": 3}
    }
  }'
```

`order` 字段使用资源 tagName 作为 key（WOOD / ORE / MERCURY / CRYSTAL / SULFUR / GEM），值为数量。不支持买卖 GOLD 本身。

## 玩家拍卖

拍卖行是玩家之间交易资源的核心渠道，需要城市建造了市场（MarketPlace）才能使用。

### 拍卖机制

拍卖分为两种：
- **出售（OFFER）**：你挂出资源，设定起拍价和一口价，其他玩家竞拍或直接一口价买走
- **求购（REQUEST）**：你挂出金币求购某种资源，其他玩家可以竞价向你出售

每笔拍卖包含：
- `startingPrice` — 起拍价
- `limitPrice` — 一口价（出售时为最高买断价，求购时为最低卖断价）
- `quantity` — 资源数量
- `bestPrice` — 当前最高竞价
- `nextBid` — 下一手最低竞价
- `endDate` — 拍卖截止时间
- `deliveryDuration` — 交货运输时间

### 时长和税率

拍卖按持续时间分为三档，时间越长税率越高：

| 时长档位 | 持续时间 | 税率 |
|---------|---------|------|
| Level1 | 12 小时 | 3% |
| Level2 | 24 小时 | 4% |
| Level3 | 48 小时 | 5% |

税费 = `max(一口价, 数量 * 基础金价) * 税率%`，在发起拍卖时扣除。

### 如何捡漏

通过 `getContent` 获取 `MarketPlaceFrame` 后检查 `auctionOfferList`：
- 如果某个出售的 `currentPrice`（当前价/起拍价）低于资源的基础价值（普通资源约1000金/个，稀有约2000金/个），就是有性价比的好价格
- 关注即将到期、无人竞价的拍卖

### 拍卖 API

通过 `marketPlaceAction` 操作拍卖：

**创建出售拍卖**：
```json
{"type":"marketPlaceAction","params":{
  "action":"CREATE_OFFER_REQUEST",
  "regionId":"<区域ID>",
  "offerOrRequest":"OFFER",
  "quantity":20,
  "ressourceEntityId":2,
  "startingPrice":5000,
  "limitPrice":15000,
  "taxRate":"Level1"
}}
```

**创建求购拍卖**：同上，`offerOrRequest` 改为 `"REQUEST"`。

`ressourceEntityId`：2=木材, 3=矿石, 4=水银, 5=水晶, 6=硫磺, 7=宝石。`taxRate` 从 `MarketPlaceFrame.taxList` 获取（Level1/Level2/Level3）。

**竞拍**：
```json
{"type":"marketPlaceAction","params":{
  "action":"BID_OFFER_REQUEST",
  "regionId":"<区域ID>",
  "auctionOfferRequestId":"<拍卖ID>",
  "newPrice":8000
}}
```

**一口价买断**：同竞拍，`newPrice` 设为拍卖的 `limitPrice`。

**取消拍卖**（仅限无人出价时）：
```json
{"type":"marketPlaceAction","params":{
  "action":"CANCEL_OFFER_REQUEST",
  "regionId":"<区域ID>",
  "auctionOfferRequestId":"<拍卖ID>"
}}
```

## 多城市商队运输

商队是城市之间运输资源的方式，需要城市有市场建筑（MarketPlace）。分为单次商队和商路（Traderoute，自动重复）。

### 商队参数格式

商队的 `actionParams` 格式为：
```
<目标区域编号>;<金币数>;<木材数>;<矿石数>;<水银数>;<水晶数>;<硫磺数>;<宝石数>;CARAVAN
```

7 种资源按 ID 顺序排列（GOLD;WOOD;ORE;MERCURY;CRYSTAL;SULFUR;GEM），用分号分隔。

### 单次商队

通过 `addAction` 发送单次商队：
```bash
curl -k -s -b $COOKIES -X POST "$BASE/api/agent/action" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "addAction",
    "params": {
      "actionType": "CARAVAN_DELIVERY",
      "actorType": "Region",
      "actorId": <发出城市的regionId>,
      "actionParams": "<目标区域编号>;5000;10;10;0;0;0;0;CARAVAN"
    }
  }'
```

### 商路（自动重复商队）

通过 `marketPlaceAction` 的 `CREATE_TRADEROUTE` 创建自动重复的商队路线：

```json
{"type":"marketPlaceAction","params":{
  "action":"CREATE_TRADEROUTE",
  "regionId":"<发出城市的区域ID>",
  "destRegionNumber":"<目标城市的区域编号>",
  "resources":{"GOLD":5000,"WOOD":10,"ORE":10,"MERCURY":0,"CRYSTAL":0,"SULFUR":0,"GEM":0},
  "repeatNb":6,
  "stockThreshold":1,
  "waitingTime":0
}}
```

参数说明：
- `destRegionNumber` — 目标城市区域编号（从 `MarketPlaceFrame.caravanDestinations` 获取）
- `resources` — 每次运输的各资源数量，用资源名做 key
- `repeatNb` — 重复次数（2~6，有特殊选项时最多10）
- `stockThreshold` — 存量阈值（1~6/10），当资源低于此比例时暂停
- `waitingTime` — 等待时间（0~3 小时），两次运输之间的间隔

### 取消商路

```json
{"type":"marketPlaceAction","params":{
  "action":"CANCEL_TRADEROUTE",
  "regionId":"<发出城市的区域ID>"
}}
```

### 运输策略

1. **新城发展期**：从主城向新城运送木材和矿石，加速建筑升级
2. **资源平衡**：不同阵营城市生产不同稀有资源，通过商队在城市间调配
3. **前线补给**：向即将攻击的前线城市运送金币和稀有资源，支持招募
4. **注意**：向其他玩家城市运输受反推手（anti-pushing）机制限制，资源余额不稳定的玩家无法交易

## 收入影响因素汇总表

| 影响因素 | 影响内容 | 说明 |
|---------|---------|------|
| 市政大厅等级 | 金币收入 + 金币存储上限 | VILLAGE_HALL → TOWN_HALL → CITY_HALL → CAPITOL |
| 矿产等级 | 对应资源产出 | 金+2000, 普通+2, 稀有+1 每级 |
| 矿产强化等级 | 产出百分比加成 | 每级 +5% |
| 英雄效果 | 多种加成 | NPC_SELL_INCREASE（卖价加成）、NPC_BUY_DECREASE（买价折扣）、STORAGE_INCREASE |
| 季节 | NPC 买卖价波动 | +20% 旺季 / -15%~-25% 淡季 |
| 每日波动 | 单一资源价格加成 | +15%~+25% 随机 |
| 资源仓等级 | 非金币资源存储上限 | 最主要的存储提升手段 |
| 野外建筑 | 存储/产出加成 | STORAGE_INCREASE 效果 |
| 市场等级 | 商队容量 + 拍卖功能 | 需要市场才能交易和运输 |
| 联盟野外建筑 | 生产/存储加成 | 通过商队贡献资源建造 |
