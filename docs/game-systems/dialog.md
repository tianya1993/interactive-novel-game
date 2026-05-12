# 对话系统

## 概述

对话系统为互动小说游戏提供丰富的对话交互功能，支持分支对话、条件判断、情感变化等特性�?
## 核心概念

### 对话节点 (DialogNode)

```javascript
{
  id: "node_001",
  speaker: "NPC名称",
  text: "对话内容文本",
  emotion: "happy",  // 可选：表情/情绪
  
  // 选项列表
  choices: [
    {
      text: "选项文本",
      nextNode: "node_002",
      condition: null,      // 显示条件
      effects: [],          // 选择后的效果
      emotionChange: 5      // 好感度变�?    }
  ],
  
  // 自动跳转（无选项时）
  autoNext: "node_003",
  
  // 进入节点时的效果
  onEnter: (state) => { }
}
```

### 对话状�?(DialogState)

```javascript
{
  isActive: true,
  currentNode: "node_001",
  history: [],           // 对话历史
  relationship: {        // NPC关系�?    "npc_001": 50
  }
}
```

## 使用方法

### 1. 定义对话�?
```javascript
const dialogs = {
  "npc_merchant": {
    name: "商人老王",
    initialNode: "greeting",
    
    nodes: {
      "greeting": {
        id: "greeting",
        speaker: "商人老王",
        text: "欢迎光临！有什么我可以帮你的吗�?,
        choices: [
          {
            text: "我想看看你的商品",
            nextNode: "show_goods",
            emotionChange: 0
          },
          {
            text: "最近有什么新闻吗�?,
            nextNode: "news",
            emotionChange: 2
          },
          {
            text: "没什么，只是路过",
            nextNode: "goodbye",
            emotionChange: -2
          }
        ]
      },
      
      "show_goods": {
        id: "show_goods",
        speaker: "商人老王",
        text: "这些都是上好的货色，看看吧！",
        onEnter: (state) => {
          // 打开商店界面
          state.openShop = true;
        },
        autoNext: "greeting"
      },
      
      "news": {
        id: "news",
        speaker: "商人老王",
        text: "听说北方的森林里出现了怪物，你要小心啊�?,
        choices: [
          {
            text: "谢谢提醒",
            nextNode: "greeting",
            emotionChange: 3
          }
        ]
      },
      
      "goodbye": {
        id: "goodbye",
        speaker: "商人老王",
        text: "慢走不送�?,
        choices: [],
        onEnter: (state) => {
          // 结束对话
          state.dialogEnded = true;
        }
      }
    }
  }
};
```

### 2. 初始化对话系�?
```javascript
const dialog = new DialogSystem(gameState);
```

### 3. 开始对�?
```javascript
// 与商人开始对�?dialog.startDialog(dialogs.npc_merchant);
```

### 4. 获取当前对话

```javascript
// 获取当前节点信息
const currentNode = dialog.getCurrentNode();

// 获取可用选项
const choices = dialog.getAvailableChoices();

// 获取对话历史
const history = dialog.getHistory();
```

### 5. 选择选项

```javascript
// 选择�?个选项
dialog.selectChoice(0);

// 或者根据选项ID选择
dialog.selectChoiceById("choice_001");
```

## 条件判断

选项可以根据游戏状态显示或隐藏�?
```javascript
{
  text: "我听说你在找冒险�?,
  nextNode: "quest_offer",
  condition: (state) => {
    // 只有当玩家等�?=5且未完成该任务时显示
    return state.player.level >= 5 && !state.flags.completedQuest001;
  }
}
```

## 效果系统

选择选项后可以触发各种效果：

```javascript
{
  text: "我接受这个任�?,
  nextNode: "quest_accepted",
  effects: [
    { type: "setFlag", key: "quest001_active", value: true },
    { type: "addItem", itemId: "quest_item", count: 1 },
    { type: "changeRelationship", npc: "npc_001", value: 10 },
    { type: "giveExperience", amount: 50 }
  ]
}
```

