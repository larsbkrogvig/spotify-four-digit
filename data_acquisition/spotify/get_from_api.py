import json
import spotipy

OUTPUT_FILENAME = 'tracks.txt'


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


def get_tracks(token, uris):
    """Download track information for uris in `uris`, using access token `token`"""
    if not token:
        raise Exception("No token")

    sp = spotipy.Spotify(auth=token)

    track_chunks = []
    for i, chunk in enumerate(chunks(uris, 50)):
        print "Fetching track chunk {0}/{1}".format(i, len(chunks(uris, 50)))
        track_chunks.append(sp.tracks(tracks=chunk))

    tracks = [t for t_chunk in track_chunks for t in t_chunk['tracks']]

    with open(OUTPUT_FILENAME, 'w') as out_file:
        out_file.writelines([json.dumps(f)+'\n' for f in tracks])
        print "Tracks stored in {0}".format(OUTPUT_FILENAME)
