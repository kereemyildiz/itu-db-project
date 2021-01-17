import os
import psycopg2 as dbapi2
import user


def add_user(columns, name, email, password):
    # TODO : İF USERNAME İS ALREADY TAKEN OR NOT

    if (not user.get_user(email)):
        query = """insert into users ({}) values ({},{},{})""".format(
            columns, name, email, password)
        run(query)
        return True
    else:
        return False


def run(query):
    with dbapi2.connect(os.getenv("DATABASE_URL")) as con:
        cur = con.cursor()
        cur.execute(query)
        con.commit()
        cur.close()
