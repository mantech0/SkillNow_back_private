import os
import sys
import logging
from logging.handlers import RotatingFileHandler

# ロギングの設定
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# アプリケーションのルートディレクトリをPythonパスに追加
app_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(app_dir)
logger.info(f"Added to Python path: {app_dir}")

# 環境変数の設定
os.environ['PYTHONUNBUFFERED'] = '1'
os.environ['FLASK_ENV'] = 'production'

try:
    logger.info("Attempting to import app...")
    from app import app
    logger.info("Successfully imported app")
except Exception as e:
    logger.error(f"Failed to import app: {str(e)}")
    logger.error("Python path:")
    for path in sys.path:
        logger.error(f"  {path}")
    raise

# Gunicornで使用するアプリケーションオブジェクト
application = app

if __name__ == "__main__":
    try:
        # Azure Web Appsの環境変数を優先
        port = int(os.environ.get('WEBSITES_PORT', os.environ.get('PORT', 8000)))
        
        logger.info(f"Starting application on port {port}")
        logger.info("Environment variables:")
        for key, value in os.environ.items():
            if key.startswith(('WEBSITE', 'PORT', 'PYTHON', 'FLASK')):
                logger.info(f"{key}: {value}")
        
        # ホストを0.0.0.0に設定して、外部からのアクセスを許可
        app.run(host='0.0.0.0', port=port)
    except Exception as e:
        logger.error(f"Failed to start application: {str(e)}", exc_info=True)
        raise