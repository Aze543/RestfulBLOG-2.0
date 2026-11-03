from sqlalchemy import ForeignKey, String, Text, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import datetime
from components.config import DEFAULT_AVATAR
from components.app_utils import gravatar_url

STATUS_PENDING = "pending"
STATUS_APPROVED = "approved"
STATUS_REJECTED = "rejected"



class Base(DeclarativeBase):
    pass

class BlogPost(Base):
    __tablename__ = "blog_post"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    img_url: Mapped[str] = mapped_column(Text, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    comments: Mapped[list["Comment"]] = relationship("Comment", back_populates="post", cascade="all, delete-orphan", order_by="Comment.id.desc()")

class User(Base):
    @property
    def avatar(self):
        return self.image or gravatar_url(self.email)
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(250), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(250), nullable=False)
    name: Mapped[str] = mapped_column(String(250), nullable=False)
    image: Mapped[str | None] = mapped_column(String(250))
    comments: Mapped[list["Comment"]] = relationship("Comment", back_populates="author")

class Comment(Base):
    @property
    def avatar(self):
         if self.author:
             return self.author.avatar
         return DEFAULT_AVATAR
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(250), nullable=False)
    comment: Mapped[str] = mapped_column(Text, nullable=False)
    name: Mapped[str] = mapped_column(String(250), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("blog_post.id", ondelete="CASCADE"))
    post: Mapped["BlogPost"] = relationship("BlogPost", back_populates="comments")
    author_id: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"))
    author: Mapped["User | None"] = relationship("User", back_populates="comments")

class PostRequest(Base):
    __tablename__ = "post_requests"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(250))
    subtitle: Mapped[str] = mapped_column(String(250))
    body: Mapped[str] = mapped_column(Text)
    img_url: Mapped[str] = mapped_column(Text)
    author_id: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"))
    author: Mapped["User | None"] = relationship()
    status: Mapped[str] = mapped_column(String(20), default=STATUS_PENDING)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    admin_note: Mapped[str | None] = mapped_column(Text)




"""
CREATE TABLE IF NOT EXISTS blog_post (
    id        SERIAL PRIMARY KEY,
    title     VARCHAR(250) NOT NULL,
    date      VARCHAR(250) NOT NULL,
    body      TEXT NOT NULL,
    author    VARCHAR(250) NOT NULL,
    img_url   TEXT NOT NULL,
    subtitle  VARCHAR(250) NOT NULL
);

CREATE TABLE IF NOT EXISTS users (
    id        SERIAL PRIMARY KEY,
    email     VARCHAR(250) NOT NULL UNIQUE,
    password  VARCHAR(250) NOT NULL,
    name      VARCHAR(250) NOT NULL
);

CREATE TABLE IF NOT EXISTS comments (
    id        SERIAL PRIMARY KEY,
    title     VARCHAR(250) NOT NULL,
    comment   TEXT NOT NULL,
    name      VARCHAR(250) NOT NULL,
    image     VARCHAR(250),
    post_id   INTEGER REFERENCES blog_post(id) ON DELETE CASCADE
);
"""
