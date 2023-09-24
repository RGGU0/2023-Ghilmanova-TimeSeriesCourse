import numpy as np


def ED_distance(ts1, ts2):
    """
    Calculate the Euclidean distance.

    Parameters
    ----------
    ts1 : numpy.ndarray
        The first time series.

    ts2 : numpy.ndarray
        The second time series.

    Returns
    -------
    ed_dist : float
        Euclidean distance between ts1 and ts2.
    """
    
    ed_dist = 0

    # INSERT YOUR CODE

    ed_dist = (sum((ts1 - ts2) ** 2)) ** 0.5
    
    return ed_dist


def norm_ED_distance(ts1, ts2):
    """
    Calculate the normalized Euclidean distance.

    Parameters
    ----------
    ts1 : numpy.ndarray
        The first time series.

    ts2 : numpy.ndarray
        The second time series.

    Returns
    -------
    norm_ed_dist : float
        The normalized Euclidean distance between ts1 and ts2.
    """

    norm_ed_dist = 0

    # INSERT YOUR CODE 

    norm_ed_dist = (sum((ts1 - ts2) ** 2)) ** 0.5

    return norm_ed_dist


def DTW_distance(ts1, ts2, r=None):
    """
    Calculate DTW distance.

    Parameters
    ----------
    ts1 : numpy.ndarray
        The first time series.

    ts2 : numpy.ndarray
        The second time series.

    r : float
        Warping window size.
    
    Returns
    -------
    dtw_dist : float
        DTW distance between ts1 and ts2.
    """

    dtw_dist = 0

    # INSERT YOUR CODE

    m = len(ts1)
    D = np.zeros((m+1,m+1))
    D[0,:] = np.inf
    D[:,0] = np.inf
    D[0,0] = 0
    for i in range(0,m) :
      for j in range(0,m):
        d = (ts1[i] - ts2[j]) ** 2
        D[i+1,j+1] = d + min(D[i,j+1],D[i+1,j],D[i,j])
    dtw_dist = D[m ,m ]
    #print(D)
    return dtw_dist
