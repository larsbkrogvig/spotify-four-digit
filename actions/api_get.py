import os
import sys
import time
import json
import ConfigParser

from spotipy import util as spotify_util

import data_acquisition
import constants
import util

VALID_DOMAINS = [
    'tracks',
    'albums',
]


def api_get(argv, sample):

    try:
        if not argv:
            raise Exception("No domain specified")

        domain = argv.pop(0)
        if domain not in VALID_DOMAINS:
            raise Exception("Invalid domain {}".format(domain))

    except Exception as err:
        print err
        print "Usage: four-digit.py [-s] api_get [{0}] ".format(' | '.join(VALID_DOMAINS))
        sys.exit(2)

    token = get_token()

    file_name = '{}/{}{}.txt'.format(constants.PATH_OBJECTS, domain, '' if not sample else '_sample')
    ids = load_ids_from_file('{}/{}{}.txt'.format(constants.PATH_IDS, domain, '' if not sample else '_sample'))

    objects = None

    if domain == 'tracks':
        objects = data_acquisition.spotify_api.get_tracks(token, ids, sample)
    if domain == 'albums':
        objects = data_acquisition.spotify_api.get_albums(token, ids, sample)

    util.write_to_file(objects, file_name)

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
            token = spotify_util.prompt_for_user_token(username=username, scope=None)
        except AttributeError:
            os.remove(".cache-{0}".format(username))
            token = spotify_util.prompt_for_user_token(username=username, scope=None)

    if not token:
        print "Warning: No token was found"

    return token


def load_ids_from_file(file_name):
    """Return a list of ids read from local file `file_name`"""
    try:
        with open(file_name, 'r') as f:
            ids = [line.rstrip('\n') for line in f.readlines()]
            return ids
    except Exception as err:
        print "Exception when reading ids from file `{}`".format(file_name)
        print err
        sys.exit(1)

    pass
