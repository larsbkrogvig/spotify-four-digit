import ConfigParser
from google.cloud import bigquery

PAGE_SIZE = 10


def read_bigquery_client_and_dataset():
    """Return the configured dataset and a connected bigquery client"""
    config = ConfigParser.ConfigParser()
    config.read('params')

    project_name = config.get('BIGQUERY', 'PROJECT_NAME')
    dataset_name = config.get('BIGQUERY', 'DATASET_NAME')

    bigquery_client = bigquery.Client(project_name)
    dataset = bigquery_client.dataset(dataset_name)

    return dataset, bigquery_client


def upload_to_table(file_name, table_name, schema):
    """Upload the contents of a file to a table. Auto-detection of schema isn't supported at the moment!"""

    dataset, _ = read_bigquery_client_and_dataset()
    table = dataset.table(table_name)
    table.schema = schema

    print "Uploading `{}` to table `{}`".format(file_name, table_name)
    with open(file_name, 'rb') as file_to_upload:
        table.upload_from_file(file_to_upload, 'NEWLINE_DELIMITED_JSON')


def get_album_ids(sample=False):
    """Get a list of album ids by querying a bigquery table of tracks"""

    dataset, bigquery_client = read_bigquery_client_and_dataset()

    query = bigquery_client.run_sync_query('''
    
        SELECT 
            DISTINCT album.id AS album_id
        FROM 
           `{}.tracks{}`
           
    '''.format(dataset.name, "_sample" if sample else ''))

    query.max_results = PAGE_SIZE
    query.use_legacy_sql = False

    query.run()

    for row in query.fetch_data():
        yield row[0]

    pass
