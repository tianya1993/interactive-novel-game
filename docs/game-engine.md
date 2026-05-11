# 娓告垙寮曟搸鏍稿績

## 姒傝堪

鏈父鎴忓紩鎿庢槸涓€涓熀浜庢枃妗ｇ殑浜掑姩灏忚娓告垙妗嗘灦锛岄噰鐢ㄦā鍧楀寲璁捐锛屾敮鎸佹垬鏂椼€佸璇濄€佽儗鍖呭拰涓栫晫鏋勫缓绛夋牳蹇冨姛鑳姐€?

## 绯荤粺鏋舵瀯

```
鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
鈹?          娓告垙寮曟搸鏍稿績               鈹?
鈹溾攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
鈹? 鐘舵€佺鐞? 鈹? 浜嬩欢绯荤粺  鈹? 瀛樻。绯荤粺   鈹?
鈹斺攢鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹粹攢鈹€鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹€鈹粹攢鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹€鈹?
     鈹?             鈹?          鈹?
鈹屸攢鈹€鈹€鈹€鈻尖攢鈹€鈹€鈹€鈹?   鈹屸攢鈹€鈹€鈹€鈻尖攢鈹€鈹€鈹€鈹? 鈹屸攢鈹€鈹€鈻尖攢鈹€鈹€鈹€鈹?
鈹?鎴樻枟绯荤粺 鈹?   鈹?瀵硅瘽绯荤粺 鈹? 鈹傝儗鍖呯郴缁熲攤
鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?   鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹? 鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
     鈹?             鈹?          鈹?
     鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹尖攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
                    鈹?
              鈹屸攢鈹€鈹€鈹€鈹€鈻尖攢鈹€鈹€鈹€鈹€鈹?
              鈹?涓栫晫鏋勫缓   鈹?
              鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
```

## 鏍稿績姒傚康

### 1. 娓告垙鐘舵€?(GameState)
娓告垙杩愯鏃剁殑鎵€鏈夋暟鎹兘瀛樺偍鍦ㄧ姸鎬佸璞′腑锛?

```javascript
{
  player: {
    name: "鐜╁鍚嶇О",
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
  flags: {},           // 鍓ф儏鏍囪
  visitedScenes: []    // 宸茶闂満鏅?
}
```

### 2. 鍦烘櫙 (Scene)
娓告垙鐨勫熀鏈崟浣嶏紝鍖呭惈锛?
- 鍦烘櫙鎻忚堪鏂囨湰
- 鍙€夊姩浣滃垪琛?
- 鏉′欢鍒ゆ柇
- 鍦烘櫙璺宠浆

### 3. 浜嬩欢绯荤粺
澶勭悊娓告垙涓殑鍚勭瑙﹀彂浜嬩欢锛?
- 杩涘叆鍦烘櫙浜嬩欢
- 瀵硅瘽閫夋嫨浜嬩欢
- 鎴樻枟缁撴灉浜嬩欢
- 鐗╁搧鑾峰彇浜嬩欢

## 浣跨敤鏂规硶

### 姝ラ1: 瀹氫箟娓告垙閰嶇疆

```javascript
const gameConfig = {
  title: "鎴戠殑鍐掗櫓鏁呬簨",
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

### 姝ラ2: 鍒涘缓鍦烘櫙

```javascript
const scenes = {
  "start": {
    description: "浣犵珯鍦ㄤ竴涓崄瀛楄矾鍙ｃ€備笢杈规槸涓€鐗囨．鏋楋紝瑗胯竟鏄竴搴у皬闀囥€?,
    choices: [
      {
        text: "鍓嶅線妫灄",
        nextScene: "forest",
        condition: null
      },
      {
        text: "鍓嶅線灏忛晣",
        nextScene: "town",
        condition: null
      }
    ]
  },
  
  "forest": {
    description: "妫灄閲屽厜绾挎槒鏆楋紝浣犲惉鍒颁簡濂囨€殑澹伴煶...",
    choices: [
      {
        text: "鎺㈢储娣卞",
        nextScene: "forest_deep",
        condition: null
      },
      {
        text: "杩斿洖璺彛",
        nextScene: "start",
        condition: null
      }
    ],
    onEnter: (state) => {
      // 杩涘叆鍦烘櫙鏃剁殑澶勭悊
      console.log("浣犺繘鍏ヤ簡妫灄");
    }
  }
};
```

### 姝ラ3: 鍒濆鍖栨父鎴?

```javascript
// 鍒涘缓娓告垙瀹炰緥
const game = new GameEngine(gameConfig);

// 鍔犺浇鍦烘櫙
game.loadScenes(scenes);

// 寮€濮嬫父鎴?
game.start();
```

### 姝ラ4: 澶勭悊鐜╁杈撳叆

```javascript
// 鏄剧ず褰撳墠鍦烘櫙
game.displayCurrentScene();

// 澶勭悊閫夋嫨
game.makeChoice(choiceIndex);

// 淇濆瓨娓告垙
game.save();

// 鍔犺浇娓告垙
game.load(saveData);
```

## API 鍙傝€?

### GameEngine 绫?

#### 鏋勯€犲嚱鏁?
```javascript
new GameEngine(config)
```

#### 鏂规硶

| 鏂规硶 | 鍙傛暟 | 璇存槑 |
|------|------|------|
| `start()` | - | 寮€濮嬫父鎴?|
| `loadScenes(scenes)` | scenes: Object | 鍔犺浇鍦烘櫙鏁版嵁 |
| `displayCurrentScene()` | - | 鏄剧ず褰撳墠鍦烘櫙 |
| `makeChoice(index)` | index: number | 鎵ц閫夋嫨 |
| `save()` | - | 淇濆瓨娓告垙鐘舵€?|
| `load(saveData)` | saveData: Object | 鍔犺浇娓告垙鐘舵€?|
| `getState()` | - | 鑾峰彇褰撳墠鐘舵€?|
| `setState(newState)` | newState: Object | 璁剧疆鐘舵€?|

## 涓庡叾浠栫郴缁熺殑闆嗘垚

### 闆嗘垚鎴樻枟绯荤粺
```javascript
// 鍦ㄥ満鏅腑瑙﹀彂鎴樻枟
{
  onEnter: (state) => {
    const combat = new CombatSystem(state);
    combat.startBattle(enemy);
  }
}
```

### 闆嗘垚瀵硅瘽绯荤粺
```javascript
// 鍦ㄥ満鏅腑鍚姩瀵硅瘽
{
  onEnter: (state) => {
    const dialog = new DialogSystem(state);
    dialog.startDialog(npc);
  }
}
```

### 闆嗘垚鑳屽寘绯荤粺
```javascript
// 鍦ㄥ満鏅腑鑾峰彇鐗╁搧
{
  onEnter: (state) => {
    const inventory = new InventorySystem(state);
    inventory.addItem(item);
  }
}
```

## 瀛樻。鏍煎紡

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

## 鎵╁睍寮€鍙?

濡傞渶娣诲姞鏂板姛鑳斤紝鍙互锛?
1. 鍦?`skills/` 鐩綍涓嬪垱寤烘柊鐨勫瓙绯荤粺
2. 缁ф壙 `GameEngine` 绫昏繘琛屾墿灞?
3. 閫氳繃浜嬩欢绯荤粺涓庡叾浠栨ā鍧楅€氫俊
