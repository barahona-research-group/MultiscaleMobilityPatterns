import numpy as np

from sklearn import metrics
from sklearn.linear_model import LinearRegression


def R2_score(X, y):

    """
    Perform univariate linear regression and return R2 score
    """

    X = X.reshape(-1, 1)

    # Linear Regression
    LsLin = LinearRegression().fit(X, y)

    # Coefficient of determination
    return LsLin.score(X, y)


def entropy(labels):
    """Calculates the Entropy for a labeling.
    Parameters
    ----------
    labels : int array, shape = [n_samples]
        The labels
    Notes
    -----
    The logarithm used is the natural logarithm (base-e).
    """
    if len(labels) == 0:
        return 1.0
    label_idx = np.unique(labels, return_inverse=True)[1]
    pi = np.bincount(label_idx).astype(np.float64)
    pi = pi[pi > 0]
    pi_sum = np.sum(pi)
    return -np.sum((pi / pi_sum) * (np.log(pi) - np.log(pi_sum)))


def variation_of_information(x, y, normalised=True):
    """Calculates the (Normalised) Variation of Information for two partitions."""
    Ex = entropy(x)
    Ey = entropy(y)
    I = metrics.mutual_info_score(x, y)

    if normalised:
        return (Ex + Ey - 2 * I) / (Ex + Ey - I)
    else:
        return Ex + Ey - 2 * I


def normalised_conditional_entropy(x, y):
    """
    H(X|Y) = H(X) - I(X,Y) and we normalise with log(N)
    """

    N = len(x)
    Ex = entropy(x)
    I = metrics.mutual_info_score(x, y)

    return (Ex - I) / np.log(N)
