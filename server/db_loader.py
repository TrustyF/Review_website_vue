from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(engine_options={'connect_args': {'connect_timeout': 10}})
