#!/bin/bash
awk ' {
        print rand() "\t" $0;
    }
 ' \
| sort \
| awk -F'\t' ' {
        out = $2;
        for (i = 3; i <= NF; i++) {
            out = out "\t" $i;
        }
        print out;
    }
 ' \
