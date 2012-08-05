# Copyright (c) 2012 Martin Ueding <dev@martin-ueding.de>

pythonfiles := $(filter-out setup.py,$(wildcard *.py)) hashtag
testfiles := $(wildcard *_test.py)

all:
	@echo "Nothing interesting to do, you can run “make install”."

test:
	python -m doctest $(pythonfiles)
	python -m unittest $(testfiles:.py=)

doc: html/index.html

html/index.html: $(pythonfiles)
	epydoc -v $^

.PHONY: clean
clean:
	$(RM) *.pyc *.pyo
	$(RM) -r build
	$(RM) -r dist
	$(RM) -r html
	$(RM) hashtagc
