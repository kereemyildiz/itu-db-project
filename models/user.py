from flask_login import UserMixin
import psycopg2 as dbapi2
import os


class User(UserMixin):
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password
        self.active = True
        self.id = -1 # default -1 we will change this value
        self.availability = True


    def get_id(self):
        _email = "'{}'".format(self.email)
        return _email
    @property
    def is_active(self):
        return self.active


def get_user(email):
    con = dbapi2.connect(os.getenv('DATABASE_URL'))
    cur = con.cursor()
    cur.execute("""SELECT * FROM  users
                WHERE (email= {})""".format(email))

    row = cur.fetchone()
    if row:
        user = User(row[1], row[3], row[2])
        user.id = row[0] # set the user id
    else:
        user = None
    if user is not None:
        return user

    print("User not found")
    return user
