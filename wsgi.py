import os
import sys
import logging

# ロギングの設定
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# アプリケーションのルートディレクトリをPythonパスに追加
app_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(app_dir)

# 環境変数の設定
os.environ['PYTHONUNBUFFERED'] = '1'

try:
    from app import app
    logger.info("Successfully imported app")
except Exception as e:
    logger.error(f"Failed to import app: {str(e)}")
    raise

if __name__ == "__main__":
    try:
        # Azure Web Appsの環境変数を優先
        port = int(os.environ.get('WEBSITES_PORT', os.environ.get('PORT', 8000)))
        
        logger.info(f"Starting application on port {port}")
        logger.info("Environment variables:")
        logger.info(f"PORT: {os.environ.get('PORT')}")
        logger.info(f"WEBSITES_PORT: {os.environ.get('WEBSITES_PORT')}")
        logger.info(f"WEBSITE_HOSTNAME: {os.environ.get('WEBSITE_HOSTNAME')}")
        logger.info(f"Current directory: {os.getcwd()}")
        logger.info(f"Python path: {sys.path}")
        
        # ホストを0.0.0.0に設定して、外部からのアクセスを許可
        app.run(host='0.0.0.0', port=port)
    except Exception as e:
        logger.error(f"Failed to start application: {str(e)}")
        raise