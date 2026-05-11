# 瀵硅瘽绯荤粺

## 姒傝堪

瀵硅瘽绯荤粺涓轰簰鍔ㄥ皬璇存父鎴忔彁渚涗赴瀵岀殑瀵硅瘽浜や簰鍔熻兘锛屾敮鎸佸垎鏀璇濄€佹潯浠跺垽鏂€佹儏鎰熷彉鍖栫瓑鐗规€с€?
## 鏍稿績姒傚康

### 瀵硅瘽鑺傜偣 (DialogNode)

```javascript
{
  id: "node_001",
  speaker: "NPC鍚嶇О",
  text: "瀵硅瘽鍐呭鏂囨湰",
  emotion: "happy",  // 鍙€夛細琛ㄦ儏/鎯呯华
  
  // 閫夐」鍒楄〃
  choices: [
    {
      text: "閫夐」鏂囨湰",
      nextNode: "node_002",
      condition: null,      // 鏄剧ず鏉′欢
      effects: [],          // 閫夋嫨鍚庣殑鏁堟灉
      emotionChange: 5      // 濂芥劅搴﹀彉鍖?    }
  ],
  
  // 鑷姩璺宠浆锛堟棤閫夐」鏃讹級
  autoNext: "node_003",
  
  // 杩涘叆鑺傜偣鏃剁殑鏁堟灉
  onEnter: (state) => { }
}
```

### 瀵硅瘽鐘舵€?(DialogState)

```javascript
{
  isActive: true,
  currentNode: "node_001",
  history: [],           // 瀵硅瘽鍘嗗彶
  relationship: {        // NPC鍏崇郴鍊?    "npc_001": 50
  }
}
```

## 浣跨敤鏂规硶

### 1. 瀹氫箟瀵硅瘽鏍?
```javascript
const dialogs = {
  "npc_merchant": {
    name: "鍟嗕汉鑰佺帇",
    initialNode: "greeting",
    
    nodes: {
      "greeting": {
        id: "greeting",
        speaker: "鍟嗕汉鑰佺帇",
        text: "娆㈣繋鍏変复锛佹湁浠€涔堟垜鍙互甯綘鐨勫悧锛?,
        choices: [
          {
            text: "鎴戞兂鐪嬬湅浣犵殑鍟嗗搧",
            nextNode: "show_goods",
            emotionChange: 0
          },
          {
            text: "鏈€杩戞湁浠€涔堟柊闂诲悧锛?,
            nextNode: "news",
            emotionChange: 2
          },
          {
            text: "娌′粈涔堬紝鍙槸璺繃",
            nextNode: "goodbye",
            emotionChange: -2
          }
        ]
      },
      
      "show_goods": {
        id: "show_goods",
        speaker: "鍟嗕汉鑰佺帇",
        text: "杩欎簺閮芥槸涓婂ソ鐨勮揣鑹诧紝鐪嬬湅鍚э紒",
        onEnter: (state) => {
          // 鎵撳紑鍟嗗簵鐣岄潰
          state.openShop = true;
        },
        autoNext: "greeting"
      },
      
      "news": {
        id: "news",
        speaker: "鍟嗕汉鑰佺帇",
        text: "鍚鍖楁柟鐨勬．鏋楅噷鍑虹幇浜嗘€墿锛屼綘瑕佸皬蹇冨晩銆?,
        choices: [
          {
            text: "璋㈣阿鎻愰啋",
            nextNode: "greeting",
            emotionChange: 3
          }
        ]
      },
      
      "goodbye": {
        id: "goodbye",
        speaker: "鍟嗕汉鑰佺帇",
        text: "鎱㈣蛋涓嶉€併€?,
        choices: [],
        onEnter: (state) => {
          // 缁撴潫瀵硅瘽
          state.dialogEnded = true;
        }
      }
    }
  }
};
```

