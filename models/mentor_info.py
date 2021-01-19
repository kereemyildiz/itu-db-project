import psycopg2 as dbapi2
import os


def get_mentor_info(mentorId,courseId):
    con = dbapi2.connect(os.getenv('DATABASE_URL'))
    cur = con.cursor()
    cur.execute("""SELECT * FROM  mentor_info
                WHERE (mentorId= {} and courseId={})""".format(mentorId,courseId))

    row = cur.fetchone()
    pr_key  = row if row else None
    if pr_key is not None:
        return pr_key

    #print("Mentor with given course code not found")
    return pr_key
