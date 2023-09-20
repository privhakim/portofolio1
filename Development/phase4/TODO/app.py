from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)



class Animal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    species = db.Column(db.String(100), nullable=False)
    zookeeper_id = db.Column(db.Integer, db.ForeignKey('zookeeper.id'))
    enclosure_id = db.Column(db.Integer, db.ForeignKey('enclosure.id'))

class Zookeeper(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    birthday = db.Column(db.String(20), nullable=False)
    animals = relationship('Animal', backref='zookeeper', lazy=True)

class Enclosure(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    environment = db.Column(db.String(50), nullable=False)
    open_to_visitors = db.Column(db.Boolean, default=False)
    animals = relationship('Animal', backref='enclosure', lazy=True)


@app.route('/animal/<int:id>')
def animal_by_id(id):
    animal = Animal.query.get(id)
    if animal:
        return jsonify({
            'name': animal.name,
            'species': animal.species,
            'zookeeper': animal.zookeeper.name if animal.zookeeper else None,
            'enclosure_environment': animal.enclosure.environment if animal.enclosure else None
        }), 200
    else:
        return jsonify({'message': 'Animal not found'}), 404

@app.route('/zookeeper/<int:id>')
def zookeeper_by_id(id):
    zookeeper = Zookeeper.query.get(id)
    if zookeeper:
        animals = [animal.name for animal in zookeeper.animals]
        return jsonify({
            'name': zookeeper.name,
            'birthday': zookeeper.birthday,
            'animals': animals
        }), 200
    else:
        return jsonify({'message': 'Zookeeper not found'}), 404

@app.route('/enclosure/<int:id>')
def enclosure_by_id(id):
    enclosure = Enclosure.query.get(id)
    if enclosure:
        animals = [animal.name for animal in enclosure.animals]
        return jsonify({
            'environment': enclosure.environment,
            'open_to_visitors': enclosure.open_to_visitors,
            'animals': animals
        }), 200
    else:
        return jsonify({'message': 'Enclosure not found'}), 404

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
