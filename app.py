import os
from db_init import initialize

from flask import Flask, redirect, url_for, request, render_template, flash, session, logging
# from data import Articles
from forms import RegisterForm, LoginForm,FilterForm
from flask_login.utils import login_required, login_user, logout_user
from flask_login import LoginManager
import psycopg2 as db
from models.user import User, get_user
from queries import add_user
import views

HEROKU = False

if (not HEROKU):
    os.environ['DATABASE_URL'] = "dbname='dbproject_2' user='postgres' host=localhost password='k1e2r3e4m5'"
    initialize(os.environ.get('DATABASE_URL'))

lm = LoginManager()


@lm.user_loader
def load_user(email):
	return get_user(email)


def create_app():
    app = Flask(__name__)
    app.config.from_object("settings")

    app.add_url_rule("/", view_func=views.home_page)
    app.add_url_rule("/about", view_func=views.about)
    app.add_url_rule("/profile", view_func=views.profile,methods = ['GET','POST'])
    app.add_url_rule("/add-mentor", view_func=views.mentor_page,methods = ['GET','POST'])
    app.add_url_rule("/mentor-list", view_func=views.mentor_list, methods = ['GET','POST'])
    app.add_url_rule("/register", view_func=views.register,
                     methods=['GET', 'POST'])
    app.add_url_rule("/login", view_func=views.login, methods=['GET', 'POST'])
    app.add_url_rule("/logout", view_func=views.logout)

    lm.init_app(app)
    lm.login_view = "login"
    return app


if __name__ == "__main__":
    if (not HEROKU):
        app = create_app()
        app.run(debug=True)
    else:
        app = create_app()
        app.run()
