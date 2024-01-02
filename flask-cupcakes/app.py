"""Flask app for Cupcakes"""

# Imports
from flask import Flask, request, jsonify, render_template
from models import db, connect_db, Cupcake, dict
# Database 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
connect_db(app)

with app.app_context():
    db.drop_all()
    db.create_all()

    c1 = Cupcake(
    flavor="cherry",
    size="large",
    rating=5,
)
    c2 = Cupcake(
    flavor="chocolate",
    size="small",
    rating=9,
    image="https://www.bakedbyrachel.com/wp-content/uploads/2018/01/chocolatecupcakesccfrosting1_bakedbyrachel.jpg"
)
    db.session.add_all([c1, c2])
    db.session.commit()

@app.route('/')
def home():
    
    return render_template('base.html')

@app.route('/api/cupcakes')
def list_cupcakes():
    cupcakes = Cupcake.query.all()

    # {cupcakes: {{},{},{},..}     
    return jsonify(cupcakes=[dict(c) for c in cupcakes])

# API add cupcake
@app.route('/api/cupcakes', methods= ['POST'])
def add_cupcake():
    flavor = request.json['flavor']
    size = request.json['size']
    rating = request.json['rating']
    image = request.json['image']
    cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)
    db.session.add(cupcake)
    db.session.commit()

    # {cupcake: {    }, 201}
    return (jsonify(cupcake=dict(cupcake)), 201)

# API get cupcake
@app.route('/api/cupcakes/<int:id>')
def list_cupcake(id):
    cupcake = Cupcake.query.get_or_404(id)
    # {cupcake: {}}
    return jsonify(cupcake=dict(cupcake))

# API patch cupcake
@app.route('/api/cupcakes/<int:id>', methods= ['PATCH'])
def edit_cupcake(id):
    cupcake = Cupcake.query.get_or_404(id)
    cupcake.flavor = request.json['flavor']
    cupcake.size= request.json['size']
    cupcake.rating = request.json['rating']
    cupcake.image = request.json['image']
    db.session.add(cupcake)
    db.session.commit()

    # {cupcake: {    }, 201}
    return (jsonify(cupcake=dict(cupcake)))

# API delete cupcake
@app.route('/api/cupcakes/<int:id>', methods= ['DELETE'])
def delete_cupcake(id):
    cupcake = Cupcake.query.get_or_404(id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(message='Deleted')

