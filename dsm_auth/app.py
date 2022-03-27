from flask import Flask
from flask_bcrypt import Bcrypt
from flask_caching import Cache
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

import settings

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
cache = Cache()


def create_app():
    app = Flask(__name__)
    app.config.from_object(settings.Config)

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    cache.init_app(app)

    return app
