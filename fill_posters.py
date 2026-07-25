import pandas as pd
import requests
import time

API_KEY = "6f82e120d9b837cd13a65dca637a8214"

movies = pd.read_csv("data/movies.csv")

# Prevent pandas warning
movies["poster"] = movies["poster"].astype("object")

headers = {
    "User-Agent": "Mozilla/5.0"
}

for i, row in movies.iterrows():

    title = row["title"]

    # Skip if poster already exists
    if pd.notna(row["poster"]) and str(row["poster"]).strip() != "":
        print(f"Skipped: {title}")
        continue

    success = False

    for attempt in range(3):

        try:

            url = (
                f"https://api.themoviedb.org/3/search/movie"
                f"?api_key={API_KEY}"
                f"&query={title}"
            )

            response = requests.get(
                url,
                headers=headers,
                timeout=20
            )

            data = response.json()

            if data["results"]:

                poster = data["results"][0]["poster_path"]

                if poster:

                    movies.at[i, "poster"] = (
                        "https://image.tmdb.org/t/p/w500"
                        + poster
                    )

                    print(f"✔ {title}")

                else:
                    print(f"No poster: {title}")

            else:
                print(f"Movie not found: {title}")

            success = True
            break

        except Exception as e:

            print(f"Retry {attempt+1}/3 : {title}")

            time.sleep(2)

    if not success:
        print(f"Failed : {title}")

    # Save after every movie
    movies.to_csv("data/movies.csv", index=False)

    # Wait so TMDB doesn't block requests
    time.sleep(0.5)

print("\n✅ All possible posters have been added.")