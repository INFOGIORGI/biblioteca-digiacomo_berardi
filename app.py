from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
import db
import json

app = Flask(__name__)
app.secret_key = "super secret key"


app.config['MYSQL_HOST'] = ''
app.config['MYSQL_PORT'] = 1
app.config['MYSQL_USER'] = 'ospite'
app.config['MYSQL_PASSWORD'] = 'ospite'
app.config['MYSQL_DB'] = 'w3schools'
mysql = MySQL(app)



@app.route("/")
def home():
    return render_template("index.html",titolo="Home")

@app.route("/addProduct/",methods=["GET","POST"])
def addProduct():
    if request.method == 'GET':
        return render_template("addProduct.html",titolo="Add")
    else:
        productName = request.form.get("productName","")
        supplierID = request.form.get("supplierID","")
        price = request.form.get("price","")

        if productName=="" or supplierID=="" or price=="":
            flash("It is necessary to fill in all the fields.")
            return redirect(url_for('addProduct'))
        
        e = db.addProduct(mysql,productName,supplierID,price)
        if not e:
            flash("Supplier ID does not exist.")
            return redirect(url_for('addProduct'))
        flash("Product added successfully.")
        return redirect(url_for('addProduct'))

@app.route("/orders/")
def orders():
    return render_template("orders.html",orders=db.allOrders(mysql),titolo="Orders")
       


@app.route("/details/<id>")
def details(id):
    return render_template("orders.html",orders=db.details(id),titolo="Details",extra = "for customerID "+id)
       
@app.route("/api/orders/")
def api_orders():
    return db.api_allOrders(mysql)

app.run(debug=True)