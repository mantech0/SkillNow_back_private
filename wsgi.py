import os
import sys

# アプリケーションのルートディレクトリをPythonパスに追加
app_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(app_dir)

from app import app

if __name__ == "__main__":
    # 環境変数からポート番号を取得
    port = int(os.environ.get('PORT', 8000))
    # ホストを0.0.0.0に設定して、外部からのアクセスを許可
    app.run(host='0.0.0.0', port=port)