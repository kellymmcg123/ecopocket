import mysql.connector

# The following code was taken and adjusted from a 'medium' article online
def get_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Furby2013!",
        database="ecopocket"
    )

    return connection



