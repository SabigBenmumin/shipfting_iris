import cv2
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.spatial import distance
from scipy import stats
from concurrent.futures import ThreadPoolExecutor

def read_image(img_path):   # read and return RGB image
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    return img

def shiftbits_ham(template, noshifts): # get template, number of shift -> return new template as an shifted bits
    templatenew = np.zeros(template.shape)
    width = template.shape[1]
    s = 2 * np.abs(noshifts)
    p = width - s

    # if no shift is needed, return original tamplate
    if noshifts == 0:
        templatenew = template
    
    # if the shift is negative, shift the bits to the left
    elif noshifts < 0: #ซ้าย
        x = np.arange(p)
        templatenew[:, x] = template[:, s - x]
        x = np.arange(p, width)
        templatenew[:, x] = template[:, x - p]
    
    # if the shift is positive, shift the bits to the right
    else: #จริงๆแล้วเป็นขวา
        x = np.arange(s, width)
        templatenew[:, x] = template[:, x - s]
        x = np.arange(s)
        templatenew[:, x] = template[:, p + x]

    return templatenew

def HammingDistance(template1, template2):
    hd = np.nan

    hd_all = [] # contain all hamming distance every shift

    bitsdiff_arr = np.empty(17, dtype=np.float64)
    totalbits_arr = np.empty(17, dtype=np.float64)

    for i, shifts in enumerate(range(-8, 9)):
        template1s = shiftbits_ham(template1, shifts)
    
        totalbits_arr[i] = template1s.size

        C = np.logical_xor(template1s, template2)
        bitsdiff_arr[i] = np.sum(C == 1)

    for i, totalbits in enumerate(totalbits_arr):
        if totalbits == 0:
            hd = np.nan
        else:
            hd1 = bitsdiff_arr[i] / totalbits

            hd_all.append(hd1)

            # select the minimum hamming distance
            if hd1 < hd or np.isnan(hd):
                hd = hd1

    return hd, hd_all

def jaccard_distance(template1, template2):
    # Flatten the templates to 1D arrays
    template1_flat = template1.flatten()
    template2_flat = template2.flatten()

    # Calculate Jaccard distance
    dist = distance.jaccard(template1_flat, template2_flat)
    
    return dist

def jaccard_distance_shifted(template1, template2):
    jaccard_distances = []

    for shifts in range(-8, 9):
        template1_shifted = shiftbits_ham(template1, shifts)
        dist = jaccard_distance(template1_shifted, template2)
        jaccard_distances.append(dist)

    return jaccard_distances

def pearson_correlation(template1, template2):
    # Flatten the templates to 1D arrays
    template1_flat = template1.flatten()
    template2_flat = template2.flatten()

    # Calculate Pearson correlation coefficient
    corr, _ = stats.pearsonr(template1_flat, template2_flat)
    
    return corr

def pearson_correlation_shifted(template1, template2):
    correlations = []

    for shifts in range(-8, 9):
        template1_shifted = shiftbits_ham(template1, shifts)
        corr = round(pearson_correlation(template1_shifted, template2), 12)
        correlations.append(corr)

    return correlations