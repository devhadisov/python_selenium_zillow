import mysql.connector
import datetime

class InsertDB:
    
    mydb_name = "arizona_zillow_db"

    def insert_document(self, documents, table_name):
        print(documents)

        # ************** DIGITAL SERVER ***************#
        mydb = mysql.connector.connect(
            user = "root",
            password = "",
            host = "192.168.1.118"
        )

        mycursor = mydb.cursor()

        mycursor.execute("CREATE DATABASE IF NOT EXISTS " + self.mydb_name + " CHARACTER SET utf8 COLLATE utf8_general_ci")

        # ********** DIGITAL OCEAN SERVER ***********#
        mydb = mysql.connector.connect(
            user = "root",
            password = "",
            host = "192.168.1.118",
            database = self.mydb_name
        )

        documents = documents[0]
        print(documents)

        mycursor = mydb.cursor()

        stmt = "SHOW TABLES LIKE '{}'".format(table_name)
        mycursor.execute(stmt)
        result = mycursor.fetchone()

        if not result:
            sql = "CREATE TABLE {} (id INT(11) UNSIGNED AUTO_INCREMENT PRIMARY KEY, PropertyAddress VARCHAR(50), Street VARCHAR(30), City VARCHAR(20), State VARCHAR(20), ZipCode VARCHAR(10), StatusText VARCHAR(50), PhoneNumber VARCHAR(15), Identifier VARCHAR(100), CreatedTime VARCHAR(30), UpdatedTime VARCHAR(30), INDEX (Identifier))".format(table_name)

            mycursor.execute(sql)
            mydb.commit()


        sql = "SELECT Identifier FROM {0} WHERE Identifier='{1}'".format(table_name, documents[7])
        mycursor.execute(sql)
        identifier_result = mycursor.fetchone()

        if not identifier_result:
            insert_sql = """INSERT INTO {} (PropertyAddress, Street, City, State, ZipCode, StatusText, PhoneNumber, Identifier, CreatedTime, UpdatedTime) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""".format(table_name)

            mycursor.execute(insert_sql, documents)
            mydb.commit()

        else:
            update_sql = 'UPDATE {0} SET PropertyAddress="{1}", Street="{2}", City="{3}", State="{4}", ZipCode="{5}", StatusText="{6}", PhoneNumber="{7}", UpdatedTime="{8}" WHERE Identifier="{9}"'.format(table_name, documents[0], documents[1], documents[2], documents[3], documents[4], documents[5], documents[6], datetime.datetime.now(), documents[7])
            print(update_sql)
            mycursor.execute(update_sql)
            
            mydb.commit()
        print("==================> Now time:", datetime.datetime.now())