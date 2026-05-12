# 游戏引擎核心

## 概述

本游戏引擎是一个基于文档的互动小说游戏框架，采用模块化设计，支持战斗、对话、背包和世界构建等核心功能�?

## 系统架构

```
┌─────────────────────────────────────�?
�?          游戏引擎核心               �?
├─────────────────────────────────────�?
�? 状态管�? �? 事件系统  �? 存档系统   �?
└────┬────────┴─────┬──────┴────┬──────�?
     �?             �?          �?
┌────▼────�?   ┌────▼────�? ┌───▼────�?
�?战斗系统 �?   �?对话系统 �? │背包系统│
└─────────�?   └─────────�? └────────�?
     �?             �?          �?
     └──────────────┼───────────�?
                    �?
              ┌─────▼─────�?
              �?世界构建   �?
              └───────────�?
```

## 核心概念

### 1. 游戏状�?(GameState)
游戏运行时的所有数据都存储在状态对象中�?

```javascript
{
  player: {
    name: "玩家名称",
    health: 100,
    maxHealth: 100,
    level: 1,
    experience: 0,
    attributes: {
      strength: 10,
      agility: 10,
      intelligence: 10
    }
  },
  currentScene: "scene_001",
  inventory: [],
  flags: {},           // 剧情标记
  visitedScenes: []    // 已访问场�?
}
```

### 2. 场景 (Scene)
游戏的基本单位，包含�?
- 场景描述文本
- 可选动作列�?
- 条件判断
- 场景跳转

### 3. 事件系统
处理游戏中的各种触发事件�?
- 进入场景事件
- 对话选择事件
- 战斗结果事件
- 物品获取事件

## 使用方法

### 步骤1: 定义游戏配置

```javascript
const gameConfig = {
  title: "我的冒险故事",
  initialScene: "start",
  player: {
    initialHealth: 100,
    initialAttributes: {
      strength: 10,
      agility: 10,
      intelligence: 10
    }
  }
};
```

### 步骤2: 创建场景

```javascript
const scenes = {
  "start": {
    description: "你站在一个十字路口。东边是一片森林，西边是一座小镇�?,
    choices: [
      {
        text: "前往森林",
        nextScene: "forest",
        condition: null
      },
      {
        text: "前往小镇",
        nextScene: "town",
        condition: null
      }
    ]
  },
  
  "forest": {
    description: "森林里光线昏暗，你听到了奇怪的声音...",
    choices: [
      {
        text: "探索深处",
        nextScene: "forest_deep",
        condition: null
      },
      {
        text: "返回路口",
        nextScene: "start",
        condition: null
      }
    ],
    onEnter: (state) => {
      // 进入场景时的处理
      console.log("你进入了森林");
    }
  }
};
```

### 步骤3: 初始化游�?

```javascript
// 创建游戏实例
const game = new GameEngine(gameConfig);

// 加载场景
game.loadScenes(scenes);

// 开始游�?
game.start();
```

### 步骤4: 处理玩家输入

```javascript
// 显示当前场景
game.displayCurrentScene();

// 处理选择
game.makeChoice(choiceIndex);

// 保存游戏
game.save();

// 加载游戏
game.load(saveData);
```

## API 参�?

### GameEngine �?

#### 构造函�?
```javascript
new GameEngine(config)
```

#### 方法

| 方法 | 参数 | 说明 |
|------|------|------|
| `start()` | - | 开始游�?|
| `loadScenes(scenes)` | scenes: Object | 加载场景数据 |
| `displayCurrentScene()` | - | 显示当前场景 |
| `makeChoice(index)` | index: number | 执行选择 |
| `save()` | - | 保存游戏状�?|
| `load(saveData)` | saveData: Object | 加载游戏状�?|
| `getState()` | - | 获取当前状�?|
| `setState(newState)` | newState: Object | 设置状�?|

## 与其他系统的集成

### 集成战斗系统
```javascript
// 在场景中触发战斗
{
  onEnter: (state) => {
    const combat = new CombatSystem(state);
    combat.startBattle(enemy);
  }
}
```

### 集成对话系统
```javascript
// 在场景中启动对话
{
  onEnter: (state) => {
    const dialog = new DialogSystem(state);
    dialog.startDialog(npc);
  }
}
```

### 集成背包系统
```javascript
// 在场景中获取物品
{
  onEnter: (state) => {
    const inventory = new InventorySystem(state);
    inventory.addItem(item);
  }
}
```

## 存档格式

```javascript
{
  version: "1.0",
  timestamp: "2026-01-01T00:00:00Z",
  state: {
    player: { ... },
    currentScene: "scene_id",
    inventory: [ ... ],
    flags: { ... }
  }
}
```

## 扩展开�?

如需添加新功能，可以�?
1. �?`skills/` 目录下创建新的子系统
2. 继承 `GameEngine` 类进行扩�?
3. 通过事件系统与其他模块通信
