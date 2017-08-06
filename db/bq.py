import ConfigParser
import pickle
from google.cloud import bigquery

QUERY_PAGE_SIZE = 10


def get_bigquery_client_and_dataset():
    """Return the configured dataset and a connected bigquery client"""
    config = ConfigParser.ConfigParser()
    config.read('.params')

    project_name = config.get('BIGQUERY', 'PROJECT_NAME')
    dataset_name = config.get('BIGQUERY', 'DATASET_NAME')

    bigquery_client = bigquery.Client(project_name)
    dataset = bigquery_client.dataset(dataset_name)

    return dataset, bigquery_client


def upload_to_table(file_name, table_name, schema):
    """Upload the contents of a file to a table. Auto-detection of schema isn't supported at the moment!"""

    dataset, _ = get_bigquery_client_and_dataset()
    table = dataset.table(table_name)
    table.schema = schema

    print "Uploading `{}` to table `{}`".format(file_name, table_name)
    with open(file_name, 'rb') as file_to_upload:
        table.upload_from_file(
            file_to_upload,
            'NEWLINE_DELIMITED_JSON',
            max_bad_records=10
        )


def get_album_ids(sample=False):
    """Get a list of album ids by querying a bigquery table of tracks"""

    dataset, bigquery_client = get_bigquery_client_and_dataset()

    query = bigquery_client.run_sync_query('''
    
        SELECT 
            DISTINCT album.id AS album_id
        FROM 
           `{}.tracks{}`
           
    '''.format(dataset.name, "_sample" if sample else ''))

    query.max_results = QUERY_PAGE_SIZE
    query.use_legacy_sql = False

    query.run()

    for row in query.fetch_data():
        yield row[0]

    pass


def connect_to_table_and_pickle_schema(table_name, schema_file_name):
    """Connect to a bigquery table and pickle the schema (Workaround for no auto-detection of schema)"""

    dataset, _ = get_bigquery_client_and_dataset()
    table = dataset.table(table_name)
    table.reload()
    schema = table.schema

    with open(schema_file_name, 'wb') as schema_file:
        print "Saving schema to {}".format(schema_file_name)
        pickle.dump(schema, schema_file)

    pass