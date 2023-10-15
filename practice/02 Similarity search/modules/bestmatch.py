import numpy as np
import copy

from modules.utils import *
from modules.metrics import *


class BestMatchFinder:
    """
    Base Best Match Finder.
    
    Parameters
    ----------
    query : numpy.ndarrray
        Query.
    
    ts : numpy.ndarrray
        Time series.
    
    excl_zone_denom : float, default = 1
        The exclusion zone.
    
    top_k : int, default = 3
        Count of the best match subsequences.
    
    normalize : bool, default = True
        Z-normalize or not subsequences before computing distances.
    
    r : float, default = 0.05
        Warping window size.
    """

    def __init__(self, ts, query=None, exclusion_zone=1, top_k=3, normalize=True, r=0.05, bestmatch = {}):

        self.query = copy.deepcopy(np.array(query))
        if (len(np.shape(ts)) == 2): # time series set
            self.ts = ts
        else:
            self.ts = sliding_window(ts, len(query))

        self.excl_zone_denom = exclusion_zone
        self.top_k = top_k
        self.normalize = normalize
        self.r = r


    def _apply_exclusion_zone(self, a, idx, excl_zone):
        """
        Apply an exclusion zone to an array (inplace).
        
        Parameters
        ----------
        a : numpy.ndarrray
            The array to apply the exclusion zone to.
        
        idx : int
            The index around which the window should be centered.
        
        excl_zone : int
            Size of the exclusion zone.
        
        Returns
        -------
        a: numpy.ndarrray
            The array which is applied the exclusion zone.
        """
        
        zone_start = max(0, idx - excl_zone)
        zone_stop = min(a.shape[-1], idx + excl_zone)
        a[zone_start : zone_stop + 1] = np.inf

        return a


    def _top_k_match(self, distances, m, bsf, excl_zone):
        """
        Find the top-k match subsequences.
        
        Parameters
        ----------
        distances : list
            Distances between query and subsequences of time series.
        
        m : int
            Subsequence length.
        
        bsf : float
            Best-so-far.
        
        excl_zone : int
            Size of the exclusion zone.
        
        Returns
        -------
        best_match_results: dict
            Dictionary containing results of algorithm.
        """
        
        data_len = len(distances)
        top_k_match = []

        distances = np.copy(distances)
        top_k_match_idx = []
        top_k_match_dist = []

        for i in range(self.top_k):
            min_idx = np.argmin(distances)
            min_dist = distances[min_idx]

            if (np.isnan(min_dist)) or (np.isinf(min_dist)) or (min_dist > bsf):
                break

            distances = self._apply_exclusion_zone(distances, min_idx, excl_zone)

            top_k_match_idx.append(min_idx)
            top_k_match_dist.append(min_dist)

        return {'index': top_k_match_idx, 'distance': top_k_match_dist}


    def perform(self):

        raise NotImplementedError


class NaiveBestMatchFinder(BestMatchFinder):
    """
    Naive Best Match Finder.
    """
    
    def __init__(self, ts=None, query=None, exclusion_zone=1, top_k=3, normalize=True, r=0.05, bestmatch={}):
        super().__init__(ts, query, exclusion_zone, top_k, normalize, r, bestmatch={})


    def perform(self):
        """
        Perform the best match finder using the naive algorithm.
        
        Returns
        -------
        best_match_results: dict
            Dictionary containing results of the naive algorithm.
        """
        N, m = self.ts.shape
        self.bestmatch = {}
        bsf = float("inf")
        
        if (self.excl_zone_denom is None):
            excl_zone = 0
        else:
            excl_zone = int(np.ceil(m / self.excl_zone_denom))
        
        # INSERT YOUR CODE
        dist_list = []
        r = self.r
        data = copy.deepcopy(self.ts)
        qery_len = len(self.query)
        bsf = float("inf")
        query = z_normalize(self.query)
        #print(N,m,excl_zone,self.excl_zone_denom)
        for i in range(0,N - qery_len,self.excl_zone_denom):
          #print(self.query)
          #print(data[i:i+qery_len][0])
          
          dist = DTW_distance(query, z_normalize(data[i:i+qery_len][0]), r)
          if dist < bsf:
            bsf = dist
            dist_list.append(bsf)
          else: 
            dist_list.append(dist)

        print(dist_list)
        bsf = float("inf")
        self.bestmatch = self._top_k_match( dist_list, m, bsf, excl_zone)
        return self.bestmatch


