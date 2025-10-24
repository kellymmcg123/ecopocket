import mysql.connector

database = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Furby2013!",
    database="ecopocket"
)

cursor = database.cursor()

# Create new table 'test'
cursor.execute("CREATE TABLE test (name VARCHAR(255), number INT)")

# Add row to new table 'test'
cursor.execute("INSERT INTO test (name, number) VALUES ('Max', 3);")

# Change already existing data
cursor.execute("UPDATE users SET email = 'mary456@gmail.com' WHERE email = 'mary123@gmail.com'")

# Insert new row into existing table
cursor.execute("INSERT INTO location (name, address) VALUES ('SuperValu', 'Ballincollig')")

# Delete Table 'test'
cursor.execute("DROP TABLE test;")

database.commit()