### 2. 鍒濆鍖栧璇濈郴缁?
```javascript
const dialog = new DialogSystem(gameState);
```

### 3. 寮€濮嬪璇?
```javascript
// 涓庡晢浜哄紑濮嬪璇?dialog.startDialog(dialogs.npc_merchant);
```

### 4. 鑾峰彇褰撳墠瀵硅瘽

```javascript
// 鑾峰彇褰撳墠鑺傜偣淇℃伅
const currentNode = dialog.getCurrentNode();

// 鑾峰彇鍙敤閫夐」
const choices = dialog.getAvailableChoices();

// 鑾峰彇瀵硅瘽鍘嗗彶
const history = dialog.getHistory();
```

### 5. 閫夋嫨閫夐」

```javascript
// 閫夋嫨绗?涓€夐」
dialog.selectChoice(0);

// 鎴栬€呮牴鎹€夐」ID閫夋嫨
dialog.selectChoiceById("choice_001");
```

## 鏉′欢鍒ゆ柇

閫夐」鍙互鏍规嵁娓告垙鐘舵€佹樉绀烘垨闅愯棌锛?
```javascript
{
  text: "鎴戝惉璇翠綘鍦ㄦ壘鍐掗櫓鑰?,
  nextNode: "quest_offer",
  condition: (state) => {
    // 鍙湁褰撶帺瀹剁瓑绾?=5涓旀湭瀹屾垚璇ヤ换鍔℃椂鏄剧ず
    return state.player.level >= 5 && !state.flags.completedQuest001;
  }
}
```

## 鏁堟灉绯荤粺

閫夋嫨閫夐」鍚庡彲浠ヨЕ鍙戝悇绉嶆晥鏋滐細

```javascript
{
  text: "鎴戞帴鍙楄繖涓换鍔?,
  nextNode: "quest_accepted",
  effects: [
    { type: "setFlag", key: "quest001_active", value: true },
    { type: "addItem", itemId: "quest_item", count: 1 },
    { type: "changeRelationship", npc: "npc_001", value: 10 },
    { type: "giveExperience", amount: 50 }
  ]
}
```

## 鍔ㄦ€佹枃鏈?
鏀寔鍦ㄦ枃鏈腑鎻掑叆鍙橀噺锛?
```javascript
{
  speaker: "鏉戦暱",
  text: "娆㈣繋锛寋player.name}锛佷綘宸茬粡{player.level}绾т簡锛岀湡鏄垚闀胯繀閫熷晩锛?,
  textProcessor: (text, state) => {
    return text
      .replace("{player.name}", state.player.name)
      .replace("{player.level}", state.player.level);
  }
}
```

## 鍏崇郴绯荤粺

璁板綍涓嶯PC鐨勫叧绯诲€硷紝褰卞搷瀵硅瘽閫夐」锛?
```javascript
// 鑾峰彇鍏崇郴鍊?const relation = dialog.getRelationship("npc_001");

// 璁剧疆鍏崇郴鍊?dialog.setRelationship("npc_001", 75);

// 淇敼鍏崇郴鍊?dialog.changeRelationship("npc_001", 10);

// 鏍规嵁鍏崇郴鍊兼樉绀轰笉鍚屽璇?{
  condition: (state) => dialog.getRelationship("npc_001") >= 50,
  text: "鑰佹湅鍙嬶紝鎴戠粰浣犲噯澶囦簡濂戒笢瑗匡紒"
}
```

## 瀵硅瘽浜嬩欢

```javascript
dialog.on("dialogStart", (npc) => {
  console.log(`寮€濮嬩笌 ${npc.name} 瀵硅瘽`);
});

dialog.on("nodeEnter", (node) => {
  console.log(`杩涘叆鑺傜偣: ${node.id}`);
});

dialog.on("choiceSelected", (choice, node) => {
  console.log(`閫夋嫨浜? ${choice.text}`);
});

dialog.on("dialogEnd", (npc) => {
  console.log(`缁撴潫涓?${npc.name} 瀵硅瘽`);
});

dialog.on("relationshipChange", (npc, oldValue, newValue) => {
  console.log(`涓?${npc} 鐨勫叧绯讳粠 ${oldValue} 鍙樹负 ${newValue}`);
});
```

