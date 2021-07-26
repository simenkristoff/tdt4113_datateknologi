"""T-SNE visualization module"""

import matplotlib.pyplot as plt
import numpy as np

from timer import Timer

DIGITS_PATH = "res/digits.csv"
DIGITS_LABEL_PATH = "res/digits_label.csv"


class TSNE:
    """Class containing T-SNE logic"""

    def __init__(self, iterations=1000, e=500, a=0.8, k=30, seed=None):
        self.iterations = iterations
        self.epsilon = e
        self.alpha = a
        self.k_neighbours = k
        if seed:
            np.random.seed(seed)
        self.x_data, self.x_labels = load_data()

    def load_data(self):
        """
        Load the digits data from the csv files.

        :raise: FileNotFoundError / IOError on failure to read file
        """
        try:
            self.x_data, self.x_labels = np.genfromtxt(DIGITS_PATH, delimiter=","), \
                                         np.genfromtxt(DIGITS_LABEL_PATH, delimiter=",")
        except FileNotFoundError as exc:
            raise exc
        except Exception as exc:
            raise exc

    def compute(self, visualize_knn=True):
        """
        Compute the T-SNE visualization of the digits dataset

        :param visualize_knn: if true, visualize the knn-matrix,
               if false proceed to iteration immediately
        :return:
        """
        print("Setting up t-SNE...")

        sample_size = 3000
        self.x_data = self.x_data[:sample_size, :]
        self.x_labels = self.x_labels[:sample_size]

        timer = Timer("setup")

        n_features = self.x_data.shape[0]
        eu_d = pairwise_euclidean_distances(self.x_data)
        k_nn = knn(eu_d, self.k_neighbours)

        if visualize_knn:
            ind = np.argsort(self.x_labels)
            plt.spy(k_nn[:, ind][ind, :], markersize=0.1)
            plt.show()

        pairwise_matrix = get_pairwise_similarities(k_nn)

        del k_nn
        del eu_d

        y_data = np.random.randn(n_features, 2) * 1e-4
        gain = np.full((n_features, 2), 1.0)
        delta = np.full((n_features, 2), 0.0)

        timer.stop()

        timer = Timer("t-SNE")
        # Perform the t-SNE
        for iteration in range(self.iterations):
            # Lower momentum the first iterations
            alpha = 0.5 if iteration < 250 else self.alpha

            if iteration % 10 == 0:
                print(f"Iteration {iteration}: alpha = {alpha}, "
                      f"P scaling factor = {1 if iteration > 100 else 4}")
                # self.plot(y)

            q_matrix = 1 / (1 + squared_euclidean_distances(y_data))

            q_matrix[range(n_features), range(n_features)] = 0  # Set the diagonal to 0
            big_q_matrix = q_matrix / np.sum(q_matrix)

            # Add "lying" factor the first 100 iterations
            g_matrix = (pairwise_matrix - big_q_matrix) * q_matrix * (1 if iteration > 100 else 4)

            s_matrix = np.diag(np.sum(g_matrix, axis=1))
            grad = 4 * (s_matrix - g_matrix) @ y_data

            gain[np.sign(grad) == np.sign(delta)] *= 0.8
            gain[np.sign(grad) != np.sign(delta)] += 0.2
            gain[gain < 0.01] = 0.01

            delta = (alpha * delta) - (self.epsilon * gain * grad)
            y_data += delta

        diff = timer.stop()
        print(f"Average time per iteration: {diff / self.iterations / 1e9:.2f}s")
        self.plot(y_data)

    def plot(self, y_data):
        """
        Plot the y_data scatterplot.

        :param y_data: visualized 2d digit-matrix
        :return:
        """
        plt.jet()
        plt.scatter(y_data[:, 0], y_data[:, 1], s=10, c=self.x_labels)
        plt.show()


def load_data():
    """
    Load the digits data from the csv files.

    :return: x_data, x_labels (np.d_array)
    :raise: FileNotFoundError / IOError on failure to read file
    """
    try:
        return np.genfromtxt(DIGITS_PATH, delimiter=","), np.genfromtxt(DIGITS_LABEL_PATH,
                                                                        delimiter=",")
    except FileNotFoundError as exc:
        raise exc
    except Exception as exc:
        raise exc


def calculate_euclidean_distances(x_data):
    """
    Calculate the eucledian distances between the points in alpha N-dimensional array.

    :param x_data: N-dimensional numpy d_array
    :return:
    """
    x_2 = x_data * x_data

    v_matrix = np.sum(x_2, axis=1, keepdims=True)

    xxt = np.matmul(x_data, x_data.T)
    d_eu = v_matrix.T + v_matrix - 2 * xxt

    return np.sqrt(np.abs(d_eu))


def knn(eu_d, k):
    """
    Find the K nearest neighbours in alpha euclidean distance neighbour matrix.

    :param eu_d: euclidean distance neighbour matrix, must be M*M
    :param k: how many neighbours to include in the matrix.
    :return: knn-nearest-neighbours matrix
    """
    k_nn = np.copy(eu_d)
    for row in k_nn:
        k_smallest = np.argpartition(row, k + 1)[k + 1:]
        row[k_smallest] = 0

    return k_nn


def get_pairwise_similarities(k_nn):
    """
    Compute the pairwise similarities from the k_nn graph

    :param k_nn: k-nearest neighbour number
    :return: pairwise similarities matrix
    """
    p_matrix = (k_nn + k_nn.T > 0).astype(float)
    return p_matrix / np.sum(p_matrix)


def pairwise_euclidean_distances(x_data):
    """
    Calculate the euclidean distances between the points in alpha N-dimensional array.

    :param x_data: N-dimensional array
    :return: matrix of pairwise euclidean distances
    """
    v_matrix = np.sum(x_data * x_data, axis=1, keepdims=True)
    return np.sqrt(np.abs(v_matrix.T + v_matrix - 2 * (x_data @ x_data.T)))


def squared_euclidean_distances(x_data):
    """
    Get the squared euclidean distance matrix for x_data

    :param x_data: N-dimensional array
    :return: matrix of pairwise squared euclidean distances
    """
    v_matrix = np.sum(x_data * x_data, axis=1, keepdims=True)
    return v_matrix.T + v_matrix - 2 * (x_data @ x_data.T)


t_sne = TSNE()
t_sne.compute(visualize_knn=False)
