from project import db
from flask import render_template, url_for, flash, redirect, request, Blueprint
from project.models import Product, User, Cart, Order
from flask_login import current_user, login_required
from sqlalchemy import func
import datetime
from helpers import apology


orders = Blueprint('orders', __name__)


@orders.route("/order", methods=["GET", "POST"])
def order():
    if request.method == "POST":
        # extract all product data
        product_id = request.form.get("product_id")
        product = Product.query.get(product_id)
        price = product.price
        number = request.form.get("number")
        number = int(number)
        if number <= 0:
            return apology("must provide positive number", 403)
        total_price = number * price
        user_id = current_user.id
        # add to cart including item data
        new_cart_item = Cart(user_id=user_id, product_id=product_id, total_price=total_price, number=number)
        db.session.add(new_cart_item)
        db.session.commit()
        flash("Your item(s) added to cart", "success")
        return redirect(url_for("orders.cart"))

    # 'args.get' retrieves the value of a query parameter from the URL of a GET request
    product_id = request.args.get("product_id")
    # get a single row of data (the product details) in return
    details = Product.query.filter_by(id=product_id).first()
    if details:
        return render_template("order.html", product_id=product_id, item=details.item, price=details.price,
                               description=details.description, image=details.image)
    else:
        flash("must provide a correct product id", category='error')


@orders.route("/cart", methods=["GET", "POST"])
@login_required
def cart():
    user_id = current_user.id
    # how to remove unnecessary product
    if request.method == "POST":
        new_id = request.form.get('id')
        if new_id:
            Cart.query.filter_by(user_id=user_id, product_id=new_id).delete()
            db.session.commit()
        return redirect(url_for("orders.cart"))
    else:
        # display all the info about items added to cart
        items = db.session.query(
            Product.item,
            Product.price,
            func.sum(Cart.number).label("number"),
            func.sum(Cart.total_price).label("total_price"),
            Cart.product_id
        ).join(
            Cart, Product.id == Cart.product_id
        ).filter(
            Cart.user_id == user_id
        ).group_by(
            Product.item
        ).all()
        grand_total = db.session.query(func.sum(Cart.total_price)).filter(Cart.user_id == user_id).scalar()
        return render_template("cart.html", items=items, grand_total=grand_total)


@orders.route("/checkout", methods=["GET", "POST"])
@login_required
def checkout():
    user_id = current_user.id
    if request.method == "POST":  # retrieve data from form
        first_name = request.form.get("firstName")
        last_name = request.form.get("lastName")
        email = request.form.get("email")
        address = request.form.get("address")
        zip = request.form.get("zip")
        phone = request.form.get("phone")
        country = request.form.get("country")
        city = request.form.get("city")
        if not first_name or not last_name or not email or not address or not zip or not phone or not country or not city:
            flash("must fill out each field", category='error')
        db.session.query(User).filter_by(id=user_id).update({
            User.first_name: first_name,
            User.last_name: last_name,
            User.email: email,
            User.address: address,
            User.zip: zip,
            User.phone: phone,
            User.country: country,
            User.city: city
        })
        db.session.commit()

        time = datetime.datetime.now()
        # pass products from cart to orders table in sql
        cart_columns = Cart.query.filter_by(user_id=user_id).all()
        # cart_columns = db.execute("SELECT product_id, total_price FROM cart WHERE user_id = ?", user_id)
        # get each products' id and total price and insert in orders
        for column in cart_columns:
            product_id = column.product_id
            total_price = column.total_price
            new_order = Order(user_id=user_id, product_id=product_id, total_price=total_price, time=time)
            db.session.add(new_order)
        db.session.commit()
        # empty the cart
        Cart.query.filter_by(user_id=user_id).delete()
        db.session.commit()
        return redirect(url_for("orders.success"))
    # if method is get, display this info
    # .scalar() returns a single value, while .first() returns a row of data(tuple)
    #  returns a single value (the sum), not a row of data
    db_grand_total = db.session.query(func.sum(Cart.total_price).label("grand_total")).filter(
        Cart.user_id == user_id).scalar()
    return render_template("checkout.html", grand_total=db_grand_total)


@orders.route("/success")
@login_required
def success():
    user_id = current_user.id
    # retrieve all the info about the user
    bio = User.query.filter_by(id=user_id).first()
    return render_template("success.html", bio=bio)
