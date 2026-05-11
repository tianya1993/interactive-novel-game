---
name: novel-config
description: >-
  浜掑姩灏忚 AI 閰嶇疆绠＄悊銆傜鐞嗘祻瑙堝櫒妯″紡涓嬬殑 AI 鏈嶅姟鍟嗐€丄PI Key銆佹ā鍨嬮€夋嫨銆?  褰撶敤鎴锋兂瑕侀厤缃?AI銆佽缃?API銆佹洿鎹㈡ā鍨嬨€佷慨鏀规湇鍔″晢鏃惰Е鍙戙€?  锛堜粎娴忚鍣ㄦā寮忛渶瑕侊紝鑱婂ぉ妯″紡鏃犻渶閰嶇疆锛?license: MIT
metadata:
  author: Claude
  version: 2.0.0
  created: 2026-04-18
  last_reviewed: 2026-05-03
  review_interval_days: 90
allowed-tools: Read Write Edit Bash
---

# /novel-config

浣犳槸浜掑姩灏忚鐨?AI 閰嶇疆绠＄悊宸ュ叿銆傝礋璐ｇ鐞?`config.json` 涓殑 AI 鏈嶅姟璁剧疆銆?
> **娉ㄦ剰锛?* 姝ら厤缃粎鐢ㄤ簬娴忚鍣ㄦā寮忥紙`/novel-play` 鈫?娴忚鍣級銆傝亰澶╂ā寮忕敱 Claude 鐩存帴椹卞姩锛屼笉闇€瑕佸閮?AI API銆?
## 瑙﹀彂绀轰緥

```
/novel-config                鈫?鏌ョ湅/淇敼閰嶇疆
閰嶇疆AI                      鈫?瑙﹀彂
璁剧疆API Key                 鈫?瑙﹀彂
鏇存崲妯″瀷                    鈫?瑙﹀彂
AI璁剧疆                      鈫?瑙﹀彂
```

## 閰嶇疆鏂囦欢

鎵€鏈夐厤缃瓨鍌ㄥ湪椤圭洰鏍圭洰褰曠殑 `config.json`锛?
```json
{
  "provider": "siliconflow",
  "model": "deepseek-ai/DeepSeek-V2.5",
  "apiKey": "",
  "customApiUrl": "",
  "useAI": true
}
```

## 宸ヤ綔娴?
### 0. 妯″紡鎻愰啋

杩涘叆鏃跺厛绠€鐭彁閱掞細"AI 閰嶇疆浠呮祻瑙堝櫒妯″紡闇€瑕併€傚鏋滀綘鐢ㄨ亰澶╂ā寮忥紙`/novel-play` 鐩存帴鍦ㄥ璇濅腑鐜╋級锛屼笉闇€瑕侀厤缃紝Claude 鏈韩灏辨槸 AI銆傜户缁厤缃紵"

鐢ㄦ埛纭缁х画鍚庢墠杩涘叆姝ラ 1銆?
### 1. 鏌ョ湅褰撳墠閰嶇疆

璇诲彇 `config.json`锛屽睍绀哄綋鍓嶈缃細

```
褰撳墠 AI 閰嶇疆锛?- 鏈嶅姟鍟嗭細SiliconFlow
- 妯″瀷锛歞eepseek-ai/DeepSeek-V2.5
- API Key锛氬凡璁剧疆 **** / 鏈缃?- AI 鐘舵€侊細宸插惎鐢?/ 宸茬鐢?```

**杈圭晫澶勭悊锛?*
- `config.json` 涓嶅瓨鍦細浣跨敤榛樿鍊煎垱寤烘柊鏂囦欢
- `config.json` 鍐呭鎹熷潖锛圝SON瑙ｆ瀽澶辫触锛夛細鎻愮ず鐢ㄦ埛锛屽浠芥崯鍧忔枃浠朵负 `config.json.bak`锛屼娇鐢ㄩ粯璁ら厤缃噸寤?- 淇濆瓨鍓嶆鏌ワ細濡傛灉 `useAI` 涓?`true` 浣?`apiKey` 涓虹┖锛屽彂鍑鸿鍛婏細"AI 宸插惎鐢ㄤ絾 API Key 鏈缃紝娓告垙灏嗘棤娉曚娇鐢?AI銆傝鍏堣缃?API Key锛屾垨鍏抽棴 AI 浣跨敤绂荤嚎妯℃澘銆?
- 纭繚 `scripts/server.py` 瀛樺湪锛堟祻瑙堝櫒妯″紡渚濊禆姝ゆ枃浠讹級锛屽鏋滀笉瀛樺湪鍒欐彁閱掔敤鎴?
### 2. 閫愰」淇敼

璇㈤棶鐢ㄦ埛瑕佷慨鏀瑰摢涓€椤癸紝閫愰」澶勭悊锛屼笉瑕佷竴涓嬪瓙鍏ㄩ棶锛?
#### AI 鏈嶅姟鍟?(`provider`)
- `siliconflow` 鈥?SiliconFlow锛堟帹鑽愶紝鍏嶈垂棰濆害锛屾棤闇€缈诲锛?- `deepseek` 鈥?DeepSeek 瀹樻柟
- `openai` 鈥?OpenAI
- `custom` 鈥?鑷畾涔?OpenAI 鍏煎 API

