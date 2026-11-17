# PostgreSQL: практический сценарий backup → restore → проверка (safe demo)

Цель: воспроизводимо отработать **логический бэкап, восстановление и проверку результата** (restore-test), не затрагивая production-данные.

> Выполнять в изолированном тестовом окружении (локальный контейнер/тестовый инстанс PostgreSQL).

## Вариант A: быстрый стенд в Docker (рекомендуется для практики)
```bash
# 1) Поднять тестовый PostgreSQL
docker run --name pg-demo -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=app_db -p 54329:5432 -d postgres:16

# 2) Создать тестовые данные
docker exec -i pg-demo psql -U postgres -d app_db <<'SQL'
CREATE TABLE IF NOT EXISTS users (id serial PRIMARY KEY, email text, created_at timestamptz default now());
INSERT INTO users(email) VALUES ('alice@example.com'), ('bob@example.com');
CREATE ROLE app_user LOGIN PASSWORD 'app_pass';
GRANT CONNECT ON DATABASE app_db TO app_user;
GRANT USAGE ON SCHEMA public TO app_user;
GRANT SELECT,INSERT,UPDATE,DELETE ON ALL TABLES IN SCHEMA public TO app_user;
SQL

# 3) Контрольные значения до бэкапа
docker exec -i pg-demo psql -U postgres -d app_db -c "SELECT count(*) AS users_count FROM users;"
docker exec -i pg-demo psql -U postgres -c "\du"

# 4) Бэкап (custom format)
mkdir -p ./backups
docker exec -t pg-demo pg_dump -U postgres -d app_db -Fc > ./backups/app_db_demo.dump

# 5) Restore в отдельную БД
docker exec -i pg-demo createdb -U postgres app_db_restore_test
cat ./backups/app_db_demo.dump | docker exec -i pg-demo pg_restore -U postgres -d app_db_restore_test --no-owner --no-privileges

# 6) Проверка восстановления (обязательно)
docker exec -i pg-demo psql -U postgres -d app_db_restore_test -c "SELECT count(*) AS users_count FROM users;"
docker exec -i pg-demo psql -U postgres -d app_db_restore_test -c "SELECT id,email FROM users ORDER BY id;"
docker exec -i pg-demo psql -U postgres -d app_db_restore_test -c "\dt"

# 7) Очистка тестового стенда
docker rm -f pg-demo
```

## Ожидаемый результат проверки
- `users_count` в `app_db_restore_test` совпадает со значением до бэкапа (в примере: `2`)
- таблица `users` и данные (`alice@example.com`, `bob@example.com`) восстановлены
- команды восстановления завершились без ошибок

## Вариант B: без Docker (локальный PostgreSQL)
```bash
# Требуются установленные psql/pg_dump/pg_restore и доступ к тестовому кластеру
createdb -U postgres app_db
psql -U postgres -d app_db -c "CREATE TABLE users(id serial primary key, email text); INSERT INTO users(email) VALUES ('alice@example.com'),('bob@example.com');"
psql -U postgres -d app_db -c "SELECT count(*) FROM users;"
pg_dump -U postgres -d app_db -Fc -f ./backups/app_db_demo.dump
createdb -U postgres app_db_restore_test
pg_restore -U postgres -d app_db_restore_test --no-owner --no-privileges ./backups/app_db_demo.dump
psql -U postgres -d app_db_restore_test -c "SELECT count(*) FROM users;"
psql -U postgres -d app_db_restore_test -c "SELECT * FROM users ORDER BY id;"
```

## Фиксация результата (рекомендуется)
- дата/время проверки
- источник бэкапа (`*.dump`/`*.sql`)
- контрольные значения до/после restore
- итог: `PASS/FAIL` и замечания
