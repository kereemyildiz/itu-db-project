import psycopg2 as dbapi2
import os

def get_teacher(teacher_name):
    con = dbapi2.connect(os.getenv('DATABASE_URL'))
    cur = con.cursor()
    cur.execute("""SELECT * FROM  teacher
                WHERE (teacher_name= {})""".format(teacher_name))

    row = cur.fetchone()
    teacherid  = row[0] if row else None
    if teacherid is not None:
        return teacherid

    print("Teacher not found")
    return teacherid
