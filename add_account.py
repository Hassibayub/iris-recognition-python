import argparse
import os 
from time import time
from time import sleep
import matplotlib.pyplot as plt
import numpy as np
from scipy.io import savemat

from Extract_FEATURE import extract_feature

##-----------------------------------------------------------------------------
###### Argument parsing
##-----------------------------------------------------------------------------


parser = argparse.ArgumentParser(description='Add new user to accounts. flag "--name" to add name')
parser.add_argument('-n', '--name', type=str, metavar='',  required=True, help='Name of the user')
parser.add_argument('-f', '--file', type=str, metavar='',  required=True, help='Name of the user')

exclusive = parser.add_mutually_exclusive_group()
exclusive.add_argument('-v', '--verbose', action='store_true', help='print Verbosse')

args = parser.parse_args()

##-----------------------------------------------------------------------------
###### verbose prints
##-----------------------------------------------------------------------------


def verbose_print():
    print(f"User name '{args.name}' add to account! ",'\n')
    sleep(0.1)
    print("Specified folder generated successfully",'\n')
    sleep(0.1)
    print("Segmentation completed successfully",'\n')
    sleep(0.1)
    print("Normalization completed successfully",'\n')
    sleep(0.1)
    print("Encoded pattern generated successfully",'\n')
    sleep(0.1)
    print("Encoded pattern saving to disk...",'\n')
    sleep(0.1)
    print("Encoded pattern saved sucessfully",'\n')
    sleep(0.1)
    print("All processed completed sucessfully",'\n')
    sleep(0.1)

##-----------------------------------------------------------------------------
###### Create username folder and save npy files. (create template folder)
##-----------------------------------------------------------------------------


def save_file(template, mask, image, username):
    BASE_DESTINITION = os.path.abspath(os.path.dirname(__file__))       # C:\Users\user\Documents\Python Scripts\Iris Recognition\complete iris rec system
    SAVE_DESTINATION = os.path.join(BASE_DESTINITION, 'template/')

    # create template folder if not exists
    if not os.path.isdir(SAVE_DESTINATION):
        print('TEMPLATE FOLDER DO NOT EXISTS')
        os.mkdir(SAVE_DESTINATION)

    # create haseeb name folder
    USERNAME_FOLDER = os.path.join(SAVE_DESTINATION, username)
    if not os.path.isdir(USERNAME_FOLDER):
        print("USER NAME FOLDER DO NOT EXISTS")
        os.mkdir(USERNAME_FOLDER)
    

    basename = os.path.basename(username)
    print("basebname: ", basename)
    outfile = os.path.join(SAVE_DESTINATION, "%s.mat" % (basename) )
    savemat(outfile, mdict={ 'template': template, 'mask':mask})



    ######## numpy save deprecated 👇

    # ## save template npy files to USERNAME FOLDER
    # user_template = os.path.join(USERNAME_FOLDER, 'haseeb_template')
    # np.save(user_template, arr= template)
    
    # ## save mask npy files to USERNAME FOLDER
    # user_mask = os.path.join(USERNAME_FOLDER, 'haseeb_mask')
    # np.save(user_mask, arr= mask)

    # ## save image npy files to USERNAME FOLDER
    # user_image = os.path.join(USERNAME_FOLDER, 'haseeb_image')
    # np.save(user_image, arr= image)


##-----------------------------------------------------------------------------
###### extract feature and save
##-----------------------------------------------------------------------------
    

if args.verbose:
    start_time = time()

    template, mask, image = extract_feature(args.file)
    

    # verbose
    save_file(template, mask, image, args.name)
    verbose_print()

    end_time = time() - start_time

    print("Total time taken {:.2f} sec".format(end_time))
else:

    start_time = time() # start elapsed time
    
    template , mask, image  = extract_feature(args.file)

    """  
    types:
        image       - Name of the file (ie: ir-eye.jpg)
        mask        - numpy (binary dense matrix)
        templare    - numpy (binary dense matrix)
        username    - args.name person name (string ie: haseeb)

    """
     
    
    save_file(template, mask, image, args.name)
    
    print("User Added.!")

    end_time = time() - start_time # calculate elapsed time.
    print("Total time taken {:.2f} sec".format(end_time)) # print elapsed time.

