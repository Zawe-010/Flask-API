from flask import Flask, jsonify, request

app = Flask(__name__)

products_list = []

@app.route("/")
def hello_world():
    res = {"Flask-API":"1.0"}
    return jsonify(res), 200


@app.route("/api/products", methods = ["GET", "POST"])
def products():
    if request.method == "GET":
        # Returns a list of products as JSON
        return jsonify(products_list), 200
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
            products_list.append(data)
            return jsonify(data), 201
    else:
        # A different rquest method was sent
        error = {"error" : "Method not allowed"}
        return jsonify(error), 405


if __name__ == "__main__":
    app.run(debug=True)