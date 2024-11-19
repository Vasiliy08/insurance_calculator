DC=docker-compose
APP_FILE = docker_compose/app.yaml
STORAGES_FILE = docker_compose/storage.yaml
LOGS = docker logs


.PHONY: start
start:
	${DC} -f ${STORAGES_FILE} -f ${APP_FILE} up --build -d


.PHONY: migrate
migrate:
	${DC} -f ${STORAGES_FILE} -f ${APP_FILE} exec -it main-app alembic revision --autogenerate

.PHONY: upgrade
upgrade:
	${DC} -f ${STORAGES_FILE} -f ${APP_FILE} exec -it main-app alembic upgrade head


.PHONY: logs
logs:
	${DC} -f ${STORAGES_FILE} -f ${APP_FILE} logs -f


.PHONY: stop
stop:
	${DC} -f ${STORAGES_FILE} -f ${APP_FILE} down -v


.PHONY: test
test:
	${DC} -f ${STORAGES_FILE} -f ${APP_FILE} exec -it main-app pytest
