# 浜掑姩灏忚娓告垙

AI 椹卞姩鐨勪簰鍔ㄥ皬璇存父鎴忓钩鍙帮紝绾?Claude Code Skill 椤圭洰銆?
## 鍒汉鍏嬮殕鍚庢€庝箞寮€濮?
```bash
git clone <repo-url>
cd 浜掑姩灏忚娓告垙
bash install.sh

# 鍦?Claude Code 閲岀洿鎺ョ帺锛堥浂渚濊禆锛?/novel-play
```

## 涓ょ鐜╂硶

| 妯″紡 | 渚濊禆 | 浣撻獙 | 閫傜敤鍦烘櫙 |
|------|------|------|---------|
| 馃挰 **鑱婂ぉ妯″紡**锛堥粯璁わ級 | 鏃?| Claude Code 瀵硅瘽涓洿鎺ョ帺 | 浠讳綍浜猴紝寮€绠卞嵆鐢?|
| 馃寪 **娴忚鍣ㄦā寮?* | Python 3.8+ | 缃戦〉 UI锛屾敮鎸佹墜鏈鸿闂?| 鎯宠鏇村ソ鐨勮瑙夋晥鏋?|

**鑱婂ぉ妯″紡**锛氫綘灏辨槸鍜屾父鎴忎笘鐣屽璇濄€侰laude 鐩存帴鎵紨娓告垙寮曟搸锛岀敓鎴愬墽鎯呫€佹彁渚涢€夐」銆佽窡韪Н鍒嗐€備笉闇€瑕?Python锛屼笉闇€瑕?API Key銆?
**娴忚鍣ㄦā寮?*锛氳繍琛?`python scripts/server.py --port 8080`锛屾墦寮€ `http://localhost:8080`銆傛墜鏈哄悓 WiFi 璁块棶 `http://<鐢佃剳IP>:8080` 涔熻兘鐜┿€?
## 涓変釜 Skill

| Skill | 鍛戒护 | 鍋氫粈涔?| 闇€瑕佷粈涔?|
|-------|------|--------|---------|
| `novel-play` | `/novel-play` | 娓哥帺锛堥粯璁よ亰澶╂ā寮忥級 | 鏃?|
| `novel-create` | `/novel-create` | 鍒涗綔鑷畾涔夊墽鏈?| 鏃?|
| `novel-config` | `/novel-config` | 閰嶇疆娴忚鍣ㄦā寮忕殑 AI | 浠呭湪娴忚鍣ㄦā寮忎笅闇€瑕?|

## 椤圭洰缁撴瀯

```
鈹溾攢鈹€ skills/                # Claude Code 鎶€鑳?鈹?  鈹溾攢鈹€ novel-play/        # 娓哥帺寮曟搸
鈹?  鈹溾攢鈹€ novel-create/      # 鍓ф湰鍒涗綔
鈹?  鈹斺攢鈹€ novel-config/      # AI 閰嶇疆锛堟祻瑙堝櫒妯″紡鐢級
鈹溾攢鈹€ scripts/server.py      # Python 鍚庣锛堟祻瑙堝櫒妯″紡鐢級
鈹溾攢鈹€ assets/                # 缃戦〉鍓嶇锛堟祻瑙堝櫒妯″紡鐢級
鈹溾攢鈹€ docs/                  # 鏂囨。
鈹?  鈹溾攢鈹€ guide.md
鈹?  鈹溾攢鈹€ prompts.md
鈹?  鈹溾攢鈹€ scripts.md
鈹?  鈹溾攢鈹€ prd.md
鈹?  鈹溾攢鈹€ game-engine.md
鈹?  鈹斺攢鈹€ game-systems/      # 鏈潵鍔熻兘璁捐锛堟垬鏂?瀵硅瘽/鑳屽寘/涓栫晫锛?鈹溾攢鈹€ saves/                 # 瀛樻。 + 鑷畾涔夊墽鏈?鈹溾攢鈹€ config.json            # AI 閰嶇疆
鈹溾攢鈹€ install.sh
鈹斺攢鈹€ README.md
```

## 璁稿彲璇?
MIT
