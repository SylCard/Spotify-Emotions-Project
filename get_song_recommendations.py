import argparse
import sys
import spotipy
from pprint import pprint
from getFeaturesFromPublicPlaylists import write_to_csv
from spotify_creds import spotifyCreds

''' Returns a list of recommended songs to listen to
Below are example commands with arguments to return song recommendations, returns 20 songs each
Song feature values are mean values taken from song cluster analysis

python get_song_recommendations.py --track 4S2hwCTt7F6QusyrYYparO --liveness 0.203 --acousticness 0.422 --danceability 0.572 --energy 0.632 --valence 0.225
python get_song_recommendations.py --track 7yJbt0kEHSdhobSf6bzopz --liveness 0.160539 --acousticness 0.712217 --danceability 0.516054 --energy 0.363559 --valence 0.331628
python get_song_recommendations.py --track 5h3xoQzVec6OCtzFuuafw7 --liveness 0.171310 --acousticness 0.194131 --danceability 0.599174 --energy 0.639073 --valence 0.442669
python get_song_recommendations.py --track 7EXPDw2u3hJLfw7NKYIoD3 --liveness 0.171310 --acousticness 0.194131 --danceability 0.599174 --energy 0.639073 --valence 0.442669
'''

sp = spotifyCreds().clientCredsFlow()

def get_tracks_from_recommendations(sp, seed_track, target_liveness,
                                                     target_acousticness, target_danceability,
                                                     target_energy, target_valence):

    recommendations = sp.recommendations(seed_tracks=[seed_track],
                                        target_liveness=[target_liveness],
                                        target_acousticness=[target_acousticness],
                                        target_danceability=[target_danceability],
                                        target_energy=[target_energy],
                                        target_valence=[target_valence])

    trackIds = []

    for i, recommendation in enumerate(recommendations['tracks']):
        trackIds.append(dict(artist = recommendation['album']['artists'][0]['name'],
                             id = recommendation['id'],
                             name = recommendation['name'],
                             popularity = recommendation['popularity']))
    pprint(trackIds)
    return trackIds

def main(track, liveness, acousticness, danceability, energy, valence):
    getSongRecommendations = get_tracks_from_recommendations(sp, track, liveness, acousticness, danceability, energy, valence)
    write_to_csv(getSongRecommendations, 'song_recommendations.csv')

if __name__ == '__main__':
    print("Let's get you some songs...")
    parser = argparse.ArgumentParser(description = 'Returns recommended tracks in a CSV file')
    parser.add_argument('--track', help = 'seedTrackId')
    parser.add_argument('--liveness', help = 'offset')
    parser.add_argument('--acousticness', help = 'loop')
    parser.add_argument('--danceability', help = 'loop')
    parser.add_argument('--energy', help = 'loop')
    parser.add_argument('--valence', help = 'loop')
    args = parser.parse_args()
    main(args.track, float(args.liveness), float(args.acousticness), float(args.danceability), float(args.energy), float(args.valence))
