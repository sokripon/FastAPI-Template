import logging
import random
import string
import time

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

log = logging.getLogger("uvicorn")


class CustomMiddleWare(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        idem = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        user_ip = request.client.host
        cf_ip = request.headers.get('cf-connecting-ip')
        if user_ip in ["127.0.0.1", "localhost", "0.0.0.0"] and cf_ip:
            user_ip = request.headers.get('cf-connecting-ip')
        log.info(
            f"->RID={idem}\tREQUEST={request.method.upper()}\tPATH={request.url.path}\tIP={user_ip}"
        )
        start_time = time.time()
        response = await call_next(request)

        process_time = (time.time() - start_time) * 1000
        formatted_process_time = '{0:.2f}'.format(process_time)
        log.info(
            f"<-RID={idem}\tREQUEST={request.method.upper()}\tPATH={request.url.path}\tSTATUS_CODE={response.status_code}\tCOMPLETED={formatted_process_time}ms"
        )

        return response
