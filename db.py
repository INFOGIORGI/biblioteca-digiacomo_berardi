import json
import datetime

def allOrders(mysql):
    cursor = mysql.connection.cursor()
    query = '''SELECT * FROM orders'''
    cursor.execute(query)
    dati = cursor.fetchall()
    cursor.close()
    return dati

def api_allOrders(mysql):
    cursor = mysql.connection.cursor()
    query = '''SELECT * FROM orders'''
    cursor.execute(query)
    row_headers=[x[0] for x in cursor.description]
    #print(row_headers)
    dati = cursor.fetchall()
    json_data=[]
    for result in dati:
        json_data.append(dict(zip(row_headers,result)))
    cursor.close()   
    #print(json_data) 
    return json.dumps(json_data,default=serialize_datetime)

def serialize_datetime(obj): #per serializzare delle date
    if isinstance(obj, datetime.date): 
        return obj.isoformat() 
    raise TypeError("Type not serializable") 

def details(mysql, id):
    cursor = mysql.connection.cursor()
    query = '''SELECT * FROM orders WHERE customerID = %s'''
    cursor.execute(query,(id,))
    dati = cursor.fetchall()
    cursor.close()
    return dati

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
        Titolo varchar (20) NOT NULL,
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

def catalogo(mysql):
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM Libro"
    cursor.execute(query)
    libri = cursor.fetchall()
    cursor.close()
    return libri

