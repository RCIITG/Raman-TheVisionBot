test: test_python.out
	cat test_python.out > test 
test_python.out: setup.py test_python.sh
	bash test_python.sh
