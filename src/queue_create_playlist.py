import pandas as pd
import random
import spotipy
import spotipy.util as util
from knn import KNearestNeighbor
from song_features import GetSongFeatures


# Create a playlist based on the mood for the user
def CreatePlaylist(username, playlist_name, new_playlist_name, mood):
    client_id = '6867ad51b8db4752935da4983bb5a7b6'
    client_secret = '24542cb6b566457993ec54998c3b006c'
    scope = 'playlist-modify-public'
    token = util.prompt_for_user_token(username, scope, client_id=client_id, client_secret=client_secret, redirect_uri='http://localhost:8000/callback') 
    sp = spotipy.Spotify(auth=token)
    
    playlist_id = GetPlaylistID(username, playlist_name, sp, filled=True)
    spotify_ids = GetPlaylistSongs(username, playlist_id, sp)
    selected_spofity_ids = GetSelectedSongs(spotify_ids, mood)

    sp.user_playlist_create(username, name=new_playlist_name)
    new_playlist_id = GetPlaylistID(username, new_playlist_name, sp, filled=False)
    sp.user_playlist_add_tracks(username, new_playlist_id, selected_spofity_ids)


# Get playlist's id given a playlist's name
def GetPlaylistID(username, playlist_name, sp, filled):
    playlist_id = ''
    playlists = sp.user_playlists(username)
    for playlist in playlists['items']:
        if filled:
            if playlist['name'] == playlist_name:
                playlist_id = playlist['id']
        else:
            if playlist['name'] == playlist_name and playlist['tracks']['total'] == 0:
                playlist_id = playlist['id']
    return playlist_id


# Queue songs based on the mood of the user (requires Spotify Premium)
def QueueSong(username, playlist_name, mood):
    client_id = '6867ad51b8db4752935da4983bb5a7b6'
    client_secret = '24542cb6b566457993ec54998c3b006c'
    scope = 'user-modify-playback-state'

    token = util.prompt_for_user_token(username, scope, client_id=client_id, client_secret=client_secret, redirect_uri='http://localhost:8000/callback') 
    sp = spotipy.Spotify(auth=token)
    playlist_id = GetPlaylistID(username, playlist_name, sp, filled=True)
    spotify_ids = GetPlaylistSongs(username, playlist_id, sp)
    selected_spofity_ids = GetSelectedSongs(spotify_ids, mood)
    ################################ print(selected_spofity_ids)
    random.shuffle(selected_spofity_ids)
    for id in selected_spofity_ids:
        sp.add_to_queue(id)


# Get the spotify ids of songs in a playlist
def GetPlaylistSongs(username, playlist_id, sp):
    tracks = sp.user_playlist_tracks(username, playlist_id)['items']
    spotify_ids = []
    for song in tracks:
        spotify_ids.append(song['track']['id'])
    return spotify_ids


# Get the spotify ids of songs that match the specified mood
def GetSelectedSongs(spotify_ids, mood):
    mood = mood.lower()

    path = '../mood_features_dataset_v5.csv'
    data = pd.read_csv(path)

    dataframe = pd.DataFrame(data, columns=['seeds', 'energy', 'valence'])
    sample = dataframe.sample(3000).to_numpy()
    training_features = sample[:, 1:]
    training_targets = sample[:, 0]
    training_targets = training_targets.reshape(training_targets.shape[0], -1)

    knn_model = KNearestNeighbor(55)
    knn_model.fit(training_features, training_targets)

    song_features = GetSongFeatures(spotify_ids)
    song_mood_predictions = knn_model.predict(song_features)
    ################################ print(song_mood_predictions)

    selected_spotify_ids = []
    for i in range(len(spotify_ids)):
        if song_mood_predictions[i] == mood:
            selected_spotify_ids.append(spotify_ids[i])
    ################################ print(selected_spotify_ids)
    return selected_spotify_ids




#CreatePlaylist('31z3bbe6wronnpxoo7ql6dh6ymxm', 'Test Songs', 'Calm/Sad Songs', 'Calm')
#CreatePlaylist('31z3bbe6wronnpxoo7ql6dh6ymxm', 'Test Songs', 'Angry Songs', 'Angry')


#QueueSong('31z3bbe6wronnpxoo7ql6dh6ymxm', 'Test Songs', 'Calm')
#QueueSong('31z3bbe6wronnpxoo7ql6dh6ymxm', 'Test Songs', 'Angry')



#CreatePlaylist('31ihlyyrqaibkq6wjgrvn65ncgr4', 'bad bdm to get out of bed ', 'Happy Boi Hours', 'Happy')
#CreatePlaylist('isaacedwin', 'Grind Music', 'Happy MLoodify', 'Happy')
#CreatePlaylist('31z3bbe6wronnpxoo7ql6dh6ymxm', '3H3r2nKWa3Yk5gt8xgmsEt', 'Calm')
#CreatePlaylist('175930984361477b', '3H3r2nKWa3Yk5gt8xgmsEt', 'Calm')
#CreatePlaylist('jwny123', 'C-Pop', 'A Happy C-Pop Playlist', 'Happy')

#QueueSong('31z3bbe6wronnpxoo7ql6dh6ymxm', '3H3r2nKWa3Yk5gt8xgmsEt')
