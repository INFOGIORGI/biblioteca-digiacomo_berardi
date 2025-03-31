from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mysqldb import MySQL
import db
import re
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "super secret key"

app.config['MYSQL_HOST'] = '138.41.20.102'
app.config['MYSQL_PORT'] = 53306
app.config['MYSQL_USER'] = '5di'
app.config['MYSQL_PASSWORD'] = 'colazzo'
app.config['MYSQL_DB'] = 'digiacomo_berardi'
mysql = MySQL(app)

app.permanent_session_lifetime = timedelta(minutes=30)

@app.route("/")
def home():
    return render_template("index.html",titolo="Home")

@app.route("/createAutore/")
def createAutore():
    return db.createAutore(mysql)

@app.route("/createLibro/")
def createLibro():
    return db.createLibro(mysql)

@app.route("/createUtente/")
def createUtente():
    return db.createUtente(mysql)

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
        parametri = []
        query = db.addQuery()
        
        if order_by:
            query += db.addOrdinamento(order_by)
            
        if genere:
            query += db.filtraGenere(parametri,genere)
                    
        libri = db.catalogo(mysql, query, tuple(parametri))
        generi = db.getGeneri(mysql)
            
        return render_template("catalogo.html",libri=libri, generi = generi, titolo = "Catalogo")
    else:
        filtro = request.form.get("filtro","")
        query = db.addQuery()
        
        if filtro:
            query += db.addFiltro(query)
            param_filtro = f"%{filtro.lower()}%" #doppia percentuale cerca il filtro in mezzo ad altre parole 
            libriFiltrati = db.catalogo(mysql, query, (param_filtro, param_filtro, param_filtro, param_filtro, param_filtro, param_filtro))
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

@app.route("/registrati/", methods=["GET", "POST"])
def registrati():
    if request.method == "POST":
        nome = request.form.get("nome")
        cognome = request.form.get("cognome")
        username = request.form.get("username")
        password = request.form.get("password")
        confirmPassword = request.form.get("confirmPassword")
        ddn = request.form.get("ddn")

        # Controllo validità password
        errore_password = db.valida_password(re,password,confirmPassword)
        if errore_password:
            flash(errore_password)
            return redirect(url_for("registrati"))

        password_hash = generate_password_hash(password)
        
        if(db.registrati(mysql,nome,cognome,username,password_hash,ddn)==False):
            flash("Username già in uso, scegline un altro.")
            return redirect(url_for("registrati"))
        
        flash("Registrazione completata con successo!")
        return redirect(url_for("registrati"))
    
    return render_template("registrati.html")

@app.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = db.getUserByUsername(mysql, username)
        if user and check_password_hash(user[3], password):
            session["user_id"] = user[0]
            session["username"] = user[2]
            flash(f"Benvenuto {username}!", "success")
            return redirect(url_for("home"))
        else:
            flash("Username o password errati.", "danger")
            return redirect(url_for("login"))
    
    return render_template("login.html")

@app.route("/logout/")
def logout():
    session.pop("username", None)  # Rimuove l'utente dalla sessione
    flash("Logout effettuato con successo!")
    return redirect(url_for("home"))

@app.route('/prestito/', methods=['GET', 'POST'])
@app.route('/prestito/<isbn>', methods=['GET', 'POST'])
def prestito(isbn=None):
    # Verifica se l'utente è loggato, se non lo è, lo reindirizza alla pagina di login
    if 'user_id' not in session:
        flash("Devi essere loggato per fare un prestito.")
        return redirect(url_for('login'))

    if isbn:
        # Se viene passato un ISBN, mostra il form per effettuare il prestito
        libro = db.get_libro_by_isbn(mysql, isbn)  # Ottieni il libro con l'ISBN specificato
        if not libro:
            flash("Libro non trovato.",)
            return redirect(url_for('catalogo'))  # Se il libro non esiste, torna al catalogo

        if request.method == 'POST':
            # Preleva i dati dal form
            username = session['username']  # Lo username dell'utente loggato
            data_inizio = request.form['data_inizio']
            data_fine = request.form['data_fine']

            # Verifica che l'utente esista
            utente = db.get_utente_by_username(mysql, username)
            if not utente:
                flash("Utente non trovato.", "danger")
                return redirect(url_for('prestito', isbn=isbn))  # Se l'utente non esiste, ritorna alla pagina di prestito

            # Aggiungi il prestito nel database
            if db.aggiungi_prestito(mysql, isbn, username, data_inizio, data_fine) == True:
                flash("Prestito effettuato con successo.", "success")
                return redirect(url_for('catalogo'))  # Dopo aver effettuato il prestito, reindirizza al catalogo
            else:
                flash("Errore nell'aggiunta")
                
        return render_template('prestito.html', libro=libro)

    else:
        # Se non viene passato un ISBN, mostra la lista dei prestiti attivi per l'utente
        username = session['username']  # Lo username dell'utente loggato
        prestiti = db.get_prestiti_attivi_per_utente(mysql, username)  # Funzione per ottenere i prestiti attivi

        return render_template('prestito.html', prestiti=prestiti)
    
@app.route('/restituisci/<isbn>', methods=['POST'])
def restituisci(isbn):
    # Verifica se l'utente è loggato
    if 'user_id' not in session:
        flash("Devi essere loggato per restituire un libro.", "danger")
        return redirect(url_for('login'))

    # Restituisce il libro (annulla il prestito e aggiorna la disponibilità)
    if db.restituire_libro(mysql, isbn):
        flash("Libro restituito con successo e stato aggiornato.", "success")
    else:
        flash("Errore nella restituzione del libro.", "danger")

    return redirect(url_for('prestito'))  # Torna alla lista dei prestiti attivi
    
@app.route("/aggiungi_riassunto", methods=["POST"])
def aggiungi_riassunto():
    isbn = request.form.get("isbn")
    titolo_riassunto = request.form.get("titoloRiassunto")
    testo_riassunto = request.form.get("testoRiassunto")

    if(db.aggiornaRiassunto(mysql,titolo_riassunto,testo_riassunto,isbn) == True):
        flash("Riassunto aggiunto con successo!")
        return redirect(url_for('catalogo'))
    
    flash("Errore nell'aggiunta")
    return redirect(url_for('catalogo'))


@app.route("/get_riassunto/<isbn>", methods=["GET"])
def get_riassunto(isbn):
    result = db.getRiassunto(mysql, isbn)

    if result:
        return jsonify({'titolo': result[0], 'riassunto': result[1]})
    else:
        return jsonify({'titolo': None, 'riassunto': 'Riassunto non disponibile'})

app.run(debug=True)