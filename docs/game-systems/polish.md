# 背包系统

## 概述

背包系统为互动小说游戏提供物品管理功能，支持物品的获取、使用、丢弃、装备等操作�?
## 核心概念

### 物品 (Item)

```javascript
{
  id: "item_001",
  name: "生命药水",
  description: "恢复50点生命�?,
  type: "consumable",  // "consumable" | "equipment" | "material" | "quest"
  icon: "potion_red.png",
  
  // 堆叠信息
  stackable: true,
  maxStack: 99,
  
  // 使用效果（消耗品�?  effects: [
    { type: "heal", value: 50 }
  ],
  
  // 装备属性（装备�?  equipment: {
    slot: "weapon",  // "weapon" | "armor" | "accessory"
    attack: 10,
    defense: 0
  },
  
  // 价�?  value: 100,  // 金币价�?  
  // 使用条件
  usable: true,
  usableIn: ["field", "battle"]  // 可用场景
}
```

### 背包格子 (InventorySlot)

```javascript
{
  itemId: "item_001",
  count: 5,
  equipped: false  // 是否已装�?}
```

### 背包状�?(InventoryState)

```javascript
{
  maxSlots: 50,        // 最大格子数
  gold: 1000,          // 金币
  items: [
    { itemId: "item_001", count: 5 },
    { itemId: "item_002", count: 1, equipped: true }
  ],
  equipped: {
    weapon: "item_002",
    armor: null,
    accessory: null
  }
}
```

## 使用方法

### 1. 定义物品

```javascript
const items = {
  "health_potion": {
    id: "health_potion",
    name: "生命药水",
    description: "恢复50点生命�?,
    type: "consumable",
    stackable: true,
    maxStack: 99,
    effects: [
      { type: "heal", value: 50 }
    ],
    value: 50,
    usable: true,
    usableIn: ["field", "battle"]
  },
  
  "iron_sword": {
    id: "iron_sword",
    name: "铁剑",
    description: "一把普通的铁剑",
    type: "equipment",
    stackable: false,
    equipment: {
      slot: "weapon",
      attack: 15,
      defense: 0
    },
    value: 200,
    usable: false
  },
  
  "leather_armor": {
    id: "leather_armor",
    name: "皮甲",
    description: "轻便的皮制护�?,
    type: "equipment",
    stackable: false,
    equipment: {
      slot: "armor",
      attack: 0,
      defense: 10
    },
    value: 150,
    usable: false
  },
  
  "magic_crystal": {
    id: "magic_crystal",
    name: "魔法水晶",
    description: "散发着神秘光芒的水�?,
    type: "material",
    stackable: true,
    maxStack: 999,
    value: 500,
    usable: false
  },
  
  "ancient_key": {
    id: "ancient_key",
    name: "古老的钥匙",
    description: "看起来能打开某扇�?,
    type: "quest",
    stackable: false,
    value: 0,
    usable: false
  }
};
```

### 2. 初始化背包系�?
```javascript
const inventory = new InventorySystem(gameState);
```

### 3. 添加物品

```javascript
// 添加单个物品
inventory.addItem("health_potion", 1);

// 添加多个物品
inventory.addItem("health_potion", 5);

// 添加物品（自动处理堆叠）
inventory.addItem("magic_crystal", 10);
```

### 4. 移除物品

```javascript
// 移除指定数量的物�?inventory.removeItem("health_potion", 2);

// 移除全部
inventory.removeItem("health_potion", 999);

// 丢弃物品
inventory.dropItem("health_potion", 1);
```

### 5. 使用物品

```javascript
// 使用消耗品
const result = inventory.useItem("health_potion");
// result: { success: true, effects: [{ type: "heal", value: 50 }] }

// 使用失败（条件不满足�?const result2 = inventory.useItem("iron_sword");
// result2: { success: false, reason: "不可使用的物品类�? }
```

### 6. 装备管理

```javascript
// 装备物品
inventory.equipItem("iron_sword");

// 卸下装备
inventory.unequipItem("weapon");

// 获取当前装备
const equipped = inventory.getEquippedItems();
// equipped: { weapon: "iron_sword", armor: null, accessory: null }

// 计算装备属性加�?const bonus = inventory.getEquipmentBonus();
// bonus: { attack: 15, defense: 0 }
```

### 7. 查询物品

```javascript
// 获取物品数量
const count = inventory.getItemCount("health_potion");

// 检查是否有某物�?const hasItem = inventory.hasItem("ancient_key");

// 获取背包中所有物�?const allItems = inventory.getAllItems();

// 按类型筛选物�?const consumables = inventory.getItemsByType("consumable");

// 获取背包使用情况
const usage = inventory.getUsage();
// usage: { used: 5, max: 50, remaining: 45 }
```

### 8. 金币管理

```javascript
// 获得金币
inventory.addGold(100);

// 花费金币
const success = inventory.spendGold(50);
// success: true（金币足够）�?false（金币不足）

// 获取当前金币
const gold = inventory.getGold();
```

## 物品分类

### 消耗品 (Consumable)
- 药水、食物等一次性使用物�?- 可以堆叠
- 有使用效�?
### 装备 (Equipment)
- 武器、防具、饰�?- 不可堆叠
- 提供属性加�?- 可以装备/卸下

