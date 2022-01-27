#!/bin/bash
WD=$1
KEYWORD=$2
NUM_SEARCH=$3

cd $WD/zicheng-ma-educational-website-and-courses-finder-for-keyword

source env/bin/activate
python3 src/main.py "$KEYWORD" $NUM_SEARCH 1 