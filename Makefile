help:
	@echo "Usage:"
	@echo "    make help        show this message"
	@echo "    make init        create virtual environment and install dependencies (include --dev)"
	@echo "    make setup       do migrations and collect static files"
	@echo "    make activate    enter virtual environment"
	@echo "    make test        run the test suite"
	@echo "    exit             leave virtual environment"

init:
	pip install pipenv
	pipenv install --dev --three

setup:
	pipenv run python ./manage.py migrate
	pipenv run python ./manage.py collectstatic
	cp testproject/settings.py.sample testproject/settings.py
	sed -i -e "s/SECRET_KEY = '.*'/SECRET_KEY = '_'/" testproject/settings.py

activate:
	pipenv shell

test:
	pipenv run coverage erase
	pipenv run ./manage.py test
	pipenv run coverage run ./manage.py test
	pipenv run coverage report

.PHONY: help activate test
