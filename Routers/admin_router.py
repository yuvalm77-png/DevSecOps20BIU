from flask import Blueprint, render_template, request, redirect, url_for, flash
from extensions import db

from Models import User, Job

admin_bp = Blueprint("admin", __name__, url_prefix="/admin", template_folder='../templates')

from flask_jwt_extended import verify_jwt_in_request, get_jwt


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

@admin_bp.route("/jobs/<int:job_id>/toggle", methods=["POST"])
def toggle_job_status(job_id):
    try:
        verify_jwt_in_request()
        claims = get_jwt()
        if not claims.get("is_admin", False):
            return redirect(url_for("auth.login_page"))
    except Exception:
        return redirect(url_for("auth.login_page"))
    job = Job.query.get_or_404(job_id)
    job.is_open = not job.is_open
    db.session.commit()
    return redirect(url_for("admin.jobs_page"))

@admin_bp.route("/jobs/<int:job_id>/delete", methods=["POST"])
def delete_job(job_id):
    try:
        verify_jwt_in_request()
        claims = get_jwt()
        if not claims.get("is_admin", False):
            return redirect(url_for("auth.login_page"))
    except Exception:
        return redirect(url_for("auth.login_page"))
    job = Job.query.get_or_404(job_id)
    db.session.delete(job)
    db.session.commit()
    return redirect(url_for("admin.jobs_page"))

@admin_bp.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    try:
        verify_jwt_in_request()
        claims = get_jwt()
        if not claims.get("is_admin", False):
            return redirect(url_for("auth.login_page"))
        current_user_id = int(claims.get("user_id"))
        if current_user_id == user_id:
            flash("You cannot delete yourself.", "error")
            return redirect(url_for("admin.users_page"))
    except Exception:
        return redirect(url_for("auth.login_page"))
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash("User deleted successfully.", "success")
    return redirect(url_for("admin.users_page"))
