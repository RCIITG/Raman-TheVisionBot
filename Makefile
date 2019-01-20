test: test_python.out
	cat test_python.out > test 
test_python.out: mmit/tests/*.py mmit/core/*.cpp mmit/core/*.h setup.py test_python.sh
bash test_python.sh
