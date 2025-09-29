# -d = detached / launch containers in background
# --build = force image rebuild before starting containers

DOCKERFILE_PATH = ./docker/docker-compose.yml

start:
	docker compose -f ${DOCKERFILE_PATH} up -d --build

stop: 
	docker compose -f ${DOCKERFILE_PATH} down

logs: 
	docker compose -f ${DOCKERFILE_PATH} logs -f

exec: 
	docker compose -f ${DOCKERFILE_PATH} exec bid_marketplace bash

test: 
	docker compose -f ${DOCKERFILE_PATH} exec bid_marketplace pytest

format:
	docker compose -f ${DOCKERFILE_PATH} exec bid_marketplace black .

lint:
	docker compose -f ${DOCKERFILE_PATH} exec bid_marketplace flake8 --max-line-length=120 --statistics .

safety:
	docker compose -f ${DOCKERFILE_PATH} exec bid_marketplace safety check --full-report

bandit:
	docker compose -f ${DOCKERFILE_PATH} exec bid_marketplace bandit -r auctions

coverage:
	docker compose -f ${DOCKERFILE_PATH} exec bid_marketplace sh -c "coverage run --source=auctions -m pytest && coverage report -m --include='*/auctions/views.py,*/auctions/forms.py'"