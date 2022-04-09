import argparse
import logging
import uuid
from datetime import datetime, timedelta

import jwt as jwt
from flask import current_app, make_response, request, jsonify
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth, MultiAuth
from gevent.pywsgi import WSGIServer

from dsm_auth.app import create_app, bcrypt
from dsm_auth.models import User
from dsm_auth.utils import create_browser_id, constant_time_compare

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)-8s "
           "[%(filename)s:line %(lineno)s %(funcName)s()] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

app = create_app()
basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth(scheme='Bearer')
multi_auth = MultiAuth(basic_auth, token_auth)


@basic_auth.verify_password
def verify_password(username, password):
    logging.debug(f"Entering verify_password(), args={username}, {password}")

    if username is None or password is None:
        logging.error("Username or password is missing")
        return None

    user = User.query.filter_by(username=username).first()
    if user:
        hash_password = user.password

        if bcrypt.check_password_hash(hash_password, password):
            logging.debug("Exiting verify_password()")
            return username
    else:
        logging.error("Username or password is incorrect.")
        return None


@token_auth.verify_token
def verify_token(token):
    logging.debug(f"Entering verify_token(), args={token}")

    if token is None:
        logging.error("Token is missing")
        return None

    # Step 1: Decode token and then check the payload of the token
    username, browser_id = decode_auth_token(token)
    if username is None or browser_id is None:
        return None

    # Step 2: Check if the browser has been changed.
    bi = create_browser_id()
    if not constant_time_compare(bi, browser_id):
        logging.error("User environment is not matched with the token.")
        return None

    user = User.query.filter_by(username=username).first()
    if user is None:
        logging.error(f"The user {username} is not found")
        return None

    logging.debug("Exiting verify_token()")
    return user.username


def encode_auth_token(username):
    """
    Generates the Auth Token
    :return: string
    """
    try:
        payload = {
            'exp': datetime.utcnow() + timedelta(minutes=3, seconds=0),
            'iat': datetime.utcnow(),
            'browser_id': create_browser_id(),
            'username': username,
        }
        return jwt.encode(
            payload=payload,
            key=current_app.config.get("SECRET_KEY"),
            algorithm='HS256'
        )
    except Exception as e:
        return e


def decode_auth_token(auth_token):
    """
    Decodes the auth token
    :param auth_token:
    :return: integer|string
    """
    try:
        payload = jwt.decode(
            jwt=auth_token,
            key=current_app.config.get("SECRET_KEY"),
            algorithms=['HS256'],
        )

        return payload["username"], payload["browser_id"]
    except jwt.ExpiredSignatureError:
        logging.warning("Signature expired. Please log in again.")
        return None, None
    except jwt.InvalidTokenError:
        logging.warning("Invalid token. Please log in again.")
        return None, None


@app.route("/auth/", methods=["GET", "POST"], strict_slashes=False)
@multi_auth.login_required()
def login():
    logging.debug(request.headers)
    logging.debug(request.url)

    message = "Login successfully."
    return response_handler(message=message)


def response_handler(status=200, message=None):
    response_object = {
        'message': message
    }
    response = make_response(jsonify(response_object))

    username = multi_auth.current_user()
    if username is not None:
        response.headers['X-Auth-User'] = username

    token = None
    if basic_auth.is_compatible_auth(request.headers):
        token = encode_auth_token(username)
    elif token_auth.is_compatible_auth(request.headers):
        _, token = request.headers.get('Authorization', '').split(None, 1)

    if token is not None:
        response.headers['X-Token'] = token

    response.headers['X-Trace-ID'] = uuid.uuid4()

    logging.debug(response.headers)
    logging.debug(response.response)

    return response, status


def parse_args():
    description = "You should launch flask app with the following parameters!"
    parser = argparse.ArgumentParser(
        description=description)
    parser.add_argument(
        '--host',
        default=u"0.0.0.0",
        help="The address exposed by flask application")
    parser.add_argument(
        '--port',
        type=int,
        default=80,
        help="The port exposed by flask application")
    arguments = parser.parse_args()

    if arguments.host is None or arguments.port is None:
        parser.print_help()
        exit(1)

    return arguments


if __name__ == "__main__":
    args = parse_args()

    http_server = WSGIServer((args.host, args.port), app)
    http_server.serve_forever()
