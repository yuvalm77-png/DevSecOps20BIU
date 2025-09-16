from Models.application import Application
from Models.applicant import Applicant
from Models.job import Job
from extensions import db



def compute_application_score(applicant: Applicant , job: Job = None, application_id: int = None) -> int | None:
    application = Application.query.get(application_id)
    if not application:
        return None  # or raise an exception

    applicant = application.applicant
    job = application.job

    score = 0

    # Example scoring logic
    if applicant.years_experience and job.required_experience:
        if applicant.years_experience >= job.required_experience:
            score += 30
        else:
            score += (applicant.years_experience / job.required_experience) * 30

    if applicant.technologies and job.required_technologies:
        applicant_techs = set(map(str.strip, applicant.technologies.split(',')))
        job_techs = set(map(str.strip, job.required_technologies.split(',')))
        matching_techs = applicant_techs.intersection(job_techs)
        score += (len(matching_techs) / len(job_techs)) * 50 if job_techs else 0

    if applicant.education and "Bachelor" in applicant.education:
        score += 10
    elif applicant.education and "Master" in applicant.education:
        score += 15
    elif applicant.education and "PhD" in applicant.education:
        score += 20

    application.score = score
    db.session.commit()
    return score