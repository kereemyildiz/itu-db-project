from wtforms import Form, StringField, TextAreaField, PasswordField,IntegerField, validators
from passlib.hash import sha256_crypt
from wtforms.validators import DataRequired, NumberRange
from datetime import datetime

class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    faculty = StringField('Faculty Name', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')


class LoginForm(Form):
    email2 = StringField('Email', [validators.Length(min=6, max=50)])
    password2 = PasswordField('Password', [
        validators.DataRequired()
    ])

class CourseForm(Form):
    course_code = StringField('Course Code', [validators.Length(min=3, max=10)])
    course_name = StringField('Course Name', [validators.Length(min=3, max=30)])
    letter_grade = StringField('Letter Grade', [validators.Length(min=2, max=2)])
    teacher = StringField('Teacher', [validators.Length(min=3, max=40)])
    faculty_name = StringField('Faculty Name', [validators.Length(min=3, max=30)])
    enrollment_year = IntegerField("Enrollment Year",
                                    validators=[
                                        NumberRange(min=1980,max=datetime.now().year),
                                    ],
                                    )

class FilterForm(Form):
    course_code = StringField('Course Code', [validators.Length(min=3, max=10),validators.DataRequired()])
class UpdateForm(Form):
    email = StringField('Email', [validators.Length(min=6, max=50),DataRequired()])
    faculty_name = StringField('Faculty Name', [validators.Length(min=6, max=50),DataRequired()])
