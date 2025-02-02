import os
import unittest
from app import app, db, Application
from werkzeug.datastructures import FileStorage

class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        """Set up a test client and initialize the database."""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        """Clean up the database after each test."""
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_index_page(self):
        """Test the index page."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to the Admission Portal', response.data)

    def test_apply_page(self):
        """Test the application form page."""
        response = self.app.get('/apply')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Application Form', response.data)

    def test_submit_application(self):
        """Test submitting an application."""
        data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'academic_background': 'Bachelor of Science',
        }
        files = {
            'degree_certificate': (FileStorage(
                stream=open('static/uploads/sample_degree.pdf', 'rb'),
                filename='sample_degree.pdf'
            ), 'sample_degree.pdf'),
            'id_proof': (FileStorage(
                stream=open('static/uploads/sample_id.pdf', 'rb'),
                filename='sample_id.pdf'
            ), 'sample_id.pdf')
        }
        response = self.app.post('/apply', data=data, files=files, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 302)  # Redirect after submission

    def test_admin_page(self):
        """Test the admin page."""
        response = self.app.get('/admin')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Admin Panel', response.data)

if __name__ == '__main__':
    unittest.main()
