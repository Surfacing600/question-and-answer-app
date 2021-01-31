from flask import g
import psycopg2
from psycopg2.extras import DictCursor

def connect_db():
    conn = psycopg2.connect('postgres://foigaraxfmyyvp:ddc8999e4410329826df6ba2145655400cddf0a636eca4859f669cf3d746428b@ec2-54-172-17-119.compute-1.amazonaws.com:5432/ddkp879j8btks9', cursor_factory=DictCursor)
    conn.autocommit = True
    sql = conn.cursor()
    return conn, sql

def get_db():
    db = connect_db()

    if not hasattr(g, 'postgres_db_conn'):
        g.postgres_db_conn = db[0]

    if not hasattr(g, 'postgres_db_cur'):
        g.postgres_db_cur = db[1]

    return g.postgres_db_cur

def init_db():
    db = connect_db()

    db[1].execute(open('schema.sql', 'r').read())
    db[1].close()

    db[0].close()

def init_admin():
    db = connect_db()

    db[1].execute('update users set admin = True where name = %s', ('admin', ))

    db[1].close()
    db[0].close()