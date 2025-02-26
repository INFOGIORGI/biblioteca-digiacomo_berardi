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
            flash("Autore inesistente.")
            return redirect(url_for('addLibro'))
        else:
            flash("Libro aggiunto con successo.")
            return redirect(url_for('addLibro'))

@app.route("/addAutore/",methods=["GET","POST"])
def addAutore():
    if request.method == 'GET':
        return render_template("addAutore.html",titolo="AddLibro")
    else:
        nome = request.form.get("nome",)
        cognome = request.form.get("cognome",)
        cf = request.form.get("cf",)
        ddn = request.form.get("ddn",)
        ddm = request.form.get("ddm",)
        
        e = db.addAutore(mysql,nome,cognome,cf,ddn,ddm)
        if not e:
            flash("Autore già esistente.")
            return redirect(url_for('addAutore'))
        else:
            flash("Autore aggiunto con successo.")
            return redirect(url_for('addAutore'))

@app.route("/catalogo/",methods=["GET","POST"])
def catalogo():
    if request.method == 'GET':
        order_by = request.args.get('order_by', None)
        genere = request.args.get('genere', None)
        
        query = "SELECT * FROM Libro"
        parametri = []
        
        if order_by:
            query += f" ORDER BY {order_by}"
        
        if genere:
            query += " WHERE Genere = %s"
            parametri.append(genere)
            
        libri = db.catalogo(mysql, query, tuple(parametri))
        generi = db.getGeneri(mysql)
            
        return render_template("catalogo.html",libri=libri, generi = generi, titolo = "Catalogo")
    else:
        filtro = request.form.get("filtro","")
        query = "SELECT * FROM Libro"
        
        if filtro:
            query += " WHERE LOWER(Titolo) LIKE %s OR LOWER(Autore) LIKE %s OR ISBN LIKE %s"
            param_filtro = f"%{filtro.lower()}%" #doppia percentuale cerca il filtro in mezzo ad altre parole 
            libriFiltrati = db.catalogo(mysql, query, (param_filtro, param_filtro, param_filtro))
        else:
            libriFiltrati = db.catalogo(mysql)
            
        return render_template("catalogo.html",libri=libriFiltrati,titolo="Catalogo")

@app.route("/autore/<cf>")
def autore(cf):
    autore = db.getAutore(mysql,cf)
    libri_autore = db.getLibriAutore(mysql,cf)
    
    if autore:
        return render_template("autore.html", autore=autore, libri=libri_autore)
    else:
        return "Autore non trovato", 404

        
app.run(debug=True)