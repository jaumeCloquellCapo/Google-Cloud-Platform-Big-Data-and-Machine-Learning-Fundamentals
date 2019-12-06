#!/usr/bin/env python

# Copyright 2016 Google Inc.
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

# [START sendgrid-imp]
import sendgrid
from sendgrid.helpers.mail import Mail
# [END sendgrid-imp]
import webapp2

# make a secure connection to SendGrid
# [START sendgrid-config]
SENDGRID_API_KEY = 'your-sendgrid-api-key'
SENDGRID_SENDER = 'your-sendgrid-sender'
# [END sendgrid-config]


def send_simple_message(recipient):
    # [START sendgrid-send]
    message = Mail(
        from_email=SENDGRID_SENDER,
        to_emails='{},'.format(recipient),
        subject='This is a test email',
        html_content='<strong>Example</strong> message.')

    sg = sendgrid.SendGridAPIClient(SENDGRID_API_KEY)
    response = sg.send(message)

    return response
    # [END sendgrid-send]


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.content_type = 'text/html'
        self.response.write("""
<!doctype html>
<html><body>
<form action="/send" method="POST">
<input type="text" name="recipient" placeholder="Enter recipient email">
<input type="submit" name="submit" value="Send simple email">
</form>
</body></html>
""")


class SendEmailHandler(webapp2.RequestHandler):
    def post(self):
        recipient = self.request.get('recipient')
        sg_response = send_simple_message(recipient)
        self.response.set_status(sg_response.status_code)
        self.response.write(sg_response.body)


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/send', SendEmailHandler)
], debug=True)
