#!/bin/bash 

BASE_PATH=$1
if [ -z "$1" ]
    then BASE_PATH="./"
fi

PY_FILES=`find $BASE_PATH -name "*.py" -not -path "*/site-packages/*"`

echo "yapf formatting"
yapf --in-place $PY_FILES --style ./setup.cfg 
