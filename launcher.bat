@echo off

:: 避免中文乱码
chcp 65001  > nul 2>&1

:: 检查是否存在 .venv 虚拟环境
echo [%~nx0] 检查是否存在 .venv 虚拟环境
if exist .venv\Scripts\activate.bat (
    echo [%~nx0] 虚拟环境已存在，启动虚拟环境...
    call .venv\Scripts\activate.bat

    :: 在虚拟环境中运行 bot.py
    echo [%~nx0] 在虚拟环境中运行 bot.py...
    echo ======================================
    python bot.py
    echo ======================================
    echo [%~nx0] 关闭虚拟环境...
    call deactivate
    pause
) else (
    echo [%~nx0] 虚拟环境不存在，请先使用 poetry update 创建 .venv 虚拟环境。
    pause
)