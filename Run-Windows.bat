@echo off

REM 判断虚拟环境是否存在
if not exist ".venv\Scripts\activate.bat" (
    echo Creating virtual environment...
    python -m venv .venv
) else (
    echo Virtual environment already exists.
)

call .venv\Scripts\activate.bat

pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

python main.py
