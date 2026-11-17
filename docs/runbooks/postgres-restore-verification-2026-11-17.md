# PostgreSQL Restore Verification — результат (2026-11-17)

Фактический прогон сценария `backup → restore → проверка` в **изолированном тестовом окружении** (k3s lab, отдельный namespace), без затрагивания production-сервисов/данных.

## Метаданные
- **Дата/время:** 2026-11-17
- **Окружение:** Proxmox CT200 `k8s-lab` (временно запущен для теста и остановлен после), k3s namespace `pg-demo`
- **Образ PostgreSQL:** `postgres:16` (временный pod `pg-demo`)
- **БД источник:** `app_db`
- **БД восстановления:** `app_db_restore_test`
- **Тип бэкапа:** `pg_dump -U postgres -d app_db -Fc -f /tmp/app_db_demo.dump`

## Выполненные шаги
- [x] Создан временный namespace/pod PostgreSQL (`pg-demo`)
- [x] Созданы тестовая таблица и данные (`users`: 2 записи)
- [x] Зафиксированы контрольные значения до бэкапа
- [x] Выполнен бэкап (`pg_dump -Fc`)
- [x] Создана отдельная БД для восстановления
- [x] Выполнено восстановление (`pg_restore --no-owner --no-privileges`)
- [x] Выполнены проверки после restore (count, выборка, `\dt`)
- [x] Временные ресурсы удалены (`namespace pg-demo`), CT200 возвращён в состояние `stopped`

## Контрольные значения
| Проверка | До бэкапа | После restore | Совпадение |
|---|---:|---:|:---:|
| `SELECT count(*) FROM users;` | 2 | 2 | ✅ |
| Выборка `id,email` (`alice@example.com`, `bob@example.com`) | совпадает | совпадает | ✅ |
| Наличие таблицы (`\dt` → `public.users`) | да | да | ✅ |

## Ключевой вывод (фрагмент)
```text
===BEFORE_BACKUP===
 users_count 
-------------
           2

 id |       email       
----+-------------------
  1 | alice@example.com
  2 | bob@example.com

===BACKUP===
-rw-r--r-- 1 root root 3.3K Nov 17 16:13 /tmp/app_db_demo.dump

===RESTORE===

===AFTER_RESTORE===
 users_count 
-------------
           2

 id |       email       
----+-------------------
  1 | alice@example.com
  2 | bob@example.com

         List of relations
 Schema | Name  | Type  |  Owner   
--------+-------+-------+----------
 public | users | table | postgres

===SUMMARY===
before=2
after_restore=2
```

## Итог
- **Статус:** PASS ✅
- **Вывод:** бэкап успешно создан, восстановление в отдельную БД выполнено, контрольные данные и схема подтверждены после restore.
- **Примечание:** тест выполнен в изолированном временном окружении; секреты/приватные данные не использовались и не фиксировались.
