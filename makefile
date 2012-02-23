# Copyright (c) 2012 Martin Ueding <dev@martin-ueding.de>

pythonfiles := $(filter-out setup.py,$(wildcard *.py)) picturerenamer hash-tags
testfiles := $(wildcard *_test.py)

test:
	python -m doctest $(pythonfiles)
	python -m unittest $(testfiles:.py=)

doc: html/index.html

html/index.html: $(pythonfiles)
	epydoc -v $^

.PHONY: clean
clean:
	$(RM) *.pyc *.pyo
	$(RM) -r html
	$(RM) picturerenamerc
