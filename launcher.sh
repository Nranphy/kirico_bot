#!/bin/bash

# 避免中文乱码
LANG=zh_CN.UTF-8

# 检查是否存在 .venv 虚拟环境
echo "[$(basename $0)] 检查是否存在 .venv 虚拟环境"
if [ -e .venv/bin/activate ]; then
    echo "[$(basename $0)] 虚拟环境已存在，启动虚拟环境..."
    source .venv/bin/activate

    # 在虚拟环境中运行 bot.py
    echo "[$(basename $0)] 在虚拟环境中运行 bot.py..."
    echo "======================================"
    python bot.py
    echo "======================================"
    echo "[$(basename $0)] 关闭虚拟环境..."
    deactivate
    read -p "按 Enter 键继续..."
else
    echo "[$(basename $0)] 虚拟环境不存在，请先使用 poetry update 创建 .venv 虚拟环境。"
    read -p "按 Enter 键继续..."
fi