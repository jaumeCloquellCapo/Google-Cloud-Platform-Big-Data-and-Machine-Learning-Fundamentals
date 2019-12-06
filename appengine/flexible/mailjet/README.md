# Python Mailjet email sample for Google App Engine Flexible

[![Open in Cloud Shell][shell_img]][shell_link]

[shell_img]: http://gstatic.com/cloudssh/images/open-btn.png
[shell_link]: https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=appengine/flexible/mailjet/README.md

This sample demonstrates how to use [Mailjet](https://www.mailjet.com) on [Google App Engine Flexible](https://cloud.google.com/appengine/docs/flexible/).

## Setup

Before you can run or deploy the sample, you will need to do the following:

1. [Create a Mailjet Account](http://www.mailjet.com/google).

2. Configure your Mailjet settings in the environment variables section in ``app.yaml``.

## Running locally

Refer to the [top-level README](../README.md) for instructions on running and deploying.

You can run the application locally and send emails from your local machine. You
will need to set environment variables before starting your application:

    $ export MAILJET_API_KEY=[your-mailjet-api-key]
    $ export MAILJET_API_SECRET=[your-mailjet-secret]
    $ export MAILJET_SENDER=[your-sender-address]
    $ python main.py
