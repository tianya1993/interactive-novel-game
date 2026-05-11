#!/usr/bin/env python3
"""浜掑姩灏忚娓告垙 - 鏈湴 HTTP 鏈嶅姟鍣?
闆堕澶栦緷璧栵紝绾?Python 鏍囧噯搴撳疄鐜般€?鍚姩鍚庤闂?http://localhost:8080 鍗冲彲娓哥帺銆?"""

import json
import os
import re
import sys
import time
import uuid
import urllib.request
import urllib.error
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path

# ---------- 椤圭洰鏍圭洰褰?----------
ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
SAVES = ROOT / "saves"
CONFIG_FILE = ROOT / "config.json"

SAVES.mkdir(exist_ok=True)

# ---------- 榛樿閰嶇疆 ----------
DEFAULT_CONFIG = {
    "provider": "siliconflow",
    "model": "deepseek-ai/DeepSeek-V2.5",
    "apiKey": "",
    "customApiUrl": "",
    "useAI": True
}

# ---------- AI Provider 閰嶇疆 ----------
PROVIDERS = {
    "siliconflow": {
        "name": "SiliconFlow",
        "url": "https://api.siliconflow.cn/v1/chat/completions",
        "models": ["deepseek-ai/DeepSeek-V2.5", "Qwen/Qwen2.5-72B-Instruct", "THUDM/glm-4-9b-chat"],
        "defaultModel": "deepseek-ai/DeepSeek-V2.5",
        "maxTokens": 2000,
        "temperature": 0.7
    },
    "deepseek": {
        "name": "DeepSeek",
        "url": "https://api.deepseek.com/v1/chat/completions",
        "models": ["deepseek-chat", "deepseek-reasoner"],
        "defaultModel": "deepseek-chat",
        "maxTokens": 2000,
        "temperature": 0.7
    },
    "openai": {
        "name": "OpenAI",
        "url": "https://api.openai.com/v1/chat/completions",
        "models": ["gpt-4o", "gpt-4o-mini", "gpt-3.5-turbo"],
        "defaultModel": "gpt-4o-mini",
        "maxTokens": 2000,
        "temperature": 0.7
    },
    "custom": {
        "name": "鑷畾涔堿PI",
        "url": "",
        "models": [],
        "defaultModel": "",
        "maxTokens": 2000,
        "temperature": 0.7
    }
}

# ---------- 棰勮鍓ф湰 ----------
PRESET_SCRIPTS = {
    "history": [
        {
            "id": "history_default",
            "name": "涓滄眽鏈勾",
            "desc": "绌胯秺鍒板叕鍏?84骞达紝榛勫肪璧蜂箟鏃舵湡锛屽湪娲涢槼鍩庡寮€濮嬩綘鐨勫巻鍙插緛绋嬨€?,
            "intro": "浣犳剰澶栫┛瓒婂埌浜嗕笢姹夋湯骞达紙鍏厓184骞达級锛岄粍宸捐捣涔夊垰鍒氱垎鍙戙€備綘鍑虹幇鍦ㄦ礇闃冲煄澶栫殑涓€鐗囪崚閲庝腑锛岃韩涓婂彧鏈夌幇浠ｇ殑琛ｆ湇鍜屼竴浜涢浂閽便€?,
            "type": "history"
        },
        {
            "id": "history_tang",
            "name": "澶у攼鐩涗笘",
            "desc": "绌胯秺鍒拌礊瑙傚勾闂达紝浣撻獙澶у攼鐩涗笘鐨勭箒鍗庝笌椋庝簯銆?,
            "intro": "浣犵┛瓒婂埌浜嗚礊瑙傚勾闂寸殑澶у攼闀垮畨鍩庯紝杩欓噷鏄綋鏃朵笘鐣屼笂鏈€绻佸崕鐨勯兘甯傘€備綘鑳藉惁鍦ㄨ繖涓洓涓栦腑寤哄姛绔嬩笟锛?,
            "type": "history"
        },
        {
            "id": "history_create",
            "name": "鍒涗綔鏂板墽鏈?,
            "desc": "鍙戞尌浣犵殑鎯宠薄鍔涳紝鍒涢€犲睘浜庤嚜宸辩殑鍘嗗彶绌胯秺鏁呬簨銆?,
            "isCreate": True,
            "type": "history"
        }
    ],
    "system": [
        {
            "id": "system_default",
            "name": "绁炵骇閫夋嫨绯荤粺",
            "desc": "缁戝畾绁炵骇閫夋嫨绯荤粺锛岄€氳繃鍋氬嚭閫夋嫨鑾峰緱濂栧姳锛岃蛋涓婁汉鐢熷穮宄般€?,
            "intro": "銆愬彯锛佺绾ч€夋嫨绯荤粺婵€娲绘垚鍔燂紒銆戜綘绐佺劧鍚埌鑴戞捣涓搷璧蜂竴涓満姊板０闊筹細\u201c娆㈣繋瀹夸富缁戝畾绁炵骇閫夋嫨绯荤粺锛乗u201d",
            "type": "system"
        },
        {
            "id": "system_signin",
            "name": "绛惧埌鎵撳崱绯荤粺",
            "desc": "姣忓ぉ绛惧埌灏辫兘鑾峰緱濂栧姳锛岃交鏉惧彉寮恒€?,
            "intro": "銆愬彯锛佺鍒版墦鍗＄郴缁熷凡婵€娲伙紒銆戞瘡鏃ョ鍒板彲鑾峰緱涓板帤濂栧姳锛岃繛缁鍒拌繕鏈夐澶栨儕鍠滐紒",
            "type": "system"
        },
        {
            "id": "system_create",
            "name": "鍒涗綔鏂板墽鏈?,
            "desc": "鍙戞尌浣犵殑鎯宠薄鍔涳紝鍒涢€犲睘浜庤嚜宸辩殑绯荤粺鏂囨晠浜嬨€?,
            "isCreate": True,
            "type": "system"
        }
    ]
}

