from flask import Blueprint, request, jsonify
from extensions import db
from Models.application import Application
from services import score_computing

apply_bp = Blueprint("apply", __name__, url_prefix="/apply")

@apply_bp.post("/<int:job_id>")
def apply_to_job(job_id):
    data = request.get_json() or {}
    if not data.get("applicant_id"):
        return jsonify({"error": "applicant_id is required"}), 400

    application = Application(
        job_id=job_id,
        applicant_id=data["applicant_id"],
        status=data.get("status", "pending"),
        score=score_computing.compute_application_score(data["applicant_id"], job_id)
    )

    db.session.add(application)
    db.session.commit()
    return jsonify({"id": application.id, "message": "application submitted"}), 201

@apply_bp.route("/<int:applicant_id>", methods=["GET"])
def get_applications_for_applicant(applicant_id):
    applications = Application.query.filter_by(applicant_id=applicant_id).all()
    if not applications:
        return jsonify({"error": "No applications found for this applicant"}), 404

    result = []
    for app in applications:
        result.append({
            "id": app.id,
            "job_id": app.job_id,
            "status": app.status,
            "score": app.score
        })

    return jsonify(result), 200