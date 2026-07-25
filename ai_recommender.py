import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

movies = pd.read_csv("data/movies.csv")

movies["features"] = (
    movies["genre"].fillna("") + " " +
    movies["mood"].fillna("") + " " +
    movies["language"].fillna("") + " " +
    movies["industry"].fillna("") + " " +
    movies["description"].fillna("")
)

vectorizer = TfidfVectorizer(stop_words="english")

tfidf_matrix = vectorizer.fit_transform(movies["features"])

similarity = cosine_similarity(tfidf_matrix)


def recommend(movie_title):

    if movie_title not in movies["title"].values:
        return []

    movie_index = movies[movies["title"] == movie_title].index[0]

    similarity_scores = list(enumerate(similarity[movie_index]))

    ranked_movies = []

    for index, score in similarity_scores:

        if index == movie_index:
            continue

        rating = float(movies.iloc[index]["rating"])

        # Final score = Similarity + Rating Bonus
        final_score = score + (rating / 100)

        ranked_movies.append((index, final_score))

    ranked_movies = sorted(
        ranked_movies,
        key=lambda x: x[1],
        reverse=True
    )

    recommended_movies = []

    for index, score in ranked_movies[:6]:

        recommended_movies.append(
            movies.iloc[index].to_dict()
        )

    return recommended_movies

def recommend_from_watchlist(watchlist):

    if len(watchlist) == 0:
        return []

    scores = {}

    for movie in watchlist:

        recommendations = recommend(movie)

        for rec in recommendations:

            title = rec["title"]

            if title in watchlist:
                continue

            if title not in scores:
                scores[title] = 0

            scores[title] += 1

    sorted_movies = sorted(
        scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    final = []

    for title, score in sorted_movies[:6]:

        movie = movies[movies["title"] == title]

        if not movie.empty:
            final.append(movie.iloc[0].to_dict())

    return final