# ---------- System Prompt 妯℃澘 ----------
HISTORY_PROMPT = """浣犳槸涓€涓巻鍙茬┛瓒婇鏉愮殑鏂囧瓧鍐掗櫓娓告垙AI銆傜帺瀹剁┛瓒婂埌浜嗕笢姹夋湯骞达紙鍏厓184骞达級锛岄粍宸捐捣涔夊垰鍒氱垎鍙戯紝澶╀笅澶т贡銆?
銆愪笘鐣岃銆?杩欐槸涓€涓兢闆勫苟璧枫€佽嫳闆勮緢鍑虹殑鏃朵唬銆備綘鎵紨鐨勬槸涓€涓剰澶栫┛瓒婂埌杩欎釜涔变笘鐨勭幇浠ｄ汉锛岃韩涓婂彧鏈夌幇浠ｇ殑鐭ヨ瘑鍜屼竴灏忚閾滈挶銆備綘蹇呴』鍦ㄤ贡涓栦腑姹傜敓瀛樸€佸彂灞曞娍鍔涖€佹敼鍙樺巻鍙层€?
銆愬啓浣滈鏍艰姹傘€?1. 鎻忓啓缁嗚吇鐢熷姩锛屾湁鐢婚潰鎰燂紙鍦烘櫙銆佷汉鐗┿€佹皼鍥达級
2. 鍓ф儏瑕佹湁寮犲姏锛屾湁鎮康锛岃鐜╁鎯崇户缁帺涓嬪幓
3. 鍔犲叆鐪熷疄鐨勫巻鍙插厓绱狅紙浜虹墿銆佷簨浠躲€侀淇楋級
4. 鏍规嵁鐜╁鐨勯€夋嫨缁欏嚭鍚堢悊鐨勫悗鏋?5. 鍙互璁剧疆绐佸彂浜嬩欢鍜屽嵄鏈猴紝澧炲姞娓告垙鎬?6. 姣忎釜鍦烘櫙瑕佹湁鍏蜂綋鐨勫湴鐐规弿鍐?
銆愬洖澶嶆牸寮忚姹傘€?1. 鍥炲鎺у埗鍦?00-300瀛?2. 鎻忚堪褰撳墠鍦烘櫙鍜孨PC鐨勫弽搴?3. 鏄庣‘鍛婅瘔鐜╁褰撳墠鐨勭姸鎬侊紙浣嶇疆銆佸懆鍥寸幆澧冦€侀亣鍒扮殑浜猴級
4. 缁撳熬鎻愪緵2-3涓叿浣撳彲琛岀殑琛屽姩閫夐」
5. 鏍煎紡锛氶€夐」鍚嶇О锛堣緭鍏ワ細鎸囦护锛?6. 鏈€鍚庡姞涓婏細鑷畾涔夎鍔紙杈撳叆锛氳嚜鐢辫緭鍏ワ級

銆愰噸瑕併€?- 浣跨敤绗簩浜虹О"浣?鍙欒堪
- 淇濇寔鍓ф儏杩炶疮锛岃浣忎箣鍓嶇殑瀵硅瘽
- 涓嶈閲嶅涔嬪墠宸茬粡鍙戠敓鐨勪簨浠?""

SYSTEM_PROMPT = """浣犳槸涓€涓郴缁熸枃棰樻潗鐨勬枃瀛楀啋闄╂父鎴廇I銆傜帺瀹剁粦瀹氫簡涓€涓?绁炵骇閫夋嫨绯荤粺"锛岄€氳繃瀹屾垚浠诲姟鑾峰緱濂栧姳锛岃蛋涓婁汉鐢熷穮宄般€?
銆愪笘鐣岃銆?杩欐槸涓€涓厖婊℃満閬囩殑涓栫晫銆傜帺瀹剁粦瀹氱殑"绁炵骇閫夋嫨绯荤粺"浼氬彂甯冨悇绉嶄换鍔″拰閫夋嫨锛屽畬鎴愬悗鑾峰緱绉垎銆佹妧鑳姐€侀亾鍏枫€佺О鍙风瓑濂栧姳銆傜帺瀹朵粠鏅€氫汉寮€濮嬶紝涓€姝ユ鍙樺己锛屾渶缁堟垚涓轰汉鐢熻耽瀹躲€?
銆愬啓浣滈鏍艰姹傘€?1. 鑺傚鏄庡揩锛岀埥鐐瑰瘑闆嗭紝璁╃帺瀹舵劅鍙楀埌鎴愰暱鐨勫揩鎰?2. 绯荤粺鎾姤瑕佹湁浠紡鎰熷拰鎴愬氨鎰?3. 浠诲姟璁捐瑕佹湁瓒ｅ懗鎬э紝涓嶈兘澶噸澶?4. 濂栧姳瑕佹湁鍚稿紩鍔涳紙绁炵骇鎶€鑳姐€佺█鏈夐亾鍏枫€佺壒娈婄О鍙风瓑锛?5. 鍙互鏈夋墦鑴告儏鑺傦紝璁╃帺瀹惰幏寰椾紭瓒婃劅
6. NPC瑕佹湁椴滄槑鐨勬€ф牸鐗圭偣

