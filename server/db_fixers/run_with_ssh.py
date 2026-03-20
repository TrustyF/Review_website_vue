import csv
import os

from dateutil import parser
from dotenv import load_dotenv
import sshtunnel
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from constants import MAIN_DIR
from sql_models.media_model import Media

load_dotenv(os.path.join(MAIN_DIR, '.env'))

SSH_USERNAME = os.getenv('SSH_USERNAME')
SSH_PASSWORD = os.getenv('SSH_PASSWORD')
MYSQL_DATABASE_USERNAME = os.getenv('MYSQL_DATABASE_USERNAME')
MYSQL_DATABASE_PASSWORD = os.getenv('MYSQL_DATABASE_PASSWORD')

sshtunnel.SSH_TIMEOUT = 5.0
sshtunnel.TUNNEL_TIMEOUT = 5.0

app = Flask(__name__)
db = SQLAlchemy(engine_options={'connect_args': {'connect_timeout': 10}})
db_session = db.session

with app.app_context():
    with sshtunnel.SSHTunnelForwarder(
            'ssh.pythonanywhere.com',
            ssh_username=SSH_USERNAME,
            ssh_password=SSH_PASSWORD,
            remote_bind_address=('TrustyFox.mysql.pythonanywhere-services.com', 3306)
    ) as tunnel:
        tunnel.start()
        print('tunnel connected')

        local_port = str(tunnel.local_bind_port)
        app.config[
            "SQLALCHEMY_DATABASE_URI"] = f'mysql+pymysql://{MYSQL_DATABASE_USERNAME}:{MYSQL_DATABASE_PASSWORD}@127.0.0.1:{local_port}/TrustyFox$review_site'

        db.init_app(app)

        print(db.session.query(Media).first())
        with open(r'C:\Users\sirja\Downloads\ratings.csv') as csv_file:
            reader = csv.reader(csv_file, delimiter=',')

            for i, row in enumerate(reader):
                date = row[2]
                print(row[4][:-1])
                try:
                    obj = db.session.query(Media).filter(Media.external_link == row[4][:-1])
                    obj.update({'created_at': parser.parse(date)})
                except Exception as e:
                    print(e)
                    print(row[3], ' not found')
                    pass

        db.session.commit()
        db.session.close()
