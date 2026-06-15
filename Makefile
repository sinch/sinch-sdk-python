.PHONY: docs

docs:
	rm -rf docs/build
	rm -rf docs/api
	sphinx-apidoc --force --separate --no-toc --maxdepth 2 \
		--templatedir docs/_templates/apidoc -o docs/api sinch \
		"sinch/core/models/base_model.py" \
		"sinch/core/models/utils.py" \
		"sinch/core/deserializers.py" \
		"sinch/core/endpoint.py" \
		"sinch/core/enums.py" \
		"sinch/core/types.py" \
		"sinch/*/api/v1/internal" "sinch/*/api/v1/internal/*" \
		"sinch/*/api/v1/base" "sinch/*/api/v1/base/*" \
		"sinch/*/models/v1/internal" "sinch/*/models/v1/internal/*" \
		"sinch/*/sinch_events/v1/internal" "sinch/*/sinch_events/v1/internal/*" \
		"sinch/domains/numbers/models/v1/utils" "sinch/domains/numbers/models/v1/utils/*" 
	sphinx-build -b html docs docs/build/html
