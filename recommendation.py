import pandas as pd


def recommend_movies(movie_title):

    movies = pd.read_csv("data/movies.csv")

    selected_movie = movies[movies["title"] == movie_title]

    if selected_movie.empty:
        return []

    genre = selected_movie.iloc[0]["genre"]

    recommendations = movies[
        (movies["genre"] == genre) &
        (movies["title"] != movie_title)
    ]

    return recommendations.to_dict(orient="records")