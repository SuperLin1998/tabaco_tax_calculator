from flask import Flask, render_template, request, jsonify, url_for
import os
import random

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
            
            # 隨機選擇一張圖片
            image_list = [f"mygo{i}.jpg" for i in range(1, 20)]
            chosen = random.choice(image_list)
            image_url = url_for('static', filename=chosen)

            # 將圖片網址加入結果中
            result = {
                "increase": increase,
                "quantity": q,
                "price": p,
                "tax": tax,
                "image_url": image_url  # 新增圖片欄位
            }
        except ValueError:
            result = {"error": "請輸入有效數字。"}
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
