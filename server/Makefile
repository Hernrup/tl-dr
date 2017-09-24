.PHONY: lint run run-debug logs shell stop clean migrate


build:
	docker-compose build server

test: test-flake test-unit

test-watch: test-flake
	docker-compose run --rm server ptw

test-unit:
	docker-compose run --rm server pytest

test-flake:
	docker-compose run --rm server flake8 /src

run:
	docker-compose up -d server

logs:
	docker-compose logs -f

shell:
	docker-compose exec server bash

db-init:
	docker-compose run --rm app python3 db_create.py
	docker-compose run --rm app python3 db_upgrade.py

db-upgrade:
	docker-compose run --rm app python3 db_upgrade.py

db-create-migration:
	docker-compose run --rm app python3 db_migrate.py

stop:
	docker-compose stop

clean: reset-containers
	@echo "Clearing state..."

reset-containers:
	@echo "Stopping any running containers..."
	@if [ -n "`docker ps -q`" ]; then docker stop `docker ps -q`; fi

	@echo "Removing containers..."
	@if [ -n "`docker ps -qa`" ]; then docker rm `docker ps -a -q`; fi

	@echo "Removing dangling images..."
	@if [ -n "`docker images -qaf dangling=true`" ]; then docker rmi -f `docker images -q -a -f dangling=true`; fi
