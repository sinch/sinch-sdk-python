.PHONY: docs

docs:
	rm -rf docs/build
	rm -rf docs/api
	sphinx-build -b html docs docs/build/html
