.PHONY: build test unit-test unit-test-watch e2e lint run logs shell stop, clean

build:
	docker-compose build client

rebuild-app:
	docker-compose run --rm client yarn build

run:
	docker-compose up -d client

logs:
	docker-compose logs -f client

shell:
	docker-compose exec client bash

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

