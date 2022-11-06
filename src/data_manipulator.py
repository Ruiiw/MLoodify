from cmath import nan
import pandas as pd
import numpy as np
import requests
import time
import spotipy  ############################################################## Didn't use



# Get Muse Dataset data
path = 'muse_v3.csv'
data = pd.read_csv(path)
dataframe = pd.DataFrame(data, columns=['seeds', 'spotify_id'])

# Remove rows that contain NaN values
df_is_nan = pd.isnull(dataframe).to_numpy()
df_is_nan = np.sum(df_is_nan, axis=1)
##############################################################print(np.argwhere(df_is_nan != 0).flatten())
dataframe = dataframe.drop(np.argwhere(df_is_nan != 0).flatten())
##############################################################print(dataframe)

# Use seeds/moods = happy/lively/cheerful/whimsical/fun/exciting/energetic/epic/bright, angry/intense/aggressive, peaceful/calm/relaxed/soft/smooth/mellow, nostalgic/sentimental, lonely/sad, gloomy/cold/dark, romantic, gentle, spiritual, uplifitng
np_df = dataframe.to_numpy()
removed_rows = []
for row in range(len(np_df)):
    if 'happy' in np_df[row][0] or 'lively' in np_df[row][0] or 'cheerful' in np_df[row][0]:
        np_df[row][0] = 'happy'
    elif 'angry' in np_df[row][0] or 'intense' in np_df[row][0] or 'aggressive' in np_df[row][0]:
        np_df[row][0] = 'angry'
    elif 'sad' in np_df[row][0] or 'lonely' in np_df[row][0] or 'cold' in np_df[row][0]:
        np_df[row][0] = 'sad'
    elif 'calm' in np_df[row][0] or 'peaceful' in np_df[row][0] or 'soft' in np_df[row][0]:
        np_df[row][0] = 'calm'
    else:
        removed_rows.append(row)
        
np_df = np.delete(np_df, removed_rows, 0)

##############################################################print(dataframe)
##############################################################print(pd.DataFrame(np_df, columns=['seeds', 'spotify_id']))


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

audio_features = np.empty((len(np_df), 11))   # 11 audio features for each song
for row in range(len(np_df)):
    # Spotify ID for the URI
    spotify_id = np_df[row][1]

    # actual GET request with proper header
    r = requests.get(BASE_URL + 'audio-features/' + spotify_id, headers=headers)
    r = r.json()
    
    try:
        audio_features[row] = [
            r['danceability'],
            r['energy'],
            r['key'],
            r['loudness'],
            r['mode'],
            r['speechiness'],
            r['acousticness'],
            r['instrumentalness'],
            r['liveness'],
            r['valence'],
            r['tempo'],
        ]
    except KeyError as err:
        print(r)
        audio_features[row] = [nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan]

    if row % 100 == 0:
        time.sleep(5)


np_df = np.hstack([np_df, audio_features])
##############################################################print(pd.DataFrame(np_df, columns=['seeds', 'spotify_id', 'danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo']))
final_df = pd.DataFrame(np_df, columns=['seeds', 'spotify_id', 'danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo'])
final_df.to_csv('mood_features_dataset_v3.csv')


#df_is_nan = np.isnan(dataframe.to_numpy())
#df_is_nan = np.sum(df_is_nan, axis=0)

#for song_row in temp_df:
#    if np.isNan(song_row.spotify_id):
#        dataframe.drop(inplace=True)


