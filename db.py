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
        Nome varchar (20),
        Cognome varchar(20),
        DataN date, 
        DataM date,
        CF varchar(16), 
        
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
        Titolo varchar (20),
        Genere varchar (20),
        Prezzo float(2), 
        Locazione varchar(20), 
        Autore varchar(16), 
        
        PRIMARY KEY (ISBN), 
        FOREIGN KEY (Autore) REFERENCES Autore (CF))
        """
    cursor.execute(query)
    cursor.close()

    return

def addLibro(mysql):
    cursor = mysql.connection.cursor()
    
    query = """
    
    """
    
    cursor.execute(query)
    cursor.close()