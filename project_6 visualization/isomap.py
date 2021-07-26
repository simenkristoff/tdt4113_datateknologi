""" Isomap module. """
import numpy as np
import matplotlib.pyplot as plt
import scipy
from sklearn.utils import graph_shortest_path


class Isomap:
    """
    Class for generating an isomap from a data set.
    """
    __k = None
    __data = None
    __n = None

    def __init__(self, data, k):
        """
        Initialize variables.
        :param data: the data to generate isomap from
        :param k: k-nearest neighbor
        """
        self.__k = k
        self.__data = data
        self.__n = data.shape[0]
        self.__digits_label = np.genfromtxt("digits.csv", delimiter=",")

    def __compute_distances(self):
        """
        Computes all pairwise Euclidean distances.
        :return: matrix of all pairwise Euclidean distances
        """
        a_value = np.sum(self.__data**2, axis=1)[:, np.newaxis]
        b_value = np.sum(self.__data**2, axis=1)
        c_value = -2 * (self.__data @ self.__data.T)
        return np.abs(a_value+b_value+c_value)

    def __compute_geodesics(self):
        """
        Takes high-dimensional data points and computes a distance matrix
        consisting only of the shortest paths between all the points in the
        data set.
        :return: distance matrix
        """
        dist = np.sqrt(self.__compute_distances())
        index = np.argsort(dist, 1)
        for _x, _rad in enumerate(index):
            for kol in _rad[self.__k:]:
                dist[_x, kol] = 0
        return graph_shortest_path.graph_shortest_path(dist, False, 'D')

    def __compute_mds(self, matrix):
        """
        Translates the entries of a distance matrix to a lower dimensional
        representation - i.e. flattens the view and preserves the distances
        between data points as well as possible.
        :param matrix: the distance matrix
        :return: coordinates of the low-dimensional mapped points
        """
        _j = np.identity(self.__n) - (1 / self.__n) * np.ones(
            (self.__n, self.__n))
        _b = -0.5 * (_j @ (np.square(matrix) @ _j))
        e_values, e_vectors = scipy.sparse.linalg.eigsh(_b, k=2, which="LM")
        e_values, e_vectors = np.flip(e_values), np.flip(e_vectors, axis=1)
        return e_vectors @ scipy.linalg.sqrtm(np.diag(e_values))

    def colors(self):
        """
        Returns correct color map for the specified data set.
        :return: color map
        """
        if self.__n > 2000:
            return np.genfromtxt("digits_label.csv")
        return np.arange(self.__n)

    def generate_isomap(self):
        """
        Applies calculations in order to generate an isomap.
        :return: isomap from data set
        """
        _d = self.__compute_geodesics()
        return self.__compute_mds(_d)


swiss_roll = np.genfromtxt('swiss_data.csv', delimiter=",")
digits = np.genfromtxt('digits.csv', delimiter=",")
iso = Isomap(digits, 30)
data = iso.generate_isomap()
C = iso.colors()
plt.scatter(data[:,0], data[:,1], s=10, c=C, marker=".", cmap=plt.cm.Spectral)
plt.show()

