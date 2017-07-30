import ConfigParser
from google.cloud import bigquery


def upload_to_table(file_name, table_name, schema):
    """Upload the contents of a file to a table. Auto-detection of schema isn't supported at the moment!"""

    config = ConfigParser.ConfigParser()
    config.read('params')

    project_name = config.get('BIGQUERY', 'PROJECT_NAME')
    dataset_name = config.get('BIGQUERY', 'DATASET_NAME')

    bigquery_client = bigquery.Client(project_name)
    dataset = bigquery_client.dataset(dataset_name)
    table = dataset.table(table_name)
    table.schema = schema

    print "Uploading {} to table {}:{}.{}".format(file_name, project_name, dataset_name, table_name)
    with open(file_name, 'rb') as file_to_upload:
        table.upload_from_file(file_to_upload, 'NEWLINE_DELIMITED_JSON')