### 材料 (Material)
- 合成、制作用的材�?- 可以大量堆叠
- 通常不可直接使用

### 任务物品 (Quest)
- 剧情相关物品
- 不可堆叠
- 不可出售
- 特定条件下使�?
## 使用效果类型

```javascript
const EFFECT_TYPES = {
  // 恢复�?  heal: { target: "hp", value: 50 },           // 恢复生命�?  restore_mp: { target: "mp", value: 30 },     // 恢复魔法�?  
  // 增益�?  buff_attack: { stat: "attack", value: 10, duration: 300 },  // 攻击力提�?  buff_defense: { stat: "defense", value: 10, duration: 300 }, // 防御力提�?  
  // 特殊�?  teleport: { target: "last_town" },           // 传�?  identify: { target: "unknown_item" },        // 鉴定
  resurrect: { target: "dead_ally" }           // 复活
};
```

## 事件回调

```javascript
inventory.on("itemAdded", (itemId, count, total) => {
  console.log(`获得 ${items[itemId].name} x${count}`);
});

inventory.on("itemRemoved", (itemId, count, remaining) => {
  console.log(`失去 ${items[itemId].name} x${count}`);
});

inventory.on("itemUsed", (itemId, effects) => {
  console.log(`使用�?${items[itemId].name}`);
});

inventory.on("itemEquipped", (itemId, slot) => {
  console.log(`装备�?${items[itemId].name}`);
});

inventory.on("itemUnequipped", (itemId, slot) => {
  console.log(`卸下�?${items[itemId].name}`);
});

inventory.on("goldChanged", (oldAmount, newAmount) => {
  console.log(`金币: ${oldAmount} -> ${newAmount}`);
});

inventory.on("inventoryFull", (itemId, count) => {
  console.log("背包已满�?);
});
```

## 与游戏引擎集�?
```javascript
// 在场景中获取物品
const scene = {
  description: "你在宝箱中发现了一些物品�?,
  onEnter: (state) => {
    const inventory = new InventorySystem(state);
    
    // 添加物品
    const result = inventory.addItem("health_potion", 3);
    if (result.success) {
      console.log("获得�?瓶生命药水！");
    }
    
    // 检查关键物�?    if (inventory.hasItem("ancient_key")) {
      console.log("你使用古老的钥匙打开了隐藏的门�?);
    }
  }
};

// 在战斗中使用物品
const combat = {
  onPlayerTurn: (state) => {
    const inventory = new InventorySystem(state);
    const consumables = inventory.getItemsByType("consumable");
    
    // 显示可用消耗品
    consumables.forEach(item => {
      console.log(`[${item.name}] x${item.count}`);
    });
    
    // 使用物品
    inventory.useItem("health_potion");
  }
};
```

## 商店交易

```javascript
// 购买物品
inventory.buyItem("iron_sword", 1, shopPrice);

// 出售物品
inventory.sellItem("health_potion", 5, sellPrice);

// 批量出售
inventory.sellItems([
  { itemId: "rusty_dagger", count: 2 },
  { itemId: "old_boots", count: 1 }
]);
```

## 存档格式

```javascript
{
  maxSlots: 50,
  gold: 1250,
  items: [
    { itemId: "health_potion", count: 5 },
    { itemId: "iron_sword", count: 1, equipped: true },
    { itemId: "leather_armor", count: 1, equipped: true }
  ],
  equipped: {
    weapon: "iron_sword",
    armor: "leather_armor",
    accessory: null
  }
}
```

## API 参�?
### InventorySystem �?
#### 构造函�?```javascript
new InventorySystem(gameState)
```

#### 方法

| 方法 | 参数 | 返回�?| 说明 |
|------|------|--------|------|
| `addItem(itemId, count)` | itemId: string, count: number | Object | 添加物品 |
| `removeItem(itemId, count)` | itemId: string, count: number | Object | 移除物品 |
| `useItem(itemId)` | itemId: string | Object | 使用物品 |
| `equipItem(itemId)` | itemId: string | Object | 装备物品 |
| `unequipItem(slot)` | slot: string | Object | 卸下装备 |
| `dropItem(itemId, count)` | itemId: string, count: number | Object | 丢弃物品 |
| `hasItem(itemId)` | itemId: string | boolean | 检查是否有物品 |
| `getItemCount(itemId)` | itemId: string | number | 获取物品数量 |
| `getAllItems()` | - | Array | 获取所有物�?|
| `getItemsByType(type)` | type: string | Array | 按类型获取物�?|
| `getEquippedItems()` | - | Object | 获取已装备物�?|
| `getEquipmentBonus()` | - | Object | 获取装备属性加�?|
| `getUsage()` | - | Object | 获取背包使用情况 |
| `addGold(amount)` | amount: number | void | 添加金币 |
| `spendGold(amount)` | amount: number | boolean | 花费金币 |
| `getGold()` | - | number | 获取金币数量 |
| `buyItem(itemId, count, price)` | itemId: string, count: number, price: number | Object | 购买物品 |
| `sellItem(itemId, count, price)` | itemId: string, count: number, price: number | Object | 出售物品 |
| `on(event, callback)` | event: string, callback: Function | void | 注册事件监听 |
