import numpy as np
from os import listdir
from fnmatch import filter
import scipy.io as sio 

import warnings
warnings.filterwarnings('ignore')

#### Function
def matching(template_extr, mask_extr, temp_dir, threshold=0.38): # threshold 0.38 -> 0.426
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
        0   if not,
        -1  if no registered sample.
    """


    n_files = len(filter(listdir(temp_dir), '*.mat'))
    if n_files == 0:
        return -1

    files = filter(listdir(temp_dir), '*.mat')
    # print("files:", files)
    # print("template_extr: ", template_extr)
    # print("mask_extr: ", mask_extr)

    result_list = []
    for file in files:
        result_list.append(matchingPool(file, template_extr, mask_extr, temp_dir))

    """ getting zero hamming distance is no good because it is for any ideal condition, so we are removing it. """

    filenames = [result_list[i][0] for i in range(len(result_list))]
    hm_dists = np.array([result_list[i][1] for i in range(len(result_list))])

    #-------------------------------------------
    # print()
    # for name_, dist_ in result_list:
    #     if dist_ == 0:
    #         print(">>>> User {} FOUND!".format(name_[:-4]), '\n')
    # print("result_list: ", result_list)
    # print("hm_dists: ", hm_dists)
    # print("filenames: ", filenames)
    #-------------------------------------------

    # print(np.where(hm_dists>0)[0])  # returns non zero array. [0] != first element only

    # remove NANs
    ind_valid = np.where(hm_dists > 0)[0]
    hm_dists = hm_dists[ind_valid]
    # print("hm_dists NANs removed: ", hm_dists)
    filenames = [filenames[idx] for idx in ind_valid] # filenames of the non zero files
    # print(filenames)

    ind_thres = np.where(hm_dists <= threshold)[0]  # hamming distance greater than the threshold are removed
    # print("ind_thres: ", ind_thres)   # number samples left

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
        Calculate the Hamming distance between two iris templates.

    Input:
        template1   - The first template.
        mask1       - The first noise mask.
        template2   - The second template.
        mask2       - The second noise mask.

    Output:
        hd          - The Hamming distance as a ratio.
    """
    # Initialize
    hd = np.nan

    # Shift template left and right, use the lowest Hamming distance
    for shifts in range(-8,9):
        template1s = shiftbits(template1, shifts)
        mask1s = shiftbits(mask1, shifts)

        mask = np.logical_or(mask1s, mask2)
        nummaskbits = np.sum(mask==1)
        totalbits = template1s.size - nummaskbits

        C = np.logical_xor(template1s, template2)
        C = np.logical_and(C, np.logical_not(mask))
        bitsdiff = np.sum(C==1)

        if totalbits==0:
            hd = np.nan
        else:
            hd1 = bitsdiff / totalbits
            if hd1 < hd or np.isnan(hd):
                hd = hd1

    # Return
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

    # Initialize
    templatenew = np.zeros(template.shape)
    width = template.shape[1]
    s = 2 * np.abs(noshifts)
    p = width - s

    # Shift
    if noshifts == 0:
        templatenew = template

    elif noshifts < 0:
        x = np.arange(p)
        templatenew[:, x] = template[:, s + x]
        x = np.arange(p, width)
        templatenew[:, x] = template[:, x - p]

    else:
        x = np.arange(s, width)
        templatenew[:, x] = template[:, x - s]
        x = np.arange(s)
        templatenew[:, x] = template[:, p + x]

    # Return
    return templatenew
    
def matchingPool(file_temp_name, template_extr, mask_extr, temp_dir):
    """
    Description:
        Perform matching session within a Pool of parallel computation

    Input:
        file_temp_name  - File name of the examining template
        template_extr   - Extracted template
        mask_extr       - Extracted mask of noise

    Output:
        hm_dist         - Hamming distance
    """

    # print("temp_dir: ", temp_dir)
    # print("file_temp_name: ", file_temp_name)

    # Load each account
    data_template = sio.loadmat('%s%s'% (temp_dir, file_temp_name))
    template = data_template['template']
    mask = data_template['mask']

    # Calculate the Hamming distance
    hm_dist = calHammingDist(template_extr, mask_extr, template, mask)
    # print("hm_dist "+str(file_temp_name)+": \t"  , hm_dist)
    
    return (file_temp_name, hm_dist)   

