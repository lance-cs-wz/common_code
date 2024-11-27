#!/bin/bash
set -x

tool_bin=$0
cmd=$1

usage()
{
    echo "usage:" >&2
    echo "    sh $tool_bin count_uniq_column < stdin > stdout" >&2
    echo "    sh $tool_bin random_lines < stdin > stdout" >&2
}

if [ -z "$cmd" ]; then
    usage
    exit 0
fi

count_uniq_column()
{
    awk -F'\t' ' {
                print NF;
            }
        ' \
        | uniq -c
}

random_lines()
{
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
     '
}

func()
{
    split -b 4096M -d uniq_pics.tar.gz uniq_pics.tar.gz.  # split 分割文件。-b 指定文件大小，可以为K。-d 为指定后缀数字递增。
}

run()
{
    $cmd
}

run

