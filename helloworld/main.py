import argparse
import logging

from flask import Flask, request, make_response, jsonify

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)-8s "
           "[%(filename)s:line %(lineno)s %(funcName)s()] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

app = Flask(__name__)


@app.route("/hello/", methods=["GET", "POST"], strict_slashes=False)
def hello():
    logging.debug(request.headers)
    logging.info(request.url)

    response_object = {
        'message': 'Hello World',
    }

    response = make_response(jsonify(response_object))
    response.headers["Token"] = request.headers["X-Token"]

    logging.debug(response.headers)
    logging.info(response.response)

    return response, 200


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
