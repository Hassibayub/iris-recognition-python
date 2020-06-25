# # # Import
import argparse
from time import time

from Extract_FEATURE import extract_feature
from matching2 import matching

##-----------------------------------------------------------------------------
###### Argument parsing
##-----------------------------------------------------------------------------
parser = argparse.ArgumentParser(description='Verify the user existance with respect to already existing users.')

parser.add_argument('-f', "--file", type=str,metavar='',
                    help="Path to the file that you want to verify.")

parser.add_argument('-d', "--temp_dir", type=str, metavar='', default="./template/",
                    help="Path to the directory containing templates.")

parser.add_argument('-t', "--thres", type=float, default=0.426, metavar='',
                    help="Threshold for matching.") # default 0.38 -> 0.426

args = parser.parse_args()
##-----------------------------------------------------------------------------
#######  Execution
##-----------------------------------------------------------------------------
# Extract feature
start = time()
print('>>> Start verifying {}\n'.format(args.file))
template, mask, file = extract_feature(args.file)

# Matching
result = matching(template, mask, args.temp_dir, args.thres)

if result == -1:
    print('>>> No registered sample.')
elif result == 0:
    print('>>> No sample matched.')
else:
    # print(result)
    print('>>> {} samples matched (descending reliability):'.format(len(result)))
    for res in result:
        print("\t", res[:-4])

# Time measure
end = time()
print('\n>>> Verification time: {} [s]\n'.format(end - start))
