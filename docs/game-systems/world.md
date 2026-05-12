# 世界构建系统

## 概述

世界构建系统为互动小说游戏提供场景管理、地图导航、环境交互等功能，帮助创建丰富多样的游戏世界�?
## 核心概念

### 场景 (Scene)

```javascript
{
  id: "scene_001",
  name: "村庄入口",
  description: "你站在村庄的入口处，几栋茅草屋散落在道路两旁�?,
  
  // 区域信息
  region: "新手�?,
  coordinates: { x: 0, y: 0 },
  
  // 环境属�?  environment: {
    type: "outdoor",      // "outdoor" | "indoor" | "dungeon"
    lighting: "day",      // "day" | "night" | "dark"
    weather: "sunny",     // "sunny" | "rainy" | "foggy"
    danger: "safe"        // "safe" | "caution" | "dangerous"
  },
  
  // 可交互对�?  objects: [
    {
      id: "well",
      name: "水井",
      description: "一口古老的水井",
      interactable: true,
      onInteract: (state) => { }
    }
  ],
  
  // NPC
  npcs: ["npc_village_head", "npc_merchant"],
  
  // 出口
  exits: {
    north: { target: "scene_002", condition: null },
    south: { target: "scene_003", condition: (state) => state.flags.hasKey }
  },
  
  // 事件
  onEnter: (state) => { },
  onExit: (state) => { },
  onStay: (state) => { }  // 每回合触�?}
```

### 区域 (Region)

```javascript
{
  id: "region_001",
  name: "新手�?,
  description: "一个宁静的小村庄，适合初学者冒险�?,
  
  // 区域属�?  level: "1-5",
  danger: "low",
  
  // 包含的场�?  scenes: ["scene_001", "scene_002", "scene_003"],
  
  // 区域效果
  effects: {
    healthRegen: 1,    // 每秒恢复1点生�?    manaRegen: 1       // 每秒恢复1点魔�?  }
}
```

### 世界地图 (WorldMap)

```javascript
{
  regions: {
    "region_001": { /* 新手�?*/ },
    "region_002": { /* 黑暗森林 */ },
    "region_003": { /* 王都 */ }
  },
  
  connections: [
    { from: "region_001", to: "region_002", requirement: "level >= 5" },
    { from: "region_001", to: "region_003", requirement: "quest_001_completed" }
  ]
}
```

## 使用方法

### 1. 定义场景

