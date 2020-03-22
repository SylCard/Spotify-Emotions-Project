import argparse
import pprint
import sys
import os
import subprocess
import json
import spotipy
import spotipy.util as util
import pandas as pd
import time
from spotifyCreds import spotifyCreds

# With much help from
# https://github.com/SylCard/Spotify-Emotions-Project
# https://towardsdatascience.com/predicting-my-mood-using-my-spotify-data-2e898add122a

sp = spotifyCreds().clientCredsFlow()

def show_tracks(tracks):
    for i, items in enumerate(tracks['items']):
        track = items['track']
        print (" %d %s %s" % (i, track['artists'][0]['name'],track['name']))

def get_track_features(track_id,sp):
    if track_id is None:
        return None
    else:
        features = sp.audio_features([track_id])
    return features

def get_features(tracks,sp):
    tracks_with_features=[]

    for track in tracks:
        features = get_track_features(track['id'],sp)
        print (track['name'])
        if not features:
            print("passing track %s" % track['name'])
            pass
        else:
            f = features[0]
            tracks_with_features.append(dict(
                                            added_at = track['added_at'],
                                            name = track['name'],
                                            artist = track['artist'],
                                            id = track['id'],
                                            popularity = track['popularity'],
                                            danceability = f['danceability'],
                                            energy = f['energy'],
                                            loudness = f['loudness'],
                                            speechiness = f['speechiness'],
                                            acousticness = f['acousticness'],
                                            tempo = f['tempo'],
                                            liveness = f['liveness'],
                                            valence = f['valence'],
                                            instrumentalness = f['instrumentalness'],
                                            key = f['key'],
                                            time_signature = f['time_signature'],
                                            mode = f['mode'],
                                            duration_ms = f['duration_ms']
                                            ))

    print("Total number of tracks with features: ", len(tracks_with_features))
    return tracks_with_features

def get_tracks_from_playlists(username, sp, loop, offset):
    playlistArray = []
    for i in range(0, int(loop)):
        playlists = sp.user_playlists(username, offset = offset)
        offset += 50
        playlistArray.append(playlists)

    trackList = []
    for i in range(0, len(playlistArray)):
        for playlist in playlistArray[i]['items']:
            if playlist['owner']['id'] == username:
                print (playlist['name'], ' no. of tracks: ', playlist['tracks']['total'])
                results = sp.user_playlist(username, playlist['id'],fields="tracks,next")
                tracks = results['tracks']
                for j, item in enumerate(tracks['items']):
                    track = item['track']
                    trackList.append(dict(name = track['name'],
                                          id = track['id'],
                                          artist = track['artists'][0]['name'],
                                          added_at = tracks['items'][0]['added_at'],
                                          popularity = track['popularity']))

    print("Wow, that's a lot of tracks: ", len(trackList))
    return trackList

def write_to_csv(track_features, name_of_csv):
    df = pd.DataFrame(track_features)
    df.drop_duplicates(subset = "id",
                       keep = "first",
                       inplace = True)
    print ('Total tracks: ', len(df))
    df.to_csv(name_of_csv, index = False)

def main(username, loop, offset):
    print ("Retrieving tracks from user playlists")
    tracks = get_tracks_from_playlists(username, sp, loop, offset)
    print ("Retrieving audio features from tracks")
    tracks_with_features = get_features(tracks, sp)
    print ("Storing de-duplicated tracks into a CSV file")
    write_to_csv(tracks_with_features, 'deduplicated_tracks_from_my_playlists-01.csv')


if __name__ == '__main__':
    print ('Up, up, and away web...')
    parser = argparse.ArgumentParser(description = 'Grabs tracks from user playlist and outputs to a CSV file')
    parser.add_argument('--username', help = 'username')
    parser.add_argument('--offset', help = 'offset')
    parser.add_argument('--loop', help = 'loop')
    args = parser.parse_args()
    main(args.username, int(args.loop), int(args.offset))
