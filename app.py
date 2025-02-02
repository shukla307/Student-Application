from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from models import db, Application
from werkzeug.utils import secure_filename
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///applications.db'
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
app.config['SECRET_KEY'] = 'your_secret_key'

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/apply', methods=['GET', 'POST'])
def apply():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        academic_background = request.form['academic_background']
        degree_certificate = request.files['degree_certificate']
        id_proof = request.files['id_proof']

        degree_filename = secure_filename(degree_certificate.filename)
        id_filename = secure_filename(id_proof.filename)

        degree_certificate.save(os.path.join(app.config['UPLOAD_FOLDER'], degree_filename))
        id_proof.save(os.path.join(app.config['UPLOAD_FOLDER'], id_filename))

        new_application = Application(
            name=name,
            email=email,
            academic_background=academic_background,
            degree_certificate=degree_filename,
            id_proof=id_filename
        )

        db.session.add(new_application)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('apply.html')

@app.route('/admin')
def admin():
    applications = Application.query.all()
    return render_template('admin.html', applications=applications)

@app.route('/approve/<int:id>')
def approve(id):
    application = Application.query.get_or_404(id)
    application.status = 'Approved'
    admission_letter_path = generate_admission_letter(application)
    application.admission_letter = admission_letter_path
    db.session.commit()
    return redirect(url_for('admin'))

@app.route('/reject/<int:id>')
def reject(id):
    application = Application.query.get_or_404(id)
    application.status = 'Rejected'
    db.session.commit()
    return redirect(url_for('admin'))

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

def generate_admission_letter(application):
    filename = f'admission_letter_{application.id}.pdf'
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    c = canvas.Canvas(filepath, pagesize=letter)
    c.drawString(100, 750, f"Admission Letter for {application.name}")
    c.drawString(100, 730, f"Email: {application.email}")
    c.drawString(100, 710, f"Academic Background: {application.academic_background}")
    c.drawString(100, 690, "Congratulations! Your application has been approved.")
    c.save()

    return filename

if __name__ == '__main__':
    app.run(debug=True)



    