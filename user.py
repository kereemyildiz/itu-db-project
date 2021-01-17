from flask_login import UserMixin
import psycopg2 as dbapi2
import os


class User(UserMixin):
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password
        self.active = True


    def get_id(self):
        _email = "'{}'".format(self.email)
        print("get id aliyorsa email")
        print(_email)
        return _email
    @property
    def is_active(self):
        return self.active


def get_user(email):
    print("*** get_userda")
    print(email)
    print(type(email))
    con = dbapi2.connect(os.getenv('DATABASE_URL'))
    cur = con.cursor()
    cur.execute("""SELECT * FROM  users
                WHERE (email= {})""".format(email))

    row = cur.fetchone()
    user = User(row[1], row[3], row[2]) if row else None
    if user is not None:
        return user

    print("User not found")
    return user
