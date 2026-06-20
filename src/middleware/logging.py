import time
import logging
from fastapi import Request

logger = logging.getLogger("mycashflow")


async def log_requests(request: Request, call_next):
    start = time.time()
    status = 500

    ip = request.client.host if request.client else "unknown"

    try:
        response = await call_next(request)
        status = response.status_code
        return response

    except Exception:
        logger.exception(f"Request failed: {request.method} {request.url.path}")
        raise

    finally:
        duration = round((time.time() - start) * 1000, 2)

        logger.info(
            f"{request.method} {request.url.path} "
            f"status={status} "
            f"{duration}ms "
            f"ip={ip}"
        )
