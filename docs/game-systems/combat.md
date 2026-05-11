# 鎴樻枟绯荤粺

## 姒傝堪

鎴樻枟绯荤粺涓轰簰鍔ㄥ皬璇存父鎴忔彁渚涘洖鍚堝埗鎴樻枟鍔熻兘锛屾敮鎸佺帺瀹朵笌鏁屼汉涔嬮棿鐨勬垬鏂椾氦浜掋€?
## 鏍稿績姒傚康

### 鎴樻枟鍗曚綅 (CombatUnit)

```javascript
{
  id: "enemy_001",
  name: "鍝ュ竷鏋?,
  type: "enemy",  // "player" | "enemy" | "npc"
  
  // 鍩虹灞炴€?  health: 50,
  maxHealth: 50,
  attack: 8,
  defense: 3,
  speed: 5,
  
  // 鎶€鑳?  skills: [
    {
      name: "鏅€氭敾鍑?,
      damage: 10,
      cooldown: 0
    }
  ],
  
  // 鎴樺埄鍝?  loot: [
    { itemId: "gold_coin", chance: 0.8, min: 5, max: 15 }
  ]
}
```

### 鎴樻枟鐘舵€?(BattleState)

```javascript
{
  isActive: true,
  turn: 1,
  currentTurnUnit: "player",
  units: [
    { /* 鐜╁鏁版嵁 */ },
    { /* 鏁屼汉鏁版嵁 */ }
  ],
  log: [],  // 鎴樻枟鏃ュ織
  result: null  // "win" | "lose" | "escape"
}
```

## 浣跨敤鏂规硶

### 1. 瀹氫箟鏁屼汉

```javascript
const enemies = {
  "goblin": {
    id: "goblin",
    name: "鍝ュ竷鏋?,
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
    name: "鍏戒汉鎴樺＋",
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

### 2. 鍒濆鍖栨垬鏂楃郴缁?
```javascript
const combat = new CombatSystem(gameState);
```

### 3. 寮€濮嬫垬鏂?
```javascript
// 寮€濮嬩笌鍝ュ竷鏋楃殑鎴樻枟
combat.startBattle(enemies.goblin);

// 鎴栬€呭紑濮嬩笌澶氫釜鏁屼汉鐨勬垬鏂?combat.startBattle([enemies.goblin, enemies.goblin]);
```

### 4. 鎵ц鎴樻枟鍔ㄤ綔

```javascript
// 鏅€氭敾鍑?combat.attack(targetId);

// 浣跨敤鎶€鑳?combat.useSkill(skillId, targetId);

// 浣跨敤鐗╁搧
combat.useItem(itemId, targetId);

// 閫冭窇
combat.escape();
```

### 5. 鑾峰彇鎴樻枟淇℃伅

```javascript
// 鑾峰彇褰撳墠鐘舵€?const state = combat.getState();

// 鑾峰彇鎴樻枟鏃ュ織
const log = combat.getLog();

// 妫€鏌ユ垬鏂楁槸鍚︾粨鏉?const isEnded = combat.isEnded();

// 鑾峰彇鎴樻枟缁撴灉
const result = combat.getResult();  // "win" | "lose" | "escape"
```

## 鎴樻枟娴佺▼

```
寮€濮嬫垬鏂?    鈹?    鈻?璁＄畻琛屽姩椤哄簭锛堟牴鎹€熷害锛?    鈹?    鈻?鐜╁鍥炲悎 鈼勨攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?    鈹?                       鈹?    鈻?                       鈹?鏄剧ず鍙€夊姩浣?                 鈹?    鈹?                       鈹?    鈻?                       鈹?鎵ц鍔ㄤ綔锛堟敾鍑?鎶€鑳?鐗╁搧/閫冭窇锛?鈹?    鈹?                       鈹?    鈻?                       鈹?妫€鏌ユ垬鏂楃粨鏉燂紵 鈹€鈹€鏄攢鈹€鈻?缁撴潫鎴樻枟
    鈹?鍚?                    鈹?    鈻?                       鈹?鏁屼汉鍥炲悎 鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?    鈹?    鈻?AI閫夋嫨鍔ㄤ綔
    鈹?    鈻?鎵ц鍔ㄤ綔
    鈹?    鈻?妫€鏌ユ垬鏂楃粨鏉燂紵 鈹€鈹€鏄攢鈹€鈻?缁撴潫鎴樻枟
    鈹?鍚?    鈻?涓嬩竴鍥炲悎
