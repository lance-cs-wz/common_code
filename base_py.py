# -*- coding:utf-8 -*-
import os
import re
import sys
import json
import time

now_time_text = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

def usage():
    sys.stderr.write("usage:\n")
    sys.stderr.write("  python3.6 %s in_file out_file\n" % sys.argv[0])


def line_file_in_pro(infile_name, outfile_name):

    with open(infile_name, "r") as in_file:
        for line in in_file:
            line = line.strip("\n")
            line_s = line.split("\t")

    with open(outfile_name, "w") as out_file:
        pass

                
def main(argv, argn):
    if argn < 3:
        usage()
        return -1

    infile_name = argv[1]
    outfile_name = argv[2]

    line_file_in_pro(infile_name, outfile_name)
    return 0

if __name__ == "__main__":
    main(sys.argv, len(sys.argv))
