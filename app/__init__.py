from flask import Flask
from flask_cors import CORS
from .routes.users import users_bp

app = Flask(__name__)

# CORS設定を詳細に指定
CORS(app, resources={
    r"/*": {
        "origins": ["http://localhost:3000"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# ルートの登録
app.register_blueprint(users_bp)

@app.route('/')
def index():
    return {'message': 'Welcome to SkillNow API'}