## 涓庢父鎴忓紩鎿庨泦鎴?
```javascript
// 鍦ㄥ満鏅腑瑙﹀彂瀵硅瘽
const scene = {
  description: "浣犳潵鍒颁簡闀囦笂鐨勫箍鍦恒€?,
  choices: [
    {
      text: "涓庡晢浜轰氦璋?,
      action: (state) => {
        const dialog = new DialogSystem(state);
        dialog.startDialog(dialogs.npc_merchant);
        
        dialog.on("dialogEnd", () => {
          // 瀵硅瘽缁撴潫锛岃繑鍥炲満鏅?          return { continueScene: true };
        });
      }
    }
  ]
};
```

## 楂樼骇鍔熻兘

### 闅忔満瀵硅瘽

```javascript
{
  id: "random_greeting",
  speaker: "鏉戞皯",
  randomTexts: [
    "浠婂ぉ澶╂皵鐪熷ソ锛?,
    "浣犵湅璧锋潵鏄釜鍐掗櫓鑰呫€?,
    "灏忓績鍖楁柟鐨勬€墿銆?
  ],
  getText: (state) => {
    return randomChoice(this.randomTexts);
  }
}
```

### 璁板繂绯荤粺

NPC浼氳浣忎箣鍓嶇殑瀵硅瘽锛?
```javascript
{
  id: "second_meeting",
  speaker: "鍟嗕汉鑰佺帇",
  getText: (state) => {
    if (state.dialogHistory.metMerchant) {
      return "鍙堣闈簡锛佽繖娆℃兂涔扮偣浠€涔堬紵";
    } else {
      state.dialogHistory.metMerchant = true;
      return "娆㈣繋绗竴娆″厜涓达紒";
    }
  }
}
```

### 鏃堕棿鏁忔劅瀵硅瘽

```javascript
{
  condition: (state) => {
    const hour = state.gameTime.hour;
    return hour >= 6 && hour < 18;  // 鍙湪鐧藉ぉ鏄剧ず
  },
  text: "鐧藉ぉ钀ヤ笟涓紒"
}
```

## API 鍙傝€?
### DialogSystem 绫?
#### 鏋勯€犲嚱鏁?```javascript
new DialogSystem(gameState)
```

#### 鏂规硶

| 鏂规硶 | 鍙傛暟 | 杩斿洖鍊?| 璇存槑 |
|------|------|--------|------|
| `startDialog(dialogData)` | dialogData: Object | void | 寮€濮嬪璇?|
| `getCurrentNode()` | - | Object | 鑾峰彇褰撳墠鑺傜偣 |
| `getAvailableChoices()` | - | Array | 鑾峰彇鍙敤閫夐」 |
| `selectChoice(index)` | index: number | void | 閫夋嫨閫夐」 |
| `getHistory()` | - | Array | 鑾峰彇瀵硅瘽鍘嗗彶 |
| `getRelationship(npcId)` | npcId: string | number | 鑾峰彇鍏崇郴鍊?|
| `setRelationship(npcId, value)` | npcId: string, value: number | void | 璁剧疆鍏崇郴鍊?|
| `changeRelationship(npcId, delta)` | npcId: string, delta: number | void | 淇敼鍏崇郴鍊?|
| `isActive()` | - | boolean | 妫€鏌ュ璇濇槸鍚﹁繘琛屼腑 |
| `endDialog()` | - | void | 缁撴潫瀵硅瘽 |
| `on(event, callback)` | event: string, callback: Function | void | 娉ㄥ唽浜嬩欢鐩戝惉 |
