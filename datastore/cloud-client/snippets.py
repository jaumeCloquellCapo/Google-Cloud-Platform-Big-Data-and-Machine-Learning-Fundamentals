# Copyright 2016, Google, Inc.
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

import argparse
from collections import defaultdict
import datetime
from pprint import pprint

from google.cloud import datastore
import google.cloud.exceptions


def incomplete_key(client):
    # [START datastore_incomplete_key]
    key = client.key('Task')
    # [END datastore_incomplete_key]

    return key


def named_key(client):
    # [START datastore_named_key]
    key = client.key('Task', 'sample_task')
    # [END datastore_named_key]

    return key


def key_with_parent(client):
    # [START datastore_key_with_parent]
    key = client.key('TaskList', 'default', 'Task', 'sample_task')
    # Alternatively
    parent_key = client.key('TaskList', 'default')
    key = client.key('Task', 'sample_task', parent=parent_key)
    # [END datastore_key_with_parent]

    return key


def key_with_multilevel_parent(client):
    # [START datastore_key_with_multilevel_parent]
    key = client.key(
        'User', 'alice',
        'TaskList', 'default',
        'Task', 'sample_task')
    # [END datastore_key_with_multilevel_parent]

    return key


def basic_entity(client):
    # [START datastore_basic_entity]
    task = datastore.Entity(client.key('Task'))
    task.update({
        'category': 'Personal',
        'done': False,
        'priority': 4,
        'description': 'Learn Cloud Datastore'
    })
    # [END datastore_basic_entity]

    return task


def entity_with_parent(client):
    # [START datastore_entity_with_parent]
    key_with_parent = client.key(
        'TaskList', 'default', 'Task', 'sample_task')

    task = datastore.Entity(key=key_with_parent)

    task.update({
        'category': 'Personal',
        'done': False,
        'priority': 4,
        'description': 'Learn Cloud Datastore'
    })
    # [END datastore_entity_with_parent]

    return task


def properties(client):
    key = client.key('Task')
    # [START datastore_properties]
    task = datastore.Entity(
        key,
        exclude_from_indexes=['description'])
    task.update({
        'category': 'Personal',
        'description': 'Learn Cloud Datastore',
        'created': datetime.datetime.utcnow(),
        'done': False,
        'priority': 4,
        'percent_complete': 10.5,
    })
    # [END datastore_properties]

    return task


def array_value(client):
    key = client.key('Task')
    # [START datastore_array_value]
    task = datastore.Entity(key)
    task.update({
        'tags': [
            'fun',
            'programming'
        ],
        'collaborators': [
            'alice',
            'bob'
        ]
    })
    # [END datastore_array_value]

    return task


def upsert(client):
    # [START datastore_upsert]
    complete_key = client.key('Task', 'sample_task')

    task = datastore.Entity(key=complete_key)

    task.update({
        'category': 'Personal',
        'done': False,
        'priority': 4,
        'description': 'Learn Cloud Datastore'
    })

    client.put(task)
    # [END datastore_upsert]

    return task


def insert(client):
    # [START datastore_insert]
    with client.transaction():
        incomplete_key = client.key('Task')

        task = datastore.Entity(key=incomplete_key)

        task.update({
            'category': 'Personal',
            'done': False,
            'priority': 4,
            'description': 'Learn Cloud Datastore'
        })

        client.put(task)
    # [END datastore_insert]

    return task


def update(client):
    # Create the entity we're going to update.
    upsert(client)

    # [START datastore_update]
    with client.transaction():
        key = client.key('Task', 'sample_task')
        task = client.get(key)

        task['done'] = True

        client.put(task)
    # [END datastore_update]

    return task


def lookup(client):
    # Create the entity that we're going to look up.
    upsert(client)

    # [START datastore_lookup]
    key = client.key('Task', 'sample_task')
    task = client.get(key)
    # [END datastore_lookup]

    return task


def delete(client):
    # Create the entity we're going to delete.
    upsert(client)

    # [START datastore_delete]
    key = client.key('Task', 'sample_task')
    client.delete(key)
    # [END datastore_delete]

    return key


def batch_upsert(client):
    # [START datastore_batch_upsert]
    task1 = datastore.Entity(client.key('Task', 1))

    task1.update({
        'category': 'Personal',
        'done': False,
        'priority': 4,
        'description': 'Learn Cloud Datastore'
    })

    task2 = datastore.Entity(client.key('Task', 2))

    task2.update({
        'category': 'Work',
        'done': False,
        'priority': 8,
        'description': 'Integrate Cloud Datastore'
    })

    client.put_multi([task1, task2])
    # [END datastore_batch_upsert]

    return task1, task2


