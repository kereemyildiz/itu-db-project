import os
import psycopg2 as dbapi2
from models.user import *
import models.course
from models.faculty import *
from models.teacher import *
from models.course import *
from models.mentor_info import *


def add_user(columns, name, email, password,facultyId):
    if (not get_user(email)):
        query = """insert into users ({}) values ({},{},{},{})""".format(
            columns, name, email, password,facultyId)
        print(query)
        run(query)
        return True
    else:
        return False

def add_mentor(columns,mentorID,facultyId,availability):
    if(get_mentor_by_id(mentorID) == False):
        query = """insert into mentor ({}) values ({},{},{})""".format(
            columns, mentorID, facultyId, availability)
        run(query)
        return True
    else:
        return False

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

def add_mentor_info(columns,mentorId,courseId,letter_grade,enrollment_year):
    if (not get_mentor_info(mentorId,courseId)):
        query = """insert into mentor_info ({}) values ({},{},{},{})""".format(
            columns, mentorId,courseId,letter_grade,enrollment_year)
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
    cur.execute("""select mentorId,name,course_code,course_name,letter_grade,enrollment_year,teacher_name,teacher.teacherId from (select * from (select * from  mentor_info
                inner join course on (course.courseId = mentor_info.courseId)) as q1
                left join users on (q1.mentorId = users.id)) as q2 inner join teacher on (q2.teacherId = teacher.teacherId) where (course_code = {}) order by mentorId asc """.format(course_code))
    result = cur.fetchall()
    print("filter by da")
    for mentor in result:
        print("++++")
        print(mentor[0])
        print(type(mentor))
    if result:
        return result

    else:
        result=None
        return result


def update_email(email,id):
    query = """update users set email = {} where id = {}""".format(email,id)
    run(query)

def update_facultyId(facultyId,id):
    query = """update users set facultyId = {} where id = {}""".format(facultyId,id)
    run(query)

def get_mentee_by_id(menteeID):
    con = dbapi2.connect(os.getenv('DATABASE_URL'))
    cur = con.cursor()
    cur.execute("""SELECT * FROM  mentee
                WHERE (menteeId= {})""".format(menteeID))
    row = cur.fetchone()
    if row:
        return True
    else:
        row=None
        return False

def add_mentee(columns,menteeId,facultyId):
    if(get_mentee_by_id(menteeId) == False):
        query = """insert into mentee ({}) values ({},{})""".format(
            columns, menteeId, facultyId)
        run(query)
        return True
    else:
        return False

def get_mentorship(menteeId,course_code):
    con = dbapi2.connect(os.getenv('DATABASE_URL'))
    cur = con.cursor()
    cur.execute("""select menteeId,course_code from mentorship inner join course
     on (mentorship.courseId = course.courseId) where (menteeId = {} and
     course_code={})""".format(menteeId,course_code))
    row = cur.fetchone()
    unique  = row if row else None
    if unique is not None:
        return unique
    #print("Mentor with given course code not found")
    return unique


def add_mentorship(columns,mentorId,menteeId,courseId,course_code):
    if (not get_mentorship(menteeId,course_code)):
        query = """insert into mentorship ({}) values ({},{},{})""".format(
            columns,mentorId,menteeId,courseId)
        run(query)
        return True
    else:
        return False

def get_mentors(menteeId):
    con = dbapi2.connect(os.getenv('DATABASE_URL'))
    cur = con.cursor()
    cur.execute("""select pairNo,name,course_code,course_name,letter_grade,teacher_name from
    (select * from(select * from(select * from (select * from mentor_info natural join
    mentorship where menteeId = {}) as q1 natural join mentor ) as q2 natural join users) as
    q3 inner join course on (course.courseId = q3.courseId)) as q4 inner join teacher on
    (teacher.teacherId = q4.teacherId)""".format(menteeId))
    result = cur.fetchall()
    for mentor in result:
        print("???")
        print(mentor[0])
        print(type(mentor))
    if result:
        return result

    else:
        result=None
        return result

def get_mentees(mentorId):
    con = dbapi2.connect(os.getenv('DATABASE_URL'))
    cur = con.cursor()
    cur.execute("""select name,course_code,course_name,email
     from(select * from(select * from (select * from mentor_info natural
     join mentorship where mentorId = {}) as q1 natural join mentee ) as q2
     natural join users) as q3 inner join course on (course.courseId =
      q3.courseId) """.format(mentorId))
    result = cur.fetchall()
    for mentor in result:
        print("???")
        print(mentor[0])
        print(type(mentor))
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
