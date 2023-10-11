from datetime import datetime
from flask import current_app
from project import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
# retrieves a user object from the database based on the user's ID
def load_user(user_id):     # load user objects when a user is logged in
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    # nullable=True означает что ты можешь заполнить это поле потом, а false - надо сейчас
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    hash = db.Column(db.String(60), nullable=False)
    address = db.Column(db.String(100), unique=True, nullable=True)
    zip = db.Column(db.Integer, unique=True, nullable=True)
    city = db.Column(db.String(50), unique=True, nullable=True)
    country = db.Column(db.String(50), unique=True, nullable=True)
    first_name = db.Column(db.String(150), unique=True, nullable=True)
    last_name = db.Column(db.String(150), unique=True, nullable=True)
    phone = db.Column(db.String(11), unique=True, nullable=True)

    # repr displays class info
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.address}', '{self.city}', '{self.country}', '{self.zip}', '{self.first_name}', '{self.last_name}'), '{self.phone}')"


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(50), unique=True, nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, unique=True, nullable=False)
    image = db.Column(db.String(150), unique=True, nullable=False)

    def __repr__(self):
        return f"Product('{self.item}', '{self.price}', '{self.description}', '{self.image}')"


class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    number = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Cart('{self.total_price}', '{self.number}')"


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    time = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Order('{self.total_price}', '{self.time}')"
