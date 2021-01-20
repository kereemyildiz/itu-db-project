import os
import sys

import psycopg2 as dbapi2

INIT_STATEMENTS = [
"""
CREATE TABLE if not exists faculty(
	facultyID serial PRIMARY KEY,
	faculty_name VARCHAR(30) UNIQUE NOT NULL
)
""",
"""
CREATE TABLE if not exists users (
	id serial PRIMARY KEY,
	name VARCHAR(40),
	email VARCHAR(30) UNIQUE NOT NULL,
	password VARCHAR(30) NOT NULL,
	facultyID INT,
	FOREIGN KEY (facultyID) REFERENCES faculty(facultyID) ON DELETE RESTRICT ON UPDATE CASCADE
)
""",
"""
CREATE TABLE if not exists mentor(
	mentorID serial PRIMARY KEY,
	facultyID INT NOT NULL,
	availability BOOLEAN DEFAULT TRUE,
	vote_score INT,
	FOREIGN KEY (mentorID) REFERENCES users(id) ON DELETE RESTRICT ON UPDATE CASCADE,
	FOREIGN KEY (facultyID) REFERENCES faculty(facultyID) ON DELETE RESTRICT ON UPDATE CASCADE
)
""",
"""
CREATE TABLE if not exists mentee(
	menteeID serial PRIMARY KEY,
	facultyID INT NOT NULL,
	voteID INT,
	FOREIGN KEY (menteeID) REFERENCES users(id) ON DELETE RESTRICT ON UPDATE CASCADE,
	FOREIGN KEY (facultyID) REFERENCES faculty(facultyID) ON DELETE RESTRICT
)
""",
"""
CREATE TABLE if not exists teacher (
	teacherID serial PRIMARY KEY,
	teacher_name VARCHAR(30),
	facultyID INT NOT NULL,
	FOREIGN KEY (facultyID) REFERENCES faculty(facultyID) ON DELETE RESTRICT ON UPDATE CASCADE
)
""",
"""
CREATE TABLE if not exists course(
	courseID serial PRIMARY KEY,
	course_code VARCHAR(7) NOT NULL,
	course_name VARCHAR(20) NOT NULL,
	teacherID INT NOT NULL,
	facultyID INT NOT NULL,
	FOREIGN KEY (teacherID) REFERENCES teacher(teacherID) ON DELETE RESTRICT ON UPDATE CASCADE,
	FOREIGN KEY (facultyID) REFERENCES faculty(facultyID) ON DELETE RESTRICT ON UPDATE CASCADE,
	UNIQUE(course_code,teacherID)
)
""",
"""
CREATE TABLE if not exists mentorship(
	pairNo serial PRIMARY KEY,
	mentorID INT NOT NULL,
	menteeID INT NOT NULL,
	courseID INT NOT NULL,
	FOREIGN KEY (mentorID) REFERENCES mentor(mentorID) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (menteeID) REFERENCES mentee(menteeID) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (courseID) REFERENCES course(courseID) ON DELETE CASCADE ON UPDATE CASCADE
)
""",
"""
CREATE TABLE if not exists mentor_info(
	mentorID INT NOT NULL,
	courseID INT NOT NULL,
	letter_grade VARCHAR(2) NOT NULL,
	enrollment_year NUMERIC(4),
	PRIMARY KEY (mentorID,courseID),
	FOREIGN KEY (mentorID) REFERENCES mentor(mentorID) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (courseID) REFERENCES course(courseID) ON DELETE CASCADE ON UPDATE CASCADE,
	CHECK ((enrollment_year >=1980) AND (enrollment_year <=2020))
)
"""
]


def initialize(url):
    with dbapi2.connect(url) as con:
        cursor = con.cursor()
        for statement in INIT_STATEMENTS:
            cursor.execute(statement)
        cursor.close()


if __name__ == "__main__":  # for heroku
    url = os.getenv("DATABASE_URL")
    if url is None:
        print("Usage: dbinit.py databse url error")
        sys.exit(1)
    initialize(url)
