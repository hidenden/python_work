#!/usr/bin/python3

import getopt
import sys

def showhow():
    print("getopt_sample [-c][-r][-u][-d] <pattern>")
    sys.exit(1)

def getopt_sample():
    if len(sys.argv[1:]) == 0:
        showhow()

    shortopts = "crud"
    try:
        opts, args = getopt.getopt(sys.argv[1:], shortopts)
    except getopt.GetoptError:
        showhow()
        
    print(opts)
    print(args)


if __name__ == '__main__':
    getopt_sample()
    sys.exit(0)
