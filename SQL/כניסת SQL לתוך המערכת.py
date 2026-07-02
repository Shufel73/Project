import mysql.connector

try:
    
    db_connection = mysql.connector.connect(
        host="localhost",
        user="shufel_db",
        password="123456",
        database="NetworkDB"
    )
    
    cursor = db_connection.cursor()
    
    
    sql = "INSERT INTO NetworkLogs (device_name, status, message) VALUES (%s, %s, %s)"
    
    # הערכים שאנחנו רוצים להכניס ללוג
    values = ("Router-HQ", "UP", "Test log from Python - Everything is working!")
    
    
    cursor.execute(sql, values)
    db_connection.commit()
    
    print(f"Boom! Record inserted successfully. Row ID is: {cursor.lastrowid}")
    
except mysql.connector.Error as err:
    print(f"Failed to insert record: {err}")
    
finally:
    
    if 'db_connection' in locals() and db_connection.is_connected():
        cursor.close()
        db_connection.close()
        print("Database connection closed.")