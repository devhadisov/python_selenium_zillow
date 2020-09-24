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
            host = "localhost"
        )

        mycursor = mydb.cursor()

        mycursor.execute("CREATE DATABASE IF NOT EXISTS " + self.mydb_name + " CHARACTER SET utf8 COLLATE utf8_general_ci")

        # ********** DIGITAL OCEAN SERVER ***********#
        mydb = mysql.connector.connect(
            user = "root",
            password = "",
            host = "localhost",
            database = self.mydb_name
        )

        documents = documents[0]
        print(documents)

        mycursor = mydb.cursor()

        stmt = "SHOW TABLES LIKE '{}'".format(table_name)
        mycursor.execute(stmt)
        result = mycursor.fetchone()

        if not result:
            sql = "CREATE TABLE {} (id INT(11) UNSIGNED AUTO_INCREMENT PRIMARY KEY, PropertyAddress VARCHAR(100), Street VARCHAR(30), City VARCHAR(20), State VARCHAR(20), ZipCode VARCHAR(10), StatusText VARCHAR(50), PhoneNumber VARCHAR(15), BathRooms VARCHAR(15), BedRooms VARCHAR(15), Tax_Assessed_Value VARCHAR(15), Zestimate VARCHAR(15), Rent_Zestimate VARCHAR(15), Home_Type VARCHAR(15), Parking VARCHAR(15), Year_Built VARCHAR(15), HOA VARCHAR(15), Heating VARCHAR(15), Lot VARCHAR(15), Cooling VARCHAR(15), Price_SQFT VARCHAR(15), Identifier VARCHAR(100), CreatedTime VARCHAR(30), UpdatedTime VARCHAR(30), INDEX (Identifier))".format(table_name)

            mycursor.execute(sql)
            mydb.commit()


        sql = "SELECT Identifier FROM {0} WHERE Identifier='{1}'".format(table_name, documents[20])
        mycursor.execute(sql)
        identifier_result = mycursor.fetchone()

        if not identifier_result:
            print("MYSQL ADD")
            insert_sql = """INSERT INTO {} (PropertyAddress, Street, City, State, ZipCode, StatusText, PhoneNumber, BathRooms, BedRooms, Tax_Assessed_Value, Zestimate, Rent_Zestimate, Home_Type, Parking, Year_Built, HOA, Heating, Lot, Cooling, Price_SQFT, Identifier, CreatedTime, UpdatedTime) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""".format(table_name)

            mycursor.execute(insert_sql, documents)
            mydb.commit()

        else:
            print("MYSQL UPDATE")
            year_built = "SELECT Year_Built FROM {0} WHERE Identifier='{1}'".format(table_name, documents[20])
            print(year_built)
            mycursor.execute(year_built)
            year_built_result = mycursor.fetchone()
            print(year_built_result[0])
            
            hoa_sql = "SELECT HOA FROM {0} WHERE Identifier='{1}'".format(table_name, documents[20])
            print(hoa_sql)
            mycursor.execute(hoa_sql)
            hoa_result = mycursor.fetchone()
            print(hoa_result[0])
            
            
            if year_built_result[0] == "" or hoa_result[0] == "":
                print("-----------Update")
            
                update_sql = 'UPDATE {0} SET PropertyAddress="{1}", Street="{2}", City="{3}", State="{4}", ZipCode="{5}", StatusText="{6}", PhoneNumber="{7}", BathRooms="{8}", BedRooms="{9}", Tax_Assessed_Value="{10}", Zestimate="{11}", Rent_Zestimate="{12}", Home_Type="{13}", Parking="{14}", Year_Built="{15}", HOA="{16}", Heating="{17}", Lot="{18}", Cooling="{19}", Price_SQFT="{20}", UpdatedTime="{21}" WHERE Identifier="{22}"'.format(table_name, documents[0], documents[1], documents[2], documents[3], documents[4], documents[5], documents[6], documents[7], documents[8], documents[9], documents[10], documents[11], documents[12], documents[13], documents[14], documents[15], documents[16], documents[17], documents[18], documents[19], datetime.datetime.now(), documents[20])
                print("Updated")
                mycursor.execute(update_sql)
            
                mydb.commit()
                print("==================> Now time:", datetime.datetime.now())