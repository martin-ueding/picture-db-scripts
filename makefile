# Copyright (c) 2012 Martin Ueding <dev@martin-ueding.de>

pythonfiles := $(filter-out setup.py,$(wildcard *.py))
testfiles := $(wildcard *_test.py)

test:
	python -m doctest $(pythonfiles)
	python -m unittest $(testfiles:.py=)

html/index.html: picturerenamer
	epydoc -v $^

.PHONY: clean
clean:
	$(RM) *.pyc *.pyo
	$(RM) -r html
	$(RM) picturerenamerc
