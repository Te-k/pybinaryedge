PWD = $(shell pwd)

check:
	flake8
	ruff check -q .
	mypy pybinaryedge

clean:
	rm -rf $(PWD)/build $(PWD)/dist $(PWD)/pybinaryedge.egg-info

dist:
	python3 setup.py sdist bdist_wheel

upload:
	python3 -m twine upload dist/*

test-upload:
	python3 -m twine upload --repository testpypi dist/*
