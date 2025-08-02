from flask import Flask, jsonify, request
from dbservice import Product, Sale, db, app, User
from datetime import datetime
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from sqlalchemy import text
# import sentry_sdk

# sentry_sdk.init(
#     dsn="https://4d7153c730323d0f8395a2016fa65653@o4509707452809216.ingest.us.sentry.io/4509707545346048",
#     # Add data like request headers and IP for users,
#     # see https://docs.sentry.io/platforms/python/data-management/data-collected/ for more info
#     send_default_pii=True,
# )

CORS(app)
app.config["JWT_SECRET_KEY"]= ""
# app.config["TESTING"] = True
jwt = JWTManager(app)

@app.route("/")
def hello_world():
    res = {"Flask-API Develop ":"1.0"}
    return jsonify(res), 200


@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    if not data or not all(k in data for k in ("full_name", "email", "password")):
        return jsonify({"error": "Missing required fields"}), 400

    # Check if user already exists
    existing_user = db.session.execute(
        db.select(User).filter_by(email=data["email"])
    ).scalar()

    if existing_user:
        return jsonify({"error": "User already exists"}), 409

    hashed_password = generate_password_hash(data["password"])

    new_user = User(
        full_name=data["full_name"],
        email=data["email"],
        password=hashed_password
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data or not all(k in data for k in ("email", "password")):
        return jsonify({"error": "Missing email or password"}), 400

    user = db.session.execute(
        db.select(User).filter_by(email=data["email"])
    ).scalar()

    if not user or not check_password_hash(user.password, data["password"]):
        return jsonify({"error": "Invalid credentials"}), 401

    # Create a token and return to the user
    token = create_access_token(identity=user.email)
    return jsonify({
        "message": "Login successful", 
        "token":token,
        "user": {
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email
        }
    }), 200


@app.route("/users", methods=["GET"])
def list_users():
    users = User.query.all()
    return jsonify([
        {"id": u.id, "full_name": u.full_name, "email": u.email}
        for u in users
    ]), 200

@app.route("/api/products", methods = ["GET", "POST"])
@jwt_required()
def products():

    email = get_jwt_identity()
    # print("Email =====", email)

    if request.method == "GET":
        products_list = Product.query.all()
        prods = []
        for i in products_list:
            product_data = {
                'id': i.id,
                'name':i.name,
                'buying_price':i.buying_price,
                'selling_price':i.selling_price
            }
            prods.append(product_data)
        # Returns a list of products as JSON
        return jsonify(prods)
    elif request.method == "POST":
        # Data will be received here as JSON , so we convert it to dictionary
        data = dict(request.get_json())
        if "name" not in data.keys() or "buying_price" not in data.keys() or "selling_price" not in data.keys():
            error = {"error" : "Invalid keys"}
            return jsonify(error), 403
        elif data["name"] == "" or data["buying_price"] == "" or data["selling_price"] == "":
            error = {"error" : "Ensure all values are set"}
            return jsonify(error), 403
        else:
            new_product = Product(name = data["name"],buying_price = data["buying_price"], selling_price = data["selling_price"])
            db.session.add(new_product)
            db.session.commit()
            return jsonify(data), 201
    else:
        # A different rquest method was sent
        error = {"error" : "Method not allowed"}
        return jsonify(error), 405


@app.route("/api/sales", methods=["GET", "POST"])
@jwt_required()
def sales():

    email = get_jwt_identity()
    # print("Email ----", email)

    if request.method == "GET":
        sales_list = Sale.query.all()
        sales_data = []
        for sale in sales_list:
            sale_info = {
                'id': sale.id,
                'pid': sale.pid,
                'quantity': sale.quantity,
                'created_at': sale.created_at
            }
            sales_data.append(sale_info)
        return jsonify(sales_data), 200
    elif request.method == "POST":
        data = dict(request.get_json())

        if "pid" not in data.keys() or "quantity" not in data.keys():
            error = {"error": "Invalid keys"}
            return jsonify(error), 403
        elif data["pid"] == "" or data["quantity"] == "":
            error = {"error": "Ensure all values are set"}
            return jsonify(error), 403
        else:
            if 'created_at' in data and data['created_at'] != "":
                try:
                    created_at = datetime.strptime(data['created_at'], '%Y-%m-%d %H:%M:%S')
                except ValueError:
                    error = {"error": "Invalid date format"}
                    return jsonify(error), 403
            else:
               created_at = datetime.now()
               
            # Optional: make sure pid and quantity are integers
            new_sale = Sale(pid=data["pid"], quantity=data["quantity"], created_at=created_at)
            db.session.add(new_sale)
            db.session.commit()

            sale_response = {
            "id": new_sale.id,
            "pid": new_sale.pid,
            "quantity": new_sale.quantity,
            "created_at": new_sale.created_at
        }
            return jsonify(sale_response), 201
    else:
        error = {"error": "Method not allowed"}
        return jsonify(error), 405
    

@app.route("/api/dashboard", methods=["GET"])
@jwt_required()
def dashboard():
    email = get_jwt_identity()
    # print("Email (dashboard) ===", email)

    # Query: Profit per product
    profit_product = db.session.execute(text("""
        SELECT p.name, 
                SUM((p.selling_price - p.buying_price) * s.quantity) AS profit
        FROM sales s
        JOIN products p ON s.pid = p.id
        GROUP BY p.id
    """)).fetchall()

    # Query: Sales per day
    sales_day = db.session.execute(text("""
        SELECT DATE(s.created_at) AS date,
               SUM(p.selling_price * s.quantity) AS sales
        FROM sales s
        JOIN products p ON s.pid = p.id
        GROUP BY date
        ORDER BY date
    """)).fetchall()

    # Function to generate colors dynamically
    def generate_colors(n):
        colors = []
        for i in range(n):
            hue = int(360 * i / n)  # evenly space hues
            colors.append(f"hsl({hue}, 70%, 50%)")
        return colors
    

     # Format for frontend
    products_name = [row[0] for row in profit_product]

    products_sales = [float(row[1]) for row in profit_product]

    # Generate as many colors as products
    products_colour = generate_colors(len(profit_product))

    # Format sales per day
    dates = [row[0].strftime("%Y-%m-%d") for row in sales_day]
    sales = [float(row[1]) for row in sales_day]
    
    data = {
    "profit_per_product": {
        "products_name": products_name,
        "products_sales": products_sales,
        "products_colour": products_colour
    },
    "sales_per_day": {
        "dates": dates,
        "sales": sales
    }
}

    return jsonify(data), 200


    # Query: Profit per product
    # profit_product = db.session.execute(text("""
    #     SELECT p.name, 
    #            SUM((p.selling_price - p.buying_price) * s.quantity) AS profit
    #     FROM sales s
    #     JOIN products p ON s.pid = p.id
    #     GROUP BY p.id
    # """)).fetchall()

    # Query: Sales per product
    # sales_product = db.session.execute(text("""
    #     SELECT p.name, 
    #            SUM(s.quantity * p.selling_price) AS sales
    #     FROM sales s
    #     JOIN products p ON s.pid = p.id
    #     GROUP BY p.id
    # """)).fetchall()

    # Query: Profit per day
    # profit_day = db.session.execute(text("""
    #     SELECT DATE(s.created_at) AS date,
    #            SUM((p.selling_price - p.buying_price) * s.quantity) AS profit
    #     FROM sales s
    #     JOIN products p ON s.pid = p.id
    #     GROUP BY date
    #     ORDER BY date
    # """)).fetchall()

    # Query: Sales per day
    # sales_day = db.session.execute(text("""
    #     SELECT DATE(s.created_at) AS date,
    #            SUM(p.selling_price * s.quantity) AS sales
    #     FROM sales s
    #     JOIN products p ON s.pid = p.id
    #     GROUP BY date
    #     ORDER BY date
    # """)).fetchall()


    # Format for frontend
    products_name = [row[0] for row in profit_product]

    products_sales = [float(dict(sales_product).get(row[0], 0)) for row in profit_product]

    products_colour = ["#3e95cd", "#8e5ea2", "#3cba9f", "#e8c3b9", "#c45850"]
    
    data = {"products_name": products_name, "products_sales": products_sales, "products_colour": products_colour}

    return jsonify(data), 200

    # products = [
    #     {
    #         "name": row[0],
    #         "sales": float(dict(sales_product).get(row[0], 0)),
    #         "profit": float(row[1] or 0)
    #     }
    #     for row in profit_product
    # ]

    daily = []
    for pd, sd in zip(profit_day, sales_day):
        daily.append({
            "date": str(pd[0]),
            "profit": float(pd[1] or 0),
            "sales": float(sd[1] or 0)
        })

    return jsonify({
        "products_name": products_name,
        "products_sale": products_sales
        # "daily": daily
    }), 200


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)