# Job table
from extensions import db  # ✅ instead of from app import db

class Job(db.Model):
    __tablename__ = "jobs"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    employment_type = db.Column(db.String(50))      # Full/Partially
    work_location = db.Column(db.String(50))        # Home/Office/Hybrid
    description = db.Column(db.Text)
    required_technologies = db.Column(db.Text)      # "AWS, Docker, K8s"
    required_experience = db.Column(db.Integer)     # Experience in years
    is_open = db.Column(db.Boolean, default=True)

    applications = db.relationship(
        "Application",
        back_populates="job",
        cascade="all, delete-orphan"
    )

