from extensions import db

#טבלת משתמשים למערכת
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    applicants = db.relationship("Applicant", back_populates="user", uselist=False)
