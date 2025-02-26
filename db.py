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
        
        PRIMARY KEY (ISBN), 
        FOREIGN KEY (Autore) REFERENCES Autore (CF))
        """
    cursor.execute(query)
    cursor.close()

    return

def addLibro(mysql,isbn,titolo,genere,prezzo,locazione,autore):
    cursor = mysql.connection.cursor()
    
    query = "SELECT * FROM Autore WHERE CF = %s"
    cursor.execute(query, (autore,))
    ris = cursor.fetchall()
    
    if len(ris)==0:
        return False

    prezzo = None if prezzo == "" else prezzo
    
    query = """
    INSERT INTO Libro 
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