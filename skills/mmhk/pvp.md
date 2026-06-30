# PvP 篇

## PvP 战斗前的准备

PvP 与打 NPC 完全不同，对手是有策略的人类玩家。必须充分准备。

## 发现其他玩家（PvP 第零步）

在侦察和攻击之前，你需要先**找到**其他玩家。有三种途径：

### 途径一：世界地图（WorldMap）

`getContent WorldMap` 返回视野内所有已占领的 Region，包含玩家信息：

```json
{"type":"getContent","params":{"elParamList":[{"elementType":"WorldMap","w":20,"h":20}]}}
```

返回的 `plains[]` 中，`captured=true` 的 Region 包含：
- `playerId` — 玩家 ID
- `playerName` — 玩家名
- `cityName` — 城市名
- `faction` — 阵营（HAVEN/INFERNO/ACADEMY/NECROPOLIS）
- `cityLevel` — 城市等级（越高说明越发达）

**用法：** 扫描 20×20 视野，找出所有 `captured=true` 且 `playerName` 不是自己的 Region。记录它们的位置（x, y）和 regionId，后续侦察和攻击需要这些信息。

可以传 `x`/`y` 参数移动视野中心，多次扫描覆盖更大范围：
```json
{"type":"getContent","params":{"elParamList":[{"elementType":"WorldMap","w":20,"h":20,"x":50,"y":50}]}}
```

### 途径二：排行榜（RankingFrame）

排行榜是发现所有活跃玩家的最佳途径，不受视野限制：

```json
{"type":"getContent","params":{"elParamList":[{
  "elementType":"RankingFrame",
  "rankingType":"DOMINATION",
  "rankingCategory":"BY_PLAYERS",
  "offset":"top"
}]}}
```

**rankingType 选项：**
- `DOMINATION` — 统治力排行（建筑 + 军事）
- `WEALTH` — 财富排行（经济产出）
- `HONOR` — 荣耀排行（战斗经验）

**rankingCategory 选项：**
- `BY_PLAYERS` — 所有玩家排行
- `BY_ALLIANCE` — 联盟排行
- `IN_ALLIANCE` — 联盟内部成员排行

**offset 选项：**
- `top` — 从第一名开始
- `me` — 以自己为中心
- `bottom` — 从末尾开始
- 数字 — 从指定位置开始

**searchType 选项**（按条件搜索）：
- `SEARCH_BY_NAME` + `searchParam:"玩家名"` — 搜索特定玩家
- `SEARCH_BY_ALLIANCE` + `searchParam:"联盟名"` — 搜索联盟成员

返回每个玩家的：`id`、`playerName`、`position`（排名）、`score`（分数）、`allianceName`（联盟）。

**用法：** 先查 `offset: "top"` 了解服务器顶尖玩家实力，再查 `offset: "me"` 找到自己附近的竞争对手。

### 途径三：联盟视图（ViewAllianceFrame）

如果知道某个联盟的 ID，可以查看其成员列表：

```json
{"type":"getContent","params":{"elParamList":[{
  "elementType":"ViewAllianceFrame",
  "elementId": 5
}]}}
```

返回联盟详情和成员列表。联盟 ID 可以从排行榜（BY_ALLIANCE）或世界地图获取。

### 综合定位策略

1. **排行榜发现** → 找到活跃玩家的名字和实力
2. **世界地图定位** → 找到目标玩家城市的坐标和 regionId
3. **侦察确认** → 用 HERO_SCOUT_CITY 获取详细防御信息
4. **决策** → 根据实力对比决定掠夺/进攻/结盟

## 侦察 (Scouting)

PvP 前**必须先侦察**。

### 侦察操作

**侦察部队**（查看守军/行军中部队）：
```json
{"type": "addAction", "params": {
  "actionType": "HERO_SCOUT_TROOPS",
  "actorType": "Hero",
  "actorId": 40,
  "actionParams": "<目标英雄ID>"
}}
```

**侦察城市**（查看城内全貌）：
```json
{"type": "addAction", "params": {
  "actionType": "HERO_SCOUT_CITY",
  "actorType": "Hero",
  "actorId": 40,
  "actionParams": "<目标区域ID>"
}}
```

**侦察区域**（查看区域内所有部署）：
```json
{"type": "addAction", "params": {
  "actionType": "HERO_SCOUT_REGION",
  "actorType": "Hero",
  "actorId": 40,
  "actionParams": "<目标区域ID>"
}}
```

### 侦察等级与信息

