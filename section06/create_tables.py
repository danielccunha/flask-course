import sqlite3

connection = sqlite3.connect("data.db")
cursor = connection.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS items (name TEXT, price REAL)")

connection.commit()
connection.close()
