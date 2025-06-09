# app.py
import os
from datetime import datetime, date
from dotenv import load_dotenv

from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

# Import models, forms, and decorators from our new files
from models import db, User, LeaveRequest
from forms import LoginForm, RegistrationForm, LeaveRequestForm, AdminLeaveActionForm
from decorators import admin_required, employee_required

# Load environment variables
load_dotenv()


# --- Flask App Configuration ---
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'a_fallback_secret_key_if_env_not_loaded')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
print(f"SECRET_KEY: {app.config['SECRET_KEY']}")

# --- Database Initialization ---
db.init_app(app) # Initialize SQLAlchemy with the Flask app

# --- Flask-Login Initialization ---
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' # Redirect to login page if user is not logged in

# --- User Loader for Flask-Login ---
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- Routes ---
@app.route('/')
def index():
    if current_user.is_authenticated:
        if current_user.is_admin():
            return redirect(url_for('admin_dashboard'))
        else:
            return redirect(url_for('employee_dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            flash('Logged in successfully!', 'success')
            return redirect(next_page or url_for('index'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, role=form.role.data)
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

# --- Employee Page ---
@app.route('/employee_dashboard')
@employee_required
def employee_dashboard():
    user_leaves = LeaveRequest.query.filter_by(user_id=current_user.id).order_by(LeaveRequest.created_at.desc()).all()
    return render_template('employee_dashboard.html', leaves=user_leaves)

@app.route('/create_leave', methods=['GET', 'POST'])
@employee_required
def create_leave():
    form = LeaveRequestForm()
    if form.validate_on_submit():
        new_leave = LeaveRequest(
            user_id=current_user.id,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            leave_type=form.leave_type.data,
            reason=form.reason.data
        )
        db.session.add(new_leave)
        db.session.commit()
        flash('Leave request submitted successfully!', 'success')
        return redirect(url_for('employee_dashboard'))
    return render_template('create_leave.html', form=form)

@app.route('/amend_leave/<int:leave_id>', methods=['GET', 'POST'])
@employee_required
def amend_leave(leave_id):
    leave = LeaveRequest.query.get_or_404(leave_id)
    if leave.user_id != current_user.id:
        flash('You are not authorized to amend this leave request.', 'danger')
        return redirect(url_for('employee_dashboard'))

    # Only allow amending if pending
    if leave.status != 'Pending':
        flash('Only pending leave requests can be amended.', 'warning')
        return redirect(url_for('employee_dashboard'))

    form = LeaveRequestForm(obj=leave) # Populate form with existing leave data
    if form.validate_on_submit():
        leave.start_date = form.start_date.data
        leave.end_date = form.end_date.data
        leave.leave_type = form.leave_type.data
        leave.reason = form.reason.data
        db.session.commit()
        flash('Leave request amended successfully!', 'success')
        return redirect(url_for('employee_dashboard'))
    return render_template('amend_leave.html', form=form, leave=leave)

@app.route('/delete_leave/<int:leave_id>', methods=['POST'])
@employee_required
def delete_leave(leave_id):
    leave = LeaveRequest.query.get_or_404(leave_id)
    if leave.user_id != current_user.id:
        flash('You are not authorized to delete this leave request.', 'danger')
        return redirect(url_for('employee_dashboard'))

    # Only allow deleting if pending
    if leave.status != 'Pending':
        flash('Only pending leave requests can be deleted.', 'warning')
        return redirect(url_for('employee_dashboard'))

    db.session.delete(leave)
    db.session.commit()
    flash('Leave request deleted successfully!', 'success')
    return redirect(url_for('employee_dashboard'))

# --- Admin Page ---
@app.route('/admin_dashboard')
@admin_required
def admin_dashboard():
    # Get username from query parameters
    action_form = AdminLeaveActionForm()
    username = request.args.get('username', default='', type=str)

    # Build query to filter only by requester username
    if username:
        leaves = LeaveRequest.query.filter(LeaveRequest.requester.has(User.username == username)).all()
    else:
        leaves = LeaveRequest.query.order_by(LeaveRequest.created_at.desc()).all()  # Fetch all if no filter is applied

    return render_template('admin_dashboard.html', leaves=leaves, selected_username=username, action_form=action_form)

   # all_leaves = LeaveRequest.query.order_by(LeaveRequest.created_at.desc()).all()
   
   # return render_template('admin_dashboard.html', leaves=all_leaves, action_form=action_form)

@app.route('/admin_action', methods=['POST'])
@admin_required
def admin_action():
    form = AdminLeaveActionForm()
    print(f"\n--- Debugging /admin_action ---")
    print(f"Request Method: {request.method}")
    print(f"Request Form Data: {request.form}")
    print(f"Form is submitted: {form.is_submitted()}")
    print(f"Forms Leave ID: {form.leave_id.data} ")
    
    validation_result = form.validate_on_submit()
    print(f"Form validate_on_submit() result: {validation_result}")
    print(f"Form errors: {form.errors}")
       
    if form.validate_on_submit():
        leave_id = form.leave_id.data
        leave = LeaveRequest.query.get_or_404(leave_id)
        print("Retrieved leave.id:", leave.id)
        new_status = form.status.data

        if leave.status == new_status:
            flash(f"Leave request {leave.id} is already '{new_status}'.", 'info')
        else:
            leave.status = new_status
            db.session.commit()
            flash(f'Leave request {leave.id} updated to {new_status}!', 'success')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error on {field}: {error}", 'danger')
    return redirect(url_for('admin_dashboard'))

# --- Main App Execution ---
if __name__ == '__main__':
    app.run(debug=True) # debug=True is for development, set to False in production