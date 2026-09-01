from app.services.data_processor import load_and_process_movies
from app.services.recommendation_engine import RecommendationEngine


movies = load_and_process_movies()

recommendation_engine = RecommendationEngine(movies)