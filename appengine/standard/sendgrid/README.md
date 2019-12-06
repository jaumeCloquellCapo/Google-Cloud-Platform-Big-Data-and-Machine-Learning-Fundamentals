# Sendgrid & Google App Engine

[![Open in Cloud Shell][shell_img]][shell_link]

[shell_img]: http://gstatic.com/cloudssh/images/open-btn.png
[shell_link]: https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GoogleCloudPlatform/python-docs-samples&page=editor&open_in_editor=appengine/standard/sendgrid/README.md

This sample application demonstrates how to use [Sendgrid with Google App Engine](https://cloud.google.com/appengine/docs/python/mail/sendgrid)

Refer to the [App Engine Samples README](../../README.md) for information on how to run and deploy this sample.

# Setup

Before running this sample:

1. You will need a [Sendgrid account](http://sendgrid.com/partner/google).
2. Update the `SENGRID_DOMAIN_NAME` and `SENGRID_API_KEY` constants in `main.py`. You can use 
the [Sendgrid sandbox domain](https://support.sendgrid.com/hc/en-us/articles/201995663-Safely-Test-Your-Sending-Speed).
