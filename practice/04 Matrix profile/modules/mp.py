import numpy as np
import pandas as pd
import math

import stumpy
from stumpy import config
from stumpy import core

def compute_mp(ts1, m, exclusion_zone=None, ts2=None):
    """
    Compute the matrix profile.

    Parameters
    ----------
    ts1 : numpy.ndarrray
        The first time series.

    m : int
        The subsequence length.

    exclusion_zone : int, default = None
        Exclusion zone.

    ts2 : numpy.ndarrray, default = None
        The second time series.

    Returns
    -------
    output : dict
        The matrix profile structure 
        (matrix profile, matrix profile index, subsequence length, 
        exclusion zone, the first and second time series).
    """
    
    # INSERT YOUR CODE

    mp = stumpy.stump(ts1.astype(float), m)

    return {'mp': mp[:, 0],
            'mpi': mp[:, 1],
            'm' : m,
            'excl_zone': exclusion_zone,
            'data': {'ts1' : ts1, 'ts2' : ts2},
            'indices': {'left' : mp[:,-2], 'right' : mp[:,-1]}
            }

def top_discords(ts, m, k=1, finite=False):
    
    excl_zone = int(np.ceil(m / config.STUMPY_EXCL_ZONE_DENOM))

    mp = stumpy.stump(ts, m)
    P = mp[:,0].astype(np.float64)

    if finite:
        P[~np.isfinite(P)] = np.NINF

    discords_idx = np.full(k, -1, dtype=np.int64)
    discords_dist = np.full(k, np.NINF, dtype=np.float64)
    discords_nn_idx = np.full(k, -1, dtype=np.int64)

    for i in range(k):
        if np.all(P == np.NINF):
            break
        mp_discord_idx = np.argmax(P)

        discords_idx[i] = mp_discord_idx
        discords_dist[i] = P[mp_discord_idx]
        discords_nn_idx[i] = mp[mp_discord_idx,1]

        core.apply_exclusion_zone(P, discords_idx[i], excl_zone, val=np.NINF)

    return {'indices': discords_idx,
            'distances': discords_dist,
            'nn_indices': discords_nn_idx
            }