import requests
import threading
import time

from flask_restplus import Resource
from flask import request

import rest_api.general_application as rest

testURL = "0.0.0.0"
testPort = 6969


def start_rest():
    @rest.api.route('/hello')
    class HelloWorld(Resource):
        def get(self):
            return {'hello': 'world'}

    @rest.api.route('/shutdown')
    class Shutdown(Resource):
        def get(self):
            func = request.environ.get('werkzeug.server.shutdown')

            if func is None:
                raise RuntimeError('Not running with the Werkzeug Server')

            func()
    rest.app.run(host=testURL, port=testPort, debug=False)


def test_rest_server():
    t = threading.Thread(target=start_rest)

    t.start()

    # Hacky solution to ensure it only tries to connect 10 times
    number_of_tries = 0
    while number_of_tries < 10:
        try:
            r = requests.get(
                "http://" + testURL + ":" + str(testPort) + "/hello")
            requests.get(
                "http://" + testURL + ":" + str(testPort) + "/shutdown")
            break
        except requests.exceptions.ConnectionError:
            number_of_tries += 1
            time.sleep(0.5)

    assert(r.json is not None)
