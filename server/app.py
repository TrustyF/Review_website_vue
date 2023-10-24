import os
from pprint import pprint

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sql_models.media_model import *
from dotenv import load_dotenv

# from database import db
from constants import MAIN_DIR
from db_loader import db

# check if using locally
dev_mode = os.path.exists(os.path.join(MAIN_DIR, 'devmode.txt'))

load_dotenv(os.path.join(MAIN_DIR, '.env'))

app = Flask(__name__)

db_username = os.getenv('MYSQL_DATABASE_USERNAME')
db_password = os.getenv('MYSQL_DATABASE_PASSWORD')
db_name = 'TrustyFox$ygo_cards_library'

database_uri = f'mysql+pymysql://{db_username}:{db_password}@TrustyFox.mysql.pythonanywhere-services.com:3306/{db_name}'
local_database_uri = f'mysql+pymysql://root:{db_password}@127.0.0.1:3306/{db_name}'

if dev_mode:
    print('using local')
    app.config["SQLALCHEMY_DATABASE_URI"] = local_database_uri
else:
    print('using cloud')
    app.config["SQLALCHEMY_DATABASE_URI"] = database_uri

CORS(app)


@app.route("/test")
def test():
    return "test", 200


with app.app_context():
    # app.config['SQLALCHEMY_POOL_SIZE'] = 1
    # app.config['SQLALCHEMY_MAX_OVERFLOW'] = 0
    # app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {"pool_size": 100, "max_overflow": 0}
    db.init_app(app)

    # db.drop_all()
    # db.create_all()

    from flask_blueprints import card_detector_blueprint, datasbase_blueprint, movie_blueprint, storage_blueprint

    app.register_blueprint(card_detector_blueprint.bp, url_prefix='/card_detector')
    app.register_blueprint(datasbase_blueprint.bp, url_prefix='/database')
    app.register_blueprint(card_blueprint.bp, url_prefix='/card')
    app.register_blueprint(storage_blueprint.bp, url_prefix='/storage')
