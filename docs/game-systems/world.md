# 涓栫晫鏋勫缓绯荤粺

## 姒傝堪

涓栫晫鏋勫缓绯荤粺涓轰簰鍔ㄥ皬璇存父鎴忔彁渚涘満鏅鐞嗐€佸湴鍥惧鑸€佺幆澧冧氦浜掔瓑鍔熻兘锛屽府鍔╁垱寤轰赴瀵屽鏍风殑娓告垙涓栫晫銆?
## 鏍稿績姒傚康

### 鍦烘櫙 (Scene)

```javascript
{
  id: "scene_001",
  name: "鏉戝簞鍏ュ彛",
  description: "浣犵珯鍦ㄦ潙搴勭殑鍏ュ彛澶勶紝鍑犳爧鑼呰崏灞嬫暎钀藉湪閬撹矾涓ゆ梺銆?,
  
  // 鍖哄煙淇℃伅
  region: "鏂版墜鏉?,
  coordinates: { x: 0, y: 0 },
  
  // 鐜灞炴€?  environment: {
    type: "outdoor",      // "outdoor" | "indoor" | "dungeon"
    lighting: "day",      // "day" | "night" | "dark"
    weather: "sunny",     // "sunny" | "rainy" | "foggy"
    danger: "safe"        // "safe" | "caution" | "dangerous"
  },
  
  // 鍙氦浜掑璞?  objects: [
    {
      id: "well",
      name: "姘翠簳",
      description: "涓€鍙ｅ彜鑰佺殑姘翠簳",
      interactable: true,
      onInteract: (state) => { }
    }
  ],
  
  // NPC
  npcs: ["npc_village_head", "npc_merchant"],
  
  // 鍑哄彛
  exits: {
    north: { target: "scene_002", condition: null },
    south: { target: "scene_003", condition: (state) => state.flags.hasKey }
  },
  
  // 浜嬩欢
  onEnter: (state) => { },
  onExit: (state) => { },
  onStay: (state) => { }  // 姣忓洖鍚堣Е鍙?}
```

### 鍖哄煙 (Region)

```javascript
{
  id: "region_001",
  name: "鏂版墜鏉?,
  description: "涓€涓畞闈欑殑灏忔潙搴勶紝閫傚悎鍒濆鑰呭啋闄┿€?,
  
  // 鍖哄煙灞炴€?  level: "1-5",
  danger: "low",
  
  // 鍖呭惈鐨勫満鏅?  scenes: ["scene_001", "scene_002", "scene_003"],
  
  // 鍖哄煙鏁堟灉
  effects: {
    healthRegen: 1,    // 姣忕鎭㈠1鐐圭敓鍛?    manaRegen: 1       // 姣忕鎭㈠1鐐归瓟娉?  }
}
```

### 涓栫晫鍦板浘 (WorldMap)

```javascript
{
  regions: {
    "region_001": { /* 鏂版墜鏉?*/ },
    "region_002": { /* 榛戞殫妫灄 */ },
    "region_003": { /* 鐜嬮兘 */ }
  },
  
  connections: [
    { from: "region_001", to: "region_002", requirement: "level >= 5" },
    { from: "region_001", to: "region_003", requirement: "quest_001_completed" }
  ]
}
```

## 浣跨敤鏂规硶

### 1. 瀹氫箟鍦烘櫙

