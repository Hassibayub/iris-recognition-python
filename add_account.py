import argparse
import os 
from time import time
from time import sleep
import matplotlib.pyplot as plt

from Extract_FEATURE import extract_feature


parser = argparse.ArgumentParser(description='Add new user to accounts. flag "--name" to add name')
parser.add_argument('-n', '--name', type=str, metavar='',  required=True, help='Name of the user')
parser.add_argument('-f', '--file', type=str, metavar='',  required=True, help='Name of the user')

exclusive = parser.add_mutually_exclusive_group()
exclusive.add_argument('-v', '--verbose', action='store_true', help='print Verbosse')

args = parser.parse_args()


def gen_file(template, mask, image, username):

    plt.imshow(template, cmap='gray')
    plt.show()
    plt.imshow(mask, cmap='gray')
    plt.show()

    print(image)
    print(username)
    
    


if args.verbose:
    start_time = time()

    template, mask, image = extract_feature(args.file)
    
    gen_file(template, mask, image, args.name)

    # verbose
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

    end_time = time() - start_time

    print("Total time taken {:.2f} sec".format(end_time))
else:
    extract_feature(args.file)
    print("User Added")

