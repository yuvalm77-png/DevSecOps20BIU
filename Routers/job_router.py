from flask import Blueprint, request, jsonify
from app import db
from Models.job import Job

jobs_bp = Blueprint("jobs", __name__, url_prefix="/jobs")

@jobs_bp.get("")
def list_jobs():
    rows = Job.query.order_by(Job.id.desc()).all()
    return jsonify([
        {
            "id": j.id,
            "title": j.title,
            "employment_type": j.employment_type,
            "work_location": j.work_location,
            "description": j.description,
            "required_technologies": j.required_technologies,
            "required_experience": j.required_experience,
            "is_open": j.is_open
        } for j in rows
    ]), 200

@jobs_bp.post("")
def create_job():
    data = request.get_json() or {}
    if not data.get("title"):
        return jsonify({"error": "title is required"}), 400

    job = Job(
        title=data["title"],
        employment_type=data.get("employment_type"),
        work_location=data.get("work_location"),
        description=data.get("description"),
        required_technologies=data.get("required_technologies"),
        required_experience=data.get("required_experience"),
        is_open=bool(data.get("is_open", True)),
    )
    db.session.add(job)
    db.session.commit()
    return jsonify({"id": job.id, "message": "job created"}), 201
