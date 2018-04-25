#!/usr/bin/python

import argparse
import sys


if __name__ == "__main__":
    ''' build and solve the transportation problem '''

    
    option_parser = argparse.ArgumentParser(description='Transportation problem')
    option_parser.add_argument("-v", "--verbose", action="store_true", dest="verbose", default=True) 
       
    (options, args) = option_parser.parse_args()
    
    if len(args) != 2:
        option_parser.print_help()
        sys.exit();

    startEnumeration(xrange(int(args[0])), int(args[1]));