def batch_lookup(client):
    # Create the entities we will lookup.
    batch_upsert(client)

    keys = [
        client.key('Task', 1),
        client.key('Task', 2)
    ]

    # [START datastore_batch_lookup]
    tasks = client.get_multi(keys)
    # [END datastore_batch_lookup]

    return tasks


def batch_delete(client):
    # Create the entities we will delete.
    batch_upsert(client)

    keys = [
        client.key('Task', 1),
        client.key('Task', 2)
    ]

    # [START datastore_batch_delete]
    client.delete_multi(keys)
    # [END datastore_batch_delete]

    return keys


def unindexed_property_query(client):
    # Create the entity that we're going to query.
    upsert(client)

    # [START datastore_unindexed_property_query]
    query = client.query(kind='Task')
    query.add_filter('description', '=', 'Learn Cloud Datastore')
    # [END datastore_unindexed_property_query]

    return list(query.fetch())


def basic_query(client):
    # Create the entity that we're going to query.
    upsert(client)

    # [START datastore_basic_query]
    query = client.query(kind='Task')
    query.add_filter('done', '=', False)
    query.add_filter('priority', '>=', 4)
    query.order = ['-priority']
    # [END datastore_basic_query]

    return list(query.fetch())


def projection_query(client):
    # Create the entity that we're going to query.
    task = datastore.Entity(client.key('Task'))
    task.update({
        'category': 'Personal',
        'done': False,
        'priority': 4,
        'description': 'Learn Cloud Datastore',
        'percent_complete': 0.5
    })
    client.put(task)

    # [START datastore_projection_query]
    query = client.query(kind='Task')
    query.projection = ['priority', 'percent_complete']
    # [END datastore_projection_query]

    # [START datastore_run_query_projection]
    priorities = []
    percent_completes = []

    for task in query.fetch():
        priorities.append(task['priority'])
        percent_completes.append(task['percent_complete'])
    # [END datastore_run_query_projection]

    return priorities, percent_completes


def ancestor_query(client):
    task = datastore.Entity(
        client.key('TaskList', 'default', 'Task'))
    task.update({
        'category': 'Personal',
        'description': 'Learn Cloud Datastore',
    })
    client.put(task)

    # [START datastore_ancestor_query]
    # Query filters are omitted in this example as any ancestor queries with a
    # non-key filter require a composite index.
    ancestor = client.key('TaskList', 'default')
    query = client.query(kind='Task', ancestor=ancestor)
    # [END datastore_ancestor_query]

    return list(query.fetch())


def run_query(client):
    # [START datastore_run_query]
    query = client.query()
    results = list(query.fetch())
    # [END datastore_run_query]

    return results


def limit(client):
    # [START datastore_limit]
    query = client.query()
    tasks = list(query.fetch(limit=5))
    # [END datastore_limit]

    return tasks


def cursor_paging(client):
    # [START datastore_cursor_paging]

    def get_one_page_of_tasks(cursor=None):
        query = client.query(kind='Task')
        query_iter = query.fetch(start_cursor=cursor, limit=5)
        page = next(query_iter.pages)

        tasks = list(page)
        next_cursor = query_iter.next_page_token

        return tasks, next_cursor
    # [END datastore_cursor_paging]

    page_one, cursor_one = get_one_page_of_tasks()
    page_two, cursor_two = get_one_page_of_tasks(cursor=cursor_one)
    return page_one, cursor_one, page_two, cursor_two


def property_filter(client):
    # Create the entity that we're going to query.
    upsert(client)

    # [START datastore_property_filter]
    query = client.query(kind='Task')
    query.add_filter('done', '=', False)
    # [END datastore_property_filter]

    return list(query.fetch())


def composite_filter(client):
    # Create the entity that we're going to query.
    upsert(client)

    # [START datastore_composite_filter]
    query = client.query(kind='Task')
    query.add_filter('done', '=', False)
    query.add_filter('priority', '=', 4)
    # [END datastore_composite_filter]

    return list(query.fetch())


def key_filter(client):
    # Create the entity that we're going to query.
    upsert(client)

    # [START datastore_key_filter]
    query = client.query(kind='Task')
    first_key = client.key('Task', 'first_task')
    # key_filter(key, op) translates to add_filter('__key__', op, key).
    query.key_filter(first_key, '>')
    # [END datastore_key_filter]

    return list(query.fetch())


def ascending_sort(client):
    # Create the entity that we're going to query.
    task = upsert(client)
    task['created'] = datetime.datetime.utcnow()
    client.put(task)

    # [START datastore_ascending_sort]
    query = client.query(kind='Task')
    query.order = ['created']
    # [END datastore_ascending_sort]

    return list(query.fetch())


