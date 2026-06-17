from flask import (Flask,render_template,request,session, url_for,
                   make_response,redirect)
import requests
from product import (products,get_product_by_id,get_product_by_title,
                     get_related_products)
import json
import random
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
USERS_FILE = os.path.join(BASE_DIR, "users.json")
ORDERS_FILE = os.path.join(BASE_DIR, "orders.json")
try:
    with open(USERS_FILE, "r") as f:
        users = json.load(f)
except:
    users = []
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)
app = Flask(__name__)
app.secret_key = "velora_secret"
# ==============================
# CONFIG
# ==============================
BOT_TOKEN = "8718190227:AAFp4P0M7ygNMJji0wsDLfrXQwtwMdB-vwE"
CHAT_ID = "-1004197660449"

SHIPPING_COST = 15
TAX_RATE = 0.05

def get_categories():
    return list({
        product["category"]["name"]
        for product in products
    })
def get_cart():
    cart_cookie = request.cookies.get("cart_list")

    if not cart_cookie:
        return []

    return json.loads(cart_cookie)
def save_cart(response, cart_products):
    response.set_cookie(
        "cart_list",
        json.dumps(cart_products)
    )
    return response
def calculate_totals(cart_products):
    subtotal = 0
    for item in cart_products:
        item["item_total"] = (
            item["price"] * item["qty"]
        )
        subtotal += item["item_total"]
    shipping = SHIPPING_COST if subtotal > 0 else 0
    tax = subtotal * TAX_RATE
    total = subtotal + shipping + tax
    return {
        "subtotal": round(subtotal, 2),
        "shipping": round(shipping, 2),
        "tax": round(tax, 2),
        "total": round(total, 2)
    }
def send_telegram_message(message):
    url = (
        f"https://api.telegram.org/"
        f"bot{BOT_TOKEN}/sendMessage"
    )
    requests.post(
        url,
        data={
            "chat_id": CHAT_ID,
            "text": message
        }
    )
# ==============================
# HOME PAGES
# ==============================
@app.route("/")
def home():
    return render_template(
        "front/index.html",
        products=products[:8]
    )
@app.route("/about")
def about():
    return render_template(
        "front/about.html",
        products=products[:4]
    )
@app.route("/contact")
def contact():
    return render_template(
        "front/contact.html"
    )
@app.route("/shop")
def shop():
    return render_template(
        "front/shop.html",
        products=products,
        categories=get_categories()
    )
# ==============================
# PRODUCTS
# ==============================
@app.route("/products")
def product_list():
    return render_template(
        "front/products.html",
        products=products,
        categories=get_categories(),
        current_category="All"
    )
@app.route("/products/category/<category_name>")
def product_category(category_name):
    filtered_products = [
        product
        for product in products
        if product["category"]["name"].lower()
        == category_name.lower()
    ]
    return render_template(
        "front/products.html",
        products=filtered_products,
        categories=get_categories(),
        current_category=category_name
    )
@app.route("/product/<int:id>")
def product_detail(id):
    product = get_product_by_id(id)
    if not product:
        return render_template(
            "front/404.html"
        ), 404
    return render_template(
        "front/product_detail.html",
        product=product,
        related_products=get_related_products(
            product["category"]["name"],
            product["id"]
        )
    )
# ==============================
# CART
# ==============================
@app.route("/cart")
def cart():
    cart_products = get_cart()
    product_name = request.args.get("product_name")
    try:
        qty = int(request.args.get("qty", 1))
    except ValueError:
        qty = 1
    if product_name:
        product = get_product_by_title(product_name)
        if product:
            existing_item = next(
                (
                    item
                    for item in cart_products
                    if item["id"] == product["id"]
                ),
                None
            )
            if existing_item:
                existing_item["qty"] += qty
            else:
                cart_products.append({
                    "id": product["id"],
                    "title": product["title"],
                    "price": product["price"],
                    "qty": qty,
                    "description": product["description"],
                    "images": product["images"],
                    "category": product["category"]
                })
    totals = calculate_totals(cart_products)
    response = make_response(
        render_template(
            "front/cart.html",
            cart_products=cart_products,
            **totals
        )
    )
    return save_cart(
        response,
        cart_products
    )
@app.route("/cart/increase/<int:product_id>")
def increase_cart(product_id):
    cart_products = get_cart()
    for item in cart_products:
        if item["id"] == product_id:
            item["qty"] += 1
            break
    response = make_response(
        redirect("/cart")
    )
    return save_cart(
        response,
        cart_products
    )
@app.route("/cart/decrease/<int:product_id>")
def decrease_cart(product_id):
    cart_products = get_cart()
    for item in cart_products:
        if item["id"] == product_id:
            item["qty"] -= 1
            if item["qty"] <= 0:
                cart_products.remove(item)
            break
    response = make_response(
        redirect("/cart")
    )
    return save_cart(
        response,
        cart_products
    )
@app.route("/cart/remove/<int:product_id>")
def remove_cart(product_id):
    cart_products = [
        item
        for item in get_cart()
        if item["id"] != product_id
    ]
    response = make_response(
        redirect("/cart")
    )
    return save_cart(
        response,
        cart_products
    )
# ==============================
# CHECKOUT
# ==============================
@app.route("/checkout")
def checkout():

    if "user" not in session:
        return redirect("/login")

    cart_products = get_cart()

    totals = calculate_totals(cart_products)

    return render_template(
        "front/checkout.html",
        cart_products=cart_products,
        user=session["user"],
        **totals
    )
