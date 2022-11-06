from cmath import nan
import numpy as np
import requests
import time


# Get the Spotify API features of each given song
def GetSongFeatures(spotify_ids):
    CLIENT_ID = '6867ad51b8db4752935da4983bb5a7b6'
    CLIENT_SECRET = '24542cb6b566457993ec54998c3b006c'

    AUTH_URL = 'https://accounts.spotify.com/api/token'

    # POST
    auth_response = requests.post(AUTH_URL, {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    })

    # convert the response to JSON
    auth_response_data = auth_response.json()

    # save the access token
    access_token = auth_response_data['access_token']

    headers = {
        'Authorization': 'Bearer {token}'.format(token=access_token)
    }

    # base URL of all Spotify API endpoints
    BASE_URL = 'https://api.spotify.com/v1/'


    new_song_features = np.empty((len(spotify_ids), 2))
    for row in range(len(spotify_ids)):
        # Spotify ID for the URI
        spotify_id = spotify_ids[row]

        # actual GET request with proper header
        r = requests.get(BASE_URL + 'audio-features/' + spotify_id, headers=headers)
        r = r.json()

        try:
            new_song_features[row] = [
                r['energy'],
                r['valence'],
            ]
        except KeyError as err:
            print(r)
            new_song_features[row] = [nan, nan]
        
        if row % 100 == 0:
            time.sleep(5)

    return new_song_features
    
    
