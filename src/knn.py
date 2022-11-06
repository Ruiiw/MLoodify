import numpy as np 

class KNearestNeighbor():  

    def __init__(self, k_neighbors):
        """
        Initialize KNN model with the given k value
        """
        self.k_neighbors = k_neighbors
        self.features = np.array([])
        self.targets = np.array([])


    def fit(self, features, targets):
        """
        Train the KNN model by saving the given feature and target values
        """
        self.features = features
        self.targets = targets
        

    def predict(self, features):
        """
        Predict the target/label values of the given features based on the KNN model
        and return an array of the predicted targets/labels 
        """
        labels = np.empty((features.shape[0], self.targets.shape[1]), dtype=object)
        distances = euclidean_distances(features, self.features)

        for row in range(len(distances)):
            distances_from_sample = distances[row]
            k_nearest_neighbors = self.get_nearest(distances_from_sample)
            labels[row] = self.aggregate(k_nearest_neighbors)
        return labels


    def get_nearest(self, distances):
        """
        Get the k nearest neighbors by finding the k smallest distances
        and returns the indexes of those nearest neighbors
        """
        return np.argpartition(a=distances, kth=(self.k_neighbors - 1))[:self.k_neighbors]


    def aggregate(self, k_nearest_neighbors):
        """
        Aggregate the targets/labels of the k nearest neighbors by taking the mode
        and returns that target/label
        """
        targets = self.targets[k_nearest_neighbors]
        targets = targets.flatten()
        # Get mode of targets of k nearest neighbors
        nearest_labels, counts = np.unique(ar=targets, return_counts=True)
        mode_index = np.argwhere(counts == np.max(counts))
        aggregate_target = nearest_labels[mode_index[0]]
        return aggregate_target


def euclidean_distances(X, Y):
    """
    Get the distances between the set of points in X and the set of points in Y
    and returns a matrix of all the distances
    """
    D = np.empty((len(X), len(Y)))
    for m in range(len(X)):
        for n in range(len(Y)):
            D[m][n] = np.sqrt(np.sum(np.square(Y[n] - X[m])))
    return D