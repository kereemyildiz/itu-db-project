import psycopg2 as dbapi2
import os

class Course():
    def __init__(self,course_code,course_name,letter_grade,teacherId):
        self.course_code = course_code
        self.course_name = course_name
        self.letter_grade = letter_grade
        self.teacherId = teacherId

def get_course(course_code,teacherId):
    con = dbapi2.connect(os.getenv('DATABASE_URL'))
    cur = con.cursor()
    cur.execute("""SELECT * FROM  course
                WHERE (course_code= {} and teacherId={})""".format(course_code,teacherId))

    row = cur.fetchone()
    course_id  = row[0] if row else None
    if course_id is not None:
        return course_id

    print("Course code not found")
    return course_id
