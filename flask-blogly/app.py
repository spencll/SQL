"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = "SECRET!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return redirect("/users")

@app.route("/users")
def list_users():
    """List users"""
    users = User.query.all()
    return render_template("home.html", users= users)

@app.route("/users/new",)
def show_form():
    """Shows form"""
    return render_template("add_form.html")


@app.route("/users/new", methods=["POST"])
def add_user():
    """Add user and redirect to user info"""

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(user)
    db.session.commit()

    return redirect(f"/users/{user.id}")

@app.route("/users/<int:user_id>")
def show_userinfo(user_id):
    '''Show information on user'''
    user = User.query.get_or_404(user_id)
    return render_template("detail.html", user=user)

@app.route("/users/<int:user_id>/edit")
def show_edit(user_id):
    '''Show edit form'''
    user = User.query.get_or_404(user_id)
    return render_template("edit_form.html", user=user)

@app.route("/users/<int:user_id>/edit", methods=['POST'])
def edit_user(user_id):

    '''Edit user'''
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']

    '''Finding user and making edits'''
    user = User.query.get(user_id)
    user.first_name = first_name
    user.last_name = last_name
    user.image_url = image_url

    '''Commiting changes'''
    db.session.add(user)
    db.session.commit()

    return redirect(f"/users/{user.id}")

@app.route("/users/<int:user_id>/delete", methods=['POST'])
def delete_user(user_id):
    '''Delete user'''
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect(f"/users")  



