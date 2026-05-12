# 战斗系统

## 概述

战斗系统为互动小说游戏提供回合制战斗功能，支持玩家与敌人之间的战斗交互�?
## 核心概念

### 战斗单位 (CombatUnit)

```javascript
{
  id: "enemy_001",
  name: "哥布�?,
  type: "enemy",  // "player" | "enemy" | "npc"
  
  // 基础属�?  health: 50,
  maxHealth: 50,
  attack: 8,
  defense: 3,
  speed: 5,
  
  // 技�?  skills: [
    {
      name: "普通攻�?,
      damage: 10,
      cooldown: 0
    }
  ],
  
  // 战利�?  loot: [
    { itemId: "gold_coin", chance: 0.8, min: 5, max: 15 }
  ]
}
```

### 战斗状�?(BattleState)

```javascript
{
  isActive: true,
  turn: 1,
  currentTurnUnit: "player",
  units: [
    { /* 玩家数据 */ },
    { /* 敌人数据 */ }
  ],
  log: [],  // 战斗日志
  result: null  // "win" | "lose" | "escape"
}
```

## 使用方法

### 1. 定义敌人

```javascript
const enemies = {
  "goblin": {
    id: "goblin",
    name: "哥布�?,
    health: 50,
    maxHealth: 50,
    attack: 8,
    defense: 3,
    speed: 5,
    experience: 20,
    loot: [
      { itemId: "gold_coin", chance: 0.8, min: 5, max: 15 },
      { itemId: "rusty_dagger", chance: 0.2 }
    ]
  },
  
  "orc": {
    id: "orc",
    name: "兽人战士",
    health: 100,
    maxHealth: 100,
    attack: 15,
    defense: 8,
    speed: 3,
    experience: 50,
    loot: [
      { itemId: "gold_coin", chance: 1.0, min: 20, max: 40 },
      { itemId: "iron_sword", chance: 0.3 }
    ]
  }
};
```

### 2. 初始化战斗系�?
```javascript
const combat = new CombatSystem(gameState);
```

### 3. 开始战�?
```javascript
// 开始与哥布林的战斗
combat.startBattle(enemies.goblin);

// 或者开始与多个敌人的战�?combat.startBattle([enemies.goblin, enemies.goblin]);
```

### 4. 执行战斗动作

```javascript
// 普通攻�?combat.attack(targetId);

// 使用技�?combat.useSkill(skillId, targetId);

// 使用物品
combat.useItem(itemId, targetId);

// 逃跑
combat.escape();
```

### 5. 获取战斗信息

```javascript
// 获取当前状�?const state = combat.getState();

// 获取战斗日志
const log = combat.getLog();

// 检查战斗是否结�?const isEnded = combat.isEnded();

// 获取战斗结果
const result = combat.getResult();  // "win" | "lose" | "escape"
```

## 战斗流程

```
开始战�?    �?    �?计算行动顺序（根据速度�?    �?    �?玩家回合 ◄───────────────────�?    �?                       �?    �?                       �?显示可选动�?                 �?    �?                       �?    �?                       �?执行动作（攻�?技�?物品/逃跑�?�?    �?                       �?    �?                       �?检查战斗结束？ ──是──�?结束战斗
    �?�?                    �?    �?                       �?敌人回合 ────────────────────�?    �?    �?AI选择动作
    �?    �?执行动作
    �?    �?检查战斗结束？ ──是──�?结束战斗
    �?�?    �?下一回合
```

## 伤害计算

```javascript
// 基础伤害公式
damage = max(1, attacker.attack - target.defense);

// 暴击判定
if (random() < critChance) {
  damage *= critMultiplier;  // 通常 1.5x �?2x
}

// 最终伤�?damage = floor(damage * randomRange(0.9, 1.1));  // ±10% 浮动
```

## 战斗AI

敌人AI的行为模式：

```javascript
const AI_BEHAVIORS = {
  // 攻击性：总是攻击
  aggressive: (unit, battleState) => {
    return { action: "attack", target: "player" };
  },
  
  // 防御性：低血量时防御
  defensive: (unit, battleState) => {
    if (unit.health / unit.maxHealth < 0.3) {
      return { action: "defend" };
    }
    return { action: "attack", target: "player" };
  },
  
  // 随机性：随机选择动作
  random: (unit, battleState) => {
    const actions = ["attack", "skill", "defend"];
    return { action: randomChoice(actions) };
  }
};
```

## 事件回调

```javascript
combat.on("turnStart", (unit) => {
  console.log(`${unit.name} 的回合开始`);
});

combat.on("damage", (attacker, target, damage) => {
  console.log(`${attacker.name} �?${target.name} 造成 ${damage} 点伤害`);
});

combat.on("battleEnd", (result, rewards) => {
  if (result === "win") {
    console.log("战斗胜利�?);
    console.log(`获得 ${rewards.experience} 经验值`);
    console.log(`获得物品:`, rewards.loot);
  }
});
```

## 与游戏引擎集�?
```javascript
// 在场景中触发战斗
const scene = {
  description: "一只哥布林挡住了你的去路！",
  onEnter: (state) => {
    const combat = new CombatSystem(state);
    combat.startBattle(enemies.goblin);
    
    combat.on("battleEnd", (result, rewards) => {
      if (result === "win") {
        // 战斗胜利，继续剧�?        state.flags.defeatedGoblin = true;
        return { nextScene: "forest_path" };
      } else {
        // 战斗失败，游戏结�?        return { nextScene: "game_over" };
      }
    });
  }
};
```

## API 参�?
### CombatSystem �?
#### 构造函�?```javascript
new CombatSystem(gameState)
```

#### 方法

| 方法 | 参数 | 返回�?| 说明 |
|------|------|--------|------|
| `startBattle(enemy)` | enemy: Object/Array | void | 开始战�?|
| `attack(targetId)` | targetId: string | Object | 普通攻�?|
| `useSkill(skillId, targetId)` | skillId: string, targetId: string | Object | 使用技�?|
| `useItem(itemId, targetId)` | itemId: string, targetId: string | Object | 使用物品 |
| `escape()` | - | boolean | 尝试逃跑 |
| `getState()` | - | Object | 获取战斗状�?|
| `getLog()` | - | Array | 获取战斗日志 |
| `isEnded()` | - | boolean | 检查战斗是否结�?|
| `getResult()` | - | string | 获取战斗结果 |
| `on(event, callback)` | event: string, callback: Function | void | 注册事件监听 |
