from flask import Flask, jsonify, request

app = Flask(__name__)


@app.get("/health")
def health():
    return jsonify(
        service="Vulnerable Backend",
        status="ok"
    )


@app.get("/products")
def products():
    category = request.args.get("category")
    product_id = request.args.get("id")

    return jsonify(
        message="Products returned from vulnerable backend",
        category=category,
        id=product_id,
        products=[
            {
                "id": 1,
                "name": "Laptop",
                "price": 1200
            },
            {
                "id": 2,
                "name": "Phone",
                "price": 800
            }
        ]
    )


@app.get("/search")
def search():
    query = request.args.get("q", "")

    return jsonify(
        message="Search result from vulnerable backend",
        query=query,
        results=[
            "Demo result 1",
            "Demo result 2"
        ]
    )


@app.post("/comments")
def comments():
    data = request.get_json(silent=True) or {}

    return jsonify(
        message="Comment received by vulnerable backend",
        comment=data.get("comment")
    )


@app.post("/login")
def login():
    data = request.get_json(silent=True) or {}

    return jsonify(
        message="Login request received by vulnerable backend",
        email=data.get("email")
    )


if __name__ == "__main__":
    app.run(debug=True, port=5001)