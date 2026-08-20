test:
	python -m unittest discover -s tests -v

web:
	python -m secpquest.cli web

check: test
	python -m secpquest.cli list-puzzles >/dev/null
	python -m secpquest.cli point 1 >/dev/null