銆愬洖澶嶆牸寮忚姹傘€?1. 鍥炲鎺у埗鍦?00-300瀛?2. 绯荤粺鎾姤瑕侀啋鐩紙浣跨敤銆愩€戞垨銆愬彯锛併€戞牸寮忥級
3. 鎻忚堪褰撳墠鎯呭喌鍜屼换鍔¤姹?4. 缁撳熬鎻愪緵2-3涓鍔ㄩ€夐」
5. 鏍煎紡锛氶€夐」鍚嶇О锛堣緭鍏ワ細鎸囦护锛夛紝骞舵爣娉ㄥ鍔?6. 鏈€鍚庡姞涓婏細鑷畾涔夎鍔紙杈撳叆锛氳嚜鐢辫緭鍏ワ級

銆愰噸瑕併€?- 浣跨敤绗簩浜虹О"浣?鍙欒堪
- 淇濇寔鐖芥枃椋庢牸锛岃鐜╁鎰熷彈鍒版垚闀跨殑蹇箰
- 濂栧姳瑕佽浜猴紝璁╃帺瀹舵湁鍔ㄥ姏缁х画鐜?""


# ---------- 绂荤嚎鏁呬簨鏁版嵁锛堜粠 JSON 鍔犺浇锛?---------
# 鑺傜偣寮忔晠浜嬪紩鎿?鈥?姣忎釜棰勮鍓ф湰鏈夊畬鏁村墽鎯呮爲銆佸垎鏀€夋嫨銆佸缁撳眬
# 鏁呬簨鏁版嵁瀛樺偍鍦?scripts/stories.json

STORIES_FILE = ROOT / "scripts" / "stories.json"

_all_stories_cache = None


def load_all_stories():
    """鍔犺浇鎵€鏈夋晠浜嬫暟鎹紙甯︾紦瀛橈級"""
    global _all_stories_cache
    if _all_stories_cache is not None:
        return _all_stories_cache
    if STORIES_FILE.exists():
        try:
            with open(STORIES_FILE, "r", encoding="utf-8") as f:
                _all_stories_cache = json.load(f)
            return _all_stories_cache
        except Exception:
            pass
    _all_stories_cache = {}
    return _all_stories_cache


