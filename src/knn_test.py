import pandas as pd
import numpy as np
from knn import KNearestNeighbor
from song_features import GetSongFeatures



path = 'mood_features_dataset_v5.csv'
data = pd.read_csv(path)
dataframe = pd.DataFrame(data, columns=['seeds', 'energy', 'valence'])
sample = dataframe.sample(4000).to_numpy()

training_sample = sample[0:3000]
training_features = training_sample[:, 1:]
training_targets = training_sample[:, 0]
training_targets = training_targets.reshape(training_targets.shape[0], -1)
testing_sample = sample[3000:]
testing_features = testing_sample[:, 1:]
testing_targets = testing_sample[:, 0]
testing_targets = testing_targets.reshape(testing_targets.shape[0], -1)

knn_model = KNearestNeighbor(55)
knn_model.fit(training_features, training_targets)


# Print the accuracy of the KNN model
# prediction = knn_model.predict(testing_features)

# num_correct = np.sum(testing_targets == prediction)
# accuracy = num_correct / testing_targets.shape[0]
# print(accuracy)


# Happy song test
# 'Happy' by Pharrel Williams
# 'My Songs Know What You Did In The Dark' by Fall Out Boy
# 'Ex's and Oh's' by Elle King
# 'See You Again' by Wiz Khalifa
# 'One Summer Day' by Kato
# 'Sad Song' by We The Kings
# 'This City' by Sam Fischer
# 'Surrender' by Natalie Taylor
# 'Photograph' by Ed Sheeran
spotify_ids = np.array(['60nZcImufyMA1MKQY3dcCH', '2E43WFS4rRc09za2r2GmZl', '70eDxAyAraNTiD6lx2ZEnH', '66CFbqJScx6zRieGllITcs', '7eo2HVkRxrDU3bQPwEiIBT', '05CrK6Q5VGtfPDtyQFJ4Kf', '3H3r2nKWa3Yk5gt8xgmsEt', '0ecC8p17cDNlxHXkuYqeR6', '6fxVffaTuwjgEk5h9QyRjy'])

song_features = GetSongFeatures(spotify_ids)
song_mood_predictions = knn_model.predict(song_features)
print(song_mood_predictions)

