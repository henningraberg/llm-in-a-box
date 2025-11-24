install:
	python3 -m venv venv
	. venv/bin/activate; \
	pip install -r requirements.txt; \
	$(MAKE) run-services; \
	python3 liab.py build-db

rebuild-db:
	python3 liab.py nuke-db
	python3 liab.py build-db

run-services:
	docker compose up -d

clean-services:
	docker compose down -v

clean-venv:
	source deactivate
	rm -rf venv

clean:
	$(MAKE) clean-services
	$(MAKE) clean-venv
