#!/bin/bash 

BASE_PATH=$1
if [ -z "$1" ]
    then BASE_PATH="./"
fi

PY_FILES=`find $BASE_PATH -name "*.py" -not -path "*/site-packages/*"`

echo "yapf checking"

for filename in $PY_FILES
do
   yapf -d $filename --style ./setup.cfg
done


echo "mypy check"

for filename in $PY_FILES
do
    mypy $filename --config-file ./setup.cfg
done


echo "flake8 check"

for filename in $PY_FILES
do
    flake8 $filename --config ./setup.cfg
done


echo "pylint check"
for filename in $PY_FILES
do
    pylint $filename --rcfile ./setup.cfg
done


# TEST_FILES=`find $BASE_PATH -name "*.py" -path "*/tests/*" -not -path "*/site-packages/*"`
# echo "running unittest"
# for filename in $TEST_FILES
# do
#     python3 -m unittest $filename
# done
