from flask import Blueprint, request, jsonify
from extensions import db
from Models.job import Job

#jobs_bp = Blueprint('jobs_bp', __name__, url_prefix='/jobs')
jobs_bp = Blueprint("jobs", __name__, url_prefix="/jobs")
@jobs_bp.get('/')
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

@jobs_bp.get("/<int:id>")    #Get job by id
def get_by_id(id):
    job = Job.query.get(id)  # fetch by primary key
    if not job:
        return jsonify({"error": "The job doesn't exist"}), 404

    return jsonify({
        "id": job.id,
        "title": job.title,
        "employment_type": job.employment_type,
        "work_location": job.work_location,
        "description": job.description,
        "required_technologies": job.required_technologies,
        "required_experience": job.required_experience,
        "is_open": job.is_open
    }), 200


@jobs_bp.put("/<int:id>")
def update_job_by_id(id):
    job = Job.query.get(id)
    if not job:
        return jsonify({"error": "Job not found"}), 404

    data = request.get_json() or {}

    # Update fields if they exist in the model
    if "title" in data:
        job.title = data["title"]
    if "employment_type" in data:
        job.employment_type = data["employment_type"]
    if "work_location" in data:
        job.work_location = data["work_location"]
    if "description" in data:
        job.description = data["description"]
    if "required_technologies" in data:
        job.required_technologies = data["required_technologies"]
    if "required_experience" in data:
        job.required_experience = data["required_experience"]
    if "is_open" in data:
        job.is_open = bool(data["is_open"])

    db.session.commit()

    return jsonify({
        "id": job.id,
        "title": job.title,
        "employment_type": job.employment_type,
        "work_location": job.work_location,
        "description": job.description,
        "required_technologies": job.required_technologies,
        "required_experience": job.required_experience,
        "is_open": job.is_open,
        "message": "Job updated successfully"
    }), 200

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


@jobs_bp.delete("/<int:id>")
def delete_by_id(id):
    job = Job.query.get(id)  # fetch by primary key
    if not job:
        return jsonify({"error": "The job doesn't exist"}), 404
    db.session.delete(job)
    db.session.commit()
    return jsonify({"status": "Done", "message": f"Job {id} deleted!"}), 200

 #
# from flask import Flask, request
#
# import application
#
# # car -> dict
# # car - > make : str
# #       > model: str
# #       > cc: int
# #       > hp: int
# #       > year: int
# #       > color: str
#
#
# cars = [
#     {"id": 1, "make": "tesla", "model": "s", "cc": 0, "hp": 1024, "year": 2022, "color": "black", },
#     {"id": 2, "make": "bmw", "model": "435i", "cc": 3600, "hp": 430, "year": 1991, "color": "grey", }
# ]
# AUTO_ID = 4
#
# # endpoints:
# # GET    /cars -> all the cars
# # GET    /cars/<id> -> single car
# # POST   /cars -> add new car
# # PUT    /cars/<id> -> change car
# # DELETE /cars -> delete all cars
#
#
# app = Flask('cars_api')
#
#
# @app.get('/')
# def home_page():
#     return 'welcome to cars api '
#
#
# # get all cars
# @app.get('/cars')
# def get_all():
#     return cars
#
#
# @app.get('/cars/<id>')
# def get_by_id(id):
#     id = int(id)
#     for car in cars:
#         if car['id'] == id:
#             return car
#     return 'not found', 404
#
#
# @app.delete('/cars')
# def delete_all():
#     cars.clear()
#     return {"status": "Done", "message": "deleted !"}
#
#
# @app.delete('/cars/<int:id>')
# def delete_by_id(id):
#     for car in cars:
#         if car['id'] == id:
#             cars.remove(car)
#     return {"status": "Done", "message": "deleted !"}
#
