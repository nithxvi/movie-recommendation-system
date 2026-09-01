from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class RecommendationEngine:

    def __init__(self, movies):

        self.movies = movies

        print("\nBuilding recommendation engine...")

        # Convert movie tags into numerical vectors
        self.vectorizer = TfidfVectorizer(
            stop_words="english"
        )

        self.movie_vectors = self.vectorizer.fit_transform(
            self.movies["tags"]
        )

        # Calculate similarity between movies
        self.similarity_matrix = cosine_similarity(
            self.movie_vectors
        )

        print(
            "Recommendation engine ready!"
        )


    def get_similar_movies(
        self,
        movie_id: int,
        top_n: int = 10
    ):

        # Find the movie index
        movie_index = self.movies[
            self.movies["movie_id"] == movie_id
        ].index

        # Movie doesn't exist
        if movie_index.empty:
            return []

        movie_index = movie_index[0]

        # Get similarity scores
        similarity_scores = list(
            enumerate(
                self.similarity_matrix[
                    movie_index
                ]
            )
        )

        # Sort movies by similarity
        similarity_scores = sorted(
            similarity_scores,
            key=lambda x: x[1],
            reverse=True
        )

        # Skip the first result because
        # it is the movie itself
        similar_movies = similarity_scores[
            1:top_n + 1
        ]

        recommendations = []

        for index, score in similar_movies:

            movie = self.movies.iloc[index]

            recommendations.append(
                {
                    "movie_id": int(
                        movie["movie_id"]
                    ),
                    "title": movie["title"],
                    "score": round(
                        float(score),
                        4
                    )
                }
            )

        return recommendations