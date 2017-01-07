import ConfigParser
import json

import spotipy
import spotipy.util as util


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

config = ConfigParser.ConfigParser()
config.read('params')

username = config.get('SPOTIFY','USER_NAME')

with open('uris.txt', 'r') as f:
    data = [line.rstrip('\n') for line in f.readlines()]

token = util.prompt_for_user_token(
    username=username,
    scope=None
)

if token:
    sp = spotipy.Spotify(auth=token)

    feature_chunks = []

    for chunk in chunks(data, 100):
        feature_chunks.append(
            sp.audio_features(tracks=chunk)
        )

    features = [f for f_chunk in feature_chunks for f in f_chunk]

    with open('audio_features.txt', 'w') as file:
        file.writelines([json.dumps(f)+'\n' for f in features])

else:
    print("Can't get token for", username)