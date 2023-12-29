# flask stuff
from flask import Flask, render_template, flash, redirect, render_template
app = Flask(__name__)
app.config["SECRET_KEY"] = "oh-so-secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///wtf"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

# model stuff
from models import db, connect_db, Pet

# form stuff
from forms import AddPetForm

# database stuff
connect_db(app)
with app.app_context():
    db.drop_all()
    db.create_all()

# debug stuff
from flask_debugtoolbar import DebugToolbarExtension
debug = DebugToolbarExtension(app)

#routes
@app.route('/')
def homepage():
    """Show homepage with pet list"""
    pets = Pet.query.all()
    return render_template("home.html", pets=pets)


@app.route('/add', methods=['GET','POST'])
def add_pet():
    """Get add form and handle post"""

    # storing form into form variable 
    form = AddPetForm()

    if form.validate_on_submit():

        # data pull
        name = form.name.data
        species = form.species.data
        photo_url = form.photo_url.data
        age= form.age.data
        notes=form.notes.data
        available= form.available.data

        # new pet
        pet = Pet(name=name, species=species, photo_url=photo_url, age=age, notes=notes, available=available)
        db.session.add(pet)
        db.session.commit()


    # Post route
        return redirect('/')
    
    # Get route
    else:
        return render_template('add_form.html',form=form)


@app.route('/<int:pid>', methods=['GET','POST'])
def edit_pet(pid):
    """Get pet info and handle post"""

    # Finding designated pet
    pet = Pet.query.get(pid)

    # storing form with designated pet info into form variable 
    form = AddPetForm(obj=pet)

    if form.validate_on_submit():

        # data edit
        pet.notes = form.notes.data
        pet.photo_url= form.photo_url.data
        pet.available= form.available.data
        db.session.commit()

    # Post route
        return redirect('/')

    # Get route with designated pet info
    else:
        return render_template('add_form.html', form=form, pet=pet)



    