```javascript
const scenes = {
  "village_entrance": {
    id: "village_entrance",
    name: "鏉戝簞鍏ュ彛",
    description: "浣犵珯鍦ㄦ潙搴勭殑鍏ュ彛澶勶紝鍑犳爧鑼呰崏灞嬫暎钀藉湪閬撹矾涓ゆ梺銆傛潙鍙ｆ湁涓€妫靛法澶х殑姗℃爲銆?,
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
        name: "澶ф鏍?,
        description: "涓€妫甸渶瑕佹暟浜哄悎鎶辩殑鍙よ€佹鏍?,
        interactable: true,
        onInteract: (state) => {
          console.log("浣犲湪鏍戜笅鍙戠幇浜嗕竴鏋氶棯闂彂鍏夌殑纭竵锛?);
          state.inventory.addGold(1);
        }
      },
      {
        id: "notice_board",
        name: "鍏憡鏉?,
        description: "涓婇潰璐寸潃鍚勭鍛婄ず",
        interactable: true,
        onInteract: (state) => {
          console.log("鍏憡鏉垮唴瀹癸細");
          console.log("1. 鎷涘嫙鍐掗櫓鑰呮竻鐞嗗寳鏂规．鏋楃殑鍝ュ竷鏋?);
          console.log("2. 瀵绘壘澶辫釜鐨勬潙闀跨殑濂冲効");
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
        console.log("绗竴娆℃潵鍒版潙搴勶紝浣犳劅鍒颁竴闃靛畞闈欍€?);
        state.flags.visitedVillage = true;
      }
    }
  },
  
  "village_square": {
    id: "village_square",
    name: "鏉戝簞骞垮満",
    description: "鏉戝簞鐨勪腑蹇冨箍鍦猴紝鏉戞皯浠湪杩欓噷鑱氶泦浜ゆ祦銆傚箍鍦轰腑澶湁涓€搴у柗娉夈€?,
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
        name: "鍠锋硥",
        description: "娓呮緢鐨勬硥姘翠粠鐭抽洉涓祦鍑?,
        interactable: true,
        onInteract: (state) => {
          console.log("浣犲枬浜嗗彛娉夋按锛屾劅鍒扮簿绁炵剷鍙戯紒");
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
    name: "榛戞殫妫灄",
    description: "鑼傚瘑鐨勬爲鏋楅伄鎸′簡闃冲厜锛屽洓鍛ㄤ竴鐗囨槒鏆椼€備綘鍚埌浜嗗鎬殑澹伴煶...",
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
        name: "绁炵娲炵┐",
        description: "涓€涓粦婕嗘紗鐨勬礊绌村叆鍙?,
        interactable: true,
        onInteract: (state) => {
          if (state.inventory.hasItem("torch")) {
            return { nextScene: "cave_entrance" };
          } else {
            console.log("澶粦浜嗭紝浣犻渶瑕佺伀鎶婃墠鑳借繘鍏ャ€?);
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
      // 闅忔満閬亣鏁屼汉
      if (Math.random() < 0.3) {
        console.log("涓€鍙摜甯冩灄浠庢爲鍚庤烦浜嗗嚭鏉ワ紒");
        state.triggerCombat = true;
        state.enemy = "goblin";
      }
    },
    
    onStay: (state) => {
      // 鍦ㄥ嵄闄╁尯鍩熸瘡鍥炲悎鍙兘閬亣
      if (Math.random() < 0.1) {
        console.log("浣犳劅瑙夊埌鏈変笢瑗垮湪闈犺繎...");
      }
    }
  }
};
```

### 2. 鍒濆鍖栦笘鐣屾瀯寤虹郴缁?
```javascript
const world = new WorldBuilder(gameState);
```

### 3. 鍔犺浇鍦烘櫙

```javascript
// 鍔犺浇鎵€鏈夊満鏅?world.loadScenes(scenes);

// 鍔犺浇鍖哄煙
world.loadRegions(regions);
```

### 4. 鍦烘櫙瀵艰埅

```javascript
// 鑾峰彇褰撳墠鍦烘櫙
const currentScene = world.getCurrentScene();

// 鑾峰彇鍦烘櫙淇℃伅
const sceneInfo = world.getSceneInfo("village_entrance");

// 绉诲姩鍒板叾浠栧満鏅?const result = world.moveTo("north");
// result: { success: true, scene: sceneObject } 鎴?{ success: false, reason: "鏉′欢涓嶆弧瓒? }

// 鐩存帴浼犻€佸埌鍦烘櫙
world.teleportTo("dark_forest");
```

### 5. 鐜浜や簰

```javascript
// 鑾峰彇鍦烘櫙涓殑鍙氦浜掑璞?const objects = world.getInteractableObjects();

// 涓庡璞′氦浜?world.interactWith("oak_tree");

// 鑾峰彇鍦烘櫙涓殑NPC
const npcs = world.getNPCs();

// 鑾峰彇鍙敤鍑哄彛
const exits = world.getAvailableExits();
```

