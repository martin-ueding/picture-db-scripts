# Copyright (c) 2012-2013 Martin Ueding <dev@martin-ueding.de>

pythonfiles := $(filter-out setup.py,$(wildcard *.py)) hashtag
testfiles := $(wildcard *_test.py)

all:
	@echo "Nothing interesting to do, you can run “make install”."

test:
	python -m doctest $(pythonfiles)
	python -m unittest $(testfiles:.py=)

doc:
	./sphinx html


install:
	python setup.py install --root "$(DESTDIR)" --install-layout=deb

.PHONY: clean
clean:
	$(RM) *.pyc *.pyo
	$(RM) -r build
	$(RM) -r dist
	$(RM) -r html
	$(RM) hashtagc
