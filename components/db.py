from flask import g, abort
from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session, sessionmaker
from sqlalchemy.engine import URL, Connection
import os
#own modules
from components.config import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD, DB_URL
from components.models import Base, BlogPost, User, Comment

if DB_URL:
    url = DB_URL.replace("postgres://", "postgresql://", 1)  # some hosts use the old prefix
else:
    url = URL.create(
        "postgresql+psycopg2",
        username=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        database=DB_NAME
    )

engine = create_engine(url, pool_pre_ping=True, echo=False)
SessionLocal = sessionmaker(engine)


def init_db():
    Base.metadata.create_all(engine)


def get_session():
    """One connection per request, closed automatically afterwards."""
    if "session" not in g:
        g.session = SessionLocal()
    return g.session


def close_db(exc):
    session = g.pop("session", None)
    if session is not None:
        # TODO 1: if exc is not None, roll back
        if exc is not None:
            session.rollback()
        # TODO 2: always close
        session.close()


def query(sql, params=(), one=False):
    with get_db().cursor() as cursor:
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        if one:
            return rows[0] if rows else None
    return rows


def execute_returning(sql, params=()):
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute(sql, params)
        row = cursor.fetchone()
    db.commit()
    return row


def execute(sql, params=()):
    db = get_db()
    with db.cursor() as cursor:
        cursor.execute(sql, params)
        count = cursor.rowcount
    db.commit()
    return count


def get_post_or_404(post_id):
    post = get_session().get(BlogPost, post_id)
    if post is None:
        abort(404)
    return post
