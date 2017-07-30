import sys
import os
import getopt
import ConfigParser
import time
import json
import pickle

from spotipy import util

import data_acquisition
import db

VALID_ARGUMENTS = [
    'get_tracks',
    'upload_tracks',
    'print_token'
]


def main(argv):
    action, sample = get_options_and_aruments(argv)

    if action == 'print_token':

        print get_token()

    if action == 'get_tracks':

        file_name = 'tracks{}.txt'.format('' if not sample else '_sample')

        token = get_token()
        uris = get_uris()

        tracks = data_acquisition.spotify_api.get_tracks(token, uris, sample=sample)
        write_to_file(tracks, file_name)

    if action == 'upload_tracks':

        file_name = 'tracks{}.txt'.format('' if not sample else '_sample')
        table_name = 'tracks{}'.format('' if not sample else '_sample')

        schema = load_schema_from_local_file('tracks')

        db.bq.upload_to_table(file_name, table_name, schema)

    pass


def load_schema_from_local_file(table_name):
    """Loads a manually created pickled schema file"""
    print "Loading schema for `{}` table from file".format(table_name)
    try:
        with open('db/schema/{}.pickle'.format(table_name)) as schema_file:
            schema = pickle.load(schema_file)
            return schema
    except Exception as err:
        print err, '\nUnable to load schema {}.pickle'.format(table_name)
        sys.exit(1)
    pass


def get_token(scope=None):
    """Return access token for the Spotify API with scope `scope`.
    Look for cached access token, get a new one if expired or unavailable"""

    config = ConfigParser.ConfigParser()
    config.read('params')
    username = config.get('SPOTIFY', 'USER_NAME')

    token = None

    try:
        with open(".cache-{0}".format(username)) as cached_token_file:
            cached_token_dict = json.load(cached_token_file)
            if cached_token_dict['scope'] != scope:
                raise Exception("Scope of cached token different from requested scope {0}".format(scope))
            if int(time.time()) < cached_token_dict['expires_at']:
                token = cached_token_dict['access_token']
            else:
                raise Exception("Expired token")
    except Exception as err:
        print err, "\nFetching new token"
        try:
            token = util.prompt_for_user_token(username=username, scope=None)
        except AttributeError:
            os.remove(".cache-{0}".format(username))
            token = util.prompt_for_user_token(username=username, scope=None)

    if not token:
        print "Warning: No token was found"

    return token


def get_uris():
    """Return a list of uris read from local file \"uris.txt\""""
    try:
        with open('playlist/uris.txt', 'r') as f:
            uris = [line.rstrip('\n').split(':')[2] for line in f.readlines()]
            return uris
    except Exception as err:
        print err
        sys.exit(1)


def get_options_and_aruments(argv):
    """Get options and arguments from user input, print usage help if invalid input"""

    try:
        opts, args = getopt.getopt(argv, 's', ['sample'])
        if not args:
            raise getopt.GetoptError('No argument given')
        if len(args) > 1:
            raise getopt.GetoptError('Only one argument allowed. Got: {}'.format(args))
        if args[0] not in VALID_ARGUMENTS:
            raise getopt.GetoptError('Unknown argument "{}"'.format(args[0]))
    except getopt.GetoptError as err:
        print err, '\nUsage: four-digit.py [{0}] [sample]'.format('|'.join(VALID_ARGUMENTS))
        sys.exit(2)

    action = args[0]

    sample = False
    for opt, arg in opts:
        if opt in ("-s", "--sample"):
            sample = True

    return action, sample


def write_to_file(objects, file_name):
    """Write the objects in `objects` as jsons to file `file_name`"""

    with open(file_name, 'w') as out_file:
        out_file.writelines([json.dumps(obj)+'\n' for obj in objects])
        print "Saved to {0}".format(file_name)

    pass


if __name__ == "__main__":
    main(sys.argv[1:])