## 动态文�?
支持在文本中插入变量�?
```javascript
{
  speaker: "村长",
  text: "欢迎，{player.name}！你已经{player.level}级了，真是成长迅速啊�?,
  textProcessor: (text, state) => {
    return text
      .replace("{player.name}", state.player.name)
      .replace("{player.level}", state.player.level);
  }
}
```

## 关系系统

记录与NPC的关系值，影响对话选项�?
```javascript
// 获取关系�?const relation = dialog.getRelationship("npc_001");

// 设置关系�?dialog.setRelationship("npc_001", 75);

// 修改关系�?dialog.changeRelationship("npc_001", 10);

// 根据关系值显示不同对�?{
  condition: (state) => dialog.getRelationship("npc_001") >= 50,
  text: "老朋友，我给你准备了好东西！"
}
```

## 对话事件

```javascript
dialog.on("dialogStart", (npc) => {
  console.log(`开始与 ${npc.name} 对话`);
});

dialog.on("nodeEnter", (node) => {
  console.log(`进入节点: ${node.id}`);
});

dialog.on("choiceSelected", (choice, node) => {
  console.log(`选择�? ${choice.text}`);
});

dialog.on("dialogEnd", (npc) => {
  console.log(`结束�?${npc.name} 对话`);
});

dialog.on("relationshipChange", (npc, oldValue, newValue) => {
  console.log(`�?${npc} 的关系从 ${oldValue} 变为 ${newValue}`);
});
```

## 与游戏引擎集�?
```javascript
// 在场景中触发对话
const scene = {
  description: "你来到了镇上的广场�?,
  choices: [
    {
      text: "与商人交�?,
      action: (state) => {
        const dialog = new DialogSystem(state);
        dialog.startDialog(dialogs.npc_merchant);
        
        dialog.on("dialogEnd", () => {
          // 对话结束，返回场�?          return { continueScene: true };
        });
      }
    }
  ]
};
```

## 高级功能

### 随机对话

```javascript
{
  id: "random_greeting",
  speaker: "村民",
  randomTexts: [
    "今天天气真好�?,
    "你看起来是个冒险者�?,
    "小心北方的怪物�?
  ],
  getText: (state) => {
    return randomChoice(this.randomTexts);
  }
}
```

### 记忆系统

NPC会记住之前的对话�?
```javascript
{
  id: "second_meeting",
  speaker: "商人老王",
  getText: (state) => {
    if (state.dialogHistory.metMerchant) {
      return "又见面了！这次想买点什么？";
    } else {
      state.dialogHistory.metMerchant = true;
      return "欢迎第一次光临！";
    }
  }
}
```

### 时间敏感对话

```javascript
{
  condition: (state) => {
    const hour = state.gameTime.hour;
    return hour >= 6 && hour < 18;  // 只在白天显示
  },
  text: "白天营业中！"
}
```

## API 参�?
### DialogSystem �?
#### 构造函�?```javascript
new DialogSystem(gameState)
```

#### 方法

| 方法 | 参数 | 返回�?| 说明 |
|------|------|--------|------|
| `startDialog(dialogData)` | dialogData: Object | void | 开始对�?|
| `getCurrentNode()` | - | Object | 获取当前节点 |
| `getAvailableChoices()` | - | Array | 获取可用选项 |
| `selectChoice(index)` | index: number | void | 选择选项 |
| `getHistory()` | - | Array | 获取对话历史 |
| `getRelationship(npcId)` | npcId: string | number | 获取关系�?|
| `setRelationship(npcId, value)` | npcId: string, value: number | void | 设置关系�?|
| `changeRelationship(npcId, delta)` | npcId: string, delta: number | void | 修改关系�?|
| `isActive()` | - | boolean | 检查对话是否进行中 |
| `endDialog()` | - | void | 结束对话 |
| `on(event, callback)` | event: string, callback: Function | void | 注册事件监听 |
