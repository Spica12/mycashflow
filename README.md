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
poetry add pwdlib[bcrypt, argon2] pyjwt python-jose pydantic[email]
```

- `python-multipart` обов'язковий, щоб FastAPI міг приймати дані з HTML-форм
- `pwdlib[bcrypt]` — відповідає за надійне криптографічне хешування паролів.
- `pyjwt` — знадобиться для генерації токенів авторизації.

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
docker compose run --rm app alembic downgrade -1
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


## 🗺️ Архітектура шляхів та Навігація (Routing Architecture)

У проєкті реалізовано чітке архітектурне розділення між візуальними сторінками додатку (Frontend) та технічними ендпоінтами (REST API). Це дозволяє відокремити бізнес-логіку від представлення та забезпечує чистоту автоматичної документації Swagger.

### 🌐 1. Веб-інтерфейс (Frontend Views)
*Ці маршрути призначені для браузера користувача. Вони не містять префіксу `/api`, обробляються модулями у папці `src/web/` та завжди повертають динамічні HTML-сторінки через рушій шаблонізації Jinja2.*

*   **`GET /` (Головна сторінка)**
    *   **Опис:** Вітальний екран персональної системи обліку MyCashFlow.
    *   **Компонент:** Рендерить шаблон `index.html`. Виводить опис системи та інтерактивний індикатор статусу підключення до PostgreSQL (зелена/червона плашка).
*   **`GET /auth/register` (Сторінка реєстрації)**
    *   **Опис:** Візуальна форма для створення нового облікового запису користувача.
    *   **Компонент:** Рендерить шаблон `register.html`. Містить поля для введення Email, Пароля та Дати народження.

---

### ⚙️ 2. Технічне API (Backend REST API)
*Ці маршрути є асинхронними ендпоінтами для обробки даних. Вони завжди починаються з єдиного глобального префіксу `/api`, групуються у папці `src/routers/` та працюють виключно з JSON-форматом. Відображаються у Swagger UI.*

*   **`/api/auth` (Модуль автентифікації користувачів)**
    *   **`POST /api/auth/register` (Обробка реєстрації)**
        *   **Вхідні дані:** JSON-об'єкт на базі Pydantic-схеми `UserSchema` (`email`, `password`, `birth_date`).
        *   **Логіка:**
            1. Приймає дані форми, які асинхронно відправляє JavaScript `fetch` API.
            2. Перевіряє наявність email у базі даних (запобігання дублікатів ➡️ `409 Conflict`).
            3. Безпечно хешує чистий пароль на апаратному рівні за допомогою сучасного алгоритму `Argon2` (`pwdlib`).
            4. Генерує захищений ідентифікатор **UUID** як первинний ключ та створює запис у PostgreSQL.
        *   **Вихідні дані:** JSON-об'єкт створеного користувача на базі `UserMyResponseSchema` (без пароля) зі статусом `201 Created`.

---

### 🔄 Схема взаємодії компонентів (Життєвий цикл запиту)

```text
 [Користувач] ──(Клік на Реєстрацію)──>  GET /auth/register  ──> [Повертає HTML сторінку]
      │
 (Вводить дані)
      │
      ▼
 [JS Fetch API] ──(Асинхронний JSON)──> POST /api/auth/register ──> [Перевірка у сервісах]
                                                                             │
                                                                       (Хешування + БД)
                                                                             │
                                                                             ▼
 [Браузер] <──(Редірект на /login) <───  JSON: {"id": "UUID"...} <── [Запис у PostgreSQL]
```
