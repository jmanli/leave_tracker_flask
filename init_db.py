# init_db.py
import os
from flask import Flask
from models import db, User # Import db and User from models.py
from dotenv import load_dotenv

load_dotenv() # Load environment variables for SECRET_KEY

def create_app_context():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'a_fallback_secret_key_if_env_not_loaded')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    return app

if __name__ == '__main__':
    app = create_app_context()
    with app.app_context():
        db.create_all()
        print("Database tables created.")

        # Create a default admin user if one doesn't exist
        admin_user = User.query.filter_by(username='admin').first()
        if not admin_user:
            admin_user = User(username='admin', role='admin')
            admin_user.set_password('adminpass') # !!! CHANGE THIS PASSWORD IN PRODUCTION!
            db.session.add(admin_user)
            db.session.commit()
            print("Default admin user 'admin' with password 'adminpass' created.")
        else:
            print("Admin user already exists.")

        # Create a default employee user if one doesn't exist
        employee_user = User.query.filter_by(username='employee').first()
        if not employee_user:
            employee_user = User(username='employee', role='employee')
            employee_user.set_password('employeepass') # !!! CHANGE THIS PASSWORD IN PRODUCTION!
            db.session.add(employee_user)
            db.session.commit()
            print("Default employee user 'employee' with password 'employeepass' created.")
        else:
            print("Employee user already exists.")

    print("Database setup complete.")