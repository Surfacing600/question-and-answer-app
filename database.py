from flask import g
import psycopg2
from psycopg2.extras import DictCursor

def connect_db():
    conn = psycopg2.connect('postgres://jqfnmdamxelzbx:c33853bb72cc77a3c771743198b2aab7078ff52f937e68d9105a9163036862de@ec2-54-242-120-138.compute-1.amazonaws.com:5432/d19cccc1ggq1or', cursor_factory=DictCursor)
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

    db[1].execute('update users set adminn = True where name = %s', ('admin', ))

    db[1].close()
    db[0].close()