# 领地篇

## 世界结构（三层地图）

```
世界地图 (World)
└── Region（区域）— 世界地图上的一个格子
    ├── Zone 30（中心）= 内城：建筑、招募、解放建筑都在这里
    ├── Zone X = 矿产区（约4个Zone有矿）
    ├── Zone Y = NPC 野怪区
    └── ...共约24个Zone
```

**Region（区域）** 是世界地图上的基本单元。世界地图由很多 Region 组成：
- **空平原 Region** — 没有玩家占领，可以派英雄去**开新城**（HERO_SETTLE_REGION）
- **已占领 Region** — 属于某个玩家的城市，每个城市对应一个 Region

**Zone（子区域）** 是 Region 内部的小格子，每个 Region 约 24 个 Zone：
- **Zone 30（中心）= 内城** — 城市核心，建造建筑（BUILD_CITYBUILDING）、招募部队（REGION_RECRUIT）、解放建筑（HERO_LIBERATE_CITY_BUILDING）都在内城进行
- **矿产 Zone** — 约 4 个 Zone 有资源矿（金、木、矿、水银、水晶、硫磺、宝石），被 NPC 守着，清掉后占领开始产出
- **普通 Zone** — 无资源，可以建造野外建筑

**关键区分：**
- Zone 里的 NPC 是城市内部的守军，打掉是为了占矿/建野外建筑 → `HERO_ATTACK_NPC`
- Region 是世界地图上的位置，找空平原是为了开新城 → `HERO_SETTLE_REGION`
- 这是完全不同的两件事，不要混淆

### Zone 布局
- 内城（Zone 30，开局已占领）
- 内圈 Zone：距离城市最近，NPC 较弱（Lv1）
- 中圈 Zone：NPC 中等（Lv2-3）
- 外圈 Zone：NPC 最强（Lv4-5）

### 占领优先级
1. 内圈的矿区（容易打，立即有收入）
2. 自己阵营主要稀有资源的矿区
3. 金矿（金币收入最重要）
4. 普通资源矿（木材、矿石用于建筑）
5. 其他稀有资源矿

## 城市数量上限（排名等级系统）

城市数量上限由**排名等级（Ranking Threshold）**决定，这是决定何时能开新城的核心机制。

### 三大排名等级

每个排名维度（统治力/财富/荣耀）都有独立的等级（1~10级），等级通过累积分数自动提升：

| 维度 | 分数来源 | gameState 字段 |
|------|---------|---------------|
| 统治力 (Domination) | 建筑价值 + 军队战力 | `dominationRankingThreshold` |
| 财富 (Wealth) | 历史累计资源收入 | `wealthRankingThreshold` |
| 荣耀 (Honor) | 英雄累计经验值 | `honorRankingThreshold` |

### 城市上限计算

```
城市上限 = max(统治力等级, 财富等级, 荣耀等级)
```

**三项取最高值**，意味着只要任意一个维度的等级提升，就能开更多城市。

gameState 返回的关键字段：
- `player.dominationRankingThreshold` / `wealthRankingThreshold` / `honorRankingThreshold` — 当前三项等级
- `player.nextDominationObjective` / `nextWealthObjective` / `nextHonorObjective` — 下一等级所需分数（null = 已满级）
- `player.maxCityCount` — 当前可拥有的最大城市数
- `player.currentCityCount` — 当前城市数

### 判断是否能开新城

```
if player.currentCityCount < player.maxCityCount:
    可以开新城
else:
    需要先提升排名等级（检查哪个维度离下一级最近）
```

### 如何提升排名等级

检查 `nextDominationObjective`、`nextWealthObjective`、`nextHonorObjective`，选择**差距最小**的维度集中提升：

| 维度离下一级最近 | 提升手段 |
|----------------|---------|
| 统治力 | 建造/升级建筑、招募更多部队、建野外建筑 |
| 财富 | 升级矿产（IMPROVE_MINE）、占领更多矿区 |
| 荣耀 | 让英雄持续战斗积累经验 |

## 开新城市（扩张）

### 前提条件
1. **城市上限允许** — `currentCityCount < maxCityCount`（最重要的前提！）
2. 英雄必须有部队
3. 目标区域必须是空的平原（未被占领）
4. 目标区域在自己或联盟的影响范围内
5. 城市名不能重复（最多11字符）

### 扩张时机

- **排名等级**已提升到允许开新城（`maxCityCount > currentCityCount`）
- 本区域大部分 Zone 已占领（没有更多矿可以打了）
- 有多余英雄可以分配到新城
- 金币充足支撑新城初期建设
- 有商队可以运输初始资源
- 已侦察到合适的开城位置

### 选址流程（三步走）

#### 第一步：查看世界地图找空平原

```json
{"type":"getContent","params":{"elParamList":[{"elementType":"WorldMap","w":15,"h":15}]}}
```
- 不传 `x`/`y` 时自动以主城为中心；传 `x`/`y` 则以该坐标为中心
- `w`/`h` 是视野宽高（最大 20），默认 11×11
- 返回 `plains` 数组（只含平原 Region）和 `terrain` 统计
- **空平原**：`captured=false` 的 Region，可以开城
- **有影响力的空平原**：带 `influencePlayerId`（属于自己或联盟），开城优先选这些

