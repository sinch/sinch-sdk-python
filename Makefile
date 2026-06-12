.PHONY: docs

docs:
	rm -rf docs/build
	rm -rf docs/api
	sphinx-apidoc --force --no-toc --maxdepth 2 --templatedir docs/_templates/apidoc -o docs/api sinch
	sphinx-build -b html docs docs/build/html
