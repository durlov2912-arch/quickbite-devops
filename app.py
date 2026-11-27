from flask import Flask, jsonify, request

app = Flask(__name__)

MENU = [
    {"id": 1, "name": "Chicken Burger", "price": 12.90},
    {"id": 2, "name": "Nasi Lemak", "price": 8.50},
    {"id": 3, "name": "Iced Milo", "price": 4.00},
]

orders = []
feedback_list = []


def calculate_total(items):
    """Return the total price for a list of {'id': int, 'qty': int}."""
    prices = {m["id"]: m["price"] for m in MENU}
    total = 0.0
    for item in items:
        if item.get("id") not in prices:
            raise ValueError("Unknown menu item")
        qty = item.get("qty", 0)
        if not isinstance(qty, int) or qty <= 0:
            raise ValueError("Invalid quantity")
        total += prices[item["id"]] * qty
    return round(total, 2)


@app.route("/")
def home():
    return jsonify(message="Welcome to QuickBite Online Food Ordering")


@app.route("/health")
def health():
    return jsonify(status="ok")


@app.route("/menu")
def menu():
    return jsonify(MENU)


@app.route("/orders", methods=["GET"])
def list_orders():
    return jsonify(orders)


@app.route("/orders", methods=["POST"])
def create_order():
    data = request.get_json(silent=True) or {}
    items = data.get("items", [])
    if not items:
        return jsonify(error="Order must contain items"), 400
    try:
        total = calculate_total(items)
    except ValueError as e:
        return jsonify(error=str(e)), 400
    order = {"order_id": len(orders) + 1, "items": items, "total": total}
    orders.append(order)
    return jsonify(order), 201


@app.route("/feedback", methods=["POST"])
def add_feedback():
    data = request.get_json(silent=True) or {}
    message = data.get("message", "").strip()
    if not message:
        return jsonify(error="Feedback message is required"), 400
    feedback_list.append(message)
    return jsonify(status="received"), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)