class StoryEngine:
    """鑺傜偣寮忔晠浜嬪紩鎿?鈥?椹卞姩绂荤嚎妯″紡"""

    @staticmethod
    def _get_story(script):
        """鏍规嵁鍓ф湰鑾峰彇鏁呬簨鏁版嵁"""
        if script and script.get("id"):
            stories = load_all_stories()
            return stories.get(script["id"])
        return None

    @staticmethod
    def intro(script=None):
        """杩斿洖鍓ф湰寮€鍦虹櫧"""
        story = StoryEngine._get_story(script)
        if story and "start" in story:
            return StoryEngine._render_node(story["start"])
        if script:
            return script.get("intro", "娆㈣繋鏉ュ埌浜掑姩灏忚涓栫晫銆?)
        return "娆㈣繋鏉ュ埌浜掑姩灏忚涓栫晫銆傝杈撳叆琛屽姩鎸囦护寮€濮嬫父鎴忋€?

    @staticmethod
    def _render_node(node):
        """娓叉煋鑺傜偣鏂囨湰 + 閫夐」"""
        text = node["text"]
        options = node.get("options", [])
        if options:
            lines = [f"{i+1}. {opt['text']}锛堣緭鍏ワ細{opt.get('cmd', opt['text'])}锛?
                     for i, opt in enumerate(options) if opt.get("cmd")]
            text += "\n\n" + "\n".join(lines)
            # 鍔犺嚜鐢辫鍔ㄦ彁绀?            text += "\n\n鎴栬€咃紝浣犳兂鍋氫粈涔堢洿鎺ュ憡璇夋垜銆?
        return text

    @staticmethod
    def process(user_input, script=None, state=None):
        """澶勭悊鐢ㄦ埛杈撳叆锛屾帹杩涙晠浜嬭妭鐐广€?        杩斿洖 (reply_text, next_node_id, flags_to_set)
        flags_to_set 浼氬悎骞跺埌 state["storyFlags"] 涓€?        """
        current_node_id = state.get("storyNode", "start") if state else "start"
        story = StoryEngine._get_story(script)

        if not story:
            # 娌℃湁鏁呬簨鏁版嵁 鈥?鍏滃簳
            return (f"浣犲喅瀹氾細{user_input}\n\n锛堝綋鍓嶅墽鏈殏鏃犵绾垮墽鎯咃紝璇烽厤缃?AI 鍚庝綋楠屽姩鎬佸墽鎯呫€傦級\n\n璇疯緭鍏ヤ綘鐨勮鍔ㄦ寚浠ょ户缁?..",
                    current_node_id, {})

        current_node = story.get(current_node_id, story.get("start"))
        if not current_node:
            return (f"鍓ф儏浼间箮璧板埌浜嗗敖澶粹€︹€n\n璇疯緭鍏ャ€岄噸鏂板紑濮嬨€嶆垨銆岄€€鍑恒€嶃€?,
                    current_node_id, {})

        # 鍖归厤鐢ㄦ埛杈撳叆鍒伴€夐」
        input_lower = user_input.strip()
        matched_option = None

        for opt in current_node.get("options", []):
            cmd = opt.get("cmd", "")
            if cmd and cmd in input_lower:
                matched_option = opt
                break

        if not matched_option:
            # 娌″尮閰嶅埌 鈥?灏濊瘯妯＄硦鍖归厤锛堥€夐」鏂囨湰鍦ㄨ緭鍏ヤ腑鍑虹幇锛?            for opt in current_node.get("options", []):
                opt_text = opt.get("text", "")
                if opt_text and opt_text in user_input:
                    matched_option = opt
                    break

        if matched_option:
            next_id = matched_option.get("next")
            flags = matched_option.get("flags", {})
            if next_id and next_id in story:
                next_node = story[next_id]
                # 妫€鏌ユ槸鍚︾粨灞€鑺傜偣
                reply = StoryEngine._render_node(next_node)
                return (reply, next_id, flags)
            elif next_id is None:
                # 閫€鍑轰俊鍙?                return ("鎰熻阿娓哥帺锛佹湡寰呬綘鐨勪笅涓€娆″啋闄┿€俓n\n杈撳叆銆岄噸鏂板紑濮嬨€嶅彲浠ュ啀鏉ヤ竴灞€銆?,
                        current_node_id, {"game_ended": True})

        # 娌″尮閰嶅埌浠讳綍閫夐」 鈥?鎻愮ず褰撳墠鍙€夐」
        reply = f"浣犳兂鍋氫粈涔堝憿锛焅n\n"
        for i, opt in enumerate(current_node.get("options", [])):
            reply += f"{i+1}. {opt['text']}锛堣緭鍏ワ細{opt.get('cmd', opt['text'])}锛塡n"
        reply += "\n鎴栬€呰緭鍏ュ叾浠栦綘鎯冲仛鐨勪簨銆?
        return (reply, current_node_id, {})


# ---------- 閰嶇疆绠＄悊 ----------
def load_config():
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                cfg = json.load(f)
            return {**DEFAULT_CONFIG, **cfg}
        except Exception:
            pass
    return dict(DEFAULT_CONFIG)


def save_config(cfg):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)


# ---------- 鑷畾涔夊墽鏈姞杞?----------
CUSTOM_SCRIPTS_DIR = SAVES / "scripts"