**鍒囨崲鏈嶅姟鍟嗘椂锛屽厛灞曠ず褰撳墠鏈嶅姟鍟嗗拰灏嗚鍒囨崲鍒扮殑鏈嶅姟鍟嗭紝纭鍚庡啀鎵ц銆?* 鍥犱负鍒囨崲鏈嶅姟鍟嗗悗褰撳墠妯″瀷鍙兘涓嶅吋瀹癸紝闇€瑕佷竴骞舵洿鏂版ā鍨嬨€?
#### API Key
- 寮曞鐢ㄦ埛鍘诲搴斿钩鍙拌幏鍙栵細
  - SiliconFlow: https://cloud.siliconflow.cn
  - DeepSeek: https://platform.deepseek.com
  - OpenAI: https://platform.openai.com
- 杈撳叆鏃朵笉瑕佸洖鏄惧畬鏁?Key
- **淇敼 API Key 鍚庯紝鍦ㄤ繚瀛樺墠鍚戠敤鎴峰睍绀轰慨鏀规憳瑕侊紝纭鍚庡啀淇濆瓨**

#### 妯″瀷閫夋嫨
- SiliconFlow 鎺ㄨ崘: `deepseek-ai/DeepSeek-V2.5`
- DeepSeek 鎺ㄨ崘: `deepseek-chat`
- OpenAI 鎺ㄨ崘: `gpt-4o-mini`

#### 鑷畾涔?API URL锛堜粎 `custom` 鏈嶅姟鍟嗛渶瑕侊級
- 蹇呴』鏄畬鏁?URL锛屼互 `https://` 寮€澶?- 鏍煎紡鏍￠獙锛氬繀椤讳互 `/v1/chat/completions` 鎴栫被浼艰矾寰勭粨灏?- 濡傛灉鏍煎紡涓嶅悎娉曪紝鎻愮ず骞惰姹備慨鏀?
#### 鍚敤/绂佺敤 AI
- `useAI: true` 鈥?浣跨敤澶栭儴 AI 鐢熸垚鍔ㄦ€佸墽鎯?- `useAI: false` 鈥?浣跨敤绂荤嚎妯℃澘锛堟棤闇€ API Key锛?
**淇敼 AI 寮€鍏冲墠锛屽厛鍚戠敤鎴风‘璁?*锛氬紑鍏?AI 浼氱洿鎺ュ奖鍝嶆父鎴忎綋楠屸€斺€旂鐢ㄥ悗鍓ф儏鐢辩绾挎ā鏉跨敓鎴愶紝瀵硅瘽璐ㄩ噺涓嬮檷锛涘惎鐢ㄤ絾 API 涓嶅彲鐢ㄥ垯浼氬鑷磋姹傚け璐ャ€?
### 3. 纭骞朵繚瀛?
淇敼瀹屾垚鍚庯紝灞曠ず淇敼鎽樿锛?
```
鍗冲皢淇敼锛?- 鏈嶅姟鍟嗭細SiliconFlow 鈫?DeepSeek
- 妯″瀷锛氫笉鍙?- API Key锛氭柊璁剧疆 ****

纭淇濆瓨锛?鏄?鍚?
```

鐢ㄦ埛纭鍚庡啓鍏?`config.json`銆傞厤缃嵆鏃剁敓鏁堬紝鏃犻渶閲嶅惎鏈嶅姟鍣ㄣ€?
### 4. 楠岃瘉锛堝彲閫夛級

璇㈤棶鐢ㄦ埛鏄惁闇€瑕佹祴璇曡繛鎺ャ€傚鏋滅敤鎴峰悓鎰忥紝鐢ㄥ綋鍓嶉厤缃彂閫佷竴鏉＄畝鐭祴璇曟秷鎭紝楠岃瘉 API 鏄惁鍙敤銆?
**杈圭晫澶勭悊锛?*
- 娴嬭瘯澶辫触锛?01/403锛夛細鎻愮ず API Key 鏃犳晥
- 娴嬭瘯澶辫触锛堢綉缁滈敊璇級锛氭彁绀烘鏌ョ綉缁滃拰 URL
- 娴嬭瘯澶辫触锛堣秴鏃讹級锛氬缓璁洿鎹㈡湇鍔″晢鎴栫◢鍚庨噸璇?- 娴嬭瘯瓒呮椂瓒呰繃 15 绉掕嚜鍔ㄦ斁寮?
### 5. 鍒囨崲鍥炶亰澶╂ā寮?
濡傛灉鐢ㄦ埛瑙夊緱娴忚鍣ㄦā寮忛厤缃お楹荤儲锛屼富鍔ㄦ彁閱掞細
- 鑱婂ぉ妯″紡鐩存帴鐢?`/novel-play` 灏辫锛屼笉闇€瑕佷换浣曢厤缃?- Claude 鏈韩灏辨槸 AI锛岃亰澶╂ā寮忎綋楠屼笉姣斿閮?API 宸?
## 娉ㄦ剰

- `apiKey` 鏄晱鎰熶俊鎭紝`config.json` 宸插姞鍏?`.gitignore`锛屼笉浼氳 git 杩借釜
- 鐢ㄦ埛涔熷彲浠ラ€氳繃娴忚鍣ㄩ〉闈㈠唴鐨?"鈿欙笍 AI閰嶇疆" 鎸夐挳淇敼閰嶇疆
- 娴忚鍣ㄦā寮忛渶瑕佸厛杩愯 `python scripts/server.py`锛岄厤缃彧鍦ㄦ湇鍔″櫒鍚姩鍚庣敓鏁?