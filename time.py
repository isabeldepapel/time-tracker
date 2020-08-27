import os
import sys
from notion.client import NotionClient

TOKEN = os.getenv('TOKEN_V2')
URL = os.getenv('URL')

def generate_var_prefix(op, env):
    '''Environment variable names are of the type <env>_<op>_<kind>. Generates
    the first part of the name using the given op and env.'''
    return f'{env.upper()}_{op.upper()}'

def get_timestamp_in_milliseconds(microseconds_as_string):
    return int(microseconds_as_string) / 1000

def get_table_view():
    client = NotionClient(token_v2=TOKEN)
    table_view = client.get_collection_view(URL)
    return table_view

def write_data(op, env, num_builds=None):
    '''Write data to table. Table is set up as name (env), op, start_ms, end_ms'''
    var_prefix = generate_var_prefix(op, env)
    start_env_var = f'{var_prefix}_START'
    end_env_var = f'{var_prefix}_END'

    start_time_in_microseconds = os.getenv(f'{var_prefix}_START')
    end_time_in_microseconds = os.getenv(f'{var_prefix}_END')

    try:
        start_time = get_timestamp_in_milliseconds(start_time_in_microseconds)
        end_time = get_timestamp_in_milliseconds(end_time_in_microseconds)

    except TypeError:
        print(
            'Missing required env var, aborting',
            f'start: {start_time_in_microseconds}',
            f'end: {end_time_in_microseconds}',
            sep='\n'
        )
        return

    else:
        print('Writing data')
        table_view = get_table_view()
        row = table_view.collection.add_row()
        row.name = env.lower()
        row.op = op.lower()
        row.start_ms = start_time
        row.end_ms = end_time
        if num_builds:
            row.num_builds = int(num_builds)
        return

if __name__ == '__main__':
    op, env, num_builds = sys.argv[1:]
    write_data(op, env, num_builds)
