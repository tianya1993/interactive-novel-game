# 鑳屽寘绯荤粺

## 姒傝堪

鑳屽寘绯荤粺涓轰簰鍔ㄥ皬璇存父鎴忔彁渚涚墿鍝佺鐞嗗姛鑳斤紝鏀寔鐗╁搧鐨勮幏鍙栥€佷娇鐢ㄣ€佷涪寮冦€佽澶囩瓑鎿嶄綔銆?
## 鏍稿績姒傚康

### 鐗╁搧 (Item)

```javascript
{
  id: "item_001",
  name: "鐢熷懡鑽按",
  description: "鎭㈠50鐐圭敓鍛藉€?,
  type: "consumable",  // "consumable" | "equipment" | "material" | "quest"
  icon: "potion_red.png",
  
  // 鍫嗗彔淇℃伅
  stackable: true,
  maxStack: 99,
  
  // 浣跨敤鏁堟灉锛堟秷鑰楀搧锛?  effects: [
    { type: "heal", value: 50 }
  ],
  
  // 瑁呭灞炴€э紙瑁呭锛?  equipment: {
    slot: "weapon",  // "weapon" | "armor" | "accessory"
    attack: 10,
    defense: 0
  },
  
  // 浠峰€?  value: 100,  // 閲戝竵浠峰€?  
  // 浣跨敤鏉′欢
  usable: true,
  usableIn: ["field", "battle"]  // 鍙敤鍦烘櫙
}
```

### 鑳屽寘鏍煎瓙 (InventorySlot)

```javascript
{
  itemId: "item_001",
  count: 5,
  equipped: false  // 鏄惁宸茶澶?}
```

### 鑳屽寘鐘舵€?(InventoryState)

```javascript
{
  maxSlots: 50,        // 鏈€澶ф牸瀛愭暟
  gold: 1000,          // 閲戝竵
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

## 浣跨敤鏂规硶

### 1. 瀹氫箟鐗╁搧

```javascript
const items = {
  "health_potion": {
    id: "health_potion",
    name: "鐢熷懡鑽按",
    description: "鎭㈠50鐐圭敓鍛藉€?,
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
    name: "閾佸墤",
    description: "涓€鎶婃櫘閫氱殑閾佸墤",
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
    name: "鐨敳",
    description: "杞讳究鐨勭毊鍒舵姢鐢?,
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
    name: "榄旀硶姘存櫠",
    description: "鏁ｅ彂鐫€绁炵鍏夎姃鐨勬按鏅?,
    type: "material",
    stackable: true,
    maxStack: 999,
    value: 500,
    usable: false
  },
  
  "ancient_key": {
    id: "ancient_key",
    name: "鍙よ€佺殑閽ュ寵",
    description: "鐪嬭捣鏉ヨ兘鎵撳紑鏌愭墖闂?,
    type: "quest",
    stackable: false,
    value: 0,
    usable: false
  }
};
```

### 2. 鍒濆鍖栬儗鍖呯郴缁?
```javascript
const inventory = new InventorySystem(gameState);
```

### 3. 娣诲姞鐗╁搧

```javascript
// 娣诲姞鍗曚釜鐗╁搧
inventory.addItem("health_potion", 1);

// 娣诲姞澶氫釜鐗╁搧
inventory.addItem("health_potion", 5);

// 娣诲姞鐗╁搧锛堣嚜鍔ㄥ鐞嗗爢鍙狅級
inventory.addItem("magic_crystal", 10);
```

### 4. 绉婚櫎鐗╁搧

```javascript
// 绉婚櫎鎸囧畾鏁伴噺鐨勭墿鍝?inventory.removeItem("health_potion", 2);

// 绉婚櫎鍏ㄩ儴
inventory.removeItem("health_potion", 999);

// 涓㈠純鐗╁搧
inventory.dropItem("health_potion", 1);
```

### 5. 浣跨敤鐗╁搧

```javascript
// 浣跨敤娑堣€楀搧
const result = inventory.useItem("health_potion");
// result: { success: true, effects: [{ type: "heal", value: 50 }] }

// 浣跨敤澶辫触锛堟潯浠朵笉婊¤冻锛?const result2 = inventory.useItem("iron_sword");
// result2: { success: false, reason: "涓嶅彲浣跨敤鐨勭墿鍝佺被鍨? }
```

### 6. 瑁呭绠＄悊

```javascript
// 瑁呭鐗╁搧
inventory.equipItem("iron_sword");

