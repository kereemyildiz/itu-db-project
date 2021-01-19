import os
import psycopg2 as dbapi2
from models.user import *
import models.course
from models.faculty import *
from models.teacher import *
from models.course import *
from models.mentor_info import *


def add_user(columns, name, email, password):
    if (not get_user(email)):
        query = """insert into users ({}) values ({},{},{})""".format(
            columns, name, email, password)
        run(query)
        return True
    else:
        return False

def add_mentor(columns,mentorID,facultyId,availability):
    if(get_mentor_by_id(mentorID) == False):
        query = """insert into mentor ({}) values ({},{},{})""".format(
            columns, mentorID, facultyId, availability)
        run(query)

def get_mentor_by_id(mentorID):
    con = dbapi2.connect(os.getenv('DATABASE_URL'))
    cur = con.cursor()
    cur.execute("""SELECT * FROM  mentor
                WHERE (mentorId= {})""".format(mentorID))
    row = cur.fetchone()
    if row:
        return True
    else:
        row=None
        return False

def add_faculty(columns,faculty_name):
    if (not get_faculty(faculty_name)):
        query = """insert into faculty ({}) values ({})""".format(
            columns, faculty_name)
        run(query)
        return True
    else:
        return False

def add_teacher(columns,teacher_name,facultyId):
    if (not get_teacher(teacher_name)):
        query = """insert into teacher ({}) values ({},{})""".format(
            columns, teacher_name,facultyId)
        run(query)
        return True
    else:
        return False


def add_course(columns,course_code,course_name,teacherId,facultyId):
    if (not get_course(course_code,teacherId)):
        query = """insert into course ({}) values ({},{},{},{})""".format(
            columns, course_code,course_name,teacherId,facultyId)
        run(query)
        return True
    else:
        return False

def add_mentor_info(columns,mentorId,courseId,letter_grade,enrollment_year,teacherId):
    if (not get_mentor_info(mentorId,courseId)):
        query = """insert into mentor_info ({}) values ({},{},{},{},{})""".format(
            columns, mentorId,courseId,letter_grade,enrollment_year,teacherId)
        run(query)
        return True
    else:
        return False


def filter_by_course_code(columns,course_code):
    keywords = []
    keywords = columns.replace(' ','').split(',')
    print("keywords")
    print(keywords)
    con = dbapi2.connect(os.getenv('DATABASE_URL'))
    cur = con.cursor()
    cur.execute("""select mentorId,name,course_code,course_name,letter_grade,enrollment_year from (select * from  mentor_info
                inner join course on (course.courseId = mentor_info.courseId)) as q1
                left join users on (q1.mentorId = users.id) where (course_code = {}) order by mentorId desc """.format(course_code))
    result = cur.fetchall()
    print("filter by da")
    if result:
        return result

    else:
        result=None
        return result


def run(query):
    with dbapi2.connect(os.getenv("DATABASE_URL")) as con:
        cur = con.cursor()
        cur.execute(query)
        con.commit()
        cur.close()
