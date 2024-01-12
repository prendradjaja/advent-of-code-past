html:
	python3 static_visualization.py > temp.html
test:
	python3 -m doctest b.py
	env/bin/pytest --exitfirst -vv
clean:
	git checkout -- temp.html
