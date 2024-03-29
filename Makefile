# This file is part of thumbor-distributed-collage-filter.
# https://github.com/globocom/thumbor-distributed-collage-filter

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2018, Globo.com <thumbor@corp.globo.com>

# lists all available targets
list:
	@sh -c "$(MAKE) -p no_targets__ | awk -F':' '/^[a-zA-Z0-9][^\$$#\/\\t=]*:([^=]|$$)/ {split(\$$1,A,/ /);for(i in A)print A[i]}' | grep -v '__\$$' | grep -v 'make\[1\]' | grep -v 'Makefile' | sort"
# required for list
no_targets__:

# install all dependencies (do not forget to create a virtualenv first)
setup:
	@pip install -U -e .\[tests\]
	@pre-commit install

# test your application (tests in the tests/ directory)
test: unit

unit:
	@coverage run --branch `which nosetests` -vv --with-yanc -s tests/
	@coverage report -m --fail-under=80

run:
	@thumbor -c ./tests/thumbor.conf -d -lDEBUG

# show coverage in html format
coverage-html: unit
	@coverage html

# run tests against all supported python versions
tox:
	@tox

format:
	@black .

publish:
	@python setup.py sdist
	@twine upload dist/*

#docs:
	#@cd thumbor_distributed_collage_filter/docs && make html && open _build/html/index.html
