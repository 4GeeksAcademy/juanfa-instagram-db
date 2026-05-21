from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

db = SQLAlchemy()

class MediaType(enum.Enum):
    image = "image"
    video = "video"


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String(120), unique= True, nullable=False)
    firstname: Mapped[str] = mapped_column(String(120), nullable=False)
    lastname: Mapped[str] = mapped_column(String(120), nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    #Relationships
    posts: Mapped["Post"] = relationship("Post", back_populates="user")
    comments: Mapped[list["Comment"]] = relationship("Comment", back_populates="author")
    followers: Mapped[list["Follower"]] = relationship("Follower", foreign_keys="Follower.user_to_id", back_populates="followed")
    following: Mapped[list["Follower"]] = relationship("Follower", foreign_keys="Follower.user_from_id", back_populates="follower")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username" : self.username,
            "firstname": self.firstname,
            "lastname": self.lastname
            # do not serialize the password, its a security breach
        }


class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String(1024), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    #Relationships
    user: Mapped["User"] = relationship("User", back_populates="posts")
    media: Mapped[list["Media"]] = relationship("Media", back_populates="post")
    comments: Mapped[list["Comment"]] = relationship("Comment", back_populates="post")

    def serialize(self):
        return {
            "id": self.id,
            "text": self.text,
            "user_id" : self.user_id,
        }
    
class Media(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[MediaType] = mapped_column(Enum(MediaType), nullable=False)
    url: Mapped[str] = mapped_column(String(512), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"), nullable=False)

    #Relationships
    post: Mapped["Post"] = relationship("Post", back_populates="media")

    def serialize(self):
        return {
            "id": self.id,
            "type": self.type.value,
            "url": self.url,
            "post_id": self.post_id,
        }
    
class Comment(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(String(512), nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"), nullable=False)
 
    # Relationships
    author: Mapped["User"] = relationship("User", back_populates="comments")
    post: Mapped["Post"] = relationship("Post", back_populates="comments")
 
    def serialize(self):
        return {
            "id": self.id,
            "comment_text": self.comment_text,
            "author_id": self.author_id,
            "post_id": self.post_id,
        }


class Follower(db.Model):
    user_from_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
    user_to_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
 
    # Relationships
    follower: Mapped["User"] = relationship("User", foreign_keys=[user_from_id], back_populates="following")
    followed: Mapped["User"] = relationship("User", foreign_keys=[user_to_id], back_populates="followers")