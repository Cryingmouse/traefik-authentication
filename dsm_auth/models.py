from datetime import datetime
from flask import current_app
from itsdangerous import URLSafeSerializer

from app import db
from dsm_auth.utils import create_browser_id


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(256), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    create_datetime = db.Column(db.DateTime, nullable=False,
                                default=datetime.utcnow())

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    def __repr__(self):
        return "User<name:%r>" % self.username

    def get_token(self, life_time=None):
        key = current_app.config.get("SECRET_KEY")
        s = URLSafeSerializer(key)
        browser_id = create_browser_id()
        if not life_time:
            life_time = current_app.config.get("TOKEN_LIFETIME")
        token = s.dumps(
            (self.id, self.username, self.password, browser_id, life_time))
        return token
