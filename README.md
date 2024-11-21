## Задача

Реализовать REST API сервис по расчёту стоимости страхования в зависимости от типа груза и объявленной стоимости (ОС).

## Требования

- [x] Сервис должен посчитать стоимость страхования для запроса, используя актуальный тариф (загружается через API).
- [x] Сервис возвращает (объявленную стоимость * rate) в зависимости от указанного в запросе типа груза и даты.
- [x] Сервис должен разворачиваться внутри Docker.
- [x] Сервис должен разрабатываться через GIT (файл README с подробным описанием развертывания).
- [x] Данные должны храниться в базе данных.

### Обновлённые требования

- [x] Добавить удаление и редактирование тарифов в crud
- [x] Добавить логирование через батч в kafka
- [x] В сообщение отправляем айди пользователь(если есть), сообщение о действие (что за целевое действие), время события.

## Технологии

- [x] Используется FastAPI как фреймворк.
- [x] Используется SQLAlchemy как ORM.
- [x] Используется PostgreSQL, MySQL или SQLite (на выбор).
- [x] Используется Docker.
- [x] Используется Docker Compose с Docker для PostgreSQL.

## Инстукция

1. Наличие docker и docker-compose.
2. Наличие make (Опционально).


## Установка

 **Клонируйте репозиторий:**

   ```bash
   git clone https://github.com/Vasiliy08/insurance_calculator.git
   ```

## Запуск приложения с использованием Makefile

* `make start` - Запуск приложения.
* `make migrate` - Создание миграции для alembic (alembic revision --autogenerate).
* `make upgrade` - Апгрейд (alembic upgrade head)
* `make logs` - Просмотр логов.
* `make stop` - Остановка приложения с удалением вольюмов.
* `make test` - Запуск тестов.


## Запуск приложения без Makefile

Если вы не хотите использовать `Makefile`, вы можете выполнить те же команды вручную, используя `docker-compose`:

* `docker-compose -f docker_compose/storage.yaml -f docker_compose/app.yaml up --build -d` - Запуск приложения.
* `docker-compose -f docker_compose/storage.yaml -f docker_compose/app.yaml exec -it main-app alembic revision --autogenerate` - Создание миграции для alembic (alembic revision --autogenerate).
* `docker-compose -f docker_compose/storage.yaml -f docker_compose/app.yaml exec -it main-app alembic upgrade head` - Апгрейд (alembic upgrade head)
* `docker-compose -f docker_compose/storage.yaml -f docker_compose/app.yaml logs -f` - Просмотр логов.
* `docker-compose -f docker_compose/storage.yaml -f docker_compose/app.yaml down -v` - Остановка приложения.
* `docker-compose -f docker_compose/storage.yaml -f docker_compose/app.yaml exec -it main-app pytest` - Запуск тестов.


## API Документация

Документация API доступна по [адресу](http://127.0.0.1:8000/api/docs).
Kafka UI доступен по [адресу](http://localhost:8090/).