def descending_sort(client):
    # Create the entity that we're going to query.
    task = upsert(client)
    task['created'] = datetime.datetime.utcnow()
    client.put(task)

    # [START datastore_descending_sort]
    query = client.query(kind='Task')
    query.order = ['-created']
    # [END datastore_descending_sort]

    return list(query.fetch())


def multi_sort(client):
    # Create the entity that we're going to query.
    task = upsert(client)
    task['created'] = datetime.datetime.utcnow()
    client.put(task)

    # [START datastore_multi_sort]
    query = client.query(kind='Task')
    query.order = [
        '-priority',
        'created'
    ]
    # [END datastore_multi_sort]

    return list(query.fetch())


def keys_only_query(client):
    # Create the entity that we're going to query.
    upsert(client)

    # [START datastore_keys_only_query]
    query = client.query()
    query.keys_only()
    # [END datastore_keys_only_query]

    keys = list([entity.key for entity in query.fetch(limit=10)])

    return keys


def distinct_on_query(client):
    # Create the entity that we're going to query.
    upsert(client)

    # [START datastore_distinct_on_query]
    query = client.query(kind='Task')
    query.distinct_on = ['category']
    query.order = ['category', 'priority']
    # [END datastore_distinct_on_query]

    return list(query.fetch())


def kindless_query(client):
    # Create the entity that we're going to query.
    upsert(client)

    last_seen_key = client.key('Task', 'a')

    # [START datastore_kindless_query]
    query = client.query()
    query.key_filter(last_seen_key, '>')
    # [END datastore_kindless_query]

    return list(query.fetch())


def inequality_range(client):
    # [START datastore_inequality_range]
    start_date = datetime.datetime(1990, 1, 1)
    end_date = datetime.datetime(2000, 1, 1)
    query = client.query(kind='Task')
    query.add_filter(
        'created', '>', start_date)
    query.add_filter(
        'created', '<', end_date)
    # [END datastore_inequality_range]

    return list(query.fetch())


def inequality_invalid(client):
    try:
        # [START datastore_inequality_invalid]
        start_date = datetime.datetime(1990, 1, 1)
        query = client.query(kind='Task')
        query.add_filter(
            'created', '>', start_date)
        query.add_filter(
            'priority', '>', 3)
        # [END datastore_inequality_invalid]

        return list(query.fetch())

    except (google.cloud.exceptions.BadRequest,
            google.cloud.exceptions.GrpcRendezvous):
        pass


def equal_and_inequality_range(client):
    # [START datastore_equal_and_inequality_range]
    start_date = datetime.datetime(1990, 1, 1)
    end_date = datetime.datetime(2000, 12, 31, 23, 59, 59)
    query = client.query(kind='Task')
    query.add_filter('priority', '=', 4)
    query.add_filter('done', '=', False)
    query.add_filter(
        'created', '>', start_date)
    query.add_filter(
        'created', '<', end_date)
    # [END datastore_equal_and_inequality_range]

    return list(query.fetch())


def inequality_sort(client):
    # [START datastore_inequality_sort]
    query = client.query(kind='Task')
    query.add_filter('priority', '>', 3)
    query.order = ['priority', 'created']
    # [END datastore_inequality_sort]

    return list(query.fetch())


def inequality_sort_invalid_not_same(client):
    try:
        # [START datastore_inequality_sort_invalid_not_same]
        query = client.query(kind='Task')
        query.add_filter('priority', '>', 3)
        query.order = ['created']
        # [END datastore_inequality_sort_invalid_not_same]

        return list(query.fetch())

    except (google.cloud.exceptions.BadRequest,
            google.cloud.exceptions.GrpcRendezvous):
        pass


def inequality_sort_invalid_not_first(client):
    try:
        # [START datastore_inequality_sort_invalid_not_first]
        query = client.query(kind='Task')
        query.add_filter('priority', '>', 3)
        query.order = ['created', 'priority']
        # [END datastore_inequality_sort_invalid_not_first]

        return list(query.fetch())

    except (google.cloud.exceptions.BadRequest,
            google.cloud.exceptions.GrpcRendezvous):
        pass


def array_value_inequality_range(client):
    # [START datastore_array_value_inequality_range]
    query = client.query(kind='Task')
    query.add_filter('tag', '>', 'learn')
    query.add_filter('tag', '<', 'math')
    # [END datastore_array_value_inequality_range]

    return list(query.fetch())


def array_value_equality(client):
    # [START datastore_array_value_equality]
    query = client.query(kind='Task')
    query.add_filter('tag', '=', 'fun')
    query.add_filter('tag', '=', 'programming')
    # [END datastore_array_value_equality]

    return list(query.fetch())


def exploding_properties(client):
    # [START datastore_exploding_properties]
    task = datastore.Entity(client.key('Task'))
    task.update({
        'tags': [
            'fun',
            'programming',
            'learn'
        ],
        'collaborators': [
            'alice',
            'bob',
            'charlie'
        ],
        'created': datetime.datetime.utcnow()
    })
    # [END datastore_exploding_properties]

    return task


