def createAutore(mysql):
    cursor = mysql.connection.cursor()

    query = """
    CREATE TABLE IF NOT EXISTS Autore(
        Nome varchar (20) NOT NULL,
        Cognome varchar(20) NOT NULL,
        CF varchar(16), 
        DataN date NOT NULL, 
        DataM date,
        
        PRIMARY KEY (CF))
    )
        """
    cursor.execute(query)
    cursor.close()
    
    return
        
def createLibro(mysql):
    cursor = mysql.connection.cursor()

    query = """
    CREATE TABLE IF NOT EXISTS Libro(
        ISBN varchar(13),
        Titolo varchar (50) NOT NULL,
        Genere varchar (20) NOT NULL,
        Prezzo float(2), 
        Locazione varchar(20), 
        Autore varchar(16), 
        Disponibile boolean DEFAULT true,
        titoloRiassunto varchar(20),
        riassunto varchar(1000),
        
        PRIMARY KEY (ISBN), 
        FOREIGN KEY (Autore) REFERENCES Autore (CF))
    )
        """
    cursor.execute(query)
    cursor.close()

    return

def createUtente(mysql):
    cursor = mysql.connection.cursor()
    
    query = """
        CREATE TABLE IF NOT EXISTS Utente(
            nome varchar(20) NOT NULL,
            cognome varchar (20) NOT NULL,
            username varchar (20) NOT NULL,
            password varchar (255) NOT NULL,
            ddn date NOT NULL,

            PRIMARY KEY(username)
        )
        """
    
    cursor.execute(query)
    cursor.close
    
def createPrestito(mysql):
    cursor = mysql.connection.cursor()
    
    query = """
       CREATE TABLE IF NOT EXISTS Prestito(
            ISBN varchar(13),
            utente varchar(20),
            dataInizio date NOT NULL,
            dataFine date NOT NULL,
            idPrestito int NOT NULL AUTO_INCREMENT,
        
            FOREIGN KEY(ISBN) references Libro(ISBN),
            FOREIGN KEY(utente) references Utente(username),
            PRIMARY KEY(idPrestito)
        )
        """
    
    cursor.execute(query)
    cursor.close

def addLibro(mysql,isbn,titolo,genere,prezzo,locazione,autore):
    cursor = mysql.connection.cursor()
    
    query = "SELECT * FROM Autore WHERE CF = %s"
    cursor.execute(query, (autore,))
    ris = cursor.fetchall()
    
    if len(ris)==0:
        return False

    prezzo = None if prezzo == "" else prezzo
    
    query = """
    INSERT INTO Libro (ISBN, Titolo, Genere, Prezzo, Locazione, Autore)
    VALUES (%s,%s,%s,%s,%s,%s)
    """
    
    cursor.execute(query, (isbn,titolo,genere,prezzo,locazione,autore))
    mysql.connection.commit()
    
    cursor.close()
    return True

def addAutore(mysql,nome,cognome,cf,ddn,ddm):
    cursor = mysql.connection.cursor()
    
    query = "SELECT * FROM Autore WHERE CF = %s"
    cursor.execute(query, (cf,))
    ris = cursor.fetchall()
    
    if len(ris)!=0:
        return False

    ddm = None if ddm == "" else ddm
    
    query = """
    INSERT INTO Autore 
    VALUES (%s,%s,%s,%s,%s)
    """
    
    cursor.execute(query, (nome,cognome,cf,ddn,ddm))
    mysql.connection.commit()
    cursor.close()
    return True

def catalogo(mysql,query, params):
    cursor = mysql.connection.cursor()
    query += " JOIN Autore ON Libro.Autore = Autore.CF"
    cursor.execute(query, params)
    libri = cursor.fetchall()
    cursor.close()
    return libri

def getGeneri(mysql):
    query_generi = "SELECT DISTINCT Genere FROM Libro"
    cursor = mysql.connection.cursor()
    cursor.execute(query_generi)
    generi = [row[0] for row in cursor.fetchall()]
    cursor.close()
    return generi

def getAutore(mysql,cf):
    cursor = mysql.connection.cursor()
    query_autore = "SELECT * FROM Autore WHERE CF = %s"
    cursor.execute(query_autore, (cf,))
    autore = cursor.fetchone()
    cursor.close()
    return autore

def getLibriAutore(mysql,cf):
    cursor = mysql.connection.cursor()
    query_libri = "SELECT * FROM Libro WHERE Autore = %s"
    cursor.execute(query_libri, (cf,))
    libri_autore = cursor.fetchall()
    cursor.close()
    return libri_autore

def addQuery():
    query = "SELECT * FROM Libro" 
    return query

def addOrdinamento(order_by):
    query = f" ORDER BY {order_by}"
    return query

def filtraGenere(parametri,genere):
    query = " WHERE Genere = %s"
    parametri.append(genere)
    return query
            
def addFiltro(query):
    query = " WHERE LOWER(Titolo) LIKE %s OR LOWER(Autore) LIKE %s OR ISBN LIKE %s"
    return query

def valida_password(re,password,confirmPassword):
    """ Verifica se la password rispetta i vincoli di sicurezza """
    if len(password) < 8:
        return "La password deve contenere almeno 8 caratteri."
    if not re.search(r"\d", password):
        return "La password deve contenere almeno un numero."
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return "La password deve contenere almeno un carattere speciale (!@#$%^&* etc.)."
    if password != confirmPassword:
        return "Le password non coincidono"
    return None