### 6. 鐜鐘舵€?
```javascript
// 鑾峰彇褰撳墠鐜
const environment = world.getEnvironment();

// 妫€鏌ユ槸鍚﹀彲浠ュ湪褰撳墠鐜鎵ц鏌愭搷浣?const canRest = world.canRest();  // 鍦ㄥ畨鍏ㄥ尯鍩熷彲浠ヤ紤鎭?
// 鑾峰彇鍖哄煙淇℃伅
const region = world.getCurrentRegion();
```

## 鍔ㄦ€佸満鏅?
### 鏃堕棿鍙樺寲

```javascript
{
  id: "village_night",
  condition: (state) => state.gameTime.hour >= 20 || state.gameTime.hour < 6,
  description: "澶滄櫄鐨勬潙搴勬牸澶栧畞闈欙紝鍙湁鍑犳埛浜哄杩樹寒鐫€鐏€?,
  npcs: ["night_watch"],  // 澶滄櫄鐗规湁鐨凬PC
  exits: {
    // 澶滄櫄鏌愪簺鍑哄彛鍙兘鍏抽棴
    north: { target: "village_square", condition: null, closed: true }
  }
}
```

### 澶╂皵绯荤粺

```javascript
// 鍦ㄥ満鏅腑鏍规嵁澶╂皵鏀瑰彉鎻忚堪
{
  id: "village_rainy",
  condition: (state) => state.weather === "rainy",
  description: "闆ㄦ按鎵撴箍浜嗘潙搴勭殑琛楅亾锛屾潙姘戜滑绾风悍韬茶繘浜嗗眿鍐呫€?,
  effects: {
    movementSpeed: 0.8  // 绉诲姩閫熷害闄嶄綆
  }
}
```

## 鍦板浘绯荤粺

```javascript
// 鑾峰彇鍖哄煙鍦板浘
const map = world.getRegionMap("newbie_village");

// 鏄剧ず褰撳墠浣嶇疆
const position = world.getCurrentPosition();
// position: { region: "newbie_village", scene: "village_entrance", x: 0, y: 0 }

// 璁＄畻璺緞
const path = world.findPath("village_entrance", "dark_forest");
// path: ["village_entrance", "wilderness", "dark_forest"]

// 鑾峰彇鐩搁偦鍦烘櫙
const neighbors = world.getNeighborScenes();
```

## 浜嬩欢绯荤粺

```javascript
world.on("sceneEnter", (scene, fromScene) => {
  console.log(`杩涘叆鍦烘櫙: ${scene.name}`);
});

world.on("sceneExit", (scene, toScene) => {
  console.log(`绂诲紑鍦烘櫙: ${scene.name}`);
});

world.on("objectInteract", (object, scene) => {
  console.log(`涓?${object.name} 浜や簰`);
});

world.on("environmentChange", (oldEnv, newEnv) => {
  console.log(`鐜鍙樺寲: ${oldEnv.weather} -> ${newEnv.weather}`);
});
```

## 涓庢父鎴忓紩鎿庨泦鎴?
```javascript
// 鍒濆鍖栨父鎴忔椂鍔犺浇涓栫晫
const game = new GameEngine(config);
const world = new WorldBuilder(game.state);

world.loadScenes(scenes);
world.loadRegions(regions);

// 璁剧疆鍒濆鍦烘櫙
world.setCurrentScene("village_entrance");

// 娓告垙涓诲惊鐜?game.on("turn", () => {
  const scene = world.getCurrentScene();
  
  // 鏄剧ず鍦烘櫙鎻忚堪
  console.log(scene.description);
  
  // 鏄剧ず鍙氦浜掑璞?  const objects = world.getInteractableObjects();
  objects.forEach((obj, index) => {
    console.log(`${index + 1}. [鏌ョ湅] ${obj.name}`);
  });
  
  // 鏄剧ず鍑哄彛
  const exits = world.getAvailableExits();
  Object.keys(exits).forEach(direction => {
    console.log(`[鍓嶅線${direction}]`);
  });
});
```

