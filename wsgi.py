import os
import sys

# アプリケーションのルートディレクトリをPythonパスに追加
app_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(app_dir)

# 環境変数の設定
os.environ['PYTHONUNBUFFERED'] = '1'

from app import app

if __name__ == "__main__":
    # Azure Web Appsの環境変数を優先
    port = int(os.environ.get('WEBSITES_PORT', os.environ.get('PORT', 8000)))
    
    print(f"Starting application on port {port}")
    print(f"Environment variables:")
    print(f"PORT: {os.environ.get('PORT')}")
    print(f"WEBSITES_PORT: {os.environ.get('WEBSITES_PORT')}")
    print(f"WEBSITE_HOSTNAME: {os.environ.get('WEBSITE_HOSTNAME')}")
    
    # ホストを0.0.0.0に設定して、外部からのアクセスを許可
    app.run(host='0.0.0.0', port=port)