```javascript
const scenes = {
  "village_entrance": {
    id: "village_entrance",
    name: "村庄入口",
    description: "你站在村庄的入口处，几栋茅草屋散落在道路两旁。村口有一棵巨大的橡树�?,
    region: "newbie_village",
    coordinates: { x: 0, y: 0 },
    
    environment: {
      type: "outdoor",
      lighting: "day",
      weather: "sunny",
      danger: "safe"
    },
    
    objects: [
      {
        id: "oak_tree",
        name: "大橡�?,
        description: "一棵需要数人合抱的古老橡�?,
        interactable: true,
        onInteract: (state) => {
          console.log("你在树下发现了一枚闪闪发光的硬币�?);
          state.inventory.addGold(1);
        }
      },
      {
        id: "notice_board",
        name: "公告�?,
        description: "上面贴着各种告示",
        interactable: true,
        onInteract: (state) => {
          console.log("公告板内容：");
          console.log("1. 招募冒险者清理北方森林的哥布�?);
          console.log("2. 寻找失踪的村长的女儿");
        }
      }
    ],
    
    npcs: ["village_guard"],
    
    exits: {
      north: { target: "village_square", condition: null },
      east: { target: "village_merchant", condition: null },
      south: { target: "wilderness", condition: null }
    },
    
    onEnter: (state) => {
      if (!state.flags.visitedVillage) {
        console.log("第一次来到村庄，你感到一阵宁静�?);
        state.flags.visitedVillage = true;
      }
    }
  },
  
  "village_square": {
    id: "village_square",
    name: "村庄广场",
    description: "村庄的中心广场，村民们在这里聚集交流。广场中央有一座喷泉�?,
    region: "newbie_village",
    coordinates: { x: 0, y: 1 },
    
    environment: {
      type: "outdoor",
      lighting: "day",
      weather: "sunny",
      danger: "safe"
    },
    
    objects: [
      {
        id: "fountain",
        name: "喷泉",
        description: "清澈的泉水从石雕中流�?,
        interactable: true,
        onInteract: (state) => {
          console.log("你喝了口泉水，感到精神焕发！");
          state.player.health = Math.min(state.player.maxHealth, state.player.health + 10);
        }
      }
    ],
    
    npcs: ["village_head", "village_elder"],
    
    exits: {
      south: { target: "village_entrance", condition: null },
      north: { target: "village_church", condition: null }
    }
  },
  
  "dark_forest": {
    id: "dark_forest",
    name: "黑暗森林",
    description: "茂密的树林遮挡了阳光，四周一片昏暗。你听到了奇怪的声音...",
    region: "dark_forest_region",
    coordinates: { x: 5, y: 3 },
    
    environment: {
      type: "outdoor",
      lighting: "dark",
      weather: "foggy",
      danger: "dangerous"
    },
    
    objects: [
      {
        id: "mysterious_cave",
        name: "神秘洞穴",
        description: "一个黑漆漆的洞穴入�?,
        interactable: true,
        onInteract: (state) => {
          if (state.inventory.hasItem("torch")) {
            return { nextScene: "cave_entrance" };
          } else {
            console.log("太黑了，你需要火把才能进入�?);
          }
        }
      }
    ],
    
    npcs: [],
    
    exits: {
      south: { target: "wilderness", condition: null },
      east: { target: "forest_deep", condition: null }
    },
    
    onEnter: (state) => {
      // 随机遭遇敌人
      if (Math.random() < 0.3) {
        console.log("一只哥布林从树后跳了出来！");
        state.triggerCombat = true;
        state.enemy = "goblin";
      }
    },
    
    onStay: (state) => {
      // 在危险区域每回合可能遭遇
      if (Math.random() < 0.1) {
        console.log("你感觉到有东西在靠近...");
      }
    }
  }
};
```

### 2. 初始化世界构建系�?
```javascript
const world = new WorldBuilder(gameState);
```

### 3. 加载场景

```javascript
// 加载所有场�?world.loadScenes(scenes);

// 加载区域
world.loadRegions(regions);
```

### 4. 场景导航

```javascript
// 获取当前场景
const currentScene = world.getCurrentScene();

// 获取场景信息
const sceneInfo = world.getSceneInfo("village_entrance");

// 移动到其他场�?const result = world.moveTo("north");
// result: { success: true, scene: sceneObject } �?{ success: false, reason: "条件不满�? }

// 直接传送到场景
world.teleportTo("dark_forest");
```

### 5. 环境交互

```javascript
// 获取场景中的可交互对�?const objects = world.getInteractableObjects();

// 与对象交�?world.interactWith("oak_tree");

// 获取场景中的NPC
const npcs = world.getNPCs();

// 获取可用出口
const exits = world.getAvailableExits();
```

### 6. 环境状�?
```javascript
// 获取当前环境
const environment = world.getEnvironment();

// 检查是否可以在当前环境执行某操�?const canRest = world.canRest();  // 在安全区域可以休�?
// 获取区域信息
const region = world.getCurrentRegion();
```

## 动态场�?
### 时间变化

```javascript
{
  id: "village_night",
  condition: (state) => state.gameTime.hour >= 20 || state.gameTime.hour < 6,
  description: "夜晚的村庄格外宁静，只有几户人家还亮着灯�?,
  npcs: ["night_watch"],  // 夜晚特有的NPC
  exits: {
    // 夜晚某些出口可能关闭
    north: { target: "village_square", condition: null, closed: true }
  }
}
```

### 天气系统

```javascript
// 在场景中根据天气改变描述
{
  id: "village_rainy",
  condition: (state) => state.weather === "rainy",
  description: "雨水打湿了村庄的街道，村民们纷纷躲进了屋内�?,
  effects: {
    movementSpeed: 0.8  // 移动速度降低
  }
}
```

## 地图系统

```javascript
// 获取区域地图
const map = world.getRegionMap("newbie_village");

// 显示当前位置
const position = world.getCurrentPosition();
// position: { region: "newbie_village", scene: "village_entrance", x: 0, y: 0 }

// 计算路径
const path = world.findPath("village_entrance", "dark_forest");
// path: ["village_entrance", "wilderness", "dark_forest"]

// 获取相邻场景
const neighbors = world.getNeighborScenes();
```

