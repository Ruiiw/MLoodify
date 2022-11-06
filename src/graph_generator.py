import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


path = 'mood_features_dataset_v3.csv'
data = pd.read_csv(path)

# Categorize songs from the dataset
dataframe = pd.DataFrame(data, columns=['seeds', 'energy', 'valence'])
np_data = dataframe.sample(3000).to_numpy()
upbeat_data = []
low_key_data = []
happy_data = []
angry_data = []
calm_data = []
sad_data = []
for row in range(len(np_data)):
    if np_data[row][0] == 'happy':
        happy_data.append(np_data[row][1:])
        upbeat_data.append(np_data[row][1:])
    elif np_data[row][0] == 'angry':
        angry_data.append(np_data[row][1:])
        upbeat_data.append(np_data[row][1:])
    elif np_data[row][0] == 'calm':
        calm_data.append(np_data[row][1:])
        low_key_data.append(np_data[row][1:])
    elif np_data[row][0] == 'sad':
        sad_data.append(np_data[row][1:])
        low_key_data.append(np_data[row][1:])

upbeat_data = np.array(upbeat_data)
low_key_data = np.array(low_key_data)
happy_data = np.array(happy_data)
angry_data = np.array(angry_data)
calm_data = np.array(calm_data)
sad_data = np.array(sad_data)


# Plot of songs in 2 mood categories
plt.figure(0)
plt.scatter(low_key_data[:, 0], low_key_data[:, 1], label='Low-key', color = 'C0')
plt.scatter(upbeat_data[:, 0], upbeat_data[:, 1], label='Upbeat', color='C1')
plt.title('Energy vs Valence')
plt.xlabel('Energy')
plt.ylabel('Valence')
plt.legend()

# Plot of songs in 3 mood categories
plt.figure(1)
plt.scatter(calm_data[:, 0], calm_data[:, 1], label='Calm', color='C0')
plt.scatter(sad_data[:, 0], sad_data[:, 1], color='C0')
plt.scatter(happy_data[:, 0], happy_data[:, 1], label='Happy', color='C1')
plt.scatter(angry_data[:, 0], angry_data[:, 1], label='Angry', color='C3')
plt.title('Energy vs Valence')
plt.xlabel('Energy')
plt.ylabel('Valence')
plt.legend()

# Plot of songs in 4 mood categories
plt.figure(2)
plt.scatter(calm_data[:, 0], calm_data[:, 1], label='Calm', color='C0')
plt.scatter(sad_data[:, 0], sad_data[:, 1], label='Sad', color='C2')
plt.scatter(happy_data[:, 0], happy_data[:, 1], label='Happy', color='C1')
plt.scatter(angry_data[:, 0], angry_data[:, 1], label='Angry', color='C3')
plt.title('Energy vs Valence')
plt.xlabel('Energy')
plt.ylabel('Valence')
plt.legend()

plt.show()
