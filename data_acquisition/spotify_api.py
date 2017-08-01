import json
import spotipy
import math


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


def get_tracks(token, uris, sample=False):
    """Download track information for uris in `uris`, using access token `token`"""
    if not token:
        raise Exception("No token")

    sp = spotipy.Spotify(auth=token)

    track_chunks = []
    chunk_size = 50
    for i, chunk in enumerate(chunks(uris, chunk_size)):
        print "Fetching track chunk {}/{:.0f}".format(i + 1, math.ceil(len(uris)/float(chunk_size)))
        track_chunks.append(sp.tracks(tracks=chunk))
        if sample:
            print "Sample run, stopping"
            break

    return [t for t_chunk in track_chunks for t in t_chunk['tracks']]


def get_albums(token, uris, sample=False):
    """Download album information for uris in `uris`, using access token `token`"""
    if not token:
        raise Exception("No token")

    sp = spotipy.Spotify(auth=token)

    album_chunks = []
    chunk_size = 20
    for i, chunk in enumerate(chunks(uris, chunk_size)):
        print "Fetching album chunk {}/{:.0f}".format(i + 1, math.ceil(len(uris)/float(chunk_size)))
        album_chunks.append(sp.albums(albums=chunk))
        if sample:
            print "Sample run, stopping"
            break

    return [a for a_chunk in album_chunks for a in a_chunk['albums']]