def transactional_update(client):
    # Create the entities we're going to manipulate
    account1 = datastore.Entity(client.key('Account'))
    account1['balance'] = 100
    account2 = datastore.Entity(client.key('Account'))
    account2['balance'] = 100
    client.put_multi([account1, account2])

    # [START datastore_transactional_update]
    def transfer_funds(client, from_key, to_key, amount):
        with client.transaction():
            from_account = client.get(from_key)
            to_account = client.get(to_key)

            from_account['balance'] -= amount
            to_account['balance'] += amount

            client.put_multi([from_account, to_account])
    # [END datastore_transactional_update]

    # [START datastore_transactional_retry]
    for _ in range(5):
        try:
            transfer_funds(client, account1.key, account2.key, 50)
            break
        except google.cloud.exceptions.Conflict:
            continue
    else:
        print('Transaction failed.')
    # [END datastore_transactional_retry]

    return account1.key, account2.key


def transactional_get_or_create(client):
    # [START datastore_transactional_get_or_create]
    with client.transaction():
        key = client.key('Task', datetime.datetime.utcnow().isoformat())

        task = client.get(key)

        if not task:
            task = datastore.Entity(key)
            task.update({
                'description': 'Example task'
            })
            client.put(task)

        return task
    # [END datastore_transactional_get_or_create]


def transactional_single_entity_group_read_only(client):
    client.put_multi([
        datastore.Entity(key=client.key('TaskList', 'default')),
        datastore.Entity(key=client.key('TaskList', 'default', 'Task', 1))
    ])

    # [START datastore_transactional_single_entity_group_read_only]
    with client.transaction(read_only=True):
        task_list_key = client.key('TaskList', 'default')

        task_list = client.get(task_list_key)

        query = client.query(kind='Task', ancestor=task_list_key)
        tasks_in_list = list(query.fetch())

        return task_list, tasks_in_list
    # [END datastore_transactional_single_entity_group_read_only]


def namespace_run_query(client):
    # Create an entity in another namespace.
    task = datastore.Entity(
        client.key('Task', 'sample-task', namespace='google'))
    client.put(task)

    # [START datastore_namespace_run_query]
    # All namespaces
    query = client.query(kind='__namespace__')
    query.keys_only()

    all_namespaces = [entity.key.id_or_name for entity in query.fetch()]

    # Filtered namespaces
    start_namespace = client.key('__namespace__', 'g')
    end_namespace = client.key('__namespace__', 'h')
    query = client.query(kind='__namespace__')
    query.key_filter(start_namespace, '>=')
    query.key_filter(end_namespace, '<')

    filtered_namespaces = [entity.key.id_or_name for entity in query.fetch()]
    # [END datastore_namespace_run_query]

    return all_namespaces, filtered_namespaces


def kind_run_query(client):
    # Create the entity that we're going to query.
    upsert(client)

    # [START datastore_kind_run_query]
    query = client.query(kind='__kind__')
    query.keys_only()

    kinds = [entity.key.id_or_name for entity in query.fetch()]
    # [END datastore_kind_run_query]

    return kinds


def property_run_query(client):
    # Create the entity that we're going to query.
    upsert(client)

    # [START datastore_property_run_query]
    query = client.query(kind='__property__')
    query.keys_only()

    properties_by_kind = defaultdict(list)

    for entity in query.fetch():
        kind = entity.key.parent.name
        property_ = entity.key.name

        properties_by_kind[kind].append(property_)
    # [END datastore_property_run_query]

    return properties_by_kind


def property_by_kind_run_query(client):
    # Create the entity that we're going to query.
    upsert(client)

    # [START datastore_property_by_kind_run_query]
    ancestor = client.key('__kind__', 'Task')
    query = client.query(kind='__property__', ancestor=ancestor)

    representations_by_property = {}

    for entity in query.fetch():
        property_name = entity.key.name
        property_types = entity['property_representation']

        representations_by_property[property_name] = property_types
    # [END datastore_property_by_kind_run_query]

    return representations_by_property


def eventual_consistent_query(client):
    # [START datastore_eventual_consistent_query]
    # Read consistency cannot be specified in google-cloud-python.
    # [END datastore_eventual_consistent_query]
    pass


def main(project_id):
    client = datastore.Client(project_id)

    for name, function in globals().iteritems():
        if name in ('main', 'defaultdict') or not callable(function):
            continue

        print(name)
        pprint(function(client))
        print('\n-----------------\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Demonstrates datastore API operations.')
    parser.add_argument('project_id', help='Your cloud project ID.')

    args = parser.parse_args()

    main(args.project_id)
