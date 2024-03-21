import json
from datetime import datetime
from gen import LRGenerator
from core import PostLR
from flask import Flask, render_template, request, redirect, url_for, jsonify, send_file

app = Flask(__name__)

# Load data from JSON file
with open('data.json', 'r') as file:
    data = json.load(file)

# Sample consignees and consigners data (you can replace this with your dynamic data)
consignees = {
    "DB Private Ltd": "Consignee Address 1",
    "XYZ Company": "Consignee Address 2",
    "ABC Corporation": "Consignee Address 3",
}

consigners = {
    "Tata Motors": "Consigner Address 1",
    "Ford Industries": "Consigner Address 2",
    "Toyota Corporation": "Consigner Address 3",
}

# Function to retrieve data for all suboptions in Rates
def get_all_suboptions_data():
    rates = ["rate_per_qty", "sur_charge", "cover_charge", "st_charge", "hamali", "other_charge"]
    data = {}
    for rate in rates:
        paid = request.form.get(f"{rate}_paid", "")
        to_pay = request.form.get(f"{rate}_to_pay", "")
        data[rate] = {"paid": paid, "to_pay": to_pay}
    return data

@app.route("/")
def index():
    return render_template("index.html", consignees=consignees, consigners=consigners)


@app.route("/generate_bill", methods=["POST"])
def generate_bill():
    if request.method == "POST":
        consignee = request.form.get('consignee_name')
        consignee_address = request.form.get('consignee_address')
        consigner = request.form.get('consigner_name')
        consigner_address = request.form.get('consigner_address')
        from_location = request.form.get('from')
        to_location = request.form.get('to')
        vehicle_number = request.form.get('vehicle_number')
        no_of_packages = request.form.get('no_of_packages')
        description = request.form.get('description')
        value_rs = request.form.get('value_rs')
        total = request.form.get('total')

        suboptions = {}

        options = ["rate_per_qty_paid",'rate_per_qty_to_pay','sur_charge_paid','sur_charge_to_pay','cover_charge_paid','cover_charge_to_pay','st_charge_paid','st_charge_to_pay','hamali_paid','hamali_to_pay','other_charge_paid','other_charge_to_pay']
        for i in options:
            if not request.form.get(i):
                suboptions.update({i: "-"})
            else:
                suboptions.update({i: request.form.get(i)})

        date = datetime.now().strftime("%d-%m-%Y") 

        # Return the extracted data (example)
        data = {
            'consignee': consignee,
            'consignee_address': consignee_address,
            'consigner': consigner,
            'consigner_address': consigner_address,
            'from': from_location,
            'to': to_location,
            'vehicle_number': vehicle_number,
            'no_of_packages': no_of_packages,
            'description': description,
            'value_rs': value_rs,
            'total': total,
            "suboptions": suboptions,
            "date": date
        }

        filepath = PostLR(data)

        return send_file(filepath, as_attachment=True)


@app.route("/editbill", methods=["GET", "POST"])
def edit_bill():
    if request.method == "POST":
        date = request.form["date"]
        bill_data = data.get(date, {})
        return jsonify(bill_data)

    dates = list(data.keys())  # Get all dates from data.json
    return render_template("editbill.html", dates=dates)


@app.route("/update_bill", methods=["POST"])
def update_bill():
    date = request.form["date"]

    data[date]["customer_company_name"] = request.form["customer_company_name"]
    data[date]["Source"] = request.form["Source"]
    data[date]["Destination"] = request.form["Destination"]
    data[date]["Vehicle No."] = request.form["Vehicle No."]
    data[date]["Consigner"] = request.form["Consigner"]
    data[date]["Consignee"] = request.form["Consignee"]
    data[date]["No. of packages"] = request.form["No. of packages"]
    data[date]["Package Description"] = request.form["Package Description"]

    # Save data to JSON file
    with open('data.json', 'w') as file:
        json.dump(data, file, indent=4)

    return redirect(url_for('edit_bill'))


if __name__ == "__main__":
    app.run(host="0.0.0.0")
