# mycashflow
Домашній вебзастосунок ведення бухгалтерії

## Запуск

### Запустіть сервер командою в терміналі:
```bash
uvicorn main:app --reload
```

### Запуск docker-compose
```bash
docker-compose up --build
```

В браузері перейти за адресою: http://127.0.0.1:8000.


## Init virtual environment

### Virtual Env

```bash
poetry init
poetry config --local virtualenvs.in-project true
C:\Users\Vital\AppData\Local\Programs\Python\Python314\python.exe -m venv .venv
poetry env use .venv\Scripts\python.exe
poetry env activate
poetry install
```


### Бібліотеки
```bash
poetry add pytest --group test
poetry add fastapi uvicorn jinja2 python-multipart
poetry add alembic
poetry add pydantic-settings
poetry add sqlalchemy psycopg-binary asyncpg
```

- `python-multipart` обов'язковий, щоб FastAPI міг приймати дані з HTML-форм


### Migrations

```bash
alembic init alembic
alembic revision --autogenerate -m 'init'
alembic upgrade head
alembic downgrade -1

# В контейнері
docker compose up -d db
docker compose run --rm app alembic revision --autogenerate -m "Initial migration"
docker compose run --rm app alembic upgrade head
```

# GIT

- `feat`    - нова фіча (функціонал)
- `fix`	    - виправлення багу
- `chore`   - технічні зміни (gitignore, refactor без логіки)
- `refactor`- перепис коду без зміни поведінки
- `docs`    - документація


## ⚙️ Environment Variables (.env)

Для запуску проєкту потрібно створити файл `.env` у корені проєкту.

### 1. Створи файл `.env`

Скопіюй приклад:

```bash
cp .env.example .env
```

### Опис змінних

| Змінна       | Опис                                                |
| ------------ | --------------------------------------------------- |
| MODE         | Режим роботи (DEV / PROD)                           |
| DB_HOST      | Хост бази даних (localhost або docker service name) |
| DB_PORT      | Порт PostgreSQL                                     |
| DB_USER      | Користувач БД                                       |
| DB_PASSWORD  | Пароль БД                                           |
| DB_NAME      | Назва бази даних                                    |
| DATABASE_URL | Повний URL БД (опціонально, для cloud / production) |

### Як це працює
- Якщо задано `DATABASE_URL` → використовується він
- Якщо ні → URL збирається автоматично з DB_* змінних

## Запуск docker-compose
```bash
docker-compose up --build
```

## Зупинка docker-compose
```bash
docker-compose down -v
```

Оновити requirements.txt
```bash
poetry lock --no-update
poetry export --without-hashes --format=requirements.txt > requirements.txt
```
