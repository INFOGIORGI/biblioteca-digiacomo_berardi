from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
import db
import json

app = Flask(__name__)
app.secret_key = "super secret key"


app.config['MYSQL_HOST'] = '138.41.20.102'
app.config['MYSQL_PORT'] = 53306
app.config['MYSQL_USER'] = '5di'
app.config['MYSQL_PASSWORD'] = 'colazzo'
app.config['MYSQL_DB'] = 'digiacomo_berardi'
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

@app.route("/createAutore/")
def createAutore():
    return db.createAutore(mysql)

@app.route("/createLibro/")
def createLibro():
    return db.createLibro(mysql)

@app.route("/addLibro/",methods=["GET","POST"])
def addLibro():
    if request.method == 'GET':
        return render_template("addLibro.html",titolo="AddLibro")
    else:
        isbn = request.form.get("isbn",)
        titolo = request.form.get("titolo",)
        genere = request.form.get("genere",)
        prezzo = request.form.get("prezzo",)
        locazione = request.form.get("locazione",)
        autore = request.form.get("autore",)
        
        e = db.addLibro(mysql,isbn,titolo,genere,prezzo,locazione,autore)
        if not e:
            flash("Supplier ID does not exist.")
            return redirect(url_for('addLibro'))
        else:
            flash("Product added successfully.")
            return redirect(url_for('addLibro'))
            
app.run(debug=True)