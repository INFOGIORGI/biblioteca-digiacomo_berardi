class db:

    app = Flask(__name__)

    app.config['MYSQL_HOST'] = '138.41.20.102'
    app.config['MYSQL_PORT'] = 53306
    app.config['MYSQL_USER'] = 'ospite'
    app.config['MYSQL_PASSWORD'] = 'ospite'
    app.config['MYSQL_DB'] = 'digiacomo_berardi'
    mysql = MySQL(app)

    def creaLibro():
        cursor = mysql.connection.cursor()

        query = """
        CREATE TABLE IF NOT EXISTS Libro(
            ISBN varchar(13),Titolo varchar (20),
            Genere varchar (20),Prezzo float(2), 
            Locazione varchar(20), Autore varchar(16), 
            PRIMARY KEY (ISBN), 
            FOREIGN KEY (Autore) REFERENCES Autore (CF))
            """
        cursor.execute(query)
        cursor.close()
        return

    def creaAutore():
        cursor = mysql.connection.cursor()

        query = "CREATE TABLE Autore(Nome varchar (20),Cognome varchar(20),DataN date, DataM date,CF varchar(16), PRIMARY KEY (CF))"
        cursor.execute(query)
        cursor.close()
        return

    if __name__ == "__main__":
        app.run(debug = True)