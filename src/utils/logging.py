import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

def setup_logging():

    logger = logging.getLogger("mycashflow")
    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    if logger.handlers:
        return logger

    Path("logs").mkdir(exist_ok=True)
    log_file = Path("logs") / "mycashflow.log"
    log_file.write_text("", encoding="utf-8")

    formatter = logging.Formatter(
        "%(asctime)s - %(filename)-20s - %(funcName)-30s(%(lineno)3d) - %(levelname)s - %(message)s"
    )

    # console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # APP file handler
    app_file_handler = RotatingFileHandler(
        filename=log_file,
        maxBytes=5 * 1024 * 1024,
        backupCount=3,
        mode="w",   # <-- щоб лог файл перезаписувався
        encoding="utf-8"
    )
    app_file_handler.setLevel(logging.INFO)
    app_file_handler.setFormatter(formatter)
    logger.addHandler(app_file_handler)

    # UVICORN file handler (ОКРЕМИЙ)
    uvicornlog_file = Path("logs") / "uvicorn.log"
    uvicornlog_file.write_text("", encoding="utf-8")

    uvicorn_file_handler = RotatingFileHandler(
        filename=uvicornlog_file,
        maxBytes=5 * 1024 * 1024,
        backupCount=3,
        mode="w",   # <-- щоб лог файл перезаписувався
        encoding="utf-8"
    )
    uvicorn_file_handler.setLevel(logging.INFO)
    uvicorn_file_handler.setFormatter(formatter)

    for name in ("uvicorn.error", "uvicorn.access"):
        uv_logger = logging.getLogger(name)
        uv_logger.setLevel(logging.INFO)

        if not uv_logger.handlers:
            uv_logger.addHandler(uvicorn_file_handler)

    return logger


logger = setup_logging()

# приклад виконання коду
# logger.debug('debug message')
# logger.info('info message')
# logger.warning('warn message')
# logger.error('error message')
# logger.critical('critical message')


# Потім у будь-якому модулі:

# from logger import logger

# logger.info("User logged in")
# logger.warning("Account not found")
# logger.error("Database connection failed")

# або, якщо не хочеш імпортувати готовий об'єкт:

#import logging

#logger = logging.getLogger("mycashflow")
#Це більш "правильний" підхід для великих проєктів.
