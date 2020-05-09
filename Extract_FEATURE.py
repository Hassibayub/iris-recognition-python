from cv2 import imread
import cv2 as cv
from segmentation import segment
from normalization import normalize
from encode import encode

# Segmentation parameters
eyelashes_thres = 80

# Normalisation parameters
radial_res = 20
angular_res = 240

# Feature encoding parameters
minWaveLength = 18
mult = 1
sigmaOnf = 0.5


def extract_feature(image, eyelashes_thres = eyelashes_thres, use_multiprocess = False):
    
    img = imread(image, cv.IMREAD_GRAYSCALE)

    ciriris, cirpupil, imwithnoise = segment(img, eyelashes_thres, use_multiprocess)

    polar_array, noise_array = normalize(imwithnoise, ciriris[1], ciriris[0], ciriris[2],cirpupil[1], cirpupil[0], cirpupil[2],radial_res, angular_res)

    template, mask = encode(polar_array, noise_array, minWaveLength, mult, sigmaOnf)

    return template, mask, image



### debugging

img = './iris-eye.jpg'
temp, mask, image = extract_feature(img)

print('temp: ', temp), '\n\n\n'
print('mask: ', mask), '\n\n\n'
print('image: ', image, '\n\n\n')
