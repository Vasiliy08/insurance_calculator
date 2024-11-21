DC=docker-compose
KAFKA=docker_compose/kafka.yaml
APP_FILE=docker_compose/app.yaml
STORAGES_FILE=docker_compose/storage.yaml
LOGS=docker logs


.PHONY: start
start:
	${DC} -f ${STORAGES_FILE} -f ${APP_FILE} -f ${KAFKA} up --build -d


.PHONY: migrate
migrate:
	${DC} -f ${STORAGES_FILE} -f ${APP_FILE} -f ${KAFKA} exec -it main-app alembic revision --autogenerate

.PHONY: upgrade
upgrade:
	${DC} -f ${STORAGES_FILE} -f ${APP_FILE} -f ${KAFKA} exec -it main-app alembic upgrade head


.PHONY: logs
logs:
	${DC} -f ${STORAGES_FILE} -f ${APP_FILE} -f ${KAFKA} logs -f


.PHONY: stop
stop:
	${DC} -f ${STORAGES_FILE} -f ${APP_FILE} -f ${KAFKA} down -v


.PHONY: test
test:
	${DC} -f ${STORAGES_FILE} -f ${APP_FILE} -f ${KAFKA} exec -it main-app pytest
