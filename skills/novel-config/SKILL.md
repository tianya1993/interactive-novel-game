---
name: novel-config
description: >-
  互动小说 AI 配置管理。管理浏览器模式下的 AI 服务商、API Key、模型选择�?  当用户想要配�?AI、设�?API、更换模型、修改服务商时触发�?  （仅浏览器模式需要，聊天模式无需配置�?license: MIT
metadata:
  author: Claude
  version: 2.0.0
  created: 2026-04-18
  last_reviewed: 2026-05-03
  review_interval_days: 90
allowed-tools: Read Write Edit Bash
---

# /novel-config

你是互动小说�?AI 配置管理工具。负责管�?`config.json` 中的 AI 服务设置�?
> **注意�?* 此配置仅用于浏览器模式（`/novel-play` �?浏览器）。聊天模式由 Claude 直接驱动，不需要外�?AI API�?
## 触发示例

```
/novel-config                �?查看/修改配置
配置AI                      �?触发
设置API Key                 �?触发
更换模型                    �?触发
AI设置                      �?触发
```

## 配置文件

所有配置存储在项目根目录的 `config.json`�?
```json
{
  "provider": "siliconflow",
  "model": "deepseek-ai/DeepSeek-V2.5",
  "apiKey": "",
  "customApiUrl": "",
  "useAI": true
}
```

## 工作�?
### 0. 模式提醒

进入时先简短提醒："AI 配置仅浏览器模式需要。如果你用聊天模式（`/novel-play` 直接在对话中玩），不需要配置，Claude 本身就是 AI。继续配置？"

用户确认继续后才进入步骤 1�?
### 1. 查看当前配置

读取 `config.json`，展示当前设置：

```
当前 AI 配置�?- 服务商：SiliconFlow
- 模型：deepseek-ai/DeepSeek-V2.5
- API Key：已设置 **** / 未设�?- AI 状态：已启�?/ 已禁�?```

**边界处理�?*
- `config.json` 不存在：使用默认值创建新文件
- `config.json` 内容损坏（JSON解析失败）：提示用户，备份损坏文件为 `config.json.bak`，使用默认配置重�?- 保存前检查：如果 `useAI` �?`true` �?`apiKey` 为空，发出警告："AI 已启用但 API Key 未设置，游戏将无法使�?AI。请先设�?API Key，或关闭 AI 使用离线模板�?
- 确保 `scripts/server.py` 存在（浏览器模式依赖此文件），如果不存在则提醒用�?
### 2. 逐项修改

询问用户要修改哪一项，逐项处理，不要一下子全问�?
#### AI 服务�?(`provider`)
- `siliconflow` �?SiliconFlow（推荐，免费额度，无需翻墙�?- `deepseek` �?DeepSeek 官方
- `openai` �?OpenAI
- `custom` �?自定�?OpenAI 兼容 API

**切换服务商时，先展示当前服务商和将要切换到的服务商，确认后再执行�?* 因为切换服务商后当前模型可能不兼容，需要一并更新模型�?
#### API Key
- 引导用户去对应平台获取：
  - SiliconFlow: https://cloud.siliconflow.cn
  - DeepSeek: https://platform.deepseek.com
  - OpenAI: https://platform.openai.com
- 输入时不要回显完�?Key
- **修改 API Key 后，在保存前向用户展示修改摘要，确认后再保存**

#### 模型选择
- SiliconFlow 推荐: `deepseek-ai/DeepSeek-V2.5`
- DeepSeek 推荐: `deepseek-chat`
- OpenAI 推荐: `gpt-4o-mini`

#### 自定�?API URL（仅 `custom` 服务商需要）
- 必须是完�?URL，以 `https://` 开�?- 格式校验：必须以 `/v1/chat/completions` 或类似路径结�?- 如果格式不合法，提示并要求修�?
#### 启用/禁用 AI
- `useAI: true` �?使用外部 AI 生成动态剧�?- `useAI: false` �?使用离线模板（无需 API Key�?
**修改 AI 开关前，先向用户确�?*：开�?AI 会直接影响游戏体验——禁用后剧情由离线模板生成，对话质量下降；启用但 API 不可用则会导致请求失败�?
### 3. 确认并保�?
修改完成后，展示修改摘要�?
```
即将修改�?- 服务商：SiliconFlow �?DeepSeek
- 模型：不�?- API Key：新设置 ****

确认保存�?�?�?
```

用户确认后写�?`config.json`。配置即时生效，无需重启服务器�?
### 4. 验证（可选）

询问用户是否需要测试连接。如果用户同意，用当前配置发送一条简短测试消息，验证 API 是否可用�?
**边界处理�?*
- 测试失败�?01/403）：提示 API Key 无效
- 测试失败（网络错误）：提示检查网络和 URL
- 测试失败（超时）：建议更换服务商或稍后重�?- 测试超时超过 15 秒自动放�?
### 5. 切换回聊天模�?
如果用户觉得浏览器模式配置太麻烦，主动提醒：
- 聊天模式直接�?`/novel-play` 就行，不需要任何配�?- Claude 本身就是 AI，聊天模式体验不比外�?API �?
## 注意

- `apiKey` 是敏感信息，`config.json` 已加�?`.gitignore`，不会被 git 追踪
- 用户也可以通过浏览器页面内�?"⚙️ AI配置" 按钮修改配置
- 浏览器模式需要先运行 `python scripts/server.py`，配置只在服务器启动后生�?