

2. Project Structure

Let's create a monorepo-like structure:

leave_tracker_flask/
├── venv
├── .env
├── app.py
├── decorators.py
├── forms.py
├── init_db.py
├── models
├── ReadMe
├── templates
│   ├── admin_dashboard.html
│   ├── amend_leave.html
│   ├── base.html
│   ├── create_leave.html
│   ├── employee_dashboard.html
│   ├── login.html
│   ├── register.html
└── .gitignore



python -m venv venv
	is used to create a virtual environment in Python. Here’s what each part does:
	- python -m: Runs a Python module as a script.
	- venv: The built-in module used to create virtual environments.
	- venv (again): The name of the virtual environment folder to be created.
	How It Works
	- It sets up an isolated environment where Python packages can be installed without interfering with the system-wide Python installation.
	- The venv folder contains its own Python interpreter and dependencies.
	- It helps manage different projects that require different versions of packages

venv\Scripts\activate
	is used to activate the environment
	
pip install Flask Flask-SQLAlchemy Flask-Login Flask-WTF python-dotenv Werkzeug
	Breakdown of Each Package
	- Flask → The web framework itself.
	- Flask-SQLAlchemy → Helps integrate SQLAlchemy for database management.
	- Flask-Login → Handles user authentication and session management.
	- Flask-WTF → Simplifies form handling with WTForms.
	- python-dotenv → Manages environment variables from a .env file.
	- Werkzeug → Provides utilities for handling HTTP requests and security.
	Once installed, you can start building your Flask app with authentication, database integration, and secure request handling.

python init_db.py 
	Running python init_db.py executes your init_db.py script, which should contain logic to initialize your database. Here’s what happens when you run it:
	What This Command Does
	- Executes init_db.py → Python runs the script that initializes your database.
	- Sets Up Tables → If init_db.py calls db.create_all(), it creates tables based on your SQLAlchemy models.
	- Configures Database Connections → If you use Flask-SQLAlchemy, ensure your database URI is correctly set in your Flask app.

python app.py 