"""
Number of times each mood appears in the dataset

{"'aggressive'": 1000, "'fun'": 998, "'sexy'": 990, "'energetic'": 998, "'angry'": 1000, "'bitter'": 805, "'epic'": 995, "'driving'": 786, "'intense'": 1000, "'uplifting'": 999, "'confrontational'": 214, "'desperate'": 292, "'fierce'": 962, "'soft'": 997, "'dark'": 999, "'powerful'": 998, "'cold'": 998, "'gritty'": 997, "'warm'": 998, "'flowing'": 366, "'smooth'": 997, "'exciting'": 820, "'hostile'": 74, "'cathartic'": 407, "'fiery'": 217, "'raucous'": 109, "'volatile'": 132, "'relaxed'": 997, "'brash'": 173, "'wry'": 171, "'carefree'": 287, "'freewheeling'": 126, "'detached'": 196, "'sparkling'": 168, "'irreverent'": 42, "'summery'": 384, "'bright'": 916, "'messy'": 219, "'sprawling'": 54, "'quirky'": 996, "'rambunctious'": 90, "'calm'": 999, "'laid-back'": 231, "'cynical'": 998, "'ethereal'": 904, "'atmospheric'": 994, "'hypnotic'": 996, "'trippy'": 799, "'explosive'": 219, "'silly'": 998, "'sweet'": 992, "'nostalgic'": 997, "'tense'": 516, "'technical'": 995, "'spooky'": 999, "'exotic'": 1000, "'witty'": 947, "'manic'": 280, "'urgent'": 284, "'dramatic'": 1000, "'complex'": 827, "'reflective'": 998, "'searching'": 146, "'gutsy'": 41, "'rousing'": 661, "'eerie'": 998, "'bleak'": 349, "'scary'": 999, "'soothing'": 997, "'positive'": 996, "'sentimental'": 997, "'strong'": 663, "'poignant'": 987, "'thoughtful'": 996, "'erotic'": 999, "'sexual'": 827, "'eccentric'": 996, "'rollicking'": 75, "'sensual'": 998, "'trashy'": 347, "'precious'": 606, "'lyrical'": 999, "'nihilistic'": 74, "'lively'": 785, "'cheerful'": 1000, "'gleeful'": 28, "'playful'": 997, "'passionate'": 999, "'crunchy'": 414, "'ominous'": 770, "'provocative'": 430, "'unsettling'": 261, "'apocalyptic'": 574, "'gloomy'": 1000, "'halloween'": 683, "'grim'": 328, "'nocturnal'": 1000, "'delicate'": 913, "'gentle'": 999, "'spiritual'": 999, "'theatrical'": 851, "'tragic'": 662, "'peaceful'": 998, "'menacing'": 445, "'negative'": 936, "'brooding'": 827, "'somber'": 317, "'rebellious'": 178, "'triumphant'": 433, "'springlike'": 19, "'spacey'": 635, "'confident'": 367, "'optimistic'": 997, "'introspective'": 771, "'bittersweet'": 994, "'reckless'": 80, "'thuggish'": 40, "'harsh'": 999, "'hyper'": 409, "'visceral'": 261, "'threatening'": 18, "'anxious'": 149, "'street-smart'": 70, "'sleazy'": 999, "'lonely'": 999, "'sophisticated'": 933, "'savage'": 126, "'whimsical'": 999, "'ironic'": 959, "'acerbic'": 61, "'narrative'": 553, "'angst-ridden'": 41, "'flashy'": 346, "'demonic'": 189, "'mysterious'": 998, "'druggy'": 195, "'belligerent'": 4, "'mystical'": 998, "'yearning'": 579, "'thrilling'": 96, "'ecstatic'": 166, "'uncompromising'": 61, "'sardonic'": 803, "'humorous'": 812, "'monumental'": 397, "'ramshackle'": 23, "'wistful'": 788, "'rowdy'": 85, "'stylish'": 998, "'paranoid'": 526, "'pure'": 628, "'cerebral'": 600, "'martial'": 999, "'melancholy'": 985, "'sad'": 983, "'mellow'": 981, "'happy'": 993, "'lush'": 1000, "'romantic'": 996, "'nervous'": 177, "'sarcastic'": 999, "'literate'": 350, "'defiant'": 496, "'malevolent'": 39, "'outrageous'": 55, "'scary music'": 61, "'light'": 999, "'elegant'": 957, "'joyous'": 299, "'bombastic'": 192, "'organic'": 999, "'autumnal'": 393, "'intimate'": 983, "'enigmatic'": 389, "'elegiac'": 133, "'resolute'": 12, "'serious'": 858, "'campy'": 78, "'earnest'": 266, "'distraught'": 35, "'airy'": 205, "'boisterous'": 74, "'plaintive'": 92, "'self-conscious'": 43, "'snide'": 23, "'swaggering'": 54, "'exuberant'": 225, "'bravado'": 38, "'feral'": 351, "'fractured'": 108, "'earthy'": 504, "'philosophical'": 440, "'shimmering'": 151, "'funereal'": 27, "'brittle'": 49, "'ambitious'": 115, "'knotty'": 17, "'difficult'": 116, "'circular'": 41, "'innocent'": 236, "'suffocating'": 20, "'insular'": 17, "'austere'": 42, "'greasy'": 54, "'meandering'": 42, "'quiet'": 992, "'perky'": 63, "'refined'": 276, "'sacred'": 994, "'graceful'": 100, "'devotional'": 144, "'athletic'": 21, "'satirical'": 66, "'suspenseful'": 50, "'reserved'": 46, "'comic'": 250, "'reassuring'": 52, "'mighty'": 68, "'macabre'": 141, "'lazy'": 975, "'spicy'": 178, "'animated'": 88, "'rustic'": 170, "'effervescent'": 41, "'elaborate'": 104, "'ornate'": 13, "'agreeable'": 2, "'euphoric'": 790, "'slick'": 638, "'mechanical'": 194, "'brassy'": 58, "'regretful'": 12, "'kinetic'": 33, "'outraged'": 8, "'reverent'": 20, "'pastoral'": 171, "'hedonistic'": 28, "'dreamy'": 998, "'meditative'": 829, "'sparse'": 309, "'amiable'": 53, "'good-natured'": 51, "'jittery'": 8, "'tender'": 936, "'naive'": 244, "'child-like'": 54, "'indulgent'": 48, "'hungry'": 44, "'clinical'": 102, "'celebratory'": 53, "'understated'": 35, "'languid'": 19, "'restrained'": 22, "'wintry'": 74, "'noble'": 45, "'giddy'": 21, "'monastic'": 48, "'narcotic'": 54, "'weary'": 51, "'stately'": 23, "'marching'": 30, "'opulent'": 1, "'transparent'": 62, "'sugary'": 31, "'benevolent'": 3, "'consoling'": 9, "'dignified'": 7, "'capricious'": 2, "'feverish'": 2, "'jovial'": 8, "'ebullient'": 3, "'motoric'": 2, "'virile'": 1, "'translucent'": 3, "'hymn-like'": 1, "'sprightly'": 2}
"""