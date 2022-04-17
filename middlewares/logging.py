import random
import string
import time

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from utils.logging import logger


class LoggingMiddleWare(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        midlogger = logger.bind(request_id="req")
        idem = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        midlogger.info(
            f"-> RID={idem}\tREQUEST={request.method.upper()}\tPATH={request.url.path}"
        )
        reqlogger = logger.bind(request_id=idem)
        request.state.logger = reqlogger
        start_time = time.time()
        response = await call_next(request)

        process_time = (time.time() - start_time) * 1000
        formatted_process_time = '{0:.2f}'.format(process_time)
        midlogger.info(
            f"<- RID={idem}\tREQUEST={request.method.upper()}\tPATH={request.url.path}\tSTATUS_CODE={response.status_code}\tCOMPLETED={formatted_process_time}ms"
        )

        return response
