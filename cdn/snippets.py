#!/usr/bin/env python
#
# Copyright 2017 Google, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This application demonstrates how to perform operations on data (content)
when using Google Cloud CDN (Content Delivery Network).

For more information, see the README.md under /cdn and the documentation
at https://cloud.google.com/cdn/docs.
"""

import argparse
import base64
import datetime
import hashlib
import hmac

from six.moves import urllib


# [START sign_url]
def sign_url(url, key_name, base64_key, expiration_time):
    """Gets the Signed URL string for the specified URL and configuration.

    Args:
        url: URL to sign as a string.
        key_name: name of the signing key as a string.
        base64_key: signing key as a base64 encoded string.
        expiration_time: expiration time as a UTC datetime object.

    Returns:
        Returns the Signed URL appended with the query parameters based on the
        specified configuration.
    """
    stripped_url = url.strip()
    parsed_url = urllib.parse.urlsplit(stripped_url)
    query_params = urllib.parse.parse_qs(
        parsed_url.query, keep_blank_values=True)
    epoch = datetime.datetime.utcfromtimestamp(0)
    expiration_timestamp = int((expiration_time - epoch).total_seconds())
    decoded_key = base64.urlsafe_b64decode(base64_key)

    url_pattern = u'{url}{separator}Expires={expires}&KeyName={key_name}'

    url_to_sign = url_pattern.format(
            url=stripped_url,
            separator='&' if query_params else '?',
            expires=expiration_timestamp,
            key_name=key_name)

    digest = hmac.new(
        decoded_key, url_to_sign.encode('utf-8'), hashlib.sha1).digest()
    signature = base64.urlsafe_b64encode(digest).decode('utf-8')

    signed_url = u'{url}&Signature={signature}'.format(
            url=url_to_sign, signature=signature)

    print(signed_url)
# [END sign_url]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
            description=__doc__,
            formatter_class=argparse.RawDescriptionHelpFormatter)

    subparsers = parser.add_subparsers(dest='command')

    sign_url_parser = subparsers.add_parser(
            'sign-url',
            help="Sign a URL to grant temporary authorized access.")
    sign_url_parser.add_argument(
            'url', help='The URL to sign.')
    sign_url_parser.add_argument(
            'key_name',
            help='Key name for the signing key.')
    sign_url_parser.add_argument(
            'base64_key',
            help='The base64 encoded signing key.')
    sign_url_parser.add_argument(
            'expiration_time',
            type=lambda d: datetime.datetime.utcfromtimestamp(float(d)),
            help='Expiration time expessed as seconds since the epoch.')

    args = parser.parse_args()

    if args.command == 'sign-url':
        sign_url(
            args.url, args.key_name, args.base64_key, args.expiration_time)
