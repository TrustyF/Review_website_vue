import logging
import os

from dotenv import load_dotenv
from flask import Flask
from flask_caching import Cache
from flask_cors import CORS

from constants import MAIN_DIR
from db_loader import db
from utilities.asset_manager import check_posters, make_home_banner
from utilities.devmode_checker import dev_mode

load_dotenv(os.path.join(MAIN_DIR, '.env'))

if dev_mode:
    app = Flask(__name__)
else:
    app = Flask(__name__, static_folder=None)

db_username = os.getenv('MYSQL_DATABASE_USERNAME')
db_password = os.getenv('MYSQL_DATABASE_PASSWORD')
db_name = 'TrustyFox$review_site'

database_uri = f'mysql+pymysql://{db_username}:{db_password}@TrustyFox.mysql.pythonanywhere-services.com:3306/{db_name}'
local_database_uri = f'mysql+pymysql://root:{db_password}@127.0.0.1:3306/{db_name}'

app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_recycle': 280,
    'pool_pre_ping': True,
}

cache_config = {
    "CACHE_TYPE": "SimpleCache",
    "CACHE_DEFAULT_TIMEOUT": 300
}
app.config.from_mapping(cache_config)
cache = Cache(app)

if dev_mode:
    print('using local')
    app.config["SQLALCHEMY_DATABASE_URI"] = local_database_uri
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = database_uri
    logging.disable(logging.WARNING)

CORS(app)

with app.app_context():
    db.init_app(app)

    from flask_blueprints import media_blueprint, tag_blueprint, tier_list_blueprint, login_blueprint, \
        user_list_blueprint, media_banner_blueprint

    app.register_blueprint(media_blueprint.bp, url_prefix='/media')
    app.register_blueprint(media_banner_blueprint.bp, url_prefix='/media_banner')
    app.register_blueprint(tag_blueprint.bp, url_prefix='/tag')
    app.register_blueprint(tier_list_blueprint.bp, url_prefix='/tier_list')
    app.register_blueprint(user_list_blueprint.bp, url_prefix='/user_list')
    app.register_blueprint(login_blueprint.bp, url_prefix='/login')
    # app.register_blueprint(task_blueprint.bp, url_prefix='/task')

# run setup tasks
with app.app_context():
    check_posters()
    make_home_banner()
