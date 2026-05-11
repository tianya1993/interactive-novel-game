#!/bin/bash
# 浜掑姩灏忚娓告垙 - Skill 瀹夎鑴氭湰
# 灏嗕笁涓?skill 瀹夎鍒?Claude Code 鐨?skills 鐩綍

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILLS_DIR="$HOME/.claude/skills"

echo "浜掑姩灏忚娓告垙 - 瀹夎 Skill"
echo "========================="
echo ""

mkdir -p "$SKILLS_DIR"

# 瀹夎 novel-play
if [ -L "$SKILLS_DIR/novel-play" ] || [ -d "$SKILLS_DIR/novel-play" ]; then
    echo "[璺宠繃] novel-play 宸插瓨鍦?
else
    ln -s "$SCRIPT_DIR/skills/novel-play" "$SKILLS_DIR/novel-play"
    echo "[瀹屾垚] novel-play 鈫?宸插畨瑁?
fi

# 瀹夎 novel-create
if [ -L "$SKILLS_DIR/novel-create" ] || [ -d "$SKILLS_DIR/novel-create" ]; then
    echo "[璺宠繃] novel-create 宸插瓨鍦?
else
    ln -s "$SCRIPT_DIR/skills/novel-create" "$SKILLS_DIR/novel-create"
    echo "[瀹屾垚] novel-create 鈫?宸插畨瑁?
fi

# 瀹夎 novel-config
if [ -L "$SKILLS_DIR/novel-config" ] || [ -d "$SKILLS_DIR/novel-config" ]; then
    echo "[璺宠繃] novel-config 宸插瓨鍦?
else
    ln -s "$SCRIPT_DIR/skills/novel-config" "$SKILLS_DIR/novel-config"
    echo "[瀹屾垚] novel-config 鈫?宸插畨瑁?
fi

echo ""
echo "瀹夎瀹屾垚锛佸彲浣跨敤浠ヤ笅鍛戒护锛?
echo "  /novel-play    鈥?鍚姩娓告垙"
echo "  /novel-create  鈥?鍒涗綔鍓ф湰"
echo "  /novel-config  鈥?閰嶇疆 AI"
echo ""
echo "鎴栧湪 Claude Code 涓洿鎺ヨ锛?
echo "  '寮€濮嬬帺娓告垙'  '鎴戞兂鍒涗綔鍓ф湰'  '閰嶇疆AI'"
