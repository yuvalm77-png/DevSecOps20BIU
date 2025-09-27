from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from services.auth_utils import admin_required

from Models import Application
from extensions import db
from Models.applicant import Applicant

applicants_bp = Blueprint("applicants", __name__)
@applicants_bp.get("")
def applicants_list_jobs():
    rows = Applicant.query.order_by(Applicant.id.desc()).all()
    return jsonify([
        {
            "id": j.id,
            "name": j.name,
            "languages": j.languages,
            "technologies": j.technologies,
            "flagship_project": j.flagship_project,
            "last_job": j.last_job,
            "education": j.education,
            "years_experience": j.years_experience,
            "resume_path": j.resume_path
        } for j in rows
    ]), 200

@applicants_bp.route("/", methods=["POST"])
@jwt_required()
@admin_required
def create_applicant():
    data = request.form
    if not data.get("name") or not data.get("resume_path"):
        return jsonify({"error": "Name and resume_path are required"}), 400
    applicant = Applicant(**data)
    db.session.add(applicant)
    db.session.commit()
    return jsonify({"id": applicant.id, "name": applicant.name}), 201



@applicants_bp.get("/by_applicant/<int:id>")
def get_applicant_by_id(id):
    applicant = Applicant.query.get(id)
    if not applicant:
        return jsonify({"error": "Applicant not found"}), 404

    return jsonify({
        "id": applicant.id,
        "name": applicant.name,
        "languages": applicant.languages,
        "technologies": applicant.technologies,
        "flagship_project": applicant.flagship_project,
        "last_job": applicant.last_job,
        "education": applicant.education,
        "years_experience": applicant.years_experience,
        "resume_path": applicant.resume_path
    }), 200

@applicants_bp.route("/<int:job_id>",methods=["GET"])
def getting_applicants_by_job_id(job_id):
    applications = Application.query.filter_by(job_id=job_id).all()
    if not applications:
        return jsonify({"error": "No applications found for this job"}), 404

    applicants_data = []
    for app in applications:
        applicant = Applicant.query.get(app.applicant_id)
        if applicant:
            applicants_data.append({
                "id": applicant.id,
                "name": applicant.name,
                "languages": applicant.languages,
                "technologies": applicant.technologies,
                "flagship_project": applicant.flagship_project,
                "last_job": applicant.last_job,
                "education": applicant.education,
                "years_experience": applicant.years_experience,
                "resume_path": applicant.resume_path,
                "application_status": app.status,
                "application_score": app.score
            })

    return jsonify(applicants_data), 200

@applicants_bp.get("/<int:job_id>/<int:applicant_id>")
def getting_applicant_details_and_score(job_id, applicant_id):
    application = Application.query.filter_by(job_id=job_id, applicant_id=applicant_id).first()
    if not application:
        return jsonify({"error": "Application not found"}), 404

    applicant = Applicant.query.get(applicant_id)
    if not applicant:
        return jsonify({"error": "Applicant not found"}), 404
    return jsonify({
        "id": applicant.id,
        "name": applicant.name,
        "languages": applicant.languages,
        "technologies": applicant.technologies,
        "flagship_project": applicant.flagship_project,
        "last_job": applicant.last_job,
        "education": applicant.education,
        "years_experience": applicant.years_experience,
        "resume_path": applicant.resume_path,
        "application_status": application.status,
        "application_score": application.score
    }), 200

@applicants_bp.route("/job/<int:job_id>/applicant/<int:applicant_id>", methods=["DELETE"])
def delete_application(job_id: int, applicant_id: int):
    application = Application.query.filter_by(job_id=job_id, applicant_id=applicant_id).first()
    if not application:
        return jsonify({"error": "Application not found"}), 404

    db.session.delete(application)
    db.session.commit()
    return jsonify({"message": "Application deleted",
                    "job_id": job_id,
                    "applicant_id": applicant_id
                    }), 200






