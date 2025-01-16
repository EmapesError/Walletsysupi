from flask import Flask, request, redirect, jsonify, render_template
import requests

app = Flask(__name__)

# Wallet balance (stored in-memory since no database is used)
wallet_balance = 0

# Cashfree API details
APP_ID = "805651d1a917471429d9005d30156508"
SECRET_KEY = "cfsk_ma_prod_59f4e8c983ea3865a5a79aa9fe7340fd_42903b0e"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/deposit", methods=["GET"])
def deposit():
    amount = request.args.get("amount")
    if not amount or int(amount) <= 0:
        return "Invalid amount", 400

    # Cashfree payment link generation
    payment_link_url = "https://api.cashfree.com/pg/orders"
    headers = {
        "Content-Type": "application/json",
        "x-client-id": APP_ID,
        "x-client-secret": SECRET_KEY,
    }
    payload = {
        "order_id": "order_" + str(hash(amount)),  # Unique order ID
        "order_amount": float(amount),
        "order_currency": "INR",
        "customer_details": {
            "customer_id": "customer_123",
            "customer_email": "test@example.com",
            "customer_phone": "9999999999",
        },
    }

    response = requests.post(payment_link_url, json=payload, headers=headers)
    data = response.json()

    if response.status_code == 200 and data["status"] == "OK":
        # Redirect user to payment link
        return redirect(data["payment_link"])
    else:
        return "Payment gateway error: " + str(data), 500

@app.route("/success", methods=["POST"])
def payment_success():
    global wallet_balance
    data = request.json

    # Verify payment status
    if data.get("txStatus") == "SUCCESS":
        wallet_balance += float(data["orderAmount"])
        return jsonify({"message": "Payment successful!", "balance": wallet_balance})
    else:
        return jsonify({"message": "Payment failed!"}), 400

@app.route("/balance", methods=["GET"])
def get_balance():
    return jsonify({"wallet_balance": wallet_balance})

if __name__ == "__main__":
    app.run(debug=True)
