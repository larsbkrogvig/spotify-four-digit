import sys
import os
import getopt
import ConfigParser
import time
import json

from spotipy import util

import data_acquisition

VALID_ARGUMENTS = [
    'get_tracks',
    'upload_tracks',
    'print_token'
]


def main(argv):
    opts, args = get_options_and_aruments(argv)

    if args[0] == 'print_token':
        print get_token()

    if args[0] == 'get_tracks':
        token = get_token()
        uris = get_uris()
        data_acquisition.spotify.get_tracks(token, uris)

    if args[0] == 'upload_tracks':
        print "Not implemented yet!"

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
        opts, args = getopt.getopt(argv, '')
        if not args:
            raise getopt.GetoptError('No argument given')
        if args[0] not in VALID_ARGUMENTS:
            raise getopt.GetoptError('Unknown argument "{0}"'.format(args[0]))

    except getopt.GetoptError as err:
        print err, '\nUsage: four-digit.py [{0}]'.format('|'.join(VALID_ARGUMENTS))
        sys.exit(2)

    return opts, args


if __name__ == "__main__":
    main(sys.argv[1:])

