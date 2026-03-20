import logging
from pathlib import Path

def setup_logger(log_file: str = "mycashflow.log"):
    # створюємо логер, даємо йому ім'я та встановлюємо рівень logging.DEBUG
    logger = logging.getLogger('logger')
    logger.setLevel(logging.DEBUG)

    # створюємо handler для виведення в консоль та встановлюємо рівень DEBUG
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # створюємо файловий handler

    PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
    LOG_DIR = PROJECT_ROOT / "logs"
    LOG_DIR.mkdir(exist_ok=True)

    file_handler = logging.FileHandler(LOG_DIR / log_file, mode="w", encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)

    # створюємо форматтер: час виведення (asctime), ім'я файлу (filename), назву функції (funcName), номер рядка (lineno), рівень (levelname) та саме повідомлення (message)
    formatter = logging.Formatter(
        '%(asctime)s - %(filename)-20s - %(funcName)-30s(%(lineno)3d) - %(levelname)s - %(message)s'
    )

    # додаємо зазначений форматтер до handler
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # додаємо handler до логера
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger

logger = setup_logger()

# приклад виконання коду
# logger.debug('debug message')
# logger.info('info message')
# logger.warning('warn message')
# logger.error('error message')
# logger.critical('critical message')
