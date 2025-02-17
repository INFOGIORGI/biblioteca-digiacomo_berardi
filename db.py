import json
import datetime

def addProduct(mysql,productName,supplierID,price):
        cursor = mysql.connection.cursor()
        query = '''SELECT * FROM suppliers WHERE supplierID=%s'''
        cursor.execute(query,(supplierID,))
        dati = cursor.fetchall() #torna il risultato della query
        if len(dati)==0:
            return False
        query = '''INSERT INTO products(ProductName, SupplierID, Price) value(%s,%s,%s)'''
        cursor.execute(query,(productName,supplierID,price))
        mysql.connection.commit()
        cursor.close()
        return True

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