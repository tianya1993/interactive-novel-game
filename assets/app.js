/**
 * 互动小说游戏 - 前端 UI
 * 所有游戏逻辑由后�?Python 服务器处理，前端只负责界面交�? */

// ============ 全局状�?============
let gameId = null;
let gameType = null;
let currentScript = null;
let isCustom = false;

// ============ API 调用 ============
const API = {
  async get(url) {
    const res = await fetch(url);
    if (!res.ok) throw new Error(await res.text());
    return res.json();
  },
  async post(url, data) {
    const res = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    const json = await res.json();
    if (!res.ok) throw new Error(json.error || res.statusText);
    return json;
  }
};

// ============ UI 辅助 ============
function show(id) {
  const el = document.getElementById(id);
  if (el) el.classList.add('active');
}

function hide(id) {
  const el = document.getElementById(id);
  if (el) el.classList.remove('active');
}

function showFlex(id) {
  const el = document.getElementById(id);
  if (el) el.style.display = 'flex';
}

function hideEl(id) {
  const el = document.getElementById(id);
  if (el) el.style.display = 'none';
}

// ============ 解析选项生成按钮 ============
function parseOptions(message) {
  const optionPattern = /（输入[�?]\s*([^）]+)�?g;
  let processedMessage = message;
  const options = [];
  const seenCommands = new Set();

  let match;
  while ((match = optionPattern.exec(message)) !== null) {
    const command = match[1].trim();
    const beforeMatch = message.substring(0, match.index);
    const lineStart = beforeMatch.lastIndexOf('\n') + 1;
    const currentLine = beforeMatch.substring(lineStart);
    const textMatch = currentLine.match(/^(?:\d+\.\s*)?(.+?)(?:\s*[�?]输入)/);
    let text = currentLine.trim() || command;
    if (textMatch) text = textMatch[1].trim();
    // 自由输入按钮用友好文�?    if (command === '自由输入' || command === '__CUSTOM__') text = '自定义行�?;

    if (!seenCommands.has(command)) {
      seenCommands.add(command);
      options.push({ text, command });
    }
  }

  if (options.length > 0) {
    const buttonsHtml = options.map(opt => {
      const encodedCommand = encodeURIComponent(opt.command);
      return `<button class="option-btn" data-command="${encodedCommand}">${opt.text}</button>`;
    }).join('');
    processedMessage += `\n\n<div class="option-buttons">${buttonsHtml}</div>`;
  }
  return processedMessage;
}

// ============ 消息渲染 ============
function addDialogueEntry(sender, message, id) {
  const historyDiv = document.getElementById('dialogue-history');
  if (!historyDiv) return;

  const item = document.createElement('div');
  item.className = `dialogue-item dialogue-${sender === '�? ? 'user' : 'ai'}`;
  if (id) item.id = id;

  let processedMessage = message;
  if (sender === 'AI' || sender === '系统') {
    processedMessage = parseOptions(message);
  }

  item.innerHTML = `
    <div class="dialogue-label">${sender}</div>
    <div class="dialogue-bubble">${processedMessage.replace(/\n/g, '<br>')}</div>
  `;
  historyDiv.appendChild(item);

  setTimeout(() => {
    historyDiv.scrollTo({ top: historyDiv.scrollHeight, behavior: 'smooth' });
  }, 10);
}

function removeEntry(id) {
  const el = document.getElementById(id);
  if (el) el.remove();
}

function updateScore(score) {
  document.getElementById('score').textContent = score;
}

// ============ 主菜单逻辑 ============
async function showScriptList(type) {
  gameType = type;
  document.getElementById('script-list-title').textContent =
    type === 'history' ? '历史穿越剧本' : '系统文剧�?;

  // 从服务器加载剧本列表
  const scripts = await API.get('/api/scripts');
  const list = scripts[type] || [];

  document.getElementById('script-list-content').innerHTML = list.map(s => `
    <div class="script-card${s.isCreate ? ' create' : ''}" data-script-id="${s.id}">
      <h3>${s.name}</h3>
      <p>${s.desc}</p>
    </div>
  `).join('');

  hideEl('main-menu');
  show('script-list-modal');
}

function closeScriptList() {
  hide('script-list-modal');
  document.getElementById('main-menu').style.display = 'grid';
  gameType = null;
}

async function selectScript(scriptId) {
  const scripts = await API.get('/api/scripts');
  const list = scripts[gameType] || [];
  const script = list.find(s => s.id === scriptId);

  if (script && script.isCreate) {
    // 自定义剧�?    hide('script-list-modal');
    show('custom-game-modal');
    document.getElementById('custom-game-name').focus();
  } else {
    currentScript = script;
    isCustom = false;
    hide('script-list-modal');
    show('name-input-modal');
    document.getElementById('player-name-input').focus();
  }
}

