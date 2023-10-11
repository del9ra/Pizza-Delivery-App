from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from sqlalchemy import func
from helpers import usd
from os import path


db = SQLAlchemy()
DB_NAME = "store.db"
login_manager = LoginManager()
login_manager.login_view = 'users.login'  # for login_required
login_manager.login_message_category = 'info'  # to show alerts(like flash)


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '34168bb04deu875tfg620ba2'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    # pass 'app' to the next variables from the above
    db.init_app(app)
    app.jinja_env.filters["usd"] = usd

    # Import your db models here (after initializing db)
    from project.models import User, Order, Cart, Product

    # Create the database tables
    with app.app_context():
        if not path.exists(DB_NAME):
            db.create_all()

    login_manager.init_app(app)

    from project.users.routes import users
    from project.orders.routes import orders
    from project.main.routes import main
    app.register_blueprint(users)
    app.register_blueprint(orders)
    app.register_blueprint(main)

    @app.context_processor
    def inject_quantity():
        if current_user.is_authenticated:
            user_id = current_user.id
            quantity = db.session.query(func.count(Cart.product_id.distinct())).filter(
                Cart.user_id == user_id).scalar()
            return {'quantity': quantity if quantity is not None else 0}
        else:
            return {'quantity': 0}

    return app
