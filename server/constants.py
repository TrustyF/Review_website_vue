import os
from dotenv import load_dotenv

MAIN_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(MAIN_DIR, '.env'))

TMDB_ACCESS_TOKEN = os.getenv('TMDB_ACCESS_TOKEN')
TMDB_API_KEY = os.getenv('TMDB_API_KEY')
IGDB_CLIENT_ID = os.getenv('IGDB_CLIENT_ID')
IGDB_CLIENT_SECRET = os.getenv('IGDB_CLIENT_SECRET')
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
FLASK_SECRET = os.getenv('FLASK_SECRET')
FIREBASE_ADMIN_UID = os.getenv('FIREBASE_ADMIN_UID')
COMIC_VINE_KEY = os.getenv('COMIC_VINE_KEY')