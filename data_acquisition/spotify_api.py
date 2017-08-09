import spotipy
import math


def _chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


def spotify_api_get_tracks(token, ids, sample=False):
    """Download track information for ids in `ids`, using access token `token`"""
    sp = _get_spotify_client(token)

    track_chunks = []
    chunk_size = 50
    for i, chunk in enumerate(_chunks(ids, chunk_size)):
        print "Fetching track chunk {}/{:.0f}".format(i + 1, math.ceil(len(ids)/float(chunk_size)))
        track_chunks.append(sp.tracks(tracks=chunk))
        if sample:
            print "Sample run, stopping"
            break

    return [t for t_chunk in track_chunks for t in t_chunk['tracks']]


def spotify_api_get_albums(token, ids, sample=False):
    """Download album information for ids in `ids`, using access token `token`"""
    sp = _get_spotify_client(token)

    album_chunks = []
    chunk_size = 20
    for i, chunk in enumerate(_chunks(ids, chunk_size)):
        print "Fetching album chunk {}/{:.0f}".format(i + 1, math.ceil(len(ids)/float(chunk_size)))
        album_chunks.append(sp.albums(albums=chunk))
        if sample:
            print "Sample run, stopping"
            break

    return [a for a_chunk in album_chunks for a in a_chunk['albums']]


def spotify_api_get_artists(token, ids, sample=False):
    """Download artists information for ids in `ids`, using access token `token`"""
    sp = _get_spotify_client(token)

    artist_chunks = []
    chunk_size = 50
    for i, chunk in enumerate(_chunks(ids, chunk_size)):
        print "Fetching artist chunk {}/{:.0f}".format(i + 1, math.ceil(len(ids)/float(chunk_size)))
        artist_chunks.append(sp.artists(artists=chunk))
        if sample:
            print "Sample run, stopping"
            break

    return [a for a_chunk in artist_chunks for a in a_chunk['artists']]


def _get_spotify_client(token):
    """Return a Spotify client using `token` for authorization and warn if it is missing"""

    if not token:
        raise Exception("No token")

    return spotipy.Spotify(auth=token)