def load_custom_scripts():
    """鎵弿 saves/scripts/ 鐩綍锛屽姞杞芥墍鏈夎嚜瀹氫箟鍓ф湰 JSON 鏂囦欢"""
    custom = {"history": [], "system": []}
    if not CUSTOM_SCRIPTS_DIR.exists():
        return custom
    for f in sorted(CUSTOM_SCRIPTS_DIR.glob("*.json")):
        try:
            with open(f, "r", encoding="utf-8") as fp:
                script = json.load(fp)
            script_type = script.get("type", "history")
            if script_type in custom:
                script["isCustom"] = True
                custom[script_type].append(script)
        except Exception:
            pass  # 璺宠繃鎹熷潖鏂囦欢
    return custom


def get_merged_scripts():
    """鍚堝苟棰勮鍓ф湰 + 鑷畾涔夊墽鏈?""
    preset = {
        "history": list(PRESET_SCRIPTS["history"]),
        "system": list(PRESET_SCRIPTS["system"])
    }
    custom = load_custom_scripts()
    for t in ["history", "system"]:
        preset[t].extend(custom[t])
    return preset


# ---------- 娓告垙鐘舵€侊紙鍐呭瓨涓級 ----------
games = {}  # game_id -> state dict


def new_game_state():
    return {
        "playerName": "",
        "gameType": None,
        "currentScript": None,
        "isCustom": False,
        "customGameName": "",
        "customGameDesc": "",
        "score": 1000,
        "history": [],
        "storyNode": "start",
        "storyFlags": {}
    }


# ---------- 鏋勫缓 Prompt ----------
def build_prompt(state, user_input):
    game_type = state["gameType"]
    script = state.get("currentScript")
    player_name = state["playerName"]
    history = state.get("history", [])
    is_custom = state.get("isCustom", False)

    # 鏈€杩戠殑瀵硅瘽鍘嗗彶
    context = history[-5:] if history else []
    context_str = "\n".join(f"{h['sender']}: {h['message']}" for h in context)

    # 鑷畾涔夊墽鏈?    if is_custom:
        system_msg = f"""浣犳槸涓€涓垱鎰忔枃瀛楀啋闄╂父鎴廇I銆傜帺瀹舵鍦ㄧ帺涓€涓悕涓?{state['customGameName']}"鐨勮嚜瀹氫箟鍓ф湰銆?