侦察结果取决于侦察等级（由英雄游侠技能决定）vs 对方反侦察能力（野蛮人技能）：

| 等级 | 可看到的信息 |
|------|-------------|
| Lv1 | 防守部队（待命兵团） |
| Lv2 | 城内所有部队、英雄训练类型 |
| Lv3 | 城防建筑类型、城防加成值、巡逻英雄 |
| Lv4+ | 英雄训练详情 |
| Lv5+ | 英雄职业 |
| Lv7 | 完整信息 |

### 侦察风险

侦察可能被对方发现，后果取决于侦察质量：
- **未被发现**：最佳结果
- **被发现**：对方收到通知但无其他影响
- **英雄受伤**：侦察失败，英雄受伤需要恢复时间
- **英雄被俘**：侦察严重失败 + 对方有野蛮人职业

## 掠夺 (Pillage)

掠夺是最常见的 PvP 行为，抢夺对方矿区的资源。

### 操作
```json
{"type": "addAction", "params": {
  "actionType": "HERO_PILLAGE_ZONE",
  "actorType": "Hero",
  "actorId": 40,
  "actionParams": "<zoneId>;1"
}}
```

### 掠夺机制
- 目标：其他玩家已占领的矿区Zone
- **巡逻英雄防守**：如果目标城市有英雄设置了巡逻(SET_PATROL)，掠夺会触发与巡逻英雄的战斗
- **无巡逻 = 无战斗**：如果没有巡逻英雄，掠夺直接成功，不需要战斗
- 掠夺量取决于军队战力和英雄掠夺技能
- 被掠夺的矿产会暂停产出一段时间（矿产损伤）

### 防守掠夺
- 给强力英雄设置巡逻：`{"type": "heroAction", "params": {"action": "SET_PATROL", "heroId": 40}}`
- 建造防御型野外建筑
- 学习掠夺防御技能

## 进攻 (Attack Region)

直接攻击敌方城市。

### 操作
```json
{"type": "addAction", "params": {
  "actionType": "HERO_ATTACK_REGION",
  "actorType": "Hero",
  "actorId": 40,
  "actionParamsJSON": {"tRI": <目标区域ID>}
}}
```

**重要限制**：
- 目标城市如果处于联盟影响下（`influenceAllianceId` 非空），直接攻击会失败，报错：`SINGLE_ELEMENT_INVALID_CONDITION_SEVERAL_RESULTS`
- 解决方法：**用 HERO_SIEGE_REGION 代替 HERO_ATTACK_REGION** — 围城不需要英雄先移动到目标旁边！

**攻击被联盟覆盖的目标正确流程**：
1. `HERO_SIEGE_REGION` — 建立围城（无需英雄在目标旁边）
2. 等待围城完成（约10-15分钟）
3. `HERO_SIEGE_ASSAULT` — 发起攻城

⚠️ 注意：攻城时英雄必须在目标城市旁边，不能远程攻城。

### ⚠️ 绕过限制：围城(SIEGE)可以直接发起！

**经验发现**：`HERO_SIEGE_REGION` 不需要英雄先移动到目标附近，可以直接对目标城市发起围城！

当英雄无法移动到目标附近时（所有相邻格子都被联盟影响），用 **围城代替进攻**：
```json
{"type": "addAction", "params": {
  "actionType": "HERO_SIEGE_REGION",
  "actorType": "Hero",
  "actorId": 40,
  "actionParams": "<目标区域ID>"
}}
```

流程：围城(12分钟) → 攻城(SIEGE_ASSAULT)

### 进攻规则
- 城防建筑大幅增加防守方战力
- 不能攻击联盟成员
- 不能攻击新手保护期内的玩家
- 防守方所有城内部队 + 非行动中英雄的部队都参与防守
- 按防守方英雄防御力计算加成

## 围城 (Siege)

围城是占领敌方城市的完整流程。

### 围城操作

**建立围城**：
```json
{"type": "addAction", "params": {
  "actionType": "HERO_SIEGE_REGION",
  "actorType": "Hero", "actorId": 40,
  "actionParams": "<目标区域ID>"
}}
```

**轰炸**（削弱城防，需 T8 弩车）：
```json
{"type": "addAction", "params": {
  "actionType": "HERO_SIEGE_BOMBARD",
  "actorType": "Hero", "actorId": 40,
  "actionParams": "<目标区域ID>"
}}
```

**攻城**（总攻，成功则占领）：
```json
{"type": "addAction", "params": {
  "actionType": "HERO_SIEGE_ASSAULT",
  "actorType": "Hero", "actorId": 40,
  "actionParams": "<目标区域ID>"
}}
```

