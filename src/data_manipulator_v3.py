from cmath import nan
import pandas as pd
import numpy as np



# Get Muse Dataset data
path = 'mood_features_dataset_v3.csv'
data = pd.read_csv(path)
dataframe = pd.DataFrame(data, columns=['seeds', 'spotify_id', 'danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo'])

# Use seeds/moods = happy/lively/cheerful/whimsical/fun/exciting/energetic/epic/bright, angry/intense/aggressive, peaceful/calm/relaxed/soft/smooth/mellow, nostalgic/sentimental, lonely/sad, gloomy/cold/dark, romantic, gentle, spiritual, uplifitng
np_df = dataframe.to_numpy()
for row in range(len(np_df)):
    if 'happy' in np_df[row][0] or 'lively' in np_df[row][0] or 'cheerful' in np_df[row][0]:
        np_df[row][0] = 'happy'
    elif 'angry' in np_df[row][0] or 'intense' in np_df[row][0] or 'aggressive' in np_df[row][0]:
        np_df[row][0] = 'angry'
    elif 'sad' in np_df[row][0] or 'lonely' in np_df[row][0] or 'cold' in np_df[row][0] or 'calm' in np_df[row][0] or 'peaceful' in np_df[row][0] or 'soft' in np_df[row][0]:
        np_df[row][0] = 'calm'

final_df = pd.DataFrame(np_df, columns=['seeds', 'spotify_id', 'danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo'])
final_df.to_csv('mood_features_dataset_v5.csv')
