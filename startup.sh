#!/bin/bash

# Pythonパスを設定
export PYTHONPATH=/home/site/wwwroot

# 依存関係のインストール
pip install -r requirements.txt

# アプリケーションディレクトリに移動
cd /home/site/wwwroot

# データディレクトリの存在確認と作成
if [ ! -d "data" ]; then
    mkdir -p data
    echo "Created data directory"
fi

# CSVファイルの存在確認
ls -la data/
echo "Current directory: $(pwd)"
echo "Python path: $PYTHONPATH"

# 環境に基づいてポート番号を設定
if [ "$ENVIRONMENT" = "production" ]; then
    # Azure Web Apps のデフォルトポート
    export PORT=8000
else
    # ローカル開発環境用のポート
    export PORT=5001
fi

# 環境変数の設定
export ENVIRONMENT=production

# Gunicornでアプリケーションを起動
echo "Starting Gunicorn on port $PORT"
gunicorn --bind=0.0.0.0:$PORT --timeout 600 --log-level debug app:app 