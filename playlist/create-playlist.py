import ConfigParser

import spotipy
import spotipy.util as util


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

config = ConfigParser.ConfigParser()
config.read('.params')

username = config.get('SPOTIFY','USER_NAME')
playlist_id = config.get('SPOTIFY','PLAYLIST_ID')

with open('uris.txt', 'r') as f:
    data = [line.rstrip('\n') for line in f.readlines()]

token = util.prompt_for_user_token(
    username=username,
    scope='playlist-modify-private'
)

if token:
    sp = spotipy.Spotify(auth=token)

    for chunk in chunks(data, 100):
        sp.user_playlist_add_tracks(
            user=username,
            playlist_id=playlist_id,
            tracks=chunk
        )
else:
    print("Can't get token for", username)