## 蹇€熸梾琛?
```javascript
// 瑙ｉ攣蹇€熸梾琛岀偣
world.unlockFastTravel("village_entrance");

// 鑾峰彇宸茶В閿佺殑蹇€熸梾琛岀偣
const travelPoints = world.getUnlockedFastTravelPoints();

// 蹇€熸梾琛?world.fastTravel("village_entrance");
```

## 鎺㈢储搴︾郴缁?
```javascript
// 璁板綍鎺㈢储杩涘害
world.discoverScene("secret_cave");

// 鑾峰彇鍖哄煙鎺㈢储搴?const exploration = world.getExplorationRate("newbie_village");
// exploration: { discovered: 5, total: 10, rate: 0.5 }

// 鑾峰彇鎺㈢储濂栧姳
if (exploration.rate >= 1.0) {
  console.log("鎭枩锛佷綘瀹屽叏鎺㈢储浜嗘柊鎵嬫潙锛?);
  game.giveReward("exploration_bonus");
}
```

## API 鍙傝€?
### WorldBuilder 绫?
#### 鏋勯€犲嚱鏁?```javascript
new WorldBuilder(gameState)
```

#### 鏂规硶

| 鏂规硶 | 鍙傛暟 | 杩斿洖鍊?| 璇存槑 |
|------|------|--------|------|
| `loadScenes(scenes)` | scenes: Object | void | 鍔犺浇鍦烘櫙鏁版嵁 |
| `loadRegions(regions)` | regions: Object | void | 鍔犺浇鍖哄煙鏁版嵁 |
| `getCurrentScene()` | - | Object | 鑾峰彇褰撳墠鍦烘櫙 |
| `setCurrentScene(sceneId)` | sceneId: string | void | 璁剧疆褰撳墠鍦烘櫙 |
| `getSceneInfo(sceneId)` | sceneId: string | Object | 鑾峰彇鍦烘櫙淇℃伅 |
| `moveTo(direction)` | direction: string | Object | 鍚戞寚瀹氭柟鍚戠Щ鍔?|
| `teleportTo(sceneId)` | sceneId: string | Object | 浼犻€佸埌鍦烘櫙 |
| `getInteractableObjects()` | - | Array | 鑾峰彇鍙氦浜掑璞?|
| `interactWith(objectId)` | objectId: string | Object | 涓庡璞′氦浜?|
| `getNPCs()` | - | Array | 鑾峰彇鍦烘櫙NPC |
| `getAvailableExits()` | - | Object | 鑾峰彇鍙敤鍑哄彛 |
| `getEnvironment()` | - | Object | 鑾峰彇鐜鐘舵€?|
| `getCurrentRegion()` | - | Object | 鑾峰彇褰撳墠鍖哄煙 |
| `getRegionMap(regionId)` | regionId: string | Object | 鑾峰彇鍖哄煙鍦板浘 |
| `getCurrentPosition()` | - | Object | 鑾峰彇褰撳墠浣嶇疆 |
| `findPath(from, to)` | from: string, to: string | Array | 鏌ユ壘璺緞 |
| `getNeighborScenes()` | - | Array | 鑾峰彇鐩搁偦鍦烘櫙 |
| `unlockFastTravel(sceneId)` | sceneId: string | void | 瑙ｉ攣蹇€熸梾琛岀偣 |
| `getUnlockedFastTravelPoints()` | - | Array | 鑾峰彇宸茶В閿佹梾琛岀偣 |
| `fastTravel(sceneId)` | sceneId: string | Object | 蹇€熸梾琛?|
| `discoverScene(sceneId)` | sceneId: string | void | 鏍囪鍦烘櫙宸插彂鐜?|
| `getExplorationRate(regionId)` | regionId: string | Object | 鑾峰彇鎺㈢储搴?|
| `on(event, callback)` | event: string, callback: Function | void | 娉ㄥ唽浜嬩欢鐩戝惉 |
