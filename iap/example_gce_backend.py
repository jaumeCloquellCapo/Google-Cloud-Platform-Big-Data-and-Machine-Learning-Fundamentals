# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import platform

import flask

import validate_jwt

CLOUD_PROJECT_ID = 'YOUR_PROJECT_ID'
BACKEND_SERVICE_ID = 'YOUR_BACKEND_SERVICE_ID'

app = flask.Flask(__name__)


@app.route('/')
def root():
    jwt = flask.request.headers.get('x-goog-iap-jwt-assertion')
    if jwt is None:
        return 'Unauthorized request.'
    user_id, user_email, error_str = (
        validate_jwt.validate_iap_jwt_from_compute_engine(
            jwt, CLOUD_PROJECT_ID, BACKEND_SERVICE_ID))
    if error_str:
        return 'Error: {}'.format(error_str)
    else:
        return 'Hi, {}. I am {}.'.format(user_email, platform.node())


if __name__ == '__main__':
    app.run()
