from flask import Blueprint, render_template

from Models import User, Job

admin_bp = Blueprint("admin", __name__, url_prefix="/admin", template_folder='../templates')

from flask_jwt_extended import verify_jwt_in_request, get_jwt
from flask import redirect, url_for

@admin_bp.route("/")
def admin_page():
    try:
        verify_jwt_in_request()
        claims = get_jwt()
        if not claims.get("is_admin", False):
            return redirect(url_for("auth.login_page"))
    except Exception:
        return redirect(url_for("auth.login_page"))
    return render_template("admin.html")

@admin_bp.route("/users")
def users_page():
    try:
        verify_jwt_in_request()
        claims = get_jwt()
        if not claims.get("is_admin", False):
            return redirect(url_for("auth.login_page"))
    except Exception:
        return redirect(url_for("auth.login_page"))
    users = User.query.all()
    return render_template("users.html", users=users)

@admin_bp.route("/jobs")
def jobs_page():
    try:
        verify_jwt_in_request()
        claims = get_jwt()
        if not claims.get("is_admin", False):
            return redirect(url_for("auth.login_page"))
    except Exception:
        return redirect(url_for("auth.login_page"))
    jobs = Job.query.all()
    return render_template("jobs.html", jobs=jobs)

@admin_bp.route("/add_applicant")
def add_applicant_page():
    try:
        verify_jwt_in_request()
        claims = get_jwt()
        if not claims.get("is_admin", False):
            return redirect(url_for("auth.login_page"))
    except Exception:
        return redirect(url_for("auth.login_page"))
    return render_template("add_applicant.html")

@admin_bp.route("/add_job")
def add_job_page():
    try:
        verify_jwt_in_request()
        claims = get_jwt()
        if not claims.get("is_admin", False):
            return redirect(url_for("auth.login_page"))
    except Exception:
        return redirect(url_for("auth.login_page"))
    return render_template("add_job.html")