```

## 浼ゅ璁＄畻

```javascript
// 鍩虹浼ゅ鍏紡
damage = max(1, attacker.attack - target.defense);

// 鏆村嚮鍒ゅ畾
if (random() < critChance) {
  damage *= critMultiplier;  // 閫氬父 1.5x 鎴?2x
}

// 鏈€缁堜激瀹?damage = floor(damage * randomRange(0.9, 1.1));  // 卤10% 娴姩
```

## 鎴樻枟AI

鏁屼汉AI鐨勮涓烘ā寮忥細

```javascript
const AI_BEHAVIORS = {
  // 鏀诲嚮鎬э細鎬绘槸鏀诲嚮
  aggressive: (unit, battleState) => {
    return { action: "attack", target: "player" };
  },
  
  // 闃插尽鎬э細浣庤閲忔椂闃插尽
  defensive: (unit, battleState) => {
    if (unit.health / unit.maxHealth < 0.3) {
      return { action: "defend" };
    }
    return { action: "attack", target: "player" };
  },
  
  // 闅忔満鎬э細闅忔満閫夋嫨鍔ㄤ綔
  random: (unit, battleState) => {
    const actions = ["attack", "skill", "defend"];
    return { action: randomChoice(actions) };
  }
};
```

## 浜嬩欢鍥炶皟

```javascript
combat.on("turnStart", (unit) => {
  console.log(`${unit.name} 鐨勫洖鍚堝紑濮媊);
});

combat.on("damage", (attacker, target, damage) => {
  console.log(`${attacker.name} 瀵?${target.name} 閫犳垚 ${damage} 鐐逛激瀹砢);
});

combat.on("battleEnd", (result, rewards) => {
  if (result === "win") {
    console.log("鎴樻枟鑳滃埄锛?);
    console.log(`鑾峰緱 ${rewards.experience} 缁忛獙鍊糮);
    console.log(`鑾峰緱鐗╁搧:`, rewards.loot);
  }
});
```

## 涓庢父鎴忓紩鎿庨泦鎴?
```javascript
// 鍦ㄥ満鏅腑瑙﹀彂鎴樻枟
const scene = {
  description: "涓€鍙摜甯冩灄鎸′綇浜嗕綘鐨勫幓璺紒",
  onEnter: (state) => {
    const combat = new CombatSystem(state);
    combat.startBattle(enemies.goblin);
    
    combat.on("battleEnd", (result, rewards) => {
      if (result === "win") {
        // 鎴樻枟鑳滃埄锛岀户缁墽鎯?        state.flags.defeatedGoblin = true;
        return { nextScene: "forest_path" };
      } else {
        // 鎴樻枟澶辫触锛屾父鎴忕粨鏉?        return { nextScene: "game_over" };
      }
    });
  }
};
```

## API 鍙傝€?
### CombatSystem 绫?
#### 鏋勯€犲嚱鏁?```javascript
new CombatSystem(gameState)
```

#### 鏂规硶

| 鏂规硶 | 鍙傛暟 | 杩斿洖鍊?| 璇存槑 |
|------|------|--------|------|
| `startBattle(enemy)` | enemy: Object/Array | void | 寮€濮嬫垬鏂?|
| `attack(targetId)` | targetId: string | Object | 鏅€氭敾鍑?|
| `useSkill(skillId, targetId)` | skillId: string, targetId: string | Object | 浣跨敤鎶€鑳?|
| `useItem(itemId, targetId)` | itemId: string, targetId: string | Object | 浣跨敤鐗╁搧 |
| `escape()` | - | boolean | 灏濊瘯閫冭窇 |
| `getState()` | - | Object | 鑾峰彇鎴樻枟鐘舵€?|
| `getLog()` | - | Array | 鑾峰彇鎴樻枟鏃ュ織 |
| `isEnded()` | - | boolean | 妫€鏌ユ垬鏂楁槸鍚︾粨鏉?|
| `getResult()` | - | string | 鑾峰彇鎴樻枟缁撴灉 |
| `on(event, callback)` | event: string, callback: Function | void | 娉ㄥ唽浜嬩欢鐩戝惉 |
