import os
import sys
import logging

# ロギングの設定
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

try:
    # アプリケーションのルートディレクトリをPythonパスに追加
    app_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(app_dir)
    logger.info(f"Added to Python path: {app_dir}")

    from app import app
    logger.info("Successfully imported app")

    # アプリケーションの設定
    app.config['ENV'] = 'production'
    app.config['DEBUG'] = False

except Exception as e:
    logger.error(f"Error during initialization: {str(e)}")
    raise