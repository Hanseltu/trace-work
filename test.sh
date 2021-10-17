#!/bin/sh
filename=$1
echo "the filename is ${filename}"
/usr/local/gcc-8.1/bin/gcc -o0 -fprofile-arcs -ftest-coverage ${filename}.c -o $filename
./$filename
/usr/local/gcc-8.1/bin/gcov ${filename}.c
rm ${filename}.gcda $filename ${filename}.gcno csmith.h.gcov platform_generic.h.gcov safe_math.h.gcov
