import os
import sys

# アプリケーションのルートディレクトリをPythonパスに追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5001))  # 環境変数PORTがない場合は5001を使用
    app.run(host='0.0.0.0', port=port)