class UCR_DTW(BestMatchFinder):
    """
    UCR-DTW Match Finder.
    """
    
    def __init__(self, ts=None, query=None, exclusion_zone=1, top_k=3, normalize=True, r=0.05):
        super().__init__(ts, query, exclusion_zone, top_k, normalize, r)


    def _LB_Kim(self, subs1, subs2):
        """
        Compute LB_Kim lower bound between two subsequences.
        
        Parameters
        ----------
        subs1 : numpy.ndarrray
            The first subsequence.
        
        subs2 : numpy.ndarrray
            The second subsequence.
        
        Returns
        -------
        lb_Kim : float
            LB_Kim lower bound.
        """

        lb_Kim = 0

        # INSERT YOUR CODE

        lb_Kim =  ((subs1[0] - subs2[0]) ** 2 + (subs1[-1] - subs2[-1]) ** 2) ** 0.5
   
        return lb_Kim


    def _LB_Keogh(self, subs1, subs2, r):
        """
        Compute LB_Keogh lower bound between two subsequences.
        
        Parameters
        ----------
        subs1 : numpy.ndarrray
            The first subsequence.
        
        subs2 : numpy.ndarrray
            The second subsequence.
        
        r : float
            Warping window size.
        
        Returns
        -------
        lb_Keogh : float
            LB_Keogh lower bound.
        """
        
        lb_Keogh = 0

        # INSERT YOUR CODE
        m = np.shape(subs1)[0]
        r = int(r*m)

        for i in range(m):
          start = max(0, i - r)
          stop = min(m, i + r + 1)
          u = np.max(subs2[start:stop])
          l = np.min(subs2[start:stop])
          c = subs1[i]
          #print(u,c,l)
          if c > u:
            lb_Keogh += (c - u)**2
            #print(lb_Keogh)
          elif c < l:
            lb_Keogh += (c - l)**2
            #print(lb_Keogh)

        return lb_Keogh


    def perform(self):
        """
        Perform the best match finder using UCR-DTW algorithm.
        
        Returns
        -------
        best_match_results: dict
            Dictionary containing results of UCR-DTW algorithm.
        """
        N, m = self.ts.shape
        
        bsf = float("inf")
        
        if (self.excl_zone_denom is None):
            excl_zone = 0
        else:
            excl_zone = int(np.ceil(m / self.excl_zone_denom))
        
        self.lb_Kim_num = 0
        self.lb_KeoghQC_num = 0
        self.lb_KeoghCQ_num = 0
        
        # INSERT YOUR CODE

        dist_list = []
        r = self.r*m
        ts = copy.deepcopy(self.ts)
        query = z_normalize(copy.deepcopy(self.query))
        qery_len = len(self.query)
        
        
        bsf = float("inf")
        for i in range(0,N - qery_len,self.excl_zone_denom):
          #bsf = float("inf")
          C =  z_normalize(ts[i:i+qery_len][0])
          
          if self._LB_Keogh(query,C,  r) < bsf:
            #print('_LB_Keogh2',self._LB_Keogh(query,C,  r), bsf)
            
            if self._LB_Keogh(C,query,  r) < bsf:
              #print('_LB_Keogh1',self._LB_Keogh(C,query,  r), bsf)
              
              if self._LB_Kim(C, query) < bsf:
                #print('_LB_Kim',self._LB_Kim(C, query), bsf)
                dist = DTW_distance(query, C, self.r)
                #print(dist)
                if dist < bsf:
                  bsf = dist
              else: 
                self.lb_Kim_num += 1
                #print('_LB_Kime',self._LB_Kim(C, query), bsf)
                dist = float("inf")
            else: 
              self.lb_KeoghQC_num += 1
              #print('_LB_Keogh1e',self._LB_Keogh(C,query,  r), bsf)
              dist = float("inf")
          else: 
            self.lb_KeoghCQ_num += 1
            #print('_LB_Keogh2e',self._LB_Keogh(query,C,  r), bsf)
            dist = float("inf")
          dist_list.append(dist)
        bsf = float("inf")
        #print(dist_list)
        self.bestmatch = self._top_k_match( dist_list, m, bsf, excl_zone)

        return {'index' : self.bestmatch['index'],
                'distance' : self.bestmatch['distance'],
                'lb_Kim_num': self.lb_Kim_num,
                'lb_KeoghCQ_num': self.lb_KeoghCQ_num,
                'lb_KeoghQC_num': self.lb_KeoghQC_num
                }
