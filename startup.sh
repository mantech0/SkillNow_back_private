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

# CSVファイルをデータディレクトリにコピー
cp -f /home/site/repository/data/*.csv data/
echo "Copied CSV files to data directory"

# CSVファイルの存在確認
ls -la data/
echo "Current directory: $(pwd)"
echo "Python path: $PYTHONPATH"
echo "Repository directory contents:"
ls -la /home/site/repository/data/

# 環境変数の設定
export ENVIRONMENT=production
export WEBSITES_PORT=8000
export PORT=8000

# デバッグ情報の出力
echo "Environment variables:"
echo "PORT: $PORT"
echo "WEBSITES_PORT: $WEBSITES_PORT"
echo "WEBSITE_HOSTNAME: $WEBSITE_HOSTNAME"

# Gunicornでアプリケーションを起動
echo "Starting Gunicorn on port $PORT"
exec gunicorn --bind=0.0.0.0:$PORT \
    --timeout 600 \
    --workers 2 \
    --threads 2 \
    --log-level debug \
    --error-logfile - \
    --access-logfile - \
    wsgi:app