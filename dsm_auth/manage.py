from flask_migrate import upgrade, migrate, stamp, init

from app import create_app, db, bcrypt
from models import User


def deploy():
    app = create_app()
    app.app_context().push()
    db.create_all()

    # migrate database to latest revision
    init()
    stamp()
    migrate()
    upgrade()


def create_user(username, password):
    user = User(
        username=username,
        password=bcrypt.generate_password_hash(password))

    db.session.add(user)
    db.session.commit()


deploy()
create_user(username="Julian", password="welcome")
