import pandas as pd
import os


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

DATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "tmdb_5000_movies.csv"
)


def load_movies():

    movies = pd.read_csv(DATA_PATH)

    print("\nDataset loaded successfully!")

    print("\nDataset shape:")
    print(movies.shape)

    print("\nColumns:")
    print(movies.columns.tolist())

    print("\nFirst 5 movies:")
    print(
        movies[
            ["id", "title", "genres", "overview"]
        ].head()
    )

    return movies