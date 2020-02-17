test:  # run local test suite
	python setup.py test

lint:  # run python linter
	black --line-length 80 --target-version py36 webstompy/

lint-check:  # run python linter and just check for linting
	black --line-length 80 --target-version py36 --check webstompy/
