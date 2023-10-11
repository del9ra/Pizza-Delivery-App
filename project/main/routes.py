from flask import Blueprint, render_template
from project.models import Product
from flask_login import login_required


main = Blueprint('main', __name__)


@main.route("/")
@login_required
def index():
    all_products = Product.query.all()      # select * from table
    return render_template("index.html", products=all_products)


@main.route("/contact")
@login_required
def contact():
    return render_template("contact.html")


@main.route("/about")
@login_required
def about():
    return render_template("about.html")
