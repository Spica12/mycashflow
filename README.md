# mycashflow
MyCashFlow — backend-сервіс для обліку особистих фінансів із REST API. Забезпечує зберігання та обробку транзакцій, управління рахунками й категоріями, автоматичний розрахунок балансу. Реалізований на Python (FastAPI) і PostgreSQL, з можливістю масштабування та розширення функціоналу.





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

Додавання pytest
```bash
poetry add pytest --group test
```