銆愬墽鏈瀹?- 蹇呴』涓ユ牸閬靛惊銆?{state['customGameDesc'] or '杩欐槸涓€涓紑鏀句笘鐣岋紝鐜╁鍙互鑷敱鎺㈢储鍜屽垱閫犺嚜宸辩殑鏁呬簨銆?}

銆愮粷瀵圭姝€?- 涓嶈鐢熸垚涓庡墽鏈瀹氭棤鍏崇殑鍐呭
- 涓嶈浣跨敤涓庤瀹氫笉绗︾殑鏃朵唬鑳屾櫙銆佷汉鐗┿€佸湴鐐?- 涓嶈鍋忕鐜╁閫夋嫨鐨勫墽鏈被鍨?
銆愬啓浣滈鏍艰姹傘€?1. 鏍规嵁鍓ф湰绫诲瀷璋冩暣鍐欎綔椋庢牸
2. 鎻忓啓缁嗚吇鐢熷姩锛屾湁鐢婚潰鎰?3. 鍓ф儏瑕佹湁寮犲姏锛屾湁鎮康
4. 鏍规嵁鐜╁鐨勯€夋嫨缁欏嚭鍚堢悊鐨勫悗鏋?
銆愬洖澶嶆牸寮忚姹傘€?1. 鍥炲鎺у埗鍦?00-300瀛?2. 鎻忚堪褰撳墠鍦烘櫙銆丯PC鍜岀帺瀹剁殑鐘舵€?3. 缁撳熬鎻愪緵2-3涓叿浣撶殑琛屽姩閫夐」
4. 鏍煎紡锛氶€夐」鍚嶇О锛堣緭鍏ワ細鎸囦护锛?5. 鏈€鍚庡姞涓婏細鑷畾涔夎鍔紙杈撳叆锛氳嚜鐢辫緭鍏ワ級

銆愰噸瑕併€?- 浣跨敤绗簩浜虹О"浣?鍙欒堪
- 淇濇寔鍓ф儏杩炶疮锛岃浣忎箣鍓嶇殑瀵硅瘽
- 涓ユ牸閬靛惊鍓ф湰璁惧畾锛岀粷涓嶅亸绂?""

    # 棰勮鍓ф湰
    elif script:
        if script["type"] == "history":
            system_msg = f"""浣犳槸涓€涓巻鍙茬┛瓒婇鏉愮殑鏂囧瓧娓告垙AI銆傜帺瀹舵鍦ㄧ帺"{script['name']}"鍓ф湰銆?
鍓ф湰鑳屾櫙锛?{script['desc']}

鍒濆鍦烘櫙锛?{script.get('intro', '')}

瑙勫垯锛?1. 淇濇寔鍘嗗彶鑳屾櫙鐨勭湡瀹炴€у拰涓€鑷存€?2. 鏍规嵁鐜╁鐨勮鍔ㄧ敓鎴愬悎鐞嗙殑鍓ф儏鍙戝睍
3. 姣忔鍥炲鎺у埗鍦?00-300瀛?4. 鍦ㄥ洖澶嶆湯灏炬彁渚?-3涓槑纭殑琛屽姩閫夐」锛屾牸寮忥細閫夐」鍚嶇О锛堣緭鍏ワ細鎸囦护锛?5. 鏈€鍚庝竴瀹氳鍔犱笂锛氳嚜瀹氫箟琛屽姩锛堣緭鍏ワ細鑷敱杈撳叆锛?6. 浣跨敤绗簩浜虹О"浣?鏉ュ彊杩?7. 淇濇寔鍓ф儏杩炶疮鎬э紝璁颁綇涔嬪墠鐨勫璇濆巻鍙?""
        else:
            system_msg = f"""浣犳槸涓€涓郴缁熸枃棰樻潗鐨勬枃瀛楁父鎴廇I銆傜帺瀹舵鍦ㄧ帺"{script['name']}"鍓ф湰銆?
鍓ф湰鑳屾櫙锛?{script['desc']}

鍒濆鍦烘櫙锛?{script.get('intro', '')}

瑙勫垯锛?1. 鏍规嵁鍓ф湰璁惧畾鐢熸垚鍚堢悊鐨勫墽鎯呭彂灞?2. 鍙互閫傚綋鍙戝竷浠诲姟銆佺粰浜堝鍔?3. 姣忔鍥炲鎺у埗鍦?00-300瀛?4. 鍦ㄥ洖澶嶆湯灏炬彁渚?-3涓槑纭殑琛屽姩閫夐」锛屾牸寮忥細閫夐」鍚嶇О锛堣緭鍏ワ細鎸囦护锛?5. 鏈€鍚庝竴瀹氳鍔犱笂锛氳嚜瀹氫箟琛屽姩锛堣緭鍏ワ細鑷敱杈撳叆锛?6. 浣跨敤绗簩浜虹О"浣?鏉ュ彊杩?7. 淇濇寔鐖芥枃椋庢牸锛岃鐜╁鎰熷彈鍒版垚闀垮拰蹇箰
8. 淇濇寔鍓ф儏杩炶疮鎬э紝璁颁綇涔嬪墠鐨勫璇濆巻鍙?""

    # 榛樿绫诲瀷
    elif game_type == "history":
        system_msg = HISTORY_PROMPT
    elif game_type == "system":
        system_msg = SYSTEM_PROMPT
    else:
        system_msg = HISTORY_PROMPT

    return [
        {"role": "system", "content": system_msg},
        {"role": "user", "content": f"鐜╁鍚嶇О锛歿player_name}\n鍘嗗彶瀵硅瘽锛歕n{context_str}\n\n褰撳墠琛屽姩锛歿user_input}"}
    ]


# ---------- 璋冪敤 AI API ----------
def call_ai(messages):
    cfg = load_config()
    provider_key = cfg.get("provider", "siliconflow")
    provider = PROVIDERS.get(provider_key, PROVIDERS["siliconflow"])

    if provider_key == "custom":
        api_url = cfg.get("customApiUrl", "")
    else:
        api_url = provider["url"]

    model = cfg.get("model") or provider["defaultModel"]
    api_key = cfg.get("apiKey", "")

    body = json.dumps({
        "model": model,
        "messages": messages,
        "max_tokens": provider["maxTokens"],
        "temperature": provider["temperature"]
    }).encode("utf-8")

    req = urllib.request.Request(api_url, data=body, headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    })

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data["choices"][0]["message"]["content"]
    except urllib.error.HTTPError as e:
        code = e.code
        if code == 402:
            raise RuntimeError("API 浣欓涓嶈冻锛岃鏇存崲 API Key 鎴栨湇鍔″晢銆?)
        elif code == 401:
            raise RuntimeError("API Key 鏃犳晥锛岃妫€鏌ラ厤缃€?)
        elif code == 429:
            raise RuntimeError("API 璇锋眰杩囦簬棰戠箒锛岃绋嶅悗鍐嶈瘯銆?)
        else:
            raise RuntimeError(f"AI 鏈嶅姟寮傚父 (HTTP {code})锛岃妫€鏌ョ綉缁滄垨閰嶇疆銆?)
    except urllib.error.URLError:
        raise RuntimeError("缃戠粶杩炴帴澶辫触锛岃妫€鏌ョ綉缁滃悗閲嶈瘯銆?)


# ---------- 娓告垙閫昏緫 ----------
def game_start(data):
    gid = str(uuid.uuid4())[:8]
    state = new_game_state()
    state["playerName"] = data.get("playerName", "鍐掗櫓鑰?)
    state["gameType"] = data.get("type", "history")
    state["isCustom"] = data.get("isCustom", False)
    state["customGameName"] = data.get("customGameName", "")
    state["customGameDesc"] = data.get("customGameDesc", "")

    script_id = data.get("scriptId")
    scripts = get_merged_scripts().get(state["gameType"], [])
    script = next((s for s in scripts if s["id"] == script_id), None)
    state["currentScript"] = script

    games[gid] = state

    # 鐢熸垚 intro
    if state["isCustom"]:
        cfg = load_config()
        if cfg.get("useAI") and cfg.get("apiKey"):
            msgs = build_prompt(state, "寮€濮嬫父鎴?)
            intro = call_ai(msgs)
        else:
            intro = f"娆㈣繋鏉ュ埌鑷畾涔夊墽鏈€寋state['customGameName']}銆嶏紒\n\n{state['customGameDesc']}\n\n璇疯緭鍏ヤ綘鐨勭涓€涓鍔ㄦ寚浠?.."
        state["history"].append({"sender": "绯荤粺", "message": intro})
        return {"gameId": gid, "state": state, "intro": intro, "isTemplate": False}

    elif script:
        # 浣跨敤鑺傜偣寮忔晠浜嬪紩鎿庣敓鎴?intro
        intro = StoryEngine.intro(script)
        state["storyNode"] = "start"
        state["storyFlags"] = {}
        state["history"].append({"sender": "绯荤粺", "message": intro})
        return {"gameId": gid, "state": state, "intro": intro, "isTemplate": True}

    else:
        # 鏃犲墽鏈椂鐨勫厹搴?        intro = "娆㈣繋鏉ュ埌浜掑姩灏忚涓栫晫锛乗n\n璇疯緭鍏ヤ綘鐨勮鍔ㄦ寚浠ゅ紑濮嬪啋闄?.."
        state["history"].append({"sender": "绯荤粺", "message": intro})
        return {"gameId": gid, "state": state, "intro": intro, "isTemplate": True}


def game_action(gid, data):
    state = games.get(gid)
    if not state:
        raise RuntimeError("娓告垙浼氳瘽宸茶繃鏈燂紝璇烽噸鏂板紑濮嬨€?)

    user_input = data.get("message", "").strip()
    if not user_input:
        raise RuntimeError("璇疯緭鍏ヨ鍔ㄦ寚浠ゃ€?)

    # 鎵ｇН鍒嗭紙姣忔浜掑姩鎵?10 鍒嗭級
    state["score"] = max(0, state["score"] - 10)
    state["history"].append({"sender": "浣?, "message": user_input})

    cfg = load_config()
    use_ai = cfg.get("useAI", True) and bool(cfg.get("apiKey"))

    if use_ai:
        try:
            msgs = build_prompt(state, user_input)
            reply = call_ai(msgs)
            is_template = False
        except RuntimeError as e:
            # AI 澶辫触锛屽洖閫€鍒扮绾挎晠浜嬪紩鎿?            if state["isCustom"]:
                reply = f"浣犲喅瀹氾細{user_input}\n\n锛圓I 鏈嶅姟鏆傛椂涓嶅彲鐢紝宸茶Е鍙戠绾挎ā寮忋€傦級\n\n璇疯緭鍏ヤ綘鐨勪笅涓€涓鍔ㄦ寚浠?.."
            else:
                reply, next_node, flags = StoryEngine.process(user_input, state.get("currentScript"), state)
                state["storyNode"] = next_node
                state["storyFlags"].update(flags)
            is_template = True
    else:
        if state["isCustom"]:
            reply = f"浣犲喅瀹氾細{user_input}\n\n锛圓I 鍔熻兘鏈惎鐢ㄣ€傝鍦ㄨ缃腑鍚敤 AI 浠ヨ幏寰楀姩鎬佸墽鎯呬綋楠屻€傦級\n\n璇疯緭鍏ヤ綘鐨勪笅涓€涓鍔ㄦ寚浠?.."
            is_template = True
        else:
            reply, next_node, flags = StoryEngine.process(user_input, state.get("currentScript"), state)
            state["storyNode"] = next_node
            state["storyFlags"].update(flags)
            is_template = True

    state["history"].append({"sender": "AI", "message": reply})

    return {"reply": reply, "score": state["score"], "isTemplate": is_template}


def game_save(gid):
    state = games.get(gid)
    if not state:
        raise RuntimeError("娓告垙浼氳瘽宸茶繃鏈熴€?)
    save_path = SAVES / f"{gid}.json"
    with open(save_path, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    return {"file": str(save_path), "message": "瀛樻。鎴愬姛"}


def game_load(save_id):
    save_path = SAVES / f"{save_id}.json"
    if not save_path.exists():
        raise RuntimeError("瀛樻。涓嶅瓨鍦ㄣ€?)
    with open(save_path, "r", encoding="utf-8") as f:
        state = json.load(f)
    gid = save_id
    games[gid] = state
    return {"gameId": gid, "state": state}


def game_export(gid):
    state = games.get(gid)
    if not state:
        raise RuntimeError("娓告垙浼氳瘽宸茶繃鏈熴€?)
    return {
        "version": "2.0",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "state": state
    }


def game_import_save(data):
    imported = data.get("state", data)
    gid = str(uuid.uuid4())[:8]
    imported["score"] = imported.get("score", 1000)
    imported["history"] = imported.get("history", [])
    games[gid] = imported
    return {"gameId": gid, "state": imported}


# ---------- 鍒楀嚭瀛樻。 ----------
def list_saves():
    saves = []
    for f in sorted(SAVES.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True):
        saves.append({"id": f.stem, "mtime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(f.stat().st_mtime))})
    return saves


# ---------- HTTP 澶勭悊鍣?----------
class GameHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        print(f"[{time.strftime('%H:%M:%S')}] {args[0]}")

    def _send_json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", len(body))
        self.end_headers()
        self.wfile.write(body)

    def _send_error(self, msg, status=400):
        self._send_json({"error": msg}, status)

    def _serve_static(self, filepath, content_type):
        full = ASSETS / filepath
        if not full.exists() or not full.is_file():
            self.send_error(404)
            return
        data = full.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", len(data))
        self.end_headers()
        self.wfile.write(data)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        path = self.path.split("?")[0]

        if path in ("/", "/index.html"):
            self._serve_static("index.html", "text/html; charset=utf-8")
        elif path == "/styles.css":
            self._serve_static("styles.css", "text/css; charset=utf-8")
        elif path == "/app.js":
            self._serve_static("app.js", "application/javascript; charset=utf-8")
        elif path == "/api/scripts":
            self._send_json(get_merged_scripts())
        elif path == "/api/config":
            cfg = load_config()
            cfg.pop("apiKey", None)  # 涓嶈繑鍥炴晱鎰熶俊鎭?            self._send_json(cfg)
        elif path == "/api/saves":
            self._send_json(list_saves())
        else:
            self._send_error("Not found", 404)

    def do_POST(self):
        path = self.path.split("?")[0]

        # 璇诲彇 body
        length = int(self.headers.get("Content-Length", 0))
        body = {}
        if length > 0:
            try:
                body = json.loads(self.rfile.read(length).decode("utf-8"))
            except Exception:
                self._send_error("Invalid JSON", 400)
                return

        try:
            if path == "/api/game/start":
                result = game_start(body)
                self._send_json(result)
            elif path == "/api/game/action":
                gid = body.get("gameId", "")
                result = game_action(gid, body)
                self._send_json(result)
            elif path == "/api/game/save":
                gid = body.get("gameId", "")
                result = game_save(gid)
                self._send_json(result)
            elif path == "/api/game/load":
                save_id = body.get("saveId", "")
                result = game_load(save_id)
                self._send_json(result)
            elif path == "/api/game/export":
                gid = body.get("gameId", "")
                result = game_export(gid)
                self._send_json(result)
            elif path == "/api/game/import":
                result = game_import_save(body)
                self._send_json(result)
            elif path == "/api/config":
                cfg = load_config()
                cfg.update(body)
                save_config(cfg)
                cfg.pop("apiKey", None)
                self._send_json({"ok": True, "config": cfg})
            else:
                self._send_error("Not found", 404)
        except RuntimeError as e:
            self._send_error(str(e), 400)
        except Exception as e:
            self._send_error(f"鏈嶅姟鍣ㄩ敊璇? {e}", 500)


def main():
    port = 8080
    if len(sys.argv) > 2 and sys.argv[1] == "--port":
        port = int(sys.argv[2])

    server = HTTPServer(("0.0.0.0", port), GameHandler)
    print(f"\n{'='*50}")
    print(f"  浜掑姩灏忚娓告垙鏈嶅姟鍣ㄥ凡鍚姩")
    print(f"  璁块棶鍦板潃: http://localhost:{port}")
    print(f"  鎸?Ctrl+C 鍋滄鏈嶅姟鍣?)
    print(f"{'='*50}\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n鏈嶅姟鍣ㄥ凡鍋滄銆?)
        server.shutdown()


if __name__ == "__main__":
    main()