def registrati(mysql,nome,cognome,username,password_hash,ddn):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Utente WHERE username = %s", (username,))
    existing_user = cur.fetchone()

    if existing_user:
        return False
    
    cur.execute("INSERT INTO Utente (nome, cognome, username, password, ddn) VALUES (%s, %s, %s, %s, %s)",
                (nome, cognome, username, password_hash, ddn))
    mysql.connection.commit()
    cur.close()

def get_utente_by_username(mysql, username):
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM Utente WHERE username = %s"
    cursor.execute(query, (username,))
    user = cursor.fetchone()
    cursor.close()
    return user

def get_utente_by_cf(mysql, cf):
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM Utenti WHERE CF = ?"
    result = cursor.execute(query, (cf,))
    return result[0] if result else None

def get_libro_by_isbn(mysql, isbn):
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM Libro WHERE ISBN = %s"  # Corretto: cambia ? con %s
    cursor.execute(query, (isbn,))
    result = cursor.fetchone()  # Ottieni il primo risultato
    cursor.close()
    return result

from datetime import datetime

def aggiungi_prestito(mysql, isbn, username, data_inizio, data_fine):
    cursor = mysql.connection.cursor()

    # Converti le date in oggetti datetime per il confronto
    try:
        data_inizio_dt = datetime.strptime(data_inizio, "%Y-%m-%d")
        data_fine_dt = datetime.strptime(data_fine, "%Y-%m-%d")
    except ValueError:
        cursor.close()
        print("Formato data non valido.")
        return False

    # Verifica che la data di fine sia successiva alla data di inizio
    if data_fine_dt <= data_inizio_dt:
        cursor.close()
        print("Errore: La data di fine deve essere successiva alla data di inizio.")
        return False

    # Verifica se il libro è disponibile
    query_check = "SELECT disponibile FROM Libro WHERE isbn = %s"
    cursor.execute(query_check, (isbn,))
    result = cursor.fetchone()

    if result and result[0]:  # Se il libro è disponibile (True)
        # Aggiungi il prestito
        query_prestito = "INSERT INTO Prestito (isbn, utente, dataInizio, dataFine) VALUES (%s, %s, %s, %s)"
        cursor.execute(query_prestito, (isbn, username, data_inizio, data_fine))

        # Imposta la disponibilità del libro su False
        query_update = "UPDATE Libro SET disponibile = False WHERE isbn = %s"
        cursor.execute(query_update, (isbn,))

        # Conferma le modifiche
        mysql.connection.commit()
        cursor.close()
        return True
    else:
        cursor.close()
        print("Il libro non è disponibile.")
        return False
  
def update_disponibilita(mysql, isbn):
    cursor = mysql.connection.cursor()
    query = "UPDATE Libro SET Disponibilità = 0 WHERE ISBN = %s"
    cursor.execute(query, (isbn,))
    mysql.connection.commit()
    cursor.close()
    
def getUserByUsername(mysql, username):
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM Utente WHERE username = %s"
    cursor.execute(query, (username,))
    user = cursor.fetchone()  # Restituisce una riga se l'utente esiste
    cursor.close()
    return user

def restituire_libro(mysql, isbn):
    cursor = mysql.connection.cursor()
    # Aggiorna la disponibilità del libro
    query_libro = "UPDATE Libro SET disponibile = 1 WHERE isbn = %s"
    cursor.execute(query_libro, (isbn,))

    mysql.connection.commit()
    cursor.close()
    return True


def get_prestiti_attivi_per_utente(mysql, username):
    cursor = mysql.connection.cursor()
    query = """
        SELECT p.isbn, l.titolo, p.dataInizio, p.dataFine
        FROM Prestito p
        JOIN Libro l ON p.isbn = l.isbn
        WHERE p.utente = %s AND p.dataFine >= CURDATE() AND l.disponibile = 0
    """
    cursor.execute(query, (username,))
    prestiti = cursor.fetchall()
    cursor.close()
    return prestiti

def elimina_prestito(mysql, isbn, username):
    cursor = mysql.connection.cursor()
    query = "DELETE FROM Prestito WHERE ISBN = %s AND utente = %s"
    cursor.execute(query, (isbn, username))
    mysql.connection.commit()
    cursor.close()

def aggiorna_disponibilita(mysql, isbn):
    cursor = mysql.connection.cursor()
    query = "UPDATE Libro SET disponibile = TRUE WHERE ISBN = %s"
    cursor.execute(query, (isbn,))
    mysql.connection.commit()
    cursor.close()

def get_prestito_by_isbn_and_user(mysql, isbn, username):
    cursor = mysql.connection.cursor()
    query = """
        SELECT * FROM Prestito
        WHERE ISBN = %s AND utente = %s AND dataFine >= CURDATE()
    """
    cursor.execute(query, (isbn, username))
    prestito = cursor.fetchone()
    cursor.close()
    return prestito

def aggiornaRiassunto(mysql,titolo_riassunto,testo_riassunto,isbn):
    # Aggiorna il riassunto nel database
    cursor = mysql.connection.cursor()
    query = """
    UPDATE Libro 
    SET titoloRiassunto = %s, riassunto = %s
    WHERE ISBN = %s
    """
    try:
        cursor.execute(query, (titolo_riassunto, testo_riassunto, isbn))
        mysql.connection.commit()
        cursor.close()
        return True
    except Exception as e:
        mysql.connection.rollback()
        cursor.close()
        return False
    
def getRiassunto(mysql, isbn):
    cursor = mysql.connection.cursor()
    query = "SELECT titoloRiassunto, riassunto FROM Libro WHERE ISBN = %s"
    cursor.execute(query, (isbn,))
    result = cursor.fetchone()
    cursor.close()
    
    return result