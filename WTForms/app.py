"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, Pet
import validators
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
    db.drop_all()
    db.create_all()

@app.route("/")
def home():
    """List pets"""
    pets = Pet.query.all()
    return render_template("home.html", pets=pets)

@app.route("/pets/add")
def show_add_form():
    """Shows form"""
    return render_template("add_form.html")

@app.route("/pets/add", methods=['POST'])
def add_pet():
    """Add user and redirect to user info"""

    name = request.form['name']
    species = request.form['species']
    if species not in ['Cat','Porcupine','Dog','cat','porcupine','dog']:
        return redirect("/pets/add")
    photo_url = request.form['photo_url']

    if not validators.url(photo_url):
        return redirect("/pets/add")
    
    age = request.form['age']
    if (int(age)<0 or int(age)>30):
        age= 'asdf'

    notes = request.form['notes']
    try:
        pet = Pet(name=name, species=species, photo_url=photo_url, age=age, notes=notes)
        db.session.add(pet)
        db.session.commit()
        return redirect("/")

    except:
        return redirect("/pets/add")
    
@app.route("/pets/<int:pet_id>")
def show_pet_info(pet_id):
    '''Show pet information'''
    pet = Pet.query.get_or_404(pet_id)

    return render_template("detail.html", pet=pet)

@app.route("/pets/<int:pet_id>", methods=['POST'])
def edit_pet(pet_id):
    '''Edit pet'''
    photo_url = request.form['photo_url']
    if not validators.url(photo_url):
        return redirect(f"/pets/{pet_id}")
    
    notes = request.form['notes']
    available = request.form['available']

    try:
        pet = Pet.query.get(pet_id)
        pet.photo_url = photo_url
        pet.notes = notes
        pet.available = available
        db.session.add(pet)
        db.session.commit()
        return redirect(f"/pets/{pet_id}")
    except:
        return redirect(f"/pets/{pet_id}")
        






