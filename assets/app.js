/**
 * 浜掑姩灏忚娓告垙 - 鍓嶇 UI
 * 鎵€鏈夋父鎴忛€昏緫鐢卞悗绔?Python 鏈嶅姟鍣ㄥ鐞嗭紝鍓嶇鍙礋璐ｇ晫闈氦浜? */

// ============ 鍏ㄥ眬鐘舵€?============
let gameId = null;
let gameType = null;
let currentScript = null;
let isCustom = false;

// ============ API 璋冪敤 ============
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

// ============ UI 杈呭姪 ============
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

// ============ 瑙ｆ瀽閫夐」鐢熸垚鎸夐挳 ============
function parseOptions(message) {
  const optionPattern = /锛堣緭鍏锛?]\s*([^锛塢+)锛?g;
  let processedMessage = message;
  const options = [];
  const seenCommands = new Set();

  let match;
  while ((match = optionPattern.exec(message)) !== null) {
    const command = match[1].trim();
    const beforeMatch = message.substring(0, match.index);
    const lineStart = beforeMatch.lastIndexOf('\n') + 1;
    const currentLine = beforeMatch.substring(lineStart);
    const textMatch = currentLine.match(/^(?:\d+\.\s*)?(.+?)(?:\s*[锛?]杈撳叆)/);
    let text = currentLine.trim() || command;
    if (textMatch) text = textMatch[1].trim();
    // 鑷敱杈撳叆鎸夐挳鐢ㄥ弸濂芥枃瀛?    if (command === '鑷敱杈撳叆' || command === '__CUSTOM__') text = '鑷畾涔夎鍔?;

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

// ============ 娑堟伅娓叉煋 ============
function addDialogueEntry(sender, message, id) {
  const historyDiv = document.getElementById('dialogue-history');
  if (!historyDiv) return;

  const item = document.createElement('div');
  item.className = `dialogue-item dialogue-${sender === '浣? ? 'user' : 'ai'}`;
  if (id) item.id = id;

  let processedMessage = message;
  if (sender === 'AI' || sender === '绯荤粺') {
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

// ============ 涓昏彍鍗曢€昏緫 ============
async function showScriptList(type) {
  gameType = type;
  document.getElementById('script-list-title').textContent =
    type === 'history' ? '鍘嗗彶绌胯秺鍓ф湰' : '绯荤粺鏂囧墽鏈?;

  // 浠庢湇鍔″櫒鍔犺浇鍓ф湰鍒楄〃
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
    // 鑷畾涔夊墽鏈?    hide('script-list-modal');
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

// ============ 娓告垙鍚姩 ============
async function confirmName() {
  const playerName = document.getElementById('player-name-input').value.trim() || '鏃犲悕鐜╁';

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
    addDialogueEntry('绯荤粺', result.intro);
    updateScore(result.state.score);
  } catch (e) {
    addDialogueEntry('绯荤粺', `鍚姩澶辫触: ${e.message}`);
  }
}

async function startCustomGame() {
  const gameName = document.getElementById('custom-game-name').value.trim() || '鑷畾涔夊墽鏈?;
  const gameDesc = document.getElementById('custom-game-desc').value.trim();
  const playerName = document.getElementById('custom-player-name').value.trim() || '鏃犲悕鐜╁';

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
    addDialogueEntry('绯荤粺', result.intro);
    updateScore(result.state.score);
  } catch (e) {
    addDialogueEntry('绯荤粺', `鍚姩澶辫触: ${e.message}`);
  }

  // 娓呯┖琛ㄥ崟
  document.getElementById('custom-game-name').value = '';
  document.getElementById('custom-game-desc').value = '';
  document.getElementById('custom-player-name').value = '';
}

// ============ 鍙戦€佹秷鎭?============
async function sendMessage() {
  const input = document.getElementById('user-input');
  if (!input) return;
  const message = input.value.trim();
  if (!message) return;

  input.value = '';

  // 鏄剧ず鐢ㄦ埛娑堟伅
  addDialogueEntry('浣?, message);

  // 鍔犺浇涓?  const loadingId = 'loading-' + Date.now();
  addDialogueEntry('绯荤粺', 'AI姝ｅ湪鎬濊€冧腑...', loadingId);

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
    addDialogueEntry('绯荤粺', `閿欒: ${e.message}`);
  }
}

// ============ 閫夐」鐐瑰嚮 ============
function selectOption(command) {
  const input = document.getElementById('user-input');
  if (!input) return;
  input.value = command;
  setTimeout(() => sendMessage(), 10);
}

function focusInput() {
  const input = document.getElementById('user-input');
  input.focus();
  input.placeholder = '璇疯緭鍏ヤ綘鎯冲仛鐨勮鍔?..';
  input.value = '';
}

// ============ 瀛樻。绠＄悊 ============
async function exportSave() {
  try {
    const result = await API.post('/api/game/export', { gameId });
    const blob = new Blob([JSON.stringify(result, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `瀛樻。_${new Date().toLocaleDateString()}.json`;
    a.click();
    URL.revokeObjectURL(url);
  } catch (e) {
    alert('瀵煎嚭澶辫触: ' + e.message);
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
      // 閲嶅缓鐣岄潰
      document.getElementById('dialogue-history').innerHTML = '';
      document.getElementById('main-header').style.display = 'none';
      show('game-interface');
      showFlex('player-hud');
      document.getElementById('hud-player-name').textContent = result.state.playerName || '鍐掗櫓鑰?;
      updateScore(result.state.score);
      (result.state.history || []).forEach(h => {
        addDialogueEntry(h.sender, h.message);
      });
      alert('瀛樻。瀵煎叆鎴愬姛锛?);
    } catch (e) {
      alert('瀵煎叆澶辫触: ' + e.message);
    }
  };
  input.click();
}

// ============ AI 璁剧疆 ============
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
    // 浣跨敤榛樿鍊?    document.getElementById('ai-provider-select').value = 'siliconflow';
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
    infoDiv.innerHTML = '璇疯緭鍏ヨ嚜瀹氫箟API鐨勫畬鏁碪RL鍦板潃';
    modelSelect.innerHTML = '<option value="">榛樿妯″瀷</option>';
    modelSelect.disabled = true;
  } else {
    customUrlDiv.style.display = 'none';
    const urls = { siliconflow: 'https://cloud.siliconflow.cn', deepseek: 'https://platform.deepseek.com', openai: 'https://platform.openai.com' };
    infoDiv.innerHTML = `鍓嶅線 <a href="${urls[provider]}" target="_blank" style="color: var(--primary);">瀹樼綉</a> 鐢宠 API Key`;
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
    alert(useAI && apiKey ? 'AI鍔熻兘宸插惎鐢紒' : '宸插垏鎹㈠埌棰勮妯″紡銆傝緭鍏PI Key鍙惎鐢ˋI鍔熻兘銆?);
    closeSettings();
  } catch (e) {
    alert('淇濆瓨澶辫触: ' + e.message);
  }
}

function closeSettings() {
  hide('ai-settings-modal');
}

// ============ 瀵艰埅 ============
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
  if (confirm('纭畾瑕佽繑鍥為椤靛悧锛熷綋鍓嶆父鎴忚繘搴﹀皢浼氫涪澶便€?)) {
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

// ============ 椤甸潰鍒濆鍖?============
document.addEventListener('DOMContentLoaded', () => {
  console.log('浜掑姩灏忚娓告垙骞冲彴宸插姞杞?(v2.0)');

  // 娓告垙绫诲瀷鍗＄墖鐐瑰嚮
  document.querySelectorAll('.game-card').forEach(card => {
    card.addEventListener('click', () => {
      const type = card.dataset.type;
      if (type) showScriptList(type);
    });
  });

  // 鍓ф湰鍗＄墖鐐瑰嚮锛堜簨浠跺鎵橈級
  document.getElementById('script-list-content').addEventListener('click', (e) => {
    const card = e.target.closest('.script-card');
    if (card) selectScript(card.dataset.scriptId);
  });

  // 閫夐」鎸夐挳鐐瑰嚮锛堜簨浠跺鎵橈級
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

  // 绉诲姩绔Е鎽告敮鎸?  document.addEventListener('touchend', (e) => {
    const btn = e.target.closest('.option-btn');
    if (!btn) return;
    e.preventDefault();
    if (btn.dataset.action === 'focus') {
      focusInput();
    } else if (btn.dataset.command) {
      selectOption(decodeURIComponent(btn.dataset.command));
    }
  });

  // 鍥炶溅鍙戦€?  document.getElementById('user-input').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
  });

  // 鍙戦€佹寜閽?  const sendBtn = document.getElementById('send-btn');
  sendBtn.addEventListener('click', (e) => {
    e.preventDefault();
    sendMessage();
  });
  sendBtn.addEventListener('touchend', (e) => {
    e.preventDefault();
    sendMessage();
  });
});
