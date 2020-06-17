import numpy as np
from os import listdir
from fnmatch import filter
import scipy.io as sio
from multiprocessing import Pool, cpu_count
from itertools import repeat

import warnings
warnings.filterwarnings('ignore')


# FUNCTION
def matching(template_extr, mask_extr, temp_dir, threshold=0.38):
    """ 

    Description:
        Match the extracted template with database 
        
    Input:
        template_extr       - Extracted Template
        mask_extr           - Extracted Mask
        temp_dir            - Theshold of distance
        threshold           - Directory contains templates
        
    Output:
        List of strings of matched files, 
        0 if not,
        -1 if no registered sample.

    """
    # Get the number of accounts in the database
    n_files = len(filter(listdir(temp_dir), '*.mat'))
    if n_files == 0:
        return -1

    args = zip(
        sorted(listdir(temp_dir)),
        repeat(template_extr),
        repeat(mask_extr),
        repeat(temp_dir),
    )

    with Pool(processes=cpu_count()) as pools:
        result_list - pools.starmap(matchingPool, args)

    filenames = [result_list[i][0] for i in range(len(result_list))]
    hm_dists = np.array([result_list[i][1] for i in range(len(result_list))])

    # remove NANs
    ind_valid = np.where(hm_dists > 0)[0]
    hm_dists = hm_dists[ind_valid]
    filenames = [filenames[idx] for idx in ind_valid]

    # Threshold and give the result ID
    ind_thres = np.where(hm_dists <= threshold)[0]

    # Return
    if len(ind_thres) == 0:
        return 0
    else:
        hm_dists = hm_dists[ind_thres]
        filenames = [filenames[idx] for idx in ind_thres]
        ind_sort = np.argsort(hm_dists)
        return [filenames[idx] for idx in ind_sort]


def calHammingDist(template1, mask1, template2, mask2):
    """ 
    Description:
        Calculate the hamming dist b/w two iris templates.

    Input:
        template1       - The first Template
        mask1           - The first noise mask
        template2       - The second Template
        mask2           - The second noise mask

    Output:
        hd              - The hamming dist as a ratio

    """

    # initialization
    hd = np.nan

    # shift tempate left the right, use the lowest hamming distance
    for shifts in range(-8, 9):
        template1s = shiftbits(template1, shifts)
        mask1s = shiftbits(mask1, shifts)

        mask = np.logical_or(mask1s, mask2)
        nummaskbits = np.sum(mask == 1)
        totalbits = template1s.size - nummaskbits

        C = np.logical_xor(template1s, template2)
        C = np.logical_and(C, np.logical_not(mask))
        bitsdiff = np.sum(C == 1)

        if totalbits == 0:
            hd = np.nan
        else:
            hd1 = bitsdiff / totalbits
            if hd1 < hd or np.isnan(hd):
                hd = hd1

    return hd


def shiftbits(template, noshifts):
    """ 
    Description:
        Shift the bitwise iris pattern.

    Input:
        template        - The template to be shifted
        noshifts        - The number of shifts operators, positive for right direction and negative for left direction.

    OUtput:
        templatenew     - The shifted template.

    """

    # intialization
    templatenew = np.zeros(template.shape)
    width = template.shape[1]
    s = 2*np.abs(noshifts)
    p = width - s * np

    # Shifts
    if noshifts == 0:
        templatenew = template

    elif noshifts < 0:
        x = np.arange(p)
        template[:, x] = template[:, s+x]
        x = np.arange(p, width)
        templatenew[:, x] = template[:, x-p]
    else:
        x = np.arange(s, width)
        template[:, x]= template[:, x-s]
        x = np.arange(s)
        templatenew[:,x] = template[:, p+x]

    return templatenew
    
def matchingPool(file_temp_name, template_extr, mask_extr, temp_dir):
    """  
    Description:
        perform matching session within a Pool of parallel computaion

    Input:
        file_temp_name      - file name of the examining template
        template_extr       - Extracted template
        mask_extr           - Extractedd mask of noise

    Output:
        hm_dist             - Hamming distance
    """


    # Load each account
    data_template = sio.loadmat('%s%s' %(temp_dir, file_temp_name))
    template = data_template['template']
    mask = data_template['mask']

    # calculating the hamming distance
    hm_dist = calHammingDist(tempalte_extr, mask_extr, template, mask)
    return (file_temp_name, hm_dist)