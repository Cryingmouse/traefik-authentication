import argparse
import logging
import uuid

from flask import current_app, make_response, request, jsonify
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth, MultiAuth
from itsdangerous import URLSafeSerializer, BadData

from app import create_app, bcrypt, cache
from dsm_auth.utils import create_browser_id, constant_time_compare
from models import User

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


# TODO:
# 1. the rotated log files.

@basic_auth.verify_password
def verify_password(username, password):
    logging.debug("Entering the function verify_password()")
    if username is None or password is None:
        logging.error("username or password is missing")
        return None

    user = User.query.filter_by(username=username).first()
    if user:
        hash_password = user.password

        if bcrypt.check_password_hash(hash_password, password):
            token = user.get_token()
            life_time = current_app.config.get("TOKEN_LIFETIME")
            cache.set(token, 1, timeout=life_time)

            logging.debug("Exiting the function verify_password()")
            return username
    else:
        logging.error("username or password is incorrect.")
        return None


# TODO: The alternative is just to check if the token is available in cache
#  (Only step 3). It would be faster for authentication.
@token_auth.verify_token
def verify_token(token):
    logging.debug("Entering the function verify_token()")

    if token is None:
        logging.error("token is missing")
        return None

    # Step 1: Check if the taken has been modified or not.
    # Parse the include_token from the client through the method loads()
    key = current_app.config.get("SECRET_KEY")
    try:
        s = URLSafeSerializer(key)
        user_id, username, password, browser_id, life_time = s.loads(token)
    except BadData:
        logging.error("token had been modified!")
        return None

    # Step 2: Check if the browser has been changed.
    bi = create_browser_id()
    if not constant_time_compare(str(bi), str(browser_id)):
        logging.error(
            "User environment had changed, so token has been expired!")
        return None

    user = User.query.filter_by(id=user_id).first()
    if user:
        # Step 3: Check if the include_token is still available
        token_cache = cache.get(token)
        if not token_cache:
            logging.error("token is not found in cache.")
            return None
        # Step 4: Check if the password in include_token is matched with the
        # one in database. If not, then delete the include_token in cache.
        if str(password) != str(user.password):
            logging.error("password in token is not matched!")
            cache.delete(token)
            return None
        else:
            cache.set(token, 1, timeout=life_time)
    else:
        logging.error('the user is not found')
        return None

    logging.debug("Exiting the function verify_token()")
    return user.username


@app.route("/auth/", methods=["GET", "POST"], strict_slashes=False)
@multi_auth.login_required()
def login():
    logging.debug(request.headers)
    logging.info(request.url)

    message = "Login successfully."
    return response_handler(message=message)


def get_token_by_current_user():
    username = multi_auth.current_user()
    user = User.query.filter_by(username=username).first()

    if user:
        return username, user.get_token()

    return username, None


def response_handler(status=200, message=None):
    username, token = get_token_by_current_user()

    response_object = {
        'message': message
    }
    response = make_response(jsonify(response_object))

    if token is not None:
        response.headers['X-Token'] = token
    if username is not None:
        response.headers['X-Auth-User'] = username

    response.headers['X-Trace-ID'] = str(uuid.uuid4())

    logging.debug(headers=response.headers)
    logging.info(response=response.response)

    return response, status


def parse_args():
    description = "You should launch flask app with the following parameters!"
    parser = argparse.ArgumentParser(
        description=description)
    parser.add_argument(
        '--host', help="The address exposed by flask application")
    parser.add_argument(
        '--port', help="The port exposed by flask application")
    arguments = parser.parse_args()

    if arguments.host is None or arguments.port is None:
        parser.print_help()
        exit(1)

    return arguments


if __name__ == "__main__":
    args = parse_args()

    app.run(host=args.host, port=args.port, debug=True)
