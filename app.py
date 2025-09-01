import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect

db = SQLAlchemy()

from Models import Job, Applicant, Application, User
from Routers.job_router import jobs_bp
# ------------------------------------------------------


def _sqlite_uri(app: Flask) -> str:
    """בונה URI מוחלט ל-SQLite בתוך instance/ אם הוגדר נתיב יחסי."""
    raw = os.getenv("DATABASE_URL", "sqlite:///instance/app.db")
    if raw.startswith("sqlite:///"):
        filename = os.path.basename(raw.replace("sqlite:///", "")) or "app.db"
        os.makedirs(app.instance_path, exist_ok=True)
        path = os.path.join(app.instance_path, filename)
        return f"sqlite:///{path}"
    return raw


def create_app() -> Flask:
    app = Flask(__name__, instance_relative_config=True)

    # קונפיג בסיסי
    app.config["SQLALCHEMY_DATABASE_URI"] = _sqlite_uri(app)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # אתחול ORM
    db.init_app(app)

    app.register_blueprint(jobs_bp)

    with app.app_context():
        db.create_all()
        print(">>> Tables now:", inspect(db.engine).get_table_names())

    # Healthcheck קטן
    @app.get("/health")
    def health():
        return {"ok": True}, 200

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True,port=5001)
