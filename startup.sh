#!/bin/bash

# Pythonパスを設定
export PYTHONPATH=/home/site/wwwroot

# 依存関係のインストール
pip install -r requirements.txt

# Gunicornでアプリケーションを起動
gunicorn --bind=0.0.0.0:8000 --timeout 600 wsgi:app 