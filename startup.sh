#!/bin/bash

# Pythonパスを設定
export PYTHONPATH=/home/site/wwwroot

# 依存関係のインストール
pip install -r requirements.txt

# アプリケーションディレクトリに移動
cd /home/site/wwwroot

# 環境に基づいてポート番号を設定
if [ "$ENVIRONMENT" = "production" ]; then
    # Azure Web Apps のデフォルトポート
    PORT="${PORT:-8000}"
else
    # ローカル開発環境用のポート
    PORT="${PORT:-5001}"
fi

# Gunicornでアプリケーションを起動
gunicorn --bind=0.0.0.0:${PORT} --timeout 600 --log-level debug app:app 