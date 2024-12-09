#!/bin/bash

# Pythonパスを設定
export PYTHONPATH=/home/site/wwwroot

# 依存関係のインストール
pip install -r requirements.txt

# アプリケーションディレクトリに移動
cd /home/site/wwwroot

# ポート番号を環境変数から取得（デフォルトは5001）
PORT="${PORT:-5001}"

# Gunicornでアプリケーションを起動
gunicorn --bind=0.0.0.0:${PORT} --timeout 600 --log-level debug app:app 