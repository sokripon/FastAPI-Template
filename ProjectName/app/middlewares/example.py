import time

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request


class CustomMiddleWare(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Do stuff before request is handled
        start = time.process_time()
        response = await call_next(request)
        # Do stuff after request is handled
        print(time.process_time() - start, "seconds")

        return response
