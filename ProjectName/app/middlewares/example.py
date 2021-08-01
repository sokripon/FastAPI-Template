from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request


class CustomMiddleWare(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Do stuff before request is handled
        response = await call_next(request)
        # Do stuff after request is handled
        return response
