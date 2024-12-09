#!/bin/bash

# デバッグ情報の出力
echo "Starting startup script"
echo "Current directory: $(pwd)"

# Pythonパスを設定
export PYTHONPATH=/home/site/wwwroot
echo "Set PYTHONPATH: $PYTHONPATH"

# 依存関係のインストール
echo "Installing dependencies..."
pip install -r requirements.txt

# アプリケーションディレクトリに移動
cd /home/site/wwwroot
echo "Changed to directory: $(pwd)"

# データディレクトリの存在確認と作成
if [ ! -d "data" ]; then
    mkdir -p data
    echo "Created data directory"
fi

# CSVファイルをデータディレクトリにコピー
echo "Copying CSV files..."
cp -f /home/site/repository/data/*.csv data/ || echo "Warning: CSV copy failed"

# CSVファイルの存在確認とパーミッション設定
echo "Setting permissions for data directory..."
chmod 755 data
find data -type f -name "*.csv" -exec chmod 644 {} \;

# ファイル一覧の表示
echo "Contents of current directory:"
ls -la
echo "Contents of data directory:"
ls -la data/

# 環境変数の設定
export FLASK_ENV=production
export FLASK_DEBUG=0

# Azure Web Appsのポート設定
export PORT=8000
export WEBSITES_PORT=8000

# デバッグ情報の出力
echo "Environment variables:"
echo "PORT: $PORT"
echo "WEBSITES_PORT: $WEBSITES_PORT"
echo "WEBSITE_HOSTNAME: $WEBSITE_HOSTNAME"
echo "PYTHONPATH: $PYTHONPATH"

# Gunicornでアプリケーションを起動
echo "Starting Gunicorn..."
exec gunicorn \
    --bind=0.0.0.0:8000 \
    --timeout 600 \
    --workers 1 \
    --threads 2 \
    --worker-class=sync \
    --log-level=debug \
    --error-logfile=- \
    --access-logfile=- \
    --capture-output \
    wsgi:app