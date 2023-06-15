'''
Ever wanted to use tree to display the structure of a directory tree and include file sizes? me too. 
With the command `tree -h -s <dir> > <outfile>` you can produce a simple tree as desired, but each directory also gets a size, but its not the size of the directory, so its not useful.  
This script will remove those entries. 
Specifically, it removes all instances of [...] where ... is only numeric.  That means that if you didnt set the -h flag in your call to tree, this will remove all entries. 

USAGE: python remove-dir-sizes.py <file>
'''

import re
import sys

# Regular expression pattern to match the desired strings within square brackets
pattern = r'\[\s*([\d]+)\]..'

# Check if the input file is provided as a command-line argument
if len(sys.argv) < 2:
    print('Please provide the input file name as a command-line argument.')
    sys.exit(1)

input_file = sys.argv[1]

# Read the content of the input file
with open(input_file, 'r') as file:
    lines = file.readlines()

# Modify the lines in memory
modified_lines = []
for line in lines:
    modified_line = re.sub(pattern, '', line)
    modified_lines.append(modified_line)

# Write the modified lines back to the input file
with open(input_file, 'w') as file:
    file.writelines(modified_lines)

print('Modifications completed in file:', input_file)

