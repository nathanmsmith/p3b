# NAME: Dawei Huang, Nathan Smith 
# EMAIL: daweihuang@ucla.edu, nathan.smith@ucla.edu
# ID: 304792166, 704787554

default: make

make:
	cp lab3b.py lab3b
	chmod +x lab3b lab3b.py

clean:
	rm -f lab3b lab3b-304792166.tar.gz

dist: clean
	tar -zcvf lab3b-304792166.tar.gz Makefile README lab3b.py