# ==============================
# AUTH
# ==============================
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        try:
            with open("users.json", "r") as f:
                users = json.load(f)

            if not isinstance(users, list):
                users = []

        except (FileNotFoundError, json.JSONDecodeError):
            users = []

        for user in users:

            if not isinstance(user, dict):
                continue

            user_email = user.get("email", "").strip().lower()
            user_password = user.get("password", "")

            if user_email == email and user_password == password:

                session["user"] = user

                return redirect("/account")

        return render_template(
            "front/login.html",
            error="Invalid Email or Password"
        )

    return render_template("front/login.html")
# ==============================
# LOGOUT
# ==============================
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")
# ==============================
# REGISTER
# ==============================
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        first_name = request.form.get("first_name", "").strip()
        last_name = request.form.get("last_name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        if not first_name or not last_name or not email or not password:
            return "All fields are required"

        if password != confirm_password:
            return "Passwords do not match"

        try:
            with open("users.json", "r") as f:
                users = json.load(f)

            if not isinstance(users, list):
                users = []

        except (FileNotFoundError, json.JSONDecodeError):
            users = []

        # Check existing email
        for user in users:
            if isinstance(user, dict) and user.get("email", "").lower() == email:
                return "Email already exists"

        new_user = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password": password
        }

        users.append(new_user)

        try:
            with open("users.json", "w") as f:
                json.dump(users, f, indent=4)
        except Exception as e:
            return f"Error saving user: {e}"

        session["user"] = new_user

        return redirect("/account")

    return render_template("front/register.html")
# ==============================
# FORGOT-PASSWORD
# ==============================
@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():

    if request.method == "POST":

        email = request.form.get(
            "email", ""
        ).strip().lower()

        try:
            with open("users.json", "r") as f:
                users = json.load(f)

            if not isinstance(users, list):
                users = []

        except:
            users = []

        for user in users:

            if not isinstance(user, dict):
                continue

            if user.get(
                "email", ""
            ).strip().lower() == email:

                session["reset_email"] = email

                return redirect("/reset-password")

        return render_template(
            "front/forgot-password.html",
            error="Email not found"
        )

    return render_template(
        "front/forgot-password.html"
    )
# ==============================
# REST-PASSWORD
# ==============================
@app.route("/reset-password", methods=["GET", "POST"])
def reset_password():

    email = session.get("reset_email")

    if not email:
        return redirect("/forgot-password")

    if request.method == "POST":

        password = request.form.get(
            "password", ""
        ).strip()

        confirm_password = request.form.get(
            "confirm_password", ""
        ).strip()

        if password != confirm_password:

            return render_template(
                "front/reset_password.html",
                email=email,
                error="Passwords do not match"
            )

        try:

            with open("users.json", "r") as f:
                users = json.load(f)

            if not isinstance(users, list):
                users = []

        except:
            users = []

        user_found = False

        for user in users:

            if not isinstance(user, dict):
                continue

            if user.get("email", "").lower() == email.lower():

                user["password"] = password
                user_found = True
                break

        if not user_found:

            return render_template(
                "front/reset_password.html",
                email=email,
                error="Account not found"
            )

        with open("users.json", "w") as f:
            json.dump(users, f, indent=4)

        session.pop("reset_email", None)

        return redirect("/login")

    return render_template(
        "front/reset_password.html",
        email=email
    )
# ==============================
# ACCOUNT
# ==============================
@app.route("/account")
def account():

    if "user" not in session:
        return redirect("/login")

    user = session["user"]

    try:
        with open("orders.json", "r") as f:
            all_orders = json.load(f)
    except:
        all_orders = []

    orders = [
        order
        for order in all_orders
        if order["email"] == user["email"]
    ]

    return render_template(
        "front/account.html",
        user=user,
        orders=orders
    )
# ==============================
# PLACE-ORDERS
# ==============================
@app.route("/place-order", methods=["POST"])
def place_order():
    try:
        cart_products = get_cart()

        if not cart_products:
            return redirect("/cart")

        first_name = request.form.get("first_name", "").strip()
        last_name = request.form.get("last_name", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()
        address = request.form.get("address", "").strip()
        payment_method = request.form.get(
            "payment_method",
            "Cash On Delivery"
        )

        totals = calculate_totals(cart_products)

        order_id = random.randint(100000, 999999)

        # Build Telegram Message
        message = (
            "🛒 NEW ORDER RECEIVED\n\n"
            f"🆔 Order ID: #{order_id}\n"
            f"👤 Customer: {first_name} {last_name}\n"
            f"📧 Email: {email}\n"
            f"📱 Phone: {phone}\n"
            f"🏠 Address: {address}\n"
            f"💳 Payment: {payment_method}\n\n"
            "📦 PRODUCTS\n\n"
        )

        for item in cart_products:
            message += (
                f"• {item.get('title', 'Unknown Product')}\n"
                f"  Qty: {item.get('qty', 0)}\n"
                f"  Price: ${item.get('price', 0)}\n"
                f"  Total: ${item.get('item_total', 0)}\n\n"
            )

        message += (
            f"Subtotal: ${totals.get('subtotal', 0)}\n"
            f"Shipping: ${totals.get('shipping', 0)}\n"
            f"Tax: ${totals.get('tax', 0)}\n"
            f"💰 Grand Total: ${totals.get('total', 0)}"
        )

        # Telegram
        try:
            send_telegram_message(message)
        except Exception as telegram_error:
            print("Telegram Error:", telegram_error)

        response = make_response(
            redirect("/order-success")
        )

        response.delete_cookie("cart_list")

        return response

    except Exception as e:
        import traceback
        print(traceback.format_exc())

        return (
            f"<h1>Order Error</h1>"
            f"<pre>{str(e)}</pre>",
            500
        )
# ==============================
# ORDER-SUCCESS
# ==============================
@app.route("/order-success")
def order_success():
    return render_template(
        "front/order_success.html"
    )
# ==============================
# RUN APP
# ==============================
if __name__ == "__main__":
    app.run(debug=True)