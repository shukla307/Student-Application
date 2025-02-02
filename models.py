from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    academic_background = db.Column(db.Text, nullable=False)
    degree_certificate = db.Column(db.String(100), nullable=False)
    id_proof = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), default='Pending')
    admission_letter = db.Column(db.String(100))

    def __repr__(self):
        return f'<Application {self.name}>'