# 互动小说游戏 - 使用指南

## 快速开�?
### 聊天模式（推荐，零依赖）

�?Claude Code 中输�?`/novel-play`，直接在对话中开始玩游戏。AI �?Claude 直接驱动，不需要任何额外配置�?
### 浏览器模式（需�?Python 3.8+�?
1. 运行 `python scripts/server.py --port 8080`
2. 浏览器访�?`http://localhost:8080`
3. 选择游戏类型（历史穿�?/ 系统文）
4. 选择剧本或创建自定义剧本
5. 输入角色名称
6. 开始游戏！

## 游戏玩法

### 选项模式
AI 生成的剧情末尾会有可点击的选项按钮，点击即可自动发送对应指令�?
### 自由输入
点击 "✏️ 自定义行�? 按钮或在输入框中直接输入你想要做的任何行动�?
### 积分系统
- 初始积分�?000
- 每次互动�?10 �?
## AI 配置

点击首页 "⚙️ AI配置" 按钮�?
1. 选择 AI 服务商（推荐 SiliconFlow，免费额度）
2. 选择合适的模型
3. 填入 API Key
4. 勾�?"启用AI功能"
5. 保存

不配�?AI 也可游玩——系统会使用内置的离线模板�?
### 服务商获�?API Key
- **SiliconFlow**: https://cloud.siliconflow.cn
- **DeepSeek**: https://platform.deepseek.com
- **OpenAI**: https://platform.openai.com

## 存档管理

- 游戏进度自动保存到服务器内存
- 点击 📤 导出�?JSON 文件
- 点击 📥 导入之前导出的存�?
## 命令行参�?
```bash
# 指定端口
python scripts/server.py --port 9090
```

默认端口�?080

## 项目结构

```
互动小说游戏/
├── skills/                # Claude Code 技�?�?  ├── novel-play/        # 游玩引擎
�?  ├── novel-create/      # 剧本创作
�?  └── novel-config/      # AI 配置（浏览器模式用）
├── scripts/server.py      # Python 后端（浏览器模式用）
├── assets/                # 网页前端（浏览器模式用）
├── docs/                  # 文档
├── saves/                 # 存档 + 自定义剧�?├── config.json            # AI 配置
├── install.sh
└── README.md
```
