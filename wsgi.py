import os
import sys

# アプリケーションのルートディレクトリをPythonパスに追加
app_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(app_dir)

from app import app

# アプリケーションの設定
app.config['ENV'] = 'production'