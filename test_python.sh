set -o errexit
set -o pipefail
python setup.py test | tee test_python.out
