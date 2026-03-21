.PHONY: install rebuild-db run-services stop-services clean-services clean test

install:
	poetry install
	$(MAKE) run-services
	poetry run liab build-db

rebuild-db:
	poetry run liab nuke-db
	poetry run liab build-db

run-services:
	docker compose up -d

stop-services:
	docker compose down

clean-services:
	docker compose down -v

clean:
	$(MAKE) clean-services

test:
	poetry run pytest tests/ -v
