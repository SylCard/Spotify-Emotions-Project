from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import spotipy

# replace first three values to grant yourself access
client_id = 'your-client-id'
client_secret = 'your-client-secret'
username = 'your-username'
scope = 'user-library-read'
redirect_uri = 'http://127.0.0.1:8081/'
# optional values to adjust scope
# ,playlist-modify-private,playlist-modify-public

class spotifyCreds():
    '''A single place to manage/retrieve your Spotify API credentials'''
    def __init__(self):
        pass

    def clientCredsFlow(self):
        global client_id
        global client_secret

        client_credentials_manager = SpotifyClientCredentials(client_id = client_id, client_secret = client_secret)

        sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
        sp.trace = False
        return sp

    def authCodeFlow(self):
        global client_id
        global client_secret
        global username
        global scope
        global redirect_uri

        token = util.prompt_for_user_token(username,
                                           scope = scope,
                                           client_id = client_id,
                                           client_secret = client_secret,
                                           redirect_uri = redirect_uri)
