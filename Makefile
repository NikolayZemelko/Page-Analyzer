myname = $(whoami)

install:
	poetry install

lint:
	poetry run flake8 page_analyzer

test:
	poetry run pytest

test-coverage:
	poetry run pytest --cov=page_analyzer --cov-report xml

dev:
	poetry run flask --app page_analyzer.app:app --debug run

PORT ?= 8000
start:
	sudo -u postgres createuser --createdb $(myname)
	sudo -u postgres createdb --owner=$(myname) pageAnalyzerTest
	createdb pageAnalyzerTest
	sudo -u postgres psql -c "ALTER USER postgres PASSWORD '!Fromakorise1977';"
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer.app:app