import os
from flask import Flask
from sqlalchemy import inspect
from extensions import db  # ✅ import db here

from Routers.job_router import jobs_bp

from Models import Job, Applicant, Application, User  # ✅ safe now
# ------------------------------------------------------

app = Flask('jobs-api')

def _sqlite_uri(app: Flask) -> str:
    raw = os.getenv("DATABASE_URL", "sqlite:///instance/app.db")
    if raw.startswith("sqlite:///"):
        filename = os.path.basename(raw.replace("sqlite:///", "")) or "app.db"
        os.makedirs(app.instance_path, exist_ok=True)
        path = os.path.join(app.instance_path, filename)
        return f"sqlite:///{path}"
    return raw


def create_app() -> Flask:
    app = Flask(__name__, instance_relative_config=True)

    app.config["SQLALCHEMY_DATABASE_URI"] = _sqlite_uri(app)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)  # ✅ initialize db

    app.register_blueprint(jobs_bp)

    with app.app_context():
        db.create_all()
        print(">>> Tables now:", inspect(db.engine).get_table_names())

    @app.get("/health")
    def health():
        return {"ok": True}, 200

    return app

app.register_blueprint(jobs_bp, url_prefix='/jobs')
#app.register_blueprint(applicant_bp, url_prefix='/applicant')


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5001)
