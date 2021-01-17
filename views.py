from flask import Flask, redirect, url_for, request, render_template, flash, session, logging
#from data import Articles
from forms import RegisterForm, LoginForm
from flask_login.utils import login_required, login_user, logout_user
from flask_login import LoginManager
import psycopg2 as db
from user import User, get_user
from queries import add_user

from passlib.hash import sha256_crypt


def home_page():
    return render_template("home_page.html")


def about():
    return render_template("about.html")


def articles():
    return render_template("articles.html", articles=Articles)


def article(id):
    return render_template("article.html", id=id)


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
        print("**** girdi ****")
        email = "'{}'".format(form.email2.data)
        global current_user
        current_user = get_user(email)
        print("***")
        print(current_user.name)
        if current_user is not None:
            pw = form.password2.data
            print("pw:")
            print(pw)
            print(str(pw))
            print(current_user.password)
            if sha256_crypt.verify(pw, current_user.password):
                login_user(current_user)
                flash("You have logged in !")
                next_page = request.args.get("next", url_for("home_page"))
                return redirect(next_page)
        flash("Invalid credentials !")
        return render_template("login.html", form=form)
    return render_template("login.html", form=form)

def logout():
    logout_user()
    flash("You have logged out")
    return redirect(url_for("home_page"))
