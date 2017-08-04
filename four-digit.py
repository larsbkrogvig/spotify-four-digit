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

VALID_ACTIONS = [
    'get',
    'get_schema',
    'upload',
    'query_ids'
]

VALID_DOMAINS = [
    'tracks',
    'albums',
    'artists',
    'audio_features'
]

VALID_ARGUMENTS = [
    'get_tracks',
    'upload_tracks',
    'get_schema_tracks',
    'query_album_ids',
    'get_albums',
    'get_schema_albums',
    'upload_albums',
    'print_token'
]

PATH_DOWNLOAD = 'data_acquisition/downloaded'
PATH_SCHEMA = 'db/schema'


def main(argv):
    action, sample = get_options_and_aruments(argv)

    if action == 'print_token':
        print get_token()

    if action == 'get_tracks':
        file_name = 'tracks{}.txt'.format('' if not sample else '_sample')
        token = get_token()
        ids = load_ids_from_file('playlist/uris.txt')

        tracks = data_acquisition.spotify_api.get_tracks(token, ids, sample=sample)
        write_to_file(tracks, file_name)

    if action == 'get_schema_tracks':

        db.bq.connect_to_table_and_pickle_schema('tracks_sample', '{}/tracks.schema'.format(PATH_SCHEMA))

    if action == 'upload_tracks':

        file_name = '{}/tracks{}.txt'.format(PATH_DOWNLOAD, '' if not sample else '_sample')
        table_name = 'tracks{}'.format('' if not sample else '_sample')
        schema = load_schema_from_local_file('{}/tracks.schema'.format(PATH_SCHEMA))

        db.bq.upload_to_table(file_name, table_name, schema)

    if action == 'query_album_ids':

        album_ids = db.bq.get_album_ids(sample)

        write_to_file(
            album_ids,
            '{}/ids_albums{}.txt'.format(PATH_DOWNLOAD, '' if not sample else '_sample'),
            text=True
        )

    if action == 'get_albums':

        file_name = '{}/albums{}.txt'.format(PATH_DOWNLOAD, '' if not sample else '_sample')
        token = get_token()

        ids = load_ids_from_file(
            '{}/ids_albums{}.txt'.format(PATH_DOWNLOAD, '' if not sample else '_sample'),
            uris=False
        )

        albums = data_acquisition.spotify_api.get_albums(token, ids, sample=sample)
        write_to_file(albums, file_name)

    if action == 'get_schema_albums':

        db.bq.connect_to_table_and_pickle_schema('albums_sample', '{}/albums.schema'.format(PATH_SCHEMA))

    if action == 'upload_albums':

        file_name = '{}/albums{}.txt'.format(PATH_DOWNLOAD, '' if not sample else '_sample')
        table_name = 'albums{}'.format('' if not sample else '_sample')
        schema = load_schema_from_local_file('{}/albums.schema'.format(PATH_SCHEMA))

        db.bq.upload_to_table(file_name, table_name, schema)




    pass


def load_schema_from_local_file(file_name):
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


def get_token(scope=None):
    """Return access token for the Spotify API with scope `scope`.
    Look for cached access token, get a new one if expired or unavailable"""

    config = ConfigParser.ConfigParser()
    config.read('.params')
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


def load_ids_from_file(file_name, uris=True):
    """Return a list of ids read from local file `file_name`"""
    try:
        with open(file_name, 'r') as f:
            ids = [line.rstrip('\n').split(':')[2] if uris else line.rstrip('\n') for line in f.readlines()]
            return ids
    except Exception as err:
        print 'Exception when reading ids from file `{}`, `uris` = {}:\n'.format(file_name, uris), err
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


def write_to_file(objects, file_name, text=False):
    """Write the objects in `objects` as jsons to file `file_name`, or write text if `text` is True"""

    with open(file_name, 'w') as out_file:
        out_file.writelines([obj+'\n' if text else json.dumps(obj)+'\n' for obj in objects])
        print "Saved to {0}".format(file_name)

    pass


if __name__ == "__main__":
    main(sys.argv[1:])

