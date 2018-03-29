#!/bin/bash

# Author : Peng Xu
# Script follows here:

# Argument is unset or set to the empty string
# if [ -z "{$@}" ];
# then
#    echo "Please type directory name as argument -> sh test.sh [directory]"
#    echo "This shell script will automatically test all .in and .out files"
#    exit
# fi
rm -r test/*.in
rm -r test/*.out
mkdir test

a=0

while [ $a -lt 1 ]
do
   echo "Generating BoardTest-$a.in file..."
   boardTest="test/BoardTest-$a.in"
   python3 ./generateTestCaese.py > $boardTest
   a=`expr $a + 1`
   cat $boardTest
done


# FILES=$@/*.in
FILES=test/*.in
for f in $FILES
do
  # take action on each file. $f store current file name
  filename=$(basename "$f")
  # Filename without extension
  fname="${filename%.*}"

  # input="$fname.in"
  # output="$fname.out"
  ouput="test/$fname.out"
  echo "Generating $fname.out file..."
  python3 ./main.py < ./$f > $ouput
  cat $ouput

done
