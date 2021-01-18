import psycopg2 as dbapi2
import os

def get_faculty(faculty_name):
    con = dbapi2.connect(os.getenv('DATABASE_URL'))
    cur = con.cursor()
    cur.execute("""SELECT * FROM  faculty
                WHERE (faculty_name= {})""".format(faculty_name))

    row = cur.fetchone()
    facultyid  = row[0] if row else None
    if facultyid is not None:
        return facultyid

    print("Faculty not found")
    return facultyid
