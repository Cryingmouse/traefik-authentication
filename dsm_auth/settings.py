import configparser

config = configparser.ConfigParser()
config.read("/opt/dsm_auth/dsm_auth.conf")
# config.read("../dsm_auth.conf")
db_config = config["Database"]
flask_config = config["Flask"]


def get_database_url():
    name = db_config["type"] or 'mariadb'
    driver = db_config["driver"] or 'mariadbconnector'
    username = 'root'
    password = db_config["root_password"] or 'NAS_PASS'
    host = db_config["host"] or 'localhost'
    port = int(db_config["port"]) if db_config["port"] is not None else 3306
    database = db_config["name"] or 'auth'

    return '{}+{}://{}:{}@{}:{}/{}'.format(name, driver, username, password,
                                           host, port, database)


class Config:
    DEBUG = eval(flask_config['debug']) \
        if flask_config['debug'] is not None else False
    SECRET_KEY = flask_config["secret_key"] or 'secret-key'

    TOKEN_LIFETIME = int(flask_config["token_lifetime"]) \
        if flask_config["token_lifetime"] is not None else 180

    SQLALCHEMY_TRACK_MODIFICATIONS = eval(flask_config['sqlalchemy_track_modifications']) \
        if flask_config['sqlalchemy_track_modifications'] is not None else False

    CACHE_KEY_PREFIX = ''
    CACHE_TYPE = 'SimpleCache'

    SQLALCHEMY_DATABASE_URI = get_database_url()
