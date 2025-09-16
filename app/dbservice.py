from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from datetime import datetime
import os
from extensions import db

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

# User model
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

# Payment model
class Payment(db.Model):
    __tablename__ = 'payments'
    id = db.Column(db.Integer, primary_key=True)
    sale_id = db.Column(db.Integer, nullable=False)
    mrid = db.Column(db.String(100), nullable=False)
    crid = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=True)
    trans_code = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# docker run -v c:/Users/PC/OneDrive/Flask-API/app:/app/database/database.db -p 127.0.0.1:5000:80 -t flask-api
# docker run -v /home/Flask-API/app/database:/app/database/database.db -p 127.0.0.1:5000:80 -t flask-api
