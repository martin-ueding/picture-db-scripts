# Copyright (c) 2012 Martin Ueding <dev@martin-ueding.de>

html/index.html: picturerenamer
	epydoc -v $^

.PHONY: clean
clean:
	$(RM) *.pyc *.pyo
	$(RM) -r html
	$(RM) picturerenamerc
