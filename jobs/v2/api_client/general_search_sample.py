#!/usr/bin/env python

# Copyright 2016 Google Inc. All Rights Reserved.
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

import time

# [START instantiate]
from googleapiclient.discovery import build

client_service = build('jobs', 'v2')
# [END instantiate]


# [START basic_keyword_search]
def basic_keyword_search(client_service, company_name, keyword):
    request_metadata = {
        'user_id': 'HashedUserId',
        'session_id': 'HashedSessionId',
        'domain': 'www.google.com'
    }
    job_query = {'query': keyword}
    if company_name is not None:
        job_query.update({'company_names': [company_name]})
    request = {
        'mode': 'JOB_SEARCH',
        'request_metadata': request_metadata,
        'query': job_query,
    }

    response = client_service.jobs().search(body=request).execute()
    print(response)
# [END basic_keyword_search]


# [START category_filter]
def category_search(client_service, company_name, categories):
    request_metadata = {
        'user_id': 'HashedUserId',
        'session_id': 'HashedSessionId',
        'domain': 'www.google.com'
    }
    job_query = {'categories': categories}
    if company_name is not None:
        job_query.update({'company_names': [company_name]})
    request = {
        'mode': 'JOB_SEARCH',
        'request_metadata': request_metadata,
        'query': job_query,
    }

    response = client_service.jobs().search(body=request).execute()
    print(response)
# [END category_filter]


# [START employment_types_filter]
def employment_types_search(client_service, company_name, employment_types):
    request_metadata = {
        'user_id': 'HashedUserId',
        'session_id': 'HashedSessionId',
        'domain': 'www.google.com'
    }
    job_query = {'employment_types': employment_types}
    if company_name is not None:
        job_query.update({'company_names': [company_name]})
    request = {
        'mode': 'JOB_SEARCH',
        'request_metadata': request_metadata,
        'query': job_query,
    }

    response = client_service.jobs().search(body=request).execute()
    print(response)
# [END employment_types_filter]


# [START date_range_filter]
def date_range_search(client_service, company_name, date_range):
    request_metadata = {
        'user_id': 'HashedUserId',
        'session_id': 'HashedSessionId',
        'domain': 'www.google.com'
    }
    job_query = {'publish_date_range': date_range}
    if company_name is not None:
        job_query.update({'company_names': [company_name]})
    request = {
        'mode': 'JOB_SEARCH',
        'request_metadata': request_metadata,
        'query': job_query,
    }

    response = client_service.jobs().search(body=request).execute()
    print(response)
# [END date_range_filter]


# [START language_code_filter]
def language_code_search(client_service, company_name, language_codes):
    request_metadata = {
        'user_id': 'HashedUserId',
        'session_id': 'HashedSessionId',
        'domain': 'www.google.com'
    }
    job_query = {'language_codes': language_codes}
    if company_name is not None:
        job_query.update({'company_names': [company_name]})
    request = {
        'mode': 'JOB_SEARCH',
        'request_metadata': request_metadata,
        'query': job_query,
    }

    response = client_service.jobs().search(body=request).execute()
    print(response)
# [END language_code_filter]


# [START company_display_name_filter]
def company_display_name_search(client_service, company_name,
                                company_display_names):
    request_metadata = {
        'user_id': 'HashedUserId',
        'session_id': 'HashedSessionId',
        'domain': 'www.google.com'
    }
    job_query = {'company_display_names': company_display_names}
    if company_name is not None:
        job_query.update({'company_names': [company_name]})
    request = {
        'mode': 'JOB_SEARCH',
        'request_metadata': request_metadata,
        'query': job_query,
    }

    response = client_service.jobs().search(body=request).execute()
    print(response)
# [END company_display_name_filter]


# [START compensation_filter]
def compensation_search(client_service, company_name):
    request_metadata = {
        'user_id': 'HashedUserId',
        'session_id': 'HashedSessionId',
        'domain': 'www.google.com'
    }
    compensation_range = {
        'max': {
            'currency_code': 'USD',
            'units': 15
        },
        'min': {
            'currency_code': 'USD',
            'units': 10,
            'nanos': 500000000
        }
    }
    compensation_filter = {
        'type': 'UNIT_AND_AMOUNT',
        'units': ['HOURLY'],
        'range': compensation_range
    }
    job_query = {'compensation_filter': compensation_filter}
    if company_name is not None:
        job_query.update({'company_names': [company_name]})
    request = {
        'mode': 'JOB_SEARCH',
        'request_metadata': request_metadata,
        'query': job_query,
    }

    response = client_service.jobs().search(body=request).execute()
    print(response)
# [END compensation_filter]


def run_sample():
    import base_company_sample
    import base_job_sample

    company_to_be_created = base_company_sample.generate_company()
    company_to_be_created.update({'display_name': 'Google'})
    company_created = base_company_sample.create_company(
        client_service, company_to_be_created)
    company_name = company_created.get('name')

    job_to_be_created = base_job_sample.generate_job_with_required_fields(
        company_name)
    amount = {'currency_code': 'USD', 'units': 12}
    compensation_info = {
        'entries': [{
            'type': 'BASE',
            'unit': 'HOURLY',
            'amount': amount
        }]
    }
    job_to_be_created.update({
        'job_title': 'Systems Administrator',
        'employment_types': 'FULL_TIME',
        'language_code': 'en-US',
        'compensation_info': compensation_info
    })
    job_name = base_job_sample.create_job(client_service,
                                          job_to_be_created).get('name')

    # Wait several seconds for post processing
    time.sleep(10)
    basic_keyword_search(client_service, company_name, 'Systems Administrator')
    category_search(client_service, company_name, ['COMPUTER_AND_IT'])
    date_range_search(client_service, company_name, 'PAST_24_HOURS')
    employment_types_search(client_service, company_name,
                            ['FULL_TIME', 'CONTRACTOR', 'PER_DIEM'])
    company_display_name_search(client_service, company_name, ['Google'])
    compensation_search(client_service, company_name)
    language_code_search(client_service, company_name, ['pt-BR', 'en-US'])

    base_job_sample.delete_job(client_service, job_name)
    base_company_sample.delete_company(client_service, company_name)


if __name__ == '__main__':
    run_sample()
