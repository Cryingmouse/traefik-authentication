from flask import Flask
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from dsm_auth import settings

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()


def create_app():
    app = Flask(__name__)
    app.config.from_object(settings.Config)

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    return app
