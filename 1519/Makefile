generate_grammar:
	python3 generate_grammar.py ex > foo.py
diff:
	make generate_grammar && git diff --no-index foo.py sandbox_ply.py
analyze:
	python3 analyze.py
run:
	./env/bin/python3 b_wip.py in
example:
	./env/bin/python3 b_wip.py med
test:
	./env/bin/python3 -m doctest b_wip.py
