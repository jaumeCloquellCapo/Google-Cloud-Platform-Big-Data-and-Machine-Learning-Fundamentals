# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import flask
import pytest
import requests
import responses

import main


# Create a fake "app" for generating test request contexts.
@pytest.fixture(scope="module")
def app():
    return flask.Flask(__name__)


def test_statelessness(app):
    with app.test_request_context():
        res = main.statelessness(flask.request)
        assert res == 'Instance execution count: 1'
        res = main.statelessness(flask.request)
        assert res == 'Instance execution count: 2'


def test_scope_demo(app):
    with app.test_request_context():
        main.scope_demo(flask.request)


@responses.activate
def test_make_request_200(app):
    responses.add(responses.GET, 'http://example.com',
                  json={'status': 'OK'}, status=200)
    with app.test_request_context():
        main.make_request(flask.request)


@responses.activate
def test_make_request_404(app):
    responses.add(responses.GET, 'http://example.com',
                  json={'error': 'not found'}, status=404)
    with app.test_request_context():
        with pytest.raises(requests.exceptions.HTTPError):
            main.make_request(flask.request)


def test_list_files(app):
    with app.test_request_context():
        res = main.list_files(flask.request)
        assert 'main.py' in res
