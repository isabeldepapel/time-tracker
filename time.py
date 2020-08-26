import os
import uuid
from datetime import datetime, timezone
from notion.client import NotionClient

TOKEN = os.getenv('TOKEN_V2')
URL = os.getenv('URL')
OPS = ['bh', 'deploy']
ENVS = ['integration', 'us', 'emea']

def get_table_view():
    client = NotionClient(token_v2=TOKEN)
    table_view = client.get_collection_view(URL)
    return table_view

def get_table(table_view=None):
    if not table_view:
        table_view = get_table_view()
    return table_view.collection

def record_start(op, env='integration'):
    formatted_op = op.lower()
    formatted_env = env.lower()

    if formatted_op not in OPS or formatted_env not in ENVS:
        print('invalid input')
        return

    start_time = datetime.now(timezone.utc)
    row_id = str(uuid.uuid4())

    table_view = get_table_view()
    # table is set up as id, env, op, start, end, (# builds?)
    row = table_view.collection.add_row()
    row.name = row_id
    row.env = formatted_env
    row.op = formatted_op
    row.start = start_time

    print(start_time)
    return row_id

def get_record(row_id):
    print(row_id)
    end_time = datetime.now(timezone.utc)
    table_view = get_table_view()

    filter_params = [{
        "property": "title",
        "comparator": "enum_is",
        "value": row_id
    }]
    print(filter_params)

    other_params = [{
        "property": "env",
        "comparator": "contains",
        "value": "emea"
    }]

    result = table_view.build_query(filter=other_params).execute()
    print(result)
    # for row in result:
    #     print('updating')
    #     print(row.name)
        # row.end = end_time

    return

# print(record_start('bh'))
TEST_UUID='24092952-4a77-42e2-a7c8-738bdf5864ca'
get_record(TEST_UUID)
