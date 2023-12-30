import os
from dotenv import load_dotenv

MAIN_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(MAIN_DIR, '.env'))

TMDB_ACCESS_TOKEN = os.getenv('TMDB_ACCESS_TOKEN')
TMDB_API_KEY = os.getenv('TMDB_API_KEY')