// 鍗镐笅瑁呭
inventory.unequipItem("weapon");

// 鑾峰彇褰撳墠瑁呭
const equipped = inventory.getEquippedItems();
// equipped: { weapon: "iron_sword", armor: null, accessory: null }

// 璁＄畻瑁呭灞炴€у姞鎴?const bonus = inventory.getEquipmentBonus();
// bonus: { attack: 15, defense: 0 }
```

### 7. 鏌ヨ鐗╁搧

```javascript
// 鑾峰彇鐗╁搧鏁伴噺
const count = inventory.getItemCount("health_potion");

// 妫€鏌ユ槸鍚︽湁鏌愮墿鍝?const hasItem = inventory.hasItem("ancient_key");

// 鑾峰彇鑳屽寘涓墍鏈夌墿鍝?const allItems = inventory.getAllItems();

// 鎸夌被鍨嬬瓫閫夌墿鍝?const consumables = inventory.getItemsByType("consumable");

// 鑾峰彇鑳屽寘浣跨敤鎯呭喌
const usage = inventory.getUsage();
// usage: { used: 5, max: 50, remaining: 45 }
```

### 8. 閲戝竵绠＄悊

```javascript
// 鑾峰緱閲戝竵
inventory.addGold(100);

// 鑺辫垂閲戝竵
const success = inventory.spendGold(50);
// success: true锛堥噾甯佽冻澶燂級鎴?false锛堥噾甯佷笉瓒筹級

// 鑾峰彇褰撳墠閲戝竵
const gold = inventory.getGold();
```

## 鐗╁搧鍒嗙被

### 娑堣€楀搧 (Consumable)
- 鑽按銆侀鐗╃瓑涓€娆℃€т娇鐢ㄧ墿鍝?- 鍙互鍫嗗彔
- 鏈変娇鐢ㄦ晥鏋?
### 瑁呭 (Equipment)
- 姝﹀櫒銆侀槻鍏枫€侀グ鍝?- 涓嶅彲鍫嗗彔
- 鎻愪緵灞炴€у姞鎴?- 鍙互瑁呭/鍗镐笅

### 鏉愭枡 (Material)
- 鍚堟垚銆佸埗浣滅敤鐨勬潗鏂?- 鍙互澶ч噺鍫嗗彔
- 閫氬父涓嶅彲鐩存帴浣跨敤

### 浠诲姟鐗╁搧 (Quest)
- 鍓ф儏鐩稿叧鐗╁搧
- 涓嶅彲鍫嗗彔
- 涓嶅彲鍑哄敭
- 鐗瑰畾鏉′欢涓嬩娇鐢?
## 浣跨敤鏁堟灉绫诲瀷

```javascript
const EFFECT_TYPES = {
  // 鎭㈠绫?  heal: { target: "hp", value: 50 },           // 鎭㈠鐢熷懡鍊?  restore_mp: { target: "mp", value: 30 },     // 鎭㈠榄旀硶鍊?  
  // 澧炵泭绫?  buff_attack: { stat: "attack", value: 10, duration: 300 },  // 鏀诲嚮鍔涙彁鍗?  buff_defense: { stat: "defense", value: 10, duration: 300 }, // 闃插尽鍔涙彁鍗?  
  // 鐗规畩绫?  teleport: { target: "last_town" },           // 浼犻€?  identify: { target: "unknown_item" },        // 閴村畾
  resurrect: { target: "dead_ally" }           // 澶嶆椿
};
```

## 浜嬩欢鍥炶皟

```javascript
inventory.on("itemAdded", (itemId, count, total) => {
  console.log(`鑾峰緱 ${items[itemId].name} x${count}`);
});

inventory.on("itemRemoved", (itemId, count, remaining) => {
  console.log(`澶卞幓 ${items[itemId].name} x${count}`);
});

inventory.on("itemUsed", (itemId, effects) => {
  console.log(`浣跨敤浜?${items[itemId].name}`);
});

inventory.on("itemEquipped", (itemId, slot) => {
  console.log(`瑁呭浜?${items[itemId].name}`);
});

inventory.on("itemUnequipped", (itemId, slot) => {
  console.log(`鍗镐笅浜?${items[itemId].name}`);
});

inventory.on("goldChanged", (oldAmount, newAmount) => {
  console.log(`閲戝竵: ${oldAmount} -> ${newAmount}`);
});

