import sys

import db
import constants
import util

VALID_DOMAINS = [
    'albums',
]


def run(argv, sample):

    try:
        if not argv:
            raise Exception("No domain specified")

        domain = argv.pop(0)
        if domain not in VALID_DOMAINS:
            raise Exception("Invalid domain {}".format(domain))

    except Exception as err:
        print err
        print "Usage: four-digit.py [-s] bq_get_ids [{0}] ".format(' | '.join(VALID_DOMAINS))
        sys.exit(2)

    ids = None
    if domain == 'albums':
        ids = db.bq.get_album_ids(sample)

    util.write_to_file(
        ids,
        '{}/{}{}.txt'.format(constants.PATH_IDS, domain, '' if not sample else '_sample'),
        text=True
    )