**从外部解围**（盟友从城外打破围城）：
```json
{"type": "addAction", "params": {
  "actionType": "HERO_SIEGE_BREAK",
  "actorType": "Hero", "actorId": 40,
  "actionParams": "<目标区域ID>"
}}
```

**从城内突围**（守方从城内打破围城）：
```json
{"type": "addAction", "params": {
  "actionType": "HERO_SIEGE_BREAK_FROM_INSIDE",
  "actorType": "Hero", "actorId": 40,
  "actionParams": "<目标区域ID>"
}}
```

**增援被围城市**：
```json
{"type": "addAction", "params": {
  "actionType": "HERO_SIEGE_REINFORCE",
  "actorType": "Hero", "actorId": 40,
  "actionParams": "<目标区域ID>"
}}
```

### 围城阶段

1. **建立围城** `HERO_SIEGE_REGION`：英雄前往目标城市建立围城态势
2. **轰炸** `HERO_SIEGE_BOMBARD`：使用 T8 弩车轰炸，削弱城防
3. **攻城** `HERO_SIEGE_ASSAULT`：发起总攻，成功则占领城市
4. **解围** `HERO_SIEGE_BREAK`/`HERO_SIEGE_BREAK_FROM_INSIDE`：从外部或城内打破围城
5. **增援** `HERO_SIEGE_REINFORCE`：增援被围城市

### 围城注意事项
- 需要 T8 弩车才能有效轰炸
- 轰炸消耗弩车但削弱城防
- 城防降到足够低后再攻城
- 被围城方的行动受限（部分操作无法执行）
- 盟友可以解围或增援

## 拦截行军 (Attack Halt)

拦截正在行军中的敌方英雄。

```json
{"type": "addAction", "params": {
  "actionType": "HERO_ATTACK_HALT",
  "actorType": "Hero",
  "actorId": 40,
  "actionParams": "<目标区域ID>"
}}
```

- 目标必须是正在行军途中的敌方英雄
- 拦截成功后触发野外战斗（无城防加成）
- 适合在敌方远征时打伏击

## 攻击区域建筑 (Attack Region Building)

攻击敌方的区域建筑（如符文要塞等）。

```json
{"type": "addAction", "params": {
  "actionType": "HERO_ATTACK_REGIONBUILDING",
  "actorType": "Hero",
  "actorId": 40,
  "actionParams": "<regionBuildingId>"
}}
```

- 区域建筑有自己的守军和防御配置
- 符文要塞有多层楼防御，需要逐层攻破
- 攻占后可获得建筑控制权

## 英雄俘虏

### 被俘条件
- 侦察严重失败 + 防守方英雄有野蛮人(BARBARIAN)职业
- 俘虏是较罕见的事件

### 被俘状态
- 英雄无法执行任何操作
- `captured_regionId` 被设置为俘虏所在区域
- 部队不跟随（可能在原区域）

### 释放方式
- `HERO_RELEASE`：自动释放（需要等待时间）
- 俘虏所在区域控制权变化时自动释放
- 可使用道具加速释放

## 英雄受伤

### 受伤条件
- 侦察失败（对方没有野蛮人职业时）
- 部分战斗结果也可能导致受伤

### 受伤影响
- 英雄无法行动，需要恢复时间
- 恢复时间受世界速度影响
- 可使用道具即时治疗

## 新手保护

- 注册后一段时间内自动获得保护
- 保护期间：不会被攻击、掠夺、围城
- 新手玩家可以主动攻击别人（不受影响）
- 保护到期后自动解除
- 也可以通过道具获得额外保护

## PvP 战斗中的城防加成

| 战斗类型 | 城防建筑效果 | 掠夺防御效果 | 说明 |
|----------|-------------|-------------|------|
| 掠夺 (Pillage) | 不生效 | 生效 | 掠夺防御是独立的加成 |
| 进攻 (Attack) | 生效 | 不生效 | 城防百分比增加所有防守兵团战力 |
| 攻城 (Siege Assault) | 生效 | 不生效 | 同进攻，但可以通过轰炸削弱 |
| NPC 战斗 | 不生效 | 不生效 | NPC 没有城防 |

## PvP 策略

- 先侦察，了解对方实力
- 分析对方兵种组成，准备克制部队
- 考虑城防加成后的实际战力比
- 多路同时进攻（多个英雄从不同方向）
- 掠夺经济骚扰比直接攻城更安全
- 注意宵禁（23:00后不能军事行动）