#### 第二步：用 scanAreaMines 批量扫矿（推荐）

**批量扫矿是选址的关键工具。** 对应前端"采矿勘探"按钮（MINE_PROSPECT_TOGGLE），一次调用返回矩形范围内所有 Region 的矿产信息，比逐个调用 `scanRegionMines` 效率高得多。

```json
{"type":"scanAreaMines","params":{"x":30,"y":45,"w":15,"h":15}}
```

参数说明：
- `x`/`y` — 矩形左上角坐标（不传则以主城为中心）
- `w`/`h` — 宽高，**最大 15×15**（超出需要分多次调用）

返回示例：
```json
{
  "centerX": 37, "centerY": 52, "w": 15, "h": 15,
  "cells": [
    {
      "regionId": 3785, "x": 35, "y": 51,
      "type": "plain", "captured": false,
      "mines": {
        "GOLD": {"name": "黄金", "count": 2},
        "WOOD": {"name": "木材", "count": 1},
        "CRYSTAL": {"name": "水晶", "count": 1}
      }
    },
    ...
  ]
}
```

**注意**：`type` 字段是小写字符串 `"plain"`（不是 "PLAIN"）。过滤平原时用 `cell["type"] == "plain"`。

**选址流程：**
1. `scanAreaMines` 扫一次 15×15 区域（以主城为中心）
2. 从 `cells` 里筛选 `captured=false` 且 `type=="plain"` 的候选
3. 按下方优先级打分选最优
4. 如果 15×15 范围内无理想位置，用不同 `x`/`y` 多次调用扩展搜索

**单个 Region 查询**（只在需要精确确认某个 regionId 时用）：
```json
{"type":"scanRegionMines","params":{"regionId": 123}}
```

#### 第三步：按选址标准打分，选最优位置

**核心原则：没有金矿的区域不能发展。** 金矿是城市经济的命脉，每个金矿提供 2000 金/天/级的收入。无金矿城市只能靠市政大厅的微薄收入（2000~13000 金/天），根本无法支撑建筑、招募和维护费用。

**选址优先级（严格按此顺序筛选）：**

**第一优先级：双金矿 + 双普通矿（最优配置）**

寻找同时拥有 2 个金矿的区域，再看剩余 2 个矿槽：
- **理想配置**：2 金矿 + 1 木矿 + 1 矿石矿（木材和矿石是建筑刚需，这种组合完全自给自足）
- **替代配置**：2 金矿 + 2 木矿，或 2 金矿 + 2 矿石矿（偏科但仍强于稀有矿）
- 总之目标是"双金 + 双普通"，这种区域发展速度最快

**第二优先级：双金矿 + 阵营稀有矿**

如果找不到双金+双普通，退而求其次：
- 2 金矿 + 1 阵营主要稀有资源（圣堂=水晶、地狱=硫磺、学院=宝石、亡灵=水银）+ 1 任意矿
- 稀有矿中后期价值高，但前期建设会缺木材/矿石，需要商队补给

**第三优先级：单金矿区域（勉强可用）**

只有 1 个金矿的区域发展缓慢但不是不能用。搭配条件：
- 1 金矿 + 木矿 + 矿石矿 + 阵营稀有矿（资源种类多弥补金矿不足）
- 仅在附近实在没有双金矿区域时考虑

**绝对不选：零金矿区域**

没有金矿的区域**不要开城**。唯一例外是终局阶段（End Game）：某些神器会掉落在特定区域，必须在该区域拥有城市才能获取，此时可以为了神器开无金矿城。

**辅助筛选条件（在同等矿产条件下比较）：**
- **无敌对联盟影响力** — `scanAreaMines` 返回的 `influenceAllianceId` 如果不是自己联盟，**该区域不能开城**（HERO_SETTLE_REGION 会失败）。必须在筛选时排除这些区域。
- **己方影响力范围内** — 有 `influencePlayerId`（属于自己）的空平原优先
- **距离适中** — 太远商队运输慢，太近与主城资源重叠（2-4 格最佳）
- **安全性** — 远离敌对联盟核心区域

**scanAreaMines 批量筛选策略：** 一次扫 15×15 区域，从 `cells[]` 筛选 `captured==false && type=="plain"` 的候选。按金矿数降序排列，金矿数相同时比较普通矿数量。**务必排除带 `influenceAllianceId`（非己方联盟）的区域**——这些区域即使矿产完美也无法开城。

### 开城操作

```json
{"type": "addAction", "params": {
  "actionType": "HERO_SETTLE_REGION",
  "actorType": "Hero",
  "actorId": 40,
  "actionParams": "<目标区域ID>;<城市名>"
}}
```
注意：不要传 actionParamsJSON（会导致错误）。