// ============ 游戏启动 ============
async function confirmName() {
  const playerName = document.getElementById('player-name-input').value.trim() || '无名玩家';

  hide('name-input-modal');
  show('game-interface');
  document.getElementById('main-header').style.display = 'none';
  showFlex('player-hud');
  document.getElementById('hud-player-name').textContent = playerName;
  document.getElementById('hud-avatar').textContent = playerName.charAt(0);
  document.getElementById('dialogue-history').innerHTML = '';

  try {
    const result = await API.post('/api/game/start', {
      type: gameType,
      scriptId: currentScript ? currentScript.id : null,
      playerName: playerName,
      isCustom: false
    });
    gameId = result.gameId;
    addDialogueEntry('系统', result.intro);
    updateScore(result.state.score);
  } catch (e) {
    addDialogueEntry('系统', `启动失败: ${e.message}`);
  }
}

async function startCustomGame() {
  const gameName = document.getElementById('custom-game-name').value.trim() || '自定义剧�?;
  const gameDesc = document.getElementById('custom-game-desc').value.trim();
  const playerName = document.getElementById('custom-player-name').value.trim() || '无名玩家';

  hide('custom-game-modal');
  show('game-interface');
  document.getElementById('main-header').style.display = 'none';
  showFlex('player-hud');
  document.getElementById('hud-player-name').textContent = playerName;
  document.getElementById('hud-avatar').textContent = playerName.charAt(0);
  document.getElementById('dialogue-history').innerHTML = '';

  isCustom = true;
  currentScript = null;

  try {
    const result = await API.post('/api/game/start', {
      type: gameType || 'history',
      playerName: playerName,
      isCustom: true,
      customGameName: gameName,
      customGameDesc: gameDesc
    });
    gameId = result.gameId;
    addDialogueEntry('系统', result.intro);
    updateScore(result.state.score);
  } catch (e) {
    addDialogueEntry('系统', `启动失败: ${e.message}`);
  }

  // 清空表单
  document.getElementById('custom-game-name').value = '';
  document.getElementById('custom-game-desc').value = '';
  document.getElementById('custom-player-name').value = '';
}

