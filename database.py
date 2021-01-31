from flask import g
import psycopg2
from psycopg2.extras import DictCursor

def connect_db():
    conn = psycopg2.connect('postgres://fhqwgsxsmvqlrs:948a494ef0bace6169dc9f91a02e4ee870ee9e9e9aba7888ba929db1f4bb2a4e@ec2-3-216-181-219.compute-1.amazonaws.com:5432/dea0pfl3pmfih2', cursor_factory=DictCursor)
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