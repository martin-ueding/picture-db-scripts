# Copyright © 2012 Martin Ueding <dev@martin-ueding.de>

pythonfiles := $(wildcard *.py)

test:
	python -m doctest $(pythonfiles)
