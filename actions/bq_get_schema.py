import sys

import db
import constants

VALID_DOMAINS = [
    'tracks',
    'albums',
    'artists',
    'audio_features'
]


def bq_get_schema(argv):

    try:
        if not argv:
            raise Exception("No domain specified")

        domain = argv.pop(0)
        if domain not in VALID_DOMAINS:
            raise Exception("Invalid domain {}".format(domain))

    except Exception as err:
        print err
        print "Usage: four-digit.py [-s] bq_get_schema [{0}] ".format(' | '.join(VALID_DOMAINS))
        sys.exit(2)

    db.bq.connect_to_table_and_pickle_schema(
        '{}_sample'.format(domain),
        '{}/{}.schema'.format(constants.PATH_SCHEMA, domain))

    pass