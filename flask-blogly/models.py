"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""
    with app.app_context():
        db.app = app
        db.init_app(app)

class User(db.Model):

    __tablename__= "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    first_name = db.Column(db.String(50),
                     nullable=False,
                    )

    last_name = db.Column(db.String(),
                     nullable=False,
                    )
    
    image_url = db.Column(db.String())

    
class Post(db.Model):

    __tablename__= "posts"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True,
                   )
    
    title = db.Column(db.String(50),
                     nullable=False,
                    )

    content = db.Column(db.String(),
                     nullable=False,
                    )
    
    created_at = db.Column(db.DateTime, default=func.now())

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

class PostTag(db.Model):

    __tablename__= "post_tags"

    post_id= db.Column(db.Integer(),
                       db.ForeignKey("posts.id"),
                       primary_key=True, nullable=False
                       )
    
    tag_id= db.Column(db.Integer(),
                       db.ForeignKey("tags.id"),
                       primary_key=True, nullable=False
                       )

class Tag(db.Model):

    __tablename__= "tags"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    name= db.Column(db.Text(),
                       )
    
    posts = db.relationship('Post', secondary='post_tags', backref='tags', cascade="all,delete"
                            )
    

    



    


    
