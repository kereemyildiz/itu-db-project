import os
import sys

import psycopg2 as dbapi2

INIT_STATEMENTS = [
    """
    create table if not exists users(
        id serial primary key,
        name varchar(100) not null,
        password varchar(100),
        email varchar(100) unique not null,
        register_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP

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