inventory.on("inventoryFull", (itemId, count) => {
  console.log("鑳屽寘宸叉弧锛?);
});
```

## 涓庢父鎴忓紩鎿庨泦鎴?
```javascript
// 鍦ㄥ満鏅腑鑾峰彇鐗╁搧
const scene = {
  description: "浣犲湪瀹濈涓彂鐜颁簡涓€浜涚墿鍝併€?,
  onEnter: (state) => {
    const inventory = new InventorySystem(state);
    
    // 娣诲姞鐗╁搧
    const result = inventory.addItem("health_potion", 3);
    if (result.success) {
      console.log("鑾峰緱浜?鐡剁敓鍛借嵂姘达紒");
    }
    
    // 妫€鏌ュ叧閿墿鍝?    if (inventory.hasItem("ancient_key")) {
      console.log("浣犱娇鐢ㄥ彜鑰佺殑閽ュ寵鎵撳紑浜嗛殣钘忕殑闂ㄣ€?);
    }
  }
};

// 鍦ㄦ垬鏂椾腑浣跨敤鐗╁搧
const combat = {
  onPlayerTurn: (state) => {
    const inventory = new InventorySystem(state);
    const consumables = inventory.getItemsByType("consumable");
    
    // 鏄剧ず鍙敤娑堣€楀搧
    consumables.forEach(item => {
      console.log(`[${item.name}] x${item.count}`);
    });
    
    // 浣跨敤鐗╁搧
    inventory.useItem("health_potion");
  }
};
```

## 鍟嗗簵浜ゆ槗

```javascript
// 璐拱鐗╁搧
inventory.buyItem("iron_sword", 1, shopPrice);

// 鍑哄敭鐗╁搧
inventory.sellItem("health_potion", 5, sellPrice);

// 鎵归噺鍑哄敭
inventory.sellItems([
  { itemId: "rusty_dagger", count: 2 },
  { itemId: "old_boots", count: 1 }
]);
```

## 瀛樻。鏍煎紡

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

## API 鍙傝€?
### InventorySystem 绫?
#### 鏋勯€犲嚱鏁?```javascript
new InventorySystem(gameState)
```

#### 鏂规硶

| 鏂规硶 | 鍙傛暟 | 杩斿洖鍊?| 璇存槑 |
|------|------|--------|------|
| `addItem(itemId, count)` | itemId: string, count: number | Object | 娣诲姞鐗╁搧 |
| `removeItem(itemId, count)` | itemId: string, count: number | Object | 绉婚櫎鐗╁搧 |
| `useItem(itemId)` | itemId: string | Object | 浣跨敤鐗╁搧 |
| `equipItem(itemId)` | itemId: string | Object | 瑁呭鐗╁搧 |
| `unequipItem(slot)` | slot: string | Object | 鍗镐笅瑁呭 |
| `dropItem(itemId, count)` | itemId: string, count: number | Object | 涓㈠純鐗╁搧 |
| `hasItem(itemId)` | itemId: string | boolean | 妫€鏌ユ槸鍚︽湁鐗╁搧 |
| `getItemCount(itemId)` | itemId: string | number | 鑾峰彇鐗╁搧鏁伴噺 |
| `getAllItems()` | - | Array | 鑾峰彇鎵€鏈夌墿鍝?|
| `getItemsByType(type)` | type: string | Array | 鎸夌被鍨嬭幏鍙栫墿鍝?|
| `getEquippedItems()` | - | Object | 鑾峰彇宸茶澶囩墿鍝?|
| `getEquipmentBonus()` | - | Object | 鑾峰彇瑁呭灞炴€у姞鎴?|
| `getUsage()` | - | Object | 鑾峰彇鑳屽寘浣跨敤鎯呭喌 |
| `addGold(amount)` | amount: number | void | 娣诲姞閲戝竵 |
| `spendGold(amount)` | amount: number | boolean | 鑺辫垂閲戝竵 |
| `getGold()` | - | number | 鑾峰彇閲戝竵鏁伴噺 |
| `buyItem(itemId, count, price)` | itemId: string, count: number, price: number | Object | 璐拱鐗╁搧 |
| `sellItem(itemId, count, price)` | itemId: string, count: number, price: number | Object | 鍑哄敭鐗╁搧 |
| `on(event, callback)` | event: string, callback: Function | void | 娉ㄥ唽浜嬩欢鐩戝惉 |