**资源消耗警告**：HERO_SETTLE_REGION 消耗大量资源（约 90k 金 + 90 木 + 90 矿），必须从资源充足的城市发起。资源不足的城市会失败，确保发起城市有足够储备再执行。

### 新城发展流程
新城市从Lv1开始，需要重走发展流程：
1. 从主城商队运输初始资源（金币 + 木材 + 矿石）
2. 建造酒馆（如果有足够资源）
3. 解放建筑 → 建造
4. 招募英雄和部队
5. 清除周围NPC占领矿区

## 野外建筑 (Zone Building)

在已占领的Zone上建造，提供各种加成。

### 建筑类型

| 类型 | 功能 | 说明 |
|------|------|------|
| 资源生产 (SUPPORT_RESEARCH) | 提升矿产产出 | 按矿产类型分，高级别加成更高 |
| 防御 (DEFENSE) | 增加区域防御值 | 被掠夺或进攻时增加防守方战力 |
| 储存 (SUPPORT_STORAGE) | 增加资源储存上限 | 城内资源仓不够时的重要补充 |
| 招募 (SUPPORT_RECRUITMENT) | 提升兵种招募速度/产量 | |
| 魔法 (MAGICAL) | 魔法相关加成 | |

### 建造条件
- 该Zone的矿产需要达到指定等级
- 英雄可能需要学习特定职业（如建筑师 ARCHITECT）
- 所属城市需要达到指定等级

### 建造操作
```json
{"type": "addAction", "params": {
  "actionType": "HERO_BUILD_ZONEBUILDING",
  "actorType": "Hero",
  "actorId": 40,
  "actionParams": "<zoneBuildingEntityId>"
}}
```

### 建造策略
- 高级矿区优先建资源生产建筑
- 前线矿区（靠近敌人）加建防御建筑
- 稀有资源矿区优先保护

## 地城探索 (Dungeon)

地城是出现在已占领Zone上的特殊建筑，英雄进入后可逐层探索，获取神器、资源、部队、经验等奖励。

### 地城流程

1. **进入地城** — 英雄移动到地城Zone
```json
{"type": "addAction", "params": {
  "actionType": "HERO_MOVE_TO_ZONEBUILDING",
  "actorType": "Hero",
  "actorId": 40,
  "actionParams": "<zoneBuildingId>"
}}
```

2. **探索地城** — 英雄在地城内搜索（触发战斗或发现奖励）
```json
{"type": "addAction", "params": {
  "actionType": "HERO_SEARCH_IN_ZONEBUILDING",
  "actorType": "Hero",
  "actorId": 40,
  "actionParams": "<zoneBuildingId>"
}}
```

3. **领取奖励并离开** — 探索完成后领取奖励，地城坍塌
```json
{"type": "zoneBuildingAction", "params": {
  "action": "HERO_DUNGEON_GET_REWARD_AND_LEAVE",
  "zoneBuildingId": 123,
  "heroId": 40
}}
```

4. **紧急撤退（可选）** — 使用回城石直接传送回城，不领取奖励
```json
{"type": "zoneBuildingAction", "params": {
  "action": "HERO_LEAVE_AND_TELEPORT_TO_TOWN",
  "zoneBuildingId": 123,
  "heroId": 40
}}
```

### 地城奖励类型

| 奖励 | 说明 |
|------|------|
| 神器 (ARTEFACT) | 获得随机神器 |
| 资源 (RESOURCES) | 获得各类资源 |
| 部队 (TROOPS) | 获得额外兵团 |
| 经验 (XP) | 英雄获得经验值 |
| 矿产 (MINE) | 发现新矿产 |
| 魔法光束 (DUNGEON_MAGIC_BEAM) | 魔法加成 |
| 回城石 (DUNGEON_RECALL_STONE) | 获得回城道具 |
| 延伸地城 (EXTRA_DUNGEON) | 解锁更深层 |

### 地城注意事项

- 英雄在地城内时无法执行其他操作（视为忙碌）
- 地城内有NPC守军，探索会触发战斗
- 探索前确保英雄有足够兵力
- 领取奖励后地城坍塌消失，一段时间后可能重新出现
- 回城石是消耗品，仅在地城内有效

## 区域建筑 (Region Building)

比野外建筑更高级的建筑系统：
- 建在区域之间（不是Zone内）
- 提供更强大的区域性加成
- 有自己的升级和组件系统
- 部分有NPC守军需要战斗占领
- 提供大量统治力分数

```json
{"type": "addAction", "params": {
  "actionType": "HERO_BUILD_REGIONBUILDING",
  "actorType": "Hero",
  "actorId": 40,
  "actionParams": "<regionBuildingEntityId>"
}}
```

## 统治力 (Domination)

- 每个野外建筑和区域建筑提供统治力分数
- 统治力是排行榜的关键指标
- 终局条件可能与统治力相关
- 更多、更高级的建筑 = 更高的统治力

## 多城市管理

- 每个城市独立发展（建筑、招募、资源）
- 英雄可以在城市之间移动（HERO_MOVE）
- 商队连接城市运输资源
- 城市越多维护费用越高
- 平衡发展 vs 集中资源
