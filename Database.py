import mysql.connector

database = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Furby2013!",
    database="ecopocket"
)

cursor = database.cursor()

#cursor.execute("INSERT INTO location (name, address) VALUES ('Aldi', 'Dublin');")
#cursor.execute("UPDATE users SET email = 'mary11@gmail.com' WHERE email = 'mary1@email.com'")
cursor.execute("CREATE TABLE test (name VARCHAR(255), number INT) "
               "INSERT INTO test (name, number) VALUES ('Max', 3);")

database.commit()



