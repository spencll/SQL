"""Models for Cupcake app."""

# Imports
from flask_sqlalchemy import SQLAlchemy

# Making db as class of SQLAlchemy (links SQLAlchemy with flask)
db = SQLAlchemy()

DEFAULT= 'https://tinyurl.com/demo-cupcake'

def connect_db(app):
    """Connect to database."""
    db.app = app
    db.init_app(app)

def dict(cupcake):
    return {    
        'id': cupcake.id,
        'flavor': cupcake.flavor,
        'size': cupcake.size,
        'rating': cupcake.rating,
        'image': cupcake.image 
    }

class Cupcake(db.Model):
    """Cupcake"""

    __tablename__= "cupcakes"

    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    flavor = db.Column(db.Text,nullable=False)
    size = db.Column(db.Text,nullable=False)
    rating = db.Column(db.Float,nullable=False)
    image = db.Column(db.Text, default=DEFAULT, nullable=False)