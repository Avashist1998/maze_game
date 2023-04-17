#!/bin/bash 

BASE_PATH=$1
if [ -z "$1" ]
    then BASE_PATH="./"
fi

PY_FILES=`find $BASE_PATH -name "*.py" -not -path "*/site-packages/*"`

echo "yapf checking"
yapf -d $PY_FILES --style ./setup.cfg

echo "mypy check"
mypy $PY_FILES --config-file ./setup.cfg --ignore-missing-imports

echo "flake8 check"
flake8 $PY_FILES --config ./setup.cfg --count --statistics

echo "pylint check"
pylint $PY_FILES --rcfile ./setup.cfg
