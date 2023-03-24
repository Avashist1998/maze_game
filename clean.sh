pyb clean
find . -name __pycache__ | xargs rm -rf
rm .coverage