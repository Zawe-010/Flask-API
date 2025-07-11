from flask import Flask, jsonify, request
from dbservice import Product, Sale, db, app
from datetime import datetime
from flask_cors import CORS

CORS(app)

@app.route("/")
def hello_world():
    res = {"Flask-API":"1.0"}
    return jsonify(res), 200


@app.route("/api/products", methods = ["GET", "POST"])
def products():
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
        if "name" not in data.keys() or "bp" not in data.keys() or "sp" not in data.keys():
            error = {"error" : "Invalid keys"}
            return jsonify(error), 403
        elif data["name"] == "" or data["bp"] == "" or data["sp"] == "":
            error = {"error" : "Ensure all values are set"}
            return jsonify(error), 403
        else:
            new_product = Product(name = data["name"],buying_price = data["bp"], selling_price = data["sp"])
            db.session.add(new_product)
            db.session.commit()
            return jsonify(data), 201
    else:
        # A different rquest method was sent
        error = {"error" : "Method not allowed"}
        return jsonify(error), 405


@app.route("/api/sales", methods=["GET", "POST"])
def sales():
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


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)