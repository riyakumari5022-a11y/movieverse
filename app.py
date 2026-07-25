from flask import Flask, render_template, request, redirect, url_for, session
from database.operations import (
    create_user,
    check_user,
    add_to_watchlist,
    get_watchlist,
    remove_from_watchlist
)
from ai_recommender import recommend, recommend_from_watchlist
import pandas as pd
import random

app = Flask(__name__)
app.secret_key = "movieverse_secret_key"


@app.route("/")
def login():

    if "user" in session:
        return redirect(url_for("home"))

    return render_template("login.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        fullname = request.form["fullname"]
        email = request.form["email"]
        password = request.form["password"]

        create_user(fullname, email, password)

        return redirect(url_for("login"))

    return render_template("signup.html")


@app.route("/login", methods=["POST"])
def login_user():

    email = request.form["email"]
    password = request.form["password"]

    user = check_user(email, password)

    if user:

        session["user"] = user[1]
        session["email"] = user[2]

        return redirect(url_for("home"))

    return render_template(
        "login.html",
        error="Incorrect Email or Password"
    )


@app.route("/home")
def home():

    if "user" not in session:
        return redirect(url_for("login"))

    movies = pd.read_csv("data/movies.csv")

    search_query = request.args.get("search", "")
    genre_query = request.args.get("genre", "")

    genres = sorted(movies["genre"].unique())

    if search_query:
        movies = movies[
            movies["title"].str.contains(
                search_query,
                case=False,
                na=False
            )
        ]

    if genre_query:
        movies = movies[
            movies["genre"] == genre_query
        ]

    movie_list = movies.to_dict(orient="records")

    all_movies = pd.read_csv("data/movies.csv")

    # ============================
    # Home Page Sections
    # ============================

    top_rated = all_movies.sort_values(
        by="rating",
        ascending=False
    ).head(6)

    latest_movies = all_movies.sort_values(
        by="year",
        ascending=False
    ).head(6)

    feel_good = all_movies[
        all_movies["mood"] == "Feel Good"
    ].head(6)

    action_movies = all_movies[
        all_movies["mood"] == "Action Rush"
    ].head(6)

    horror_movies = all_movies[
        all_movies["mood"] == "Horror Night"
    ].head(6)

    mind_bending = all_movies[
        all_movies["mood"] == "Mind Bending"
    ].head(6)

    # ============================
    # Personalized Recommendation
    # ============================

    watchlist = get_watchlist(session["email"])

    watchlist_titles = []

    for movie in watchlist:
        watchlist_titles.append(movie["title"])

    personalized = recommend_from_watchlist(
        watchlist_titles
    )

    return render_template(
        "home.html",
        movies=movie_list,
        top_rated=top_rated.to_dict(orient="records"),
        latest_movies=latest_movies.to_dict(orient="records"),
        personalized=personalized,
        feel_good=feel_good.to_dict(orient="records"),
        action_movies=action_movies.to_dict(orient="records"),
        horror_movies=horror_movies.to_dict(orient="records"),
        mind_bending=mind_bending.to_dict(orient="records"),
        genres=genres,
        search_query=search_query,
        genre_query=genre_query
    )

@app.route("/movie/<title>")
def movie(title):

    if "user" not in session:
        return redirect(url_for("login"))

    movies = pd.read_csv("data/movies.csv")

    movie_data = movies[
        movies["title"] == title
    ]

    if movie_data.empty:
        return "Movie not found"

    movie_data = movie_data.iloc[0].to_dict()

    recommendations = recommend(title)

    return render_template(
        "movie.html",
        movie=movie_data,
        recommendations=recommendations
    )
    

@app.route("/watchlist")
def watchlist():

    if "user" not in session:
        return redirect(url_for("login"))

    movies = get_watchlist(session["email"])

    return render_template(
        "watchlist.html",
        movies=movies
    )

@app.route("/add_watchlist/<title>")
def add_watchlist(title):

    if "user" not in session:
        return redirect(url_for("login"))

    add_to_watchlist(session["email"], title)

    return redirect(url_for("movie", title=title))


@app.route("/remove_watchlist/<title>")
def remove_watchlist(title):

    if "user" not in session:
        return redirect(url_for("login"))

    remove_from_watchlist(session["email"], title)

    return redirect(url_for("watchlist"))


@app.route("/random")
def random_movie():

    if "user" not in session:
        return redirect(url_for("login"))

    movies = pd.read_csv("data/movies.csv")

    random_title = random.choice(
        movies["title"].tolist()
    )

    return redirect(
        url_for(
            "movie",
            title=random_title
        )
    )



@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)