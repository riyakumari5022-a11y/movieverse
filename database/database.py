import sqlite3

connection = sqlite3.connect("movieverse.db")

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    fullname TEXT NOT NULL,

    email TEXT UNIQUE NOT NULL,

    password TEXT NOT NULL

)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS watchlist(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    user_email TEXT,

    movie_title TEXT,

    genre TEXT,

    rating TEXT,

    poster TEXT

)
""")

connection.commit()

connection.close()

print("Database Created Successfully!")