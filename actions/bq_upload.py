import sys
import pickle

import db
import constants

VALID_DOMAINS = [
    'tracks',
    'albums',
    'artists',
    'audio_features',
]


def bq_upload(argv, sample):

    try:
        if not argv:
            raise Exception("No domain specified")

        domain = argv.pop(0)
        if domain not in VALID_DOMAINS:
            raise Exception("Invalid domain {}".format(domain))

    except Exception as err:
        print err
        print "Usage: four-digit.py [-s] bq_upload [{0}] ".format(' | '.join(VALID_DOMAINS))
        sys.exit(2)

    file_name = '{}/{}{}.txt'.format(constants.PATH_OBJECTS, domain, '' if not sample else '_sample')
    table_name = '{}{}'.format(domain, '' if not sample else '_sample')
    schema = _load_schema_from_local_file('{}/{}.schema'.format(constants.PATH_SCHEMA, domain))

    db.bq_upload_to_table(file_name, table_name, schema)

    pass


def _load_schema_from_local_file(file_name):
    """Loads a manually created pickled schema file"""
    print "Loading schema from file '{}'".format(file_name)
    try:
        with open(file_name) as schema_file:
            schema = pickle.load(schema_file)
            return schema
    except Exception as err:
        print err, "\nUnable to load schema from file '{}'".format(file_name)
        sys.exit(1)
    pass
