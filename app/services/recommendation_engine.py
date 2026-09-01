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

    def get_personalized_recommendations(
        self,
        liked_movie_ids: list[int],
        preferred_genres: list[str],
        interacted_movie_ids: list[int],
        top_n: int = 10
    ):

        # Store recommendation scores
        recommendation_scores = {}

        # Find recommendations based on liked/highly-rated movies
        for movie_id in liked_movie_ids:

            # Find movie index
            movie_index = self.movies[
                self.movies["movie_id"] == movie_id
            ].index

            # Skip if movie doesn't exist in dataset
            if movie_index.empty:
                continue

            movie_index = movie_index[0]

            # Get similarity scores
            similarity_scores = enumerate(
                self.similarity_matrix[movie_index]
            )

            for index, score in similarity_scores:

                movie = self.movies.iloc[index]

                candidate_movie_id = int(movie["movie_id"])

                # Don't recommend movies the user already interacted with
                if candidate_movie_id in interacted_movie_ids:
                    continue

                # Skip the source movie itself
                if candidate_movie_id == movie_id:
                    continue

                # Add similarity score
                if candidate_movie_id not in recommendation_scores:
                    recommendation_scores[candidate_movie_id] = 0

                recommendation_scores[candidate_movie_id] += float(score)

        # Add genre preference bonus
        for movie_id in recommendation_scores:

            movie = self.movies[
                self.movies["movie_id"] == movie_id
            ].iloc[0]

            movie_genres = movie["genres"]

            # Normalize genres for comparison
            normalized_movie_genres = [
                genre.lower()
                for genre in movie_genres
            ]

            normalized_preferences = [
                genre.lower().replace(" ", "")
                for genre in preferred_genres
            ]

            # Add bonus if genres match
            matching_genres = set(
                normalized_movie_genres
            ).intersection(
                normalized_preferences
            )

            if matching_genres:
                recommendation_scores[movie_id] += 0.2

        # Sort recommendations
        sorted_recommendations = sorted(
            recommendation_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )

        # Build final response
        recommendations = []

        for movie_id, score in sorted_recommendations[:top_n]:

            movie = self.movies[
                self.movies["movie_id"] == movie_id
            ].iloc[0]

            recommendations.append(
                {
                    "movie_id": movie_id,
                    "title": movie["title"],
                    "genres": movie["genres"],
                    "score": round(float(score), 4)
                }
            )

        return recommendations

    def get_cold_start_recommendations(
        self,
        preferred_genres: list[str],
        top_n: int = 10
    ):

        movies = self.movies.copy()

        # Normalize user preferences
        normalized_preferences = [
            genre.lower().replace(" ", "")
            for genre in preferred_genres
        ]

        # Calculate genre match score
        def genre_match_score(movie_genres):

            normalized_movie_genres = [
                genre.lower()
                for genre in movie_genres
            ]

            matches = set(
                normalized_movie_genres
            ).intersection(
                normalized_preferences
            )

            return len(matches)

        movies["genre_match"] = movies[
            "genres"
        ].apply(genre_match_score)

        # Prefer movies matching user genres
        genre_movies = movies[
            movies["genre_match"] > 0
        ]

        # If no genre matches, use all movies
        if genre_movies.empty:
            genre_movies = movies

        # Remove movies with very few votes
        genre_movies = genre_movies[
            genre_movies["vote_count"] >= 100
        ]

        # Sort based on:
        # 1. Genre match
        # 2. Average rating
        # 3. Popularity
        genre_movies = genre_movies.sort_values(
            by=[
                "genre_match",
                "vote_average",
                "popularity"
            ],
            ascending=False
        )

        recommendations = []

        for _, movie in genre_movies.head(top_n).iterrows():

            recommendations.append(
                {
                    "movie_id": int(movie["movie_id"]),
                    "title": movie["title"],
                    "genres": movie["genres"],
                    "vote_average": round(
                        float(movie["vote_average"]),
                        2
                    ),
                    "score": int(movie["genre_match"])
                }
            )

        return recommendations