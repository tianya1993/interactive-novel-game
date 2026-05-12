#!/bin/bash
# 互动小说游戏 - Skill 安装脚本
# 将三�?skill 安装�?Claude Code �?skills 目录

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILLS_DIR="$HOME/.claude/skills"

echo "互动小说游戏 - 安装 Skill"
echo "========================="
echo ""

mkdir -p "$SKILLS_DIR"

# 安装 novel-play
if [ -L "$SKILLS_DIR/novel-play" ] || [ -d "$SKILLS_DIR/novel-play" ]; then
    echo "[跳过] novel-play 已存�?
else
    ln -s "$SCRIPT_DIR/skills/novel-play" "$SKILLS_DIR/novel-play"
    echo "[完成] novel-play �?已安�?
fi

# 安装 novel-create
if [ -L "$SKILLS_DIR/novel-create" ] || [ -d "$SKILLS_DIR/novel-create" ]; then
    echo "[跳过] novel-create 已存�?
else
    ln -s "$SCRIPT_DIR/skills/novel-create" "$SKILLS_DIR/novel-create"
    echo "[完成] novel-create �?已安�?
fi

# 安装 novel-config
if [ -L "$SKILLS_DIR/novel-config" ] || [ -d "$SKILLS_DIR/novel-config" ]; then
    echo "[跳过] novel-config 已存�?
else
    ln -s "$SCRIPT_DIR/skills/novel-config" "$SKILLS_DIR/novel-config"
    echo "[完成] novel-config �?已安�?
fi

echo ""
echo "安装完成！可使用以下命令�?
echo "  /novel-play    �?启动游戏"
echo "  /novel-create  �?创作剧本"
echo "  /novel-config  �?配置 AI"
echo ""
echo "或在 Claude Code 中直接说�?
echo "  '开始玩游戏'  '我想创作剧本'  '配置AI'"
