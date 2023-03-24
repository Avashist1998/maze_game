#!/bin/bash 

BASE_PATH=$1
if [ -z "$1" ]
    then BASE_PATH="./"
fi

PY_FILES=`find $BASE_PATH -name "*.py" -not -path "*/site-packages/*"`

echo "yapf formatting"

for filename in $PY_FILES
do
   yapf --in-place $filename --style ./setup.cfg 
done