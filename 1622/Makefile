# Not really a "real" Makefile. This isn't for any sort of compilation step.
# It just makes it easy for me to run my code (I have a shortcut for "make" in
# my text editor.)
#
# Piping to tee >(tail -n1 |pbcopy) allows me to simultaneously
# - View the full output
# - Copy just the last line into my clipboard

.PHONY: run test copy-last example

SHELL=/bin/bash

run:
	@python3 b2_wip.py in.map.txt

test:
	clear
	python3 -m doctest b2_wip.py

copy-last:
	python3 b2_wip.py | tee >(tail -n1 | pbcopy)

example:
	@python3 b2_wip.py ex.map.txt
