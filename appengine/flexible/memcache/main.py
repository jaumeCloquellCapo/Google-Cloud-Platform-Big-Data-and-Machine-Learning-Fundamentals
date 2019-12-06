# Copyright 2015 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import os

from flask import Flask
import pylibmc

app = Flask(__name__)


# [START gae_flex_redislabs_memcache]
# Environment variables are defined in app.yaml.
MEMCACHE_SERVER = os.environ.get('MEMCACHE_SERVER', 'localhost:11211')
MEMCACHE_USERNAME = os.environ.get('MEMCACHE_USERNAME')
MEMCACHE_PASSWORD = os.environ.get('MEMCACHE_PASSWORD')

memcache_client = pylibmc.Client(
    [MEMCACHE_SERVER], binary=True,
    username=MEMCACHE_USERNAME, password=MEMCACHE_PASSWORD)
# [END gae_flex_redislabs_memcache]


@app.route('/')
def index():

    # Set initial value if necessary
    if not memcache_client.get('counter'):
        memcache_client.set('counter', 0)

    value = memcache_client.incr('counter', 1)

    return 'Value is {}'.format(value)


@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
