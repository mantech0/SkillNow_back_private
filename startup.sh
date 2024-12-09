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
if [ -n "$WEBSITES_PORT" ]; then
    export PORT=$WEBSITES_PORT
else
    export PORT=8000
fi

# Gunicornでアプリケーションを起動
exec gunicorn --bind=0.0.0.0:$PORT wsgi:app