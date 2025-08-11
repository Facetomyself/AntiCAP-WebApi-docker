@echo off

python -m venv .venv

call .venv\Scripts\activate.bat

pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

python main.py