// ============ 发送消�?============
async function sendMessage() {
  const input = document.getElementById('user-input');
  if (!input) return;
  const message = input.value.trim();
  if (!message) return;

  input.value = '';

  // 显示用户消息
  addDialogueEntry('�?, message);

  // 加载�?  const loadingId = 'loading-' + Date.now();
  addDialogueEntry('系统', 'AI正在思考中...', loadingId);

  try {
    const result = await API.post('/api/game/action', {
      gameId: gameId,
      message: message
    });
    removeEntry(loadingId);
    addDialogueEntry('AI', result.reply);
    updateScore(result.score);
  } catch (e) {
    removeEntry(loadingId);
    addDialogueEntry('系统', `错误: ${e.message}`);
  }
}

// ============ 选项点击 ============
function selectOption(command) {
  const input = document.getElementById('user-input');
  if (!input) return;
  input.value = command;
  setTimeout(() => sendMessage(), 10);
}

function focusInput() {
  const input = document.getElementById('user-input');
  input.focus();
  input.placeholder = '请输入你想做的行�?..';
  input.value = '';
}

// ============ 存档管理 ============
async function exportSave() {
  try {
    const result = await API.post('/api/game/export', { gameId });
    const blob = new Blob([JSON.stringify(result, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `存档_${new Date().toLocaleDateString()}.json`;
    a.click();
    URL.revokeObjectURL(url);
  } catch (e) {
    alert('导出失败: ' + e.message);
  }
}

function importSave() {
  const input = document.createElement('input');
  input.type = 'file';
  input.accept = '.json';
  input.onchange = async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    try {
      const text = await file.text();
      const saveData = JSON.parse(text);
      const result = await API.post('/api/game/import', saveData);
      gameId = result.gameId;
      // 重建界面
      document.getElementById('dialogue-history').innerHTML = '';
      document.getElementById('main-header').style.display = 'none';
      show('game-interface');
      showFlex('player-hud');
      document.getElementById('hud-player-name').textContent = result.state.playerName || '冒险�?;
      updateScore(result.state.score);
      (result.state.history || []).forEach(h => {
        addDialogueEntry(h.sender, h.message);
      });
      alert('存档导入成功�?);
    } catch (e) {
      alert('导入失败: ' + e.message);
    }
  };
  input.click();
}

// ============ AI 设置 ============
const PROVIDER_INFO = {
  siliconflow: { models: ['deepseek-ai/DeepSeek-V2.5', 'Qwen/Qwen2.5-72B-Instruct', 'THUDM/glm-4-9b-chat'], defaultModel: 'deepseek-ai/DeepSeek-V2.5' },
  deepseek: { models: ['deepseek-chat', 'deepseek-reasoner'], defaultModel: 'deepseek-chat' },
  openai: { models: ['gpt-4o', 'gpt-4o-mini', 'gpt-3.5-turbo'], defaultModel: 'gpt-4o-mini' },
  custom: { models: [], defaultModel: '' }
};

async function openSettings() {
  show('ai-settings-modal');
  try {
    const cfg = await API.get('/api/config');
    document.getElementById('api-key-input').value = '';
    document.getElementById('use-ai-checkbox').checked = cfg.useAI !== false;
    document.getElementById('ai-provider-select').value = cfg.provider || 'siliconflow';
    onProviderChange();
    if (cfg.provider === 'custom') {
      document.getElementById('custom-api-url').value = cfg.customApiUrl || '';
    }
  } catch (e) {
    // 使用默认�?    document.getElementById('ai-provider-select').value = 'siliconflow';
    onProviderChange();
  }
}

function onProviderChange() {
  const provider = document.getElementById('ai-provider-select').value;
  const customUrlDiv = document.getElementById('custom-api-url-div');
  const infoDiv = document.getElementById('provider-info');
  const modelSelect = document.getElementById('ai-model-select');

  if (provider === 'custom') {
    customUrlDiv.style.display = 'block';
    infoDiv.innerHTML = '请输入自定义API的完整URL地址';
    modelSelect.innerHTML = '<option value="">默认模型</option>';
    modelSelect.disabled = true;
  } else {
    customUrlDiv.style.display = 'none';
    const urls = { siliconflow: 'https://cloud.siliconflow.cn', deepseek: 'https://platform.deepseek.com', openai: 'https://platform.openai.com' };
    infoDiv.innerHTML = `前往 <a href="${urls[provider]}" target="_blank" style="color: var(--primary);">官网</a> 申请 API Key`;
    const info = PROVIDER_INFO[provider] || { models: [], defaultModel: '' };
    modelSelect.innerHTML = info.models.map(m =>
      `<option value="${m}" ${m === info.defaultModel ? 'selected' : ''}>${m}</option>`
    ).join('');
    modelSelect.disabled = false;
  }
}

async function saveSettings() {
  const provider = document.getElementById('ai-provider-select').value;
  const model = document.getElementById('ai-model-select').value;
  const apiKey = document.getElementById('api-key-input').value.trim();
  const useAI = document.getElementById('use-ai-checkbox').checked;
  const customApiUrl = document.getElementById('custom-api-url').value.trim();

  try {
    await API.post('/api/config', { provider, model, apiKey, useAI, customApiUrl });
    alert(useAI && apiKey ? 'AI功能已启用！' : '已切换到预设模式。输入API Key可启用AI功能�?);
    closeSettings();
  } catch (e) {
    alert('保存失败: ' + e.message);
  }
}

function closeSettings() {
  hide('ai-settings-modal');
}

// ============ 导航 ============
function backToMenu() {
  hide('game-interface');
  document.getElementById('main-menu').style.display = 'grid';
  document.getElementById('main-header').style.display = 'block';
  document.getElementById('dialogue-history').innerHTML = '';
  hideEl('player-hud');
  gameId = null;
  gameType = null;
  currentScript = null;
  isCustom = false;
}

function returnToHome() {
  if (confirm('确定要返回首页吗？当前游戏进度将会丢失�?)) {
    backToMenu();
  }
}

function backToMenuFromNameInput() {
  hide('name-input-modal');
  document.getElementById('main-menu').style.display = 'grid';
  document.getElementById('main-header').style.display = 'block';
  gameType = null;
  currentScript = null;
}

function closeCustomGameModal() {
  hide('custom-game-modal');
  document.getElementById('main-menu').style.display = 'grid';
  document.getElementById('main-header').style.display = 'block';
  gameType = null;
  isCustom = false;
}

// ============ 页面初始�?============
document.addEventListener('DOMContentLoaded', () => {
  console.log('互动小说游戏平台已加�?(v2.0)');

  // 游戏类型卡片点击
  document.querySelectorAll('.game-card').forEach(card => {
    card.addEventListener('click', () => {
      const type = card.dataset.type;
      if (type) showScriptList(type);
    });
  });

  // 剧本卡片点击（事件委托）
  document.getElementById('script-list-content').addEventListener('click', (e) => {
    const card = e.target.closest('.script-card');
    if (card) selectScript(card.dataset.scriptId);
  });

  // 选项按钮点击（事件委托）
  document.addEventListener('click', (e) => {
    const btn = e.target.closest('.option-btn');
    if (!btn) return;
    e.preventDefault();
    if (btn.dataset.action === 'focus') {
      focusInput();
    } else if (btn.dataset.command) {
      selectOption(decodeURIComponent(btn.dataset.command));
    }
  });

  // 移动端触摸支�?  document.addEventListener('touchend', (e) => {
    const btn = e.target.closest('.option-btn');
    if (!btn) return;
    e.preventDefault();
    if (btn.dataset.action === 'focus') {
      focusInput();
    } else if (btn.dataset.command) {
      selectOption(decodeURIComponent(btn.dataset.command));
    }
  });

  // 回车发�?  document.getElementById('user-input').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
  });

  // 发送按�?  const sendBtn = document.getElementById('send-btn');
  sendBtn.addEventListener('click', (e) => {
    e.preventDefault();
    sendMessage();
  });
  sendBtn.addEventListener('touchend', (e) => {
    e.preventDefault();
    sendMessage();
  });
});
