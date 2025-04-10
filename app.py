from flask import Flask, render_template, request

app = Flask(__name__)

def calculate_total_tax(x):
    base_price = 105
    base_tax = 20
    base_quantity = 1320000000
    elasticity = 0.04

    price_increase_rate = (x / base_price) * (1 / 0.1) * elasticity
    new_quantity = base_quantity * (1 - price_increase_rate)
    new_price = base_price + x
    new_tax_total = (base_tax + x) * new_quantity
    return round(new_quantity / 1e6, 2), round(new_price, 2), round(new_tax_total / 1e8, 2)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        try:
            increase = float(request.form["increase"])
            q, p, tax = calculate_total_tax(increase)
            result = {
                "increase": increase,
                "quantity": q,
                "price": p,
                "tax": tax
            }
        except ValueError:
            result = {"error": "請輸入有效數字。"}
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
