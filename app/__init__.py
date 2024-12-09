from flask import Flask, jsonify
from flask_cors import CORS
from .routes.users import users_bp
from .routes.projects import projects_bp
import os
import logging

# ロギングの設定
logger = logging.getLogger(__name__)

app = Flask(__name__)

# CORS設定を詳細に指定
CORS(app, resources={
    r"/*": {
        "origins": "*",  # すべてのオリジンを許可
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "expose_headers": ["Content-Type"],
        "supports_credentials": True
    }
})

# エラーハンドリング
@app.errorhandler(404)
def not_found_error(error):
    logger.error(f"404 error: {error}")
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"500 error: {error}")
    return jsonify({"error": "Internal server error"}), 500

# ルートの登録
app.register_blueprint(users_bp)
app.register_blueprint(projects_bp)

@app.route('/')
def index():
    try:
        # 基本的な情報を返す
        return jsonify({
            'message': 'Welcome to SkillNow API',
            'status': 'running',
            'environment': os.environ.get('FLASK_ENV', 'unknown'),
            'host': os.environ.get('WEBSITE_HOSTNAME', 'unknown')
        })
    except Exception as e:
        logger.error(f"Error in index route: {str(e)}")
        return jsonify({"error": str(e)}), 500

# 起動時のログ出力
logger.info("Application initialized")
