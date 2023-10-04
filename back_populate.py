from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker


# https://stackoverflow.com/questions/51335298/concepts-of-backref-and-back-populate-in-sqlalchemy


app = Flask(__name__)

# Configure the SQLAlchemy database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db = SQLAlchemy(app)

# Define the Parent and Child models
class Parent(db.Model):
    __tablename__ = 'parent'
    id = db.Column(db.Integer, primary_key=True)
    children = db.relationship("Child", back_populates="parent")

class Child(db.Model):
    __tablename__ = 'child'
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('parent.id'))
    parent = db.relationship("Parent", back_populates="children")

# Create the database tables
with app.app_context():
    db.create_all()
    if Parent.query.get(1) is None:
        p1=Parent()
        p2=Parent()
        c1=Child(parent=p1)
        c2=Child(parent=p1)
        c3=Child(parent=p2)
        c4=Child(parent=p2)
        db.session.add_all([p1,p2,c1,c2,c3,c4])
        db.session.commit()



@app.route('/')
def index():
    p=Parent.query.first()
    print(p.children)
    return "hello"

@app.route('/1')
def index1():
    p=Child.query.first()
    print(p.parent)
    return "hello"
if __name__ == '__main__':
    app.run(debug=True)
