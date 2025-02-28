install:
	python -m venv venv
	. venv/bin/activate
	pip install -r requirements.txt
	docker-compose up -d
	python liab.py build-db

rebuild-db:
	python liab.py nuke-db
	python liab.py build-db

clean:
	docker-compose down -v
	rm -rf venv
	deactivate