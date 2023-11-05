import numpy as np

from modules.utils import *


def top_k_motifs(matrix_profile, top_k=3):
    """
    Find the top-k motifs based on matrix profile.

    Parameters
    ---------
    matrix_profile : dict
        The matrix profile structure.

    top_k : int
        Number of motifs.

    Returns
    --------
    motifs : dict
        Top-k motifs (left and right indices and distances).
    """

    motifs_idx = []
    motifs_dist = []

    # INSERT YOUR CODE
    motifs_dist = np.sort(matrix_profile['mp'])[:top_k]
    motifs_idx = []
    motifs_idx_left = []
    motifs_idx_right = []
    for dist in motifs_dist:
      min_mp = np.where(matrix_profile['mp']==dist,matrix_profile['mpi'],None)
      idxs = min_mp[min_mp != np.array(None)]
      for i in idxs:
        if i not in motifs_idx:
          motifs_idx.append(i)
          idx_i = np.where(matrix_profile['mpi']==i)[0][0]
          motifs_idx_left.append(matrix_profile['indices']['left'][idx_i])
          motifs_idx_right.append(matrix_profile['indices']['right'][idx_i])
    return {
            "indices" : np.array([motifs_idx_left,motifs_idx_right]).T,
            "distances" : motifs_dist
            }