## 事件系统

```javascript
world.on("sceneEnter", (scene, fromScene) => {
  console.log(`进入场景: ${scene.name}`);
});

world.on("sceneExit", (scene, toScene) => {
  console.log(`离开场景: ${scene.name}`);
});

world.on("objectInteract", (object, scene) => {
  console.log(`�?${object.name} 交互`);
});

world.on("environmentChange", (oldEnv, newEnv) => {
  console.log(`环境变化: ${oldEnv.weather} -> ${newEnv.weather}`);
});
```

## 与游戏引擎集�?
```javascript
// 初始化游戏时加载世界
const game = new GameEngine(config);
const world = new WorldBuilder(game.state);

world.loadScenes(scenes);
world.loadRegions(regions);

// 设置初始场景
world.setCurrentScene("village_entrance");

// 游戏主循�?game.on("turn", () => {
  const scene = world.getCurrentScene();
  
  // 显示场景描述
  console.log(scene.description);
  
  // 显示可交互对�?  const objects = world.getInteractableObjects();
  objects.forEach((obj, index) => {
    console.log(`${index + 1}. [查看] ${obj.name}`);
  });
  
  // 显示出口
  const exits = world.getAvailableExits();
  Object.keys(exits).forEach(direction => {
    console.log(`[前往${direction}]`);
  });
});
```

## 快速旅�?
```javascript
// 解锁快速旅行点
world.unlockFastTravel("village_entrance");

// 获取已解锁的快速旅行点
const travelPoints = world.getUnlockedFastTravelPoints();

// 快速旅�?world.fastTravel("village_entrance");
```

## 探索度系�?
```javascript
// 记录探索进度
world.discoverScene("secret_cave");

// 获取区域探索�?const exploration = world.getExplorationRate("newbie_village");
// exploration: { discovered: 5, total: 10, rate: 0.5 }

// 获取探索奖励
if (exploration.rate >= 1.0) {
  console.log("恭喜！你完全探索了新手村�?);
  game.giveReward("exploration_bonus");
}
```

## API 参�?
### WorldBuilder �?
#### 构造函�?```javascript
new WorldBuilder(gameState)
```

#### 方法

| 方法 | 参数 | 返回�?| 说明 |
|------|------|--------|------|
| `loadScenes(scenes)` | scenes: Object | void | 加载场景数据 |
| `loadRegions(regions)` | regions: Object | void | 加载区域数据 |
| `getCurrentScene()` | - | Object | 获取当前场景 |
| `setCurrentScene(sceneId)` | sceneId: string | void | 设置当前场景 |
| `getSceneInfo(sceneId)` | sceneId: string | Object | 获取场景信息 |
| `moveTo(direction)` | direction: string | Object | 向指定方向移�?|
| `teleportTo(sceneId)` | sceneId: string | Object | 传送到场景 |
| `getInteractableObjects()` | - | Array | 获取可交互对�?|
| `interactWith(objectId)` | objectId: string | Object | 与对象交�?|
| `getNPCs()` | - | Array | 获取场景NPC |
| `getAvailableExits()` | - | Object | 获取可用出口 |
| `getEnvironment()` | - | Object | 获取环境状�?|
| `getCurrentRegion()` | - | Object | 获取当前区域 |
| `getRegionMap(regionId)` | regionId: string | Object | 获取区域地图 |
| `getCurrentPosition()` | - | Object | 获取当前位置 |
| `findPath(from, to)` | from: string, to: string | Array | 查找路径 |
| `getNeighborScenes()` | - | Array | 获取相邻场景 |
| `unlockFastTravel(sceneId)` | sceneId: string | void | 解锁快速旅行点 |
| `getUnlockedFastTravelPoints()` | - | Array | 获取已解锁旅行点 |
| `fastTravel(sceneId)` | sceneId: string | Object | 快速旅�?|
| `discoverScene(sceneId)` | sceneId: string | void | 标记场景已发�?|
| `getExplorationRate(regionId)` | regionId: string | Object | 获取探索�?|
| `on(event, callback)` | event: string, callback: Function | void | 注册事件监听 |
