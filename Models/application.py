from app import db

# טבלת קישור מועמדויות
class Application(db.Model):
    __tablename__ = "applications"
    id = db.Column(db.Integer, primary_key=True)
    applicant_id = db.Column(db.Integer, db.ForeignKey("applicants.id"), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey("jobs.id"), nullable=False)
    status = db.Column(db.String(50), default="pending")
    score = db.Column(db.Float)

    applicant = db.relationship("Applicant", back_populates="applications")
    job = db.relationship("Job", back_populates="applications")
