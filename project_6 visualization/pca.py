"""Module for Principal Component Analysis"""
import matplotlib.pyplot as plt
import numpy as np
from scipy.sparse.linalg import eigs


class PCA:
    """Principal Component Analysis"""

    def __init__(self, data):
        self.data = data

    @staticmethod
    def fit_transform(data):
        """Transforms multidimensional data to 2-dimensional data

        Args:
            data (matrix): multidimensional data to be transformed

        Returns:
            matrix: transformed 2-dimensional matrix
        """
        rows, columns = data.shape

        # Find the mean vectors for all dimensions
        means = np.mean(data, 0)

        # Center the data with x_i <- x_1 - mu
        for i in range(columns):
            data[i, :] = data[i, :] - means[i]

        # Compute the covariance matrix
        cov_matrix = np.cov(data)

        # Compute the eigenvectors
        if columns - 1 == 2:
            eigenvalues, eigenvectors = np.linalg.eigh(cov_matrix)
        else:
            eigenvalues, eigenvectors = eigs(cov_matrix)

        # Compute corresponding pairs of eigenvalues and eigenvectors
        eigenpairs = [(np.abs(eigenvalues[i]), eigenvectors[:, i])
                      for i in range(len(eigenvalues))]

        # Sort the eigenpairs by eigenvalues
        eigenpairs.sort(key=lambda x: x[0], reverse=True)

        # Choose the eigenvectors corresponding the d highest eigenvalues
        eigenmatrix = np.hstack((eigenpairs[0][1].reshape(
            rows, 1), eigenpairs[1][1].reshape(rows, 1)))

        # Compute the transformed matrix
        transformed = eigenmatrix.transpose()
        transformed.dot(data)

        return transformed

    @staticmethod
    def plot(data, colour):
        """Plots 2-dimensional data with scatter plot

        Args:
            data (matrix): 2-dimensional data
        """
        plt.jet()
        plt.scatter(data[0, :], data[1, :], s=10, c=colour, marker=".")
        plt.show()


def swiss_to_2d():
    """Plots Swiss roll in 2D"""
    swiss_roll = np.genfromtxt('res/swiss_data.csv', delimiter=',')
    pca = PCA(swiss_roll)
    two_dimensional_swiss_roll = pca.fit_transform(swiss_roll)
    pca.plot(two_dimensional_swiss_roll, np.arange(2000))


def digits_to_2d():
    """Plots Digits in 2D"""
    digits = np.genfromtxt('res/digits.csv', delimiter=',')
    digits_labels = np.genfromtxt('res/digits_label.csv', delimiter=',')
    pca = PCA(digits)
    two_dimensional_digits = pca.fit_transform(digits)
    pca.plot(two_dimensional_digits, digits_labels)


swiss_to_2d()
digits_to_2d()
