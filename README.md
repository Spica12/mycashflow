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

У проєкті реалізовано суворе архітектурне розділення між візуальними сторінками додатку (Frontend Views) та технічними ендпоінтами для обробки даних (REST API). Це дозволяє відокремити інтерфейс від бізнес-логіки та забезпечує чистоту автоматичної документації Swagger.

### 🌐 1. Веб-інтерфейс (Frontend Views)
*Ці маршрути призначені виключно для браузера користувача. Вони не містять префіксу `/api`, обробляються модулями у папці `src/web/` та завжди повертають динамічні HTML-сторінки через рушій шаблонізації Jinja2 або виконують редіректи.*

*   **`GET /` (Головна сторінка)**
    *   **Опис:** Вітальний екран персональної системи обліку MyCashFlow.
    *   **Логіка:** Перевіряє статус підключення до бази даних PostgreSQL за допомогою асинхронного healthcheck (`SELECT 1`).
    *   **Компонент:** Рендерить шаблон `index.html`. Завдяки залежності `get_current_user_from_cookie` динамічно відображає Email авторизованого користувача справа вгорі (Navbar) або кнопки входу/реєстрації для гостей.
*   **`GET /auth/register` (Сторінка реєстрації)**
    *   **Опис:** Візуальна форма для створення нового облікового запису. Рендерить шаблон `register.html`.
*   **`GET /auth/login` (Сторінка входу)**
    *   **Опис:** Візуальна форма для автентифікації користувача. Рендерить шаблон `login.html`.
*   **`GET /auth/logout` (Вихід із системи)**
    *   **Опис:** Браузерний маршрут для завершення сесії.
    *   **Логіка:** Примусово викликає бізнес-метод анулювання сесії в БД, видаляє куку `access_token` та перенаправляє користувача на головну сторінку (`/`) зі статусом `302 Found`.

---

### ⚙️ 2. Технічне API (Backend REST API)
*Ці асинхронні ендпоінти призначені для обробки даних у фоні. Вони завжди починаються з єдиного глобального префіксу `/api`, групуються у папці `src/routers/`, працюють виключно з JSON-форматом (або OAuth2 Form Data) та автоматично документуються у Swagger UI.*

*   **`/api/auth` (Модуль автентифікації користувачів)**
    *   **`POST /api/auth/register` (Реєстрація користувача)**
        *   **Формат:** `application/json` (Pydantic-схема `UserSchema`).
        *   **Логіка:** Перевіряє унікальність Email (запобігання дублікатів ➡️ `409 Conflict`), хешує чистий пароль за допомогою сучасного алгоритму `Argon2` (`pwdlib`) та створює новий рядок у базі даних PostgreSQL із захищеним первинним ключем **UUID**.
        *   **Відповідь:** Об'єкт створеного користувача на базі `UserMyResponseSchema` (без пароля) зі статусом `201 Created`.
    *   **`POST /api/auth/login` (Авторизація та видача токенів)**
        *   **Формат:** `application/x-www-form-urlencoded` (`OAuth2PasswordRequestForm`).
        *   **Логіка:** Зчитує `username` (email) та `password`, перевіряє відповідність хешу в БД, генерує двотокенну сесію (Access + Refresh токени). Записує короткостроковий `access_token` у безпечну **HTTP-Only Cookie** для роботи фронтенду, а довготривалий `refresh_token` реєструє у таблиці `tokens` PostgreSQL через `UserRepo`.
        *   **Відповідь:** JSON-об'єкт `TokenSchema` для зовнішніх клієнтів API зі статусом `200 OK`.
    *   **`POST /api/auth/refresh` (Автоматична ротація токенів)**
        *   **Формат:** `application/json` (`RefreshTokenRequestSchema`).
        *   **Логіка:** Приймає діючий `refresh_token`, перевіряє його криптографічний підпис та наявність активної сесії в базі даних. У разі успіху реалізує **безпечну ротацію токенів**: старий токен видаляється з БД, замість нього створюється нова пара Access/Refresh токенів, а також оновлюється HTTP-Only кука в браузері.
        *   **Відповідь:** Нова пара токенів у форматі JSON зі статусом `200 OK`.
    *   **`POST /api/auth/logout` (Технічний вихід)**
        *   **Логіка:** Примусово та безповоротно видаляє запис сесії з таблиці `tokens` в PostgreSQL та очищає куки доступу.

---

### 🔄 Схема взаємодії компонентів при Авторизації (Життєвий цикл)

```text
 [Браузер Користувача] ────(Заповнення форми входу)────>  GET /auth/login  (Відображення форми)
         │
  (Клік на "Увійти")
         │
         ▼
  [JS URLSearchParams] ────(Формат Form Data)────> POST /api/auth/login (FastAPI / OAuth2)
                                                                 │
                                                    (Перевірка Argon2 Хешу у БД)
                                                                 │
                                                                 ▼
                                                    [Генерація токенів: JWT]
                                                                 │
                                                   (Запис Refresh у таблицю tokens)
                                                                 │
         ┌───────────────────────────────────────────────────────┘
         ▼
  [Установка Куки] ──────> Response: HTTP-Only Cookie ("access_token")
         │
   (JS Редірект)
         │
         ▼
 [Браузер Користувача] ──────────(Оновлення екрану)──────────> GET / (Головна сторінка)
                                                                    │
                                                      (dependencies.py розшифровує куку)
                                                                    │
                                                                    ▼
                                                       [Результат: Рендеринг шаблону]
                                                       Navbar ──> 👤 user@example.com (Справа вгорі)
```

