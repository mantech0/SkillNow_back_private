#!/bin/bash

# Pythonパスを設定
export PYTHONPATH=/home/site/wwwroot

# 依存関係のインストール
pip install -r requirements.txt

# データディレクトリの作成とCSVファイルのコピー
mkdir -p data
cp -f /home/site/repository/data/*.csv data/ || echo "Warning: CSV copy failed"

# CSVファイルの存在確認
echo "Checking CSV files..."
ls -la data/

# 環境変数の設定
export PORT=8000
export WEBSITES_PORT=8000

# デバッグ情報
echo "Current directory: $(pwd)"
echo "PORT: $PORT"
echo "WEBSITES_PORT: $WEBSITES_PORT"

# Gunicornでアプリケーションを起動
cd /home/site/wwwroot && \
exec gunicorn \
    --bind=0.0.0.0:8000 \
    --timeout 600 \
    --workers 1 \
    --log-level debug \
    wsgi:app