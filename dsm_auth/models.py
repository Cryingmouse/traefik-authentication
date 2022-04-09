from datetime import datetime

from dsm_auth.app import db


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
