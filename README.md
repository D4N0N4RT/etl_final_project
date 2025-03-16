# Итоговый проект по ETL-процессам

## Запуск

### Описание сервисов из docker-compose
В docker-compose файле описаны следующие сервисы, необходимые для работы системы:
- **airflow-postgres** - контейнер с СУБД PostgreSQL, необходимый для хранения служебных данных из Airflow.
- **airflow-init** - контейнер, в котором запускается процесс инициализации Airflow.
- **postgres** - контейнер с СУБД PostgreSQL, в которой будут храниться основные данные приложения.
- **mongo** - контейнер с СУБД MySQL, в которой будут храниться основные данные приложения.
- **database-data-init** - контейнер со скриптом на языке Python, который генерирует данные для 
коллекций в MongoDB с использованием библиотеки Faker.
- **airflow-webserver** - контейнер, в котором запускается вэб-сервер Airflow.
- **airflow-scheduler** - контейнер с шэдулером Airflow, который выполняет описанные DAG'и по расписанию.
### Поднятие сервисов
Чтобы запустить все описанные сервисы, выполните:
```bash
docker compose up
```

---

## Airflow

### Вход в Airflow
Перейдите по адресу: [http://localhost:8080/](http://localhost:8080/).  
Используйте следующие учетные данные для входа:
- **Логин:** `admin`
- **Пароль:** `admin`

### Описание созданных DAG в Airflow

#### 1. **`user_sessions_etl_replication`**
- Периодичность: **ежедневно**.
- Функциональность:
  - Репликация данных коллекции **user_sessions** из MongoDB в таблицу PostgreSQL.

#### 2. **`product_price_history_etl_replication`**
- Периодичность: **ежедневно**.
- Функциональность:
  - Репликация данных коллекции **product_price_history** из MongoDB в таблицу PostgreSQL.

#### 3. **`event_logs_etl_replication`**
- Периодичность: **ежедневно**.
- Функциональность:
  - Репликация данных коллекции **event_logs** из MongoDB в таблицу PostgreSQL.

#### 4. **`support_tickets_etl_replication`**
- Периодичность: **ежедневно**.
- Функциональность:
  - Репликация данных коллекции **support_tickets** из MongoDB в таблицу PostgreSQL.

#### 5. **`user_recommendations_etl_replication`**
- Периодичность: **ежедневно**.
- Функциональность:
  - Репликация данных коллекции **user_recommendations** из MongoDB в таблицу PostgreSQL.

#### 6. **`moderation_queue_etl_replication`**
- Периодичность: **ежедневно**.
- Функциональность:
  - Репликация данных коллекции **moderation_queue** из MongoDB в таблицу PostgreSQL.

#### 7. **`search_queries_etl_replication`**
- Периодичность: **ежедневно**.
- Функциональность:
  - Репликация данных коллекции **search_queries** из MongoDB в таблицу PostgreSQL.
---
