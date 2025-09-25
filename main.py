import os
import sqlite3
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from sqlalchemy import inspect,event
from sqlalchemy.engine import Engine
from extensions import db  # ✅ import db here
from datetime import timedelta

from Routers.job_router import jobs_bp
from Routers.applicant_router import applicants_bp
from Routers.application_router import apply_bp
from Routers.users_router import users_bp
from Routers.auth_router import auth_bp
from Models import Job, Applicant, Application, User  # ✅ safe now
# ------------------------------------------------------

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, sqlite3.Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()

def _sqlite_uri(app: Flask) -> str:
    raw = os.getenv("DATABASE_URL", "sqlite:///instance/app.db")
    if raw.startswith("sqlite:///"):
        filename = os.path.basename(raw.replace("sqlite:///", "")) or "app.db"
        os.makedirs(app.instance_path, exist_ok=True)
        path = os.path.join(app.instance_path, filename)
        return f"sqlite:///{path}"
    return raw

def init_security_and_cors(app: Flask):
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "super-secret")
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=7)
    app.config["JWT_TOKEN_LOCATION"] = ["headers"]
    app.config["JWT_ALGORITHM"] = "HS256"

    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=False)

    jwt = JWTManager(app)
    @jwt.unauthorized_loader
    def unauthorized_loader(msg):
        return {"error": "Missing or invalid token", "detail":msg}, 401

    @jwt.invalid_token_loader
    def invalid_token_loader(msg):
        return {"error": "Invalid token", "detail":msg}, 422

    return jwt

def create_app() -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    load_dotenv()
    app.config["SQLALCHEMY_DATABASE_URI"] = _sqlite_uri(app)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)  # ✅ initialize db

    jwt = init_security_and_cors(app)

    app.register_blueprint(jobs_bp, url_prefix="/jobs")
    app.register_blueprint(applicants_bp, url_prefix="/applicants")
    app.register_blueprint(apply_bp, url_prefix="/apply")
    app.register_blueprint(users_bp, url_prefix="/users")
    app.register_blueprint(auth_bp, url_prefix="/auth")
    with app.app_context():
        db.create_all()
        print(">>> Tables now:", inspect(db.engine).get_table_names())

    @app.get("/health")
    def health():
        return {"ok": True}, 200

    @app.route('/')
    def homepage():
        return 'hello'

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5001)

