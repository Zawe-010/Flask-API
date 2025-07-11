from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from datetime import datetime

# Initialize the flask application
app = Flask(__name__)

# Set up the database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:@localhost:5432/flask_api'

# Disables events / tracks objects changes
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Bind sqlalchemy to our flask application
db = SQLAlchemy(app)

# Creating models
# Products model
class Product(db.Model):
    __tablename__='products'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String,nullable=False)
    buying_price=db.Column(db.Float,nullable=False)
    selling_price=db.Column(db.Float,nullable=False)

    sales=db.relationship('Sale',backref='product')

# Sales model
class Sale(db.Model):
    __tablename__='sales'
    id=db.Column(db.Integer,primary_key=True)
    pid=db.Column(db.Integer,db.ForeignKey('products.id'),nullable=False)
    quantity=db.Column(db.Integer,nullable=False)
    created_at=db.Column(db.DateTime,nullable=False)



