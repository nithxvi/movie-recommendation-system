import os
import ast
import pandas as pd


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

MOVIES_PATH = os.path.join(
    BASE_DIR,
    "data",
    "tmdb_5000_movies.csv"
)

CREDITS_PATH = os.path.join(
    BASE_DIR,
    "data",
    "tmdb_5000_credits.csv"
)


def convert_names(data):
    """
    Extract names from TMDB JSON-like data.

    Example:
    [{"id": 28, "name": "Action"}]

    becomes:

    ["Action"]
    """

    try:
        data = ast.literal_eval(data)

        return [
            item["name"].replace(" ", "")
            for item in data
        ]

    except (ValueError, SyntaxError):
        return []


def load_and_process_movies():

    print("\nLoading movie datasets...")

    movies = pd.read_csv(MOVIES_PATH)
    credits = pd.read_csv(CREDITS_PATH)

    print("Movies dataset shape:", movies.shape)
    print("Credits dataset shape:", credits.shape)

    # Merge datasets using movie title
    movies = movies.merge(
        credits,
        on="title"
    )

    print("Merged dataset shape:", movies.shape)

    # Keep only useful columns
    movies = movies[
        [
            "movie_id",
            "title",
            "overview",
            "genres",
            "keywords"
        ]
    ]

    # Remove movies with missing values
    movies.dropna(inplace=True)

    # Convert genres and keywords into lists
    movies["genres"] = movies["genres"].apply(convert_names)

    movies["keywords"] = movies["keywords"].apply(convert_names)

    # Convert overview into words
    movies["overview"] = movies["overview"].apply(
        lambda x: x.split()
    )

    # Create combined feature column
    movies["tags"] = (
        movies["overview"]
        + movies["genres"]
        + movies["keywords"]
    )

    # Convert tags list into a single string
    movies["tags"] = movies["tags"].apply(
        lambda x: " ".join(x)
    )

    # Final cleaned dataset
    movies = movies[
        [
            "movie_id",
            "title",
            "genres",
            "tags"
        ]
    ]

    # Convert movie IDs to integers
    movies["movie_id"] = movies["movie_id"].astype(int)

    # Reset index
    movies.reset_index(
        drop=True,
        inplace=True
    )

    print("\nMovie data processed successfully!")
    print("Final dataset shape:", movies.shape)

    print("\nSample processed movie:")

    print(
        movies[
            ["movie_id", "title", "genres", "tags"]
        ].head(3)
    )

    return movies