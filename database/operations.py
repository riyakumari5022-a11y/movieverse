import sqlite3
import pandas as pd


# ----------------------------
# Create New User
# ----------------------------

def create_user(fullname, email, password):

    connection = sqlite3.connect("movieverse.db")
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO users(fullname, email, password)
        VALUES (?, ?, ?)
        """,
        (fullname, email, password)
    )

    connection.commit()
    connection.close()


# ----------------------------
# Login User
# ----------------------------

def check_user(email, password):

    connection = sqlite3.connect("movieverse.db")
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT * FROM users
        WHERE email = ? AND password = ?
        """,
        (email, password)
    )

    user = cursor.fetchone()

    connection.close()

    return user


# ----------------------------
# Add Movie to Watchlist
# ----------------------------

def add_to_watchlist(user_email, movie_title):

    movies = pd.read_csv("data/movies.csv")

    movie = movies[movies["title"] == movie_title]

    if movie.empty:
        return

    movie = movie.iloc[0]

    connection = sqlite3.connect("movieverse.db")
    cursor = connection.cursor()

    # Check if movie already exists
    cursor.execute(
        """
        SELECT *

        FROM watchlist

        WHERE user_email = ?

        AND movie_title = ?
        """,
        (
            user_email,
            movie_title
        )
    )

    existing_movie = cursor.fetchone()

    if existing_movie:

        connection.close()
        return

    cursor.execute(
        """
        INSERT INTO watchlist
        (user_email, movie_title, genre, rating, poster)

        VALUES (?, ?, ?, ?, ?)
        """,
        (
            user_email,
            movie["title"],
            movie["genre"],
            movie["rating"],
            movie["poster"]
        )
    )

    connection.commit()
    connection.close()


# ----------------------------
# Get User Watchlist
# ----------------------------

def get_watchlist(user_email):

    connection = sqlite3.connect("movieverse.db")
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT movie_title, genre, rating, poster

        FROM watchlist

        WHERE user_email = ?
        """,
        (user_email,)
    )

    rows = cursor.fetchall()

    connection.close()

    movies = []

    for row in rows:

        movies.append(
            {
                "title": row[0],
                "genre": row[1],
                "rating": row[2],
                "poster": row[3]
            }
        )

    return movies


# ----------------------------
# Remove Movie from Watchlist
# ----------------------------

def remove_from_watchlist(user_email, movie_title):

    connection = sqlite3.connect("movieverse.db")
    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM watchlist

        WHERE user_email = ?

        AND movie_title = ?
        """,
        (
            user_email,
            movie_title
        )
    )

    connection.commit()
    connection.close()