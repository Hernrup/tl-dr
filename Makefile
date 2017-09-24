.PHONY: lint run run-debug logs shell stop clean migrate

build:
	make -C ./client build
	make -C ./server build

run:
	docker-compose up -d server client nginx

logs:
	docker-compose logs -f

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
