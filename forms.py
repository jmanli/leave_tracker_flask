# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, TextAreaField, SelectField, HiddenField
from wtforms.validators import DataRequired, EqualTo, ValidationError
from models import User # Import User model to validate username
from config import ROLE_CHOICES, NAME_CHOICES  # Import choices

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Role', choices=ROLE_CHOICES, validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

class LeaveRequestForm(FlaskForm):
    start_date = DateField('Start Date', format='%Y-%m-%d', validators=[DataRequired()])
    end_date = DateField('End Date', format='%Y-%m-%d', validators=[DataRequired()])
    leave_type = SelectField('Leave Type', choices=[
        ('Vacation', 'Vacation'),
        ('Sick Leave', 'Sick Leave'),
        ('Personal Leave', 'Personal Leave'),
        ('Maternity/Paternity', 'Maternity/Paternity')
    ], validators=[DataRequired()])
    reason = TextAreaField('Reason (Optional)')
    submit = SubmitField('Submit Leave Request')

    def validate(self, extra_validators=None):
        if not super().validate(extra_validators):
            return False
        if self.start_date.data and self.end_date.data and self.start_date.data > self.end_date.data:
            self.end_date.errors.append('End date must not be before start date.')
            return False
        return True

class AdminLeaveActionForm(FlaskForm):
    leave_id = HiddenField('Leave ID', validators=[DataRequired()])
    status = SelectField('Status', choices=[
        ('Approved', 'Approve'),
        ('Rejected', 'Reject')
    ], validators=[DataRequired()])
    submit = SubmitField('Update Status')