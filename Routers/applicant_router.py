from flask import Blueprint, request, jsonify
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

@applicants_bp.post("")
def create_applicant():
    data = request.get_json() or {}
    if not data.get("name"):
        return jsonify({"error": "name is required"}), 400

    applicant = Applicant(
        name=data["name"],
        languages=data.get("languages"),
        technologies=data.get("technologies"),
        flagship_project=data.get("flagship_project"),
        last_job=data.get("last_job"),
        education=data.get("education"),
        years_experience=data.get("years_experience"),
        resume_path=data.get("resume_path"))

    db.session.add(applicant)
    db.session.commit()
    return jsonify({"id": applicant.id, "message": "applicant created"}), 201



# @applicant_bp.put("/<int:id>")
# def update_job_by_id(id):
#     applicant = applicant.query.get(id)
#     if not applicant:
#         return jsonify({"error": "applicant not found"}), 404
#
#     data = request.get_json() or {}
#
#     # Update fields if they exist in the model
#     if "title" in data:
#         job.title = data["title"]
#     if "employment_type" in data:
#         job.employment_type = data["employment_type"]
#     if "work_location" in data:
#         job.work_location = data["work_location"]
#     if "description" in data:
#         job.description = data["description"]
#     if "required_technologies" in data:
#         job.required_technologies = data["required_technologies"]
#     if "required_experience" in data:
#         job.required_experience = data["required_experience"]
#     if "is_open" in data:
#         job.is_open = bool(data["is_open"])
#
#     db.session.commit()
#
#     return jsonify({
#         "id": job.id,
#         "title": job.title,
#         "employment_type": job.employment_type,
#         "work_location": job.work_location,
#         "description": job.description,
#         "required_technologies": job.required_technologies,
#         "required_experience": job.required_experience,
#         "is_open": job.is_open,
#         "message": "Job updated successfully"
#     }), 200
