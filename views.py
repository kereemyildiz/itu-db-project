from flask import Flask, redirect, url_for, request, render_template, flash, session, logging
#from data import Articles
from forms import RegisterForm, LoginForm, CourseForm,FilterForm
from flask_login.utils import login_required, login_user, logout_user,current_user
from flask_login import LoginManager
import psycopg2 as db
from models.user import User, get_user
from queries import *
from models.faculty import get_faculty
from passlib.hash import sha256_crypt

global current_user

def home_page():
    return render_template("home_page.html")


def about():
    return render_template("about.html")



def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():

        user = User(form.name.data, form.email.data,
                    sha256_crypt.hash(form.password.data))
        print("password:")
        print(form.password.data)
        print(user.password)

        is_new_user = add_user(columns="name,email,password", name="'{}'".format(
            user.name), email="'{}'".format(user.email), password="'{}'".format(user.password))

        if (is_new_user):
            flash('You are now registered and can login', 'success')
            return redirect(url_for('login'))
        else:
            flash('Account with given email already exist', 'danger')
            return redirect(url_for('register'))

    return render_template("register.html", form=form)


def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        email = "'{}'".format(form.email2.data)
        current_user = get_user(email)
        if current_user is not None:
            pw = form.password2.data
            if sha256_crypt.verify(pw, current_user.password):
                login_user(current_user)
                flash("You have logged in !")
                next_page = request.args.get("next", url_for("home_page"))
                return redirect(next_page)
        flash("Invalid credentials !")
        return render_template("login.html", form=form)
    return render_template("login.html", form=form)


@login_required
def profile():
    return render_template("profile.html")

@login_required
def mentor_page():
    form  = CourseForm(request.form)
    if request.method == 'POST' and form.validate():
        course_code = "'{}'".format(form.course_code.data)
        course_name = "'{}'".format(form.course_name.data)
        letter_grade = "'{}'".format(form.letter_grade.data)
        teacher = "'{}'".format(form.teacher.data)
        faculty_name = "'{}'".format(form.faculty_name.data)
        enrollment_year = form.enrollment_year.data

        add_faculty(columns="faculty_name",faculty_name=faculty_name)
        faculty_id = get_faculty(faculty_name)

        add_teacher(columns="teacher_name,facultyId",teacher_name=teacher,facultyId=faculty_id)
        teacher_id = get_teacher(teacher)

        add_mentor(columns="mentorID,facultyId,availability",mentorID=current_user.id,facultyId=faculty_id,availability=current_user.availability)
        mentor_id = current_user.id

        add_course(columns="course_code,course_name,teacherId,facultyId",course_code=course_code,course_name=course_name,teacherId=teacher_id,facultyId=faculty_id)
        course_id = get_course(course_code,teacher_id)

        add_mentor_info(columns="mentorId,courseId,letter_grade,enrollment_year,teacherId",
                        mentorId=mentor_id,courseId=course_id,letter_grade=letter_grade,enrollment_year=enrollment_year,teacherId=teacher_id)

        flash('Successfully added to mentor list','success')
        return render_template("home_page.html",form=form)
    return render_template("mentor_page.html",form=form)


@login_required
def mentor_list():
    form = FilterForm(request.form)
    flag = False
    mentors = []
    if request.method == 'POST' and form.validate():
        flag = True
        course_code = "'{}'".format(form.course_code.data)
        mentors = filter_by_course_code(columns="mentorId,name,course_code,course_name,letter_grade,enrollment_year",course_code=course_code)
        print("type of mentors is")
        print(mentors)
        print(type(mentors))
        if mentors is None:
            flash('No mentors found with given course code','danger')
            next_page = request.args.get("next", url_for("mentor_list"))
            return redirect(next_page)
        flash('Mentors are successfully listed','success')
        return render_template("mentor_list_page.html",form=form,mentors=mentors,flag=flag)
    elif request.method == 'POST' and not form.validate():
        mentor_id = int(request.form['mentor_key'])
        mentee_id = current_user.id
        


        return redirect(url_for('login'))
    return render_template('mentor_list_page.html',form=form,mentors=mentors,flag=flag)



@login_required
def logout():
    logout_user()
    flash("You have logged out")
    return redirect(url_for("home_page"))
