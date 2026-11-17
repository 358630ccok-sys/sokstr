# PostgreSQL: бэкапы, роли/права и проверка восстановления

Практический runbook для администрирования PostgreSQL на уровне эксплуатации: **роли/права**, **резервное копирование**, **восстановление** и обязательная **проверка restore**.

> Цель: не просто «сделать бэкап», а убедиться, что из него **можно восстановиться**.

---

## 1) Базовая модель доступа (роли и права)

### Проверка ролей и подключений
```bash
# Список ролей
psql -U postgres -c "\du+"

# Текущие подключения
psql -U postgres -c "SELECT pid, usename, datname, client_addr, state, query_start FROM pg_stat_activity ORDER BY query_start DESC;"
```

### Принцип минимальных прав (пример)
```sql
-- Отдельная роль приложения (без суперправ)
CREATE ROLE app_user LOGIN PASSWORD 'CHANGE_ME';

-- Права только на нужную БД/схему
GRANT CONNECT ON DATABASE app_db TO app_user;
GRANT USAGE ON SCHEMA public TO app_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO app_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO app_user;

-- Отдельная роль для бэкапа (минимально необходимая)
CREATE ROLE backup_user LOGIN PASSWORD 'CHANGE_ME';
GRANT CONNECT ON DATABASE app_db TO backup_user;
GRANT USAGE ON SCHEMA public TO backup_user;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO backup_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO backup_user;
```

**Практики:**
- не использовать суперпользователя для приложений;
- хранить пароли/DSN в секретах/`.env`, а не в git;
- периодически ревизировать роли (`\du+`) и лишние привилегии.

---

## 2) Резервное копирование

### Логический бэкап одной БД (`pg_dump`)
```bash
# Рекомендуемый формат: custom (-Fc), сжатый и удобный для pg_restore
export PGPASSWORD='***'
pg_dump -h 127.0.0.1 -p 5432 -U backup_user -d app_db -Fc -f /backups/app_db_$(date +%F_%H%M).dump

# Альтернатива: plain SQL
pg_dump -h 127.0.0.1 -p 5432 -U backup_user -d app_db -Fp -f /backups/app_db_$(date +%F_%H%M).sql
```

### Бэкап всех БД/ролей кластера (`pg_dumpall`)
```bash
# Глобальные объекты (роли, tablespaces) + все базы
pg_dumpall -h 127.0.0.1 -p 5432 -U postgres -f /backups/pg_dumpall_$(date +%F_%H%M).sql

# Только глобальные объекты (роли/права)
pg_dumpall -h 127.0.0.1 -p 5432 -U postgres --globals-only -f /backups/pg_globals_$(date +%F_%H%M).sql
```

### Бэкап в Docker/контейнере
```bash
# Пример: дамп из контейнера postgres
docker exec -t <postgres_container> pg_dump -U postgres -d app_db -Fc > /backups/app_db_$(date +%F_%H%M).dump

# Пример: pg_dumpall
docker exec -t <postgres_container> pg_dumpall -U postgres > /backups/pg_dumpall_$(date +%F_%H%M).sql
```

### Рекомендации
- автоматизировать по расписанию (cron/systemd timer/CI job);
- хранить бэкапы отдельно от хоста/тома БД;
- использовать ротацию (например, daily/weekly) и контроль свободного места;
- проверять код возврата команд и логировать результат.

---

## 3) Восстановление

### Восстановление из custom dump (`pg_restore`)
```bash
# 1) Создать пустую БД для восстановления
createdb -h 127.0.0.1 -p 5432 -U postgres app_db_restore_test

# 2) Восстановить
pg_restore -h 127.0.0.1 -p 5432 -U postgres -d app_db_restore_test --clean --if-exists --no-owner --no-privileges /backups/app_db_YYYY-MM-DD_HHMM.dump
```

### Восстановление из SQL (`psql`)
```bash
createdb -h 127.0.0.1 -p 5432 -U postgres app_db_restore_test
psql -h 127.0.0.1 -p 5432 -U postgres -d app_db_restore_test -f /backups/app_db_YYYY-MM-DD_HHMM.sql
```

### Восстановление `pg_dumpall`
```bash
# Обычно выполняется в чистый кластер/инстанс (осторожно в production)
psql -h 127.0.0.1 -p 5432 -U postgres -f /backups/pg_dumpall_YYYY-MM-DD_HHMM.sql
```

---

## 4) Проверка восстановления (обязательно)

Проверка должна подтверждать, что **данные и схема доступны** после restore.

### Чеклист проверки
```bash
# 1) БД создана и доступна
psql -h 127.0.0.1 -U postgres -d app_db_restore_test -c "SELECT now();"

# 2) Схема/таблицы на месте
psql -h 127.0.0.1 -U postgres -d app_db_restore_test -c "\dt+"

# 3) Базовая валидация данных (количество записей в ключевых таблицах)
psql -h 127.0.0.1 -U postgres -d app_db_restore_test -c "SELECT 'users' AS t, count(*) FROM users;"
psql -h 127.0.0.1 -U postgres -d app_db_restore_test -c "SELECT 'events' AS t, count(*) FROM events;"

# 4) Критичные запросы приложения (smoke-check)
psql -h 127.0.0.1 -U postgres -d app_db_restore_test -c "SELECT id, created_at FROM users ORDER BY created_at DESC LIMIT 5;"

# 5) Роли/права (если восстанавливали globals)
psql -h 127.0.0.1 -U postgres -c "\du+"
```

### Критерии успешного restore-теста
- восстановление завершилось без ошибок;
- ключевые таблицы/объекты присутствуют;
- контрольные counts/запросы совпадают с ожиданиями;
- приложение может подключиться тестовым пользователем (при проверке доступа);
- результат проверки зафиксирован (дата, файл бэкапа, итог).

---

## 5) Операционные практики

- **Регулярность:** бэкапы по расписанию + периодические restore-тесты (не только создание дампа).
- **Изоляция:** отдельные учётные данные для app/backup/admin, минимальные привилегии.
- **Наблюдаемость:** логирование/алерты на ошибки бэкапа и нехватку места.
- **Безопасность:** шифрование/ограничение доступа к хранилищу бэкапов, секреты вне git.
- **Документирование:** фиксировать процедуру, расположение бэкапов и результаты тестов восстановления.
