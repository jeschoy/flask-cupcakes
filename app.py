"""Flask app for Cupcakes"""
from flask import Flask, render_template, jsonify, request
from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = "thisisasecret"

app.app_context().push()
connect_db(app)

@app.route('/')
def root():
  """Show root page"""
  return render_template('index.html')

@app.route('/api/cupcakes')
def show_cupcakes():
  """Return all cupcakes in database"""
  cupcakes = [cupcake.to_dict() for cupcake in Cupcake.query.all()]
  return jsonify(cupcakes=cupcakes)

@app.route('/api/cupcakes/<int:cupcake_id>')
def get_cupcake(cupcake_id):
  """Show individual cupcake"""
  cupcake = Cupcake.query.get_or_404(cupcake_id)
  return jsonify(cupcake=cupcake.to_dict())

@app.route('/api/cupcakes', methods=["POST"])
def create_cupcake():
  data = request.json

  cupcake = Cupcake(flavor=data['flavor'], size=data['size'], rating=data['rating'], image=data['image'] or None)
  db.session.add(cupcake)
  db.session.commit()
  return (jsonify(cupcake=cupcake.to_dict()), 201)

@app.route('/api/cupcakes/<int:cupcake_id>', methods=["PATCH"])
def edit_cupcake(cupcake_id):
  """To edit an exisiting cupcake"""
  cupcake = Cupcake.query.get_or_404(cupcake_id)
  data = request.json

  """New data for cupcake"""
  cupcake.flavor=data['flavor']
  cupcake.size=data['size']
  cupcake.rating=data['rating']
  cupcake.image=data['image'] or None

  db.session.add(cupcake)
  db.session.commit()

  return jsonify(cupcake=cupcake.to_dict())

@app.route('/api/cupcakes/<int:cupcake_id>', methods=["DELETE"])
def delete_cupcake(cupcake_id):
  """To delete an existing cupcake from database"""
  cupcake = Cupcake.query.get_or_404(cupcake_id)
  db.session.delete(cupcake)
  db.session.commit()
  return jsonify(message="Deleted")
