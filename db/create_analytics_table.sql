SELECT
  uri,
  track,
  album_artist as artist,
  album,
  duration_ms,
  rank,
  tempo,
  time_signature
  acousticness,
  danceability,
  energy,
  instrumentalness,
  liveness,
  loudness,
  speechiness,
  valence,
  mode,
  key
FROM
  `spotify-four-digit.data.songs` s
JOIN -- Filter songs without features, they were duplicates and no lookups was made
  `spotify-four-digit.data.song_features` a
USING(uri)
