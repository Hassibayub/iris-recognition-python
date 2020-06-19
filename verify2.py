import argparse
from time import time 
import os
from os import listdir

from Extract_FEATURE import extract_feature 
from matching import matching
from matching import matchingPool

from itertools import repeat
import cv2 as cv

####### Args parser

parser = argparse.ArgumentParser()

parser.add_argument('--file', type=str, help='file you want to verify')

parser.add_argument('--temp_dir', type=str, default= './template/',help='template directory')

parser.add_argument('--thres', type=float, default=0.38, help='Threshold for matching.')

args = parser.parse_args()


####### execution

im = cv.imread('ir-eye.jpg', cv.COLOR_BGR2GRAY)
template_, mask_, image_ = extract_feature(im)

# template_, mask_, image_ = extract_feature(args.file)

TEMP_DIRECTORY = args.temp_dir

# result = matching(template_, mask_, args.temp_dir, args.thres)

n_files = len(listdir(TEMP_DIRECTORY))

if n_files == 0:
    print("return -1")


kargs = zip(
    sorted(listdir(TEMP_DIRECTORY)),
    repeat(template_),
    repeat(mask_)
    repeat(arg.temp_dir)
)

matchingPool(image_, template_, mask_, TEMP_DIRECTORY)

# for (dir_, _, fileList) in os.walk(TEMP_DIRECTORY):

#     for file in fileList:
#         # print(file)

#         # tempalte
#         if file[-12:] == 'template.npy': 
#             print(file)
        
#         # mask
#         if file[-8:] == 'mask.npy':
#             print(file)
        
#         # #image
#         # if file[-9:] == 'image.npy':
#         #     print(file)
