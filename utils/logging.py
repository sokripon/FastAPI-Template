"""Configure handlers and formats for application loggers."""
import inspect
import logging
import sys
from pprint import pformat
from loguru import logger


class CustomLogger:
    def __init__(self):
        self.logger = logger

    def init_logging(self):
        intercept_handler = self.InterceptHandler()
        logging.getLogger("uvicorn").handlers = [intercept_handler]
        logging.getLogger("uvicorn.access").handlers = [intercept_handler]

        sys.stderr = object  # disable stderr output
        # TODO: Find the intended way to configure this

        logger.configure(
            handlers=[{"sink": sys.stdout, "level": logging.DEBUG, "format": self.format_record}]
        )

        logger.add("logs/log_{time}.log", rotation="1 days", backtrace=True, diagnose=True)


    @staticmethod
    def format_record(record: dict) -> str:
        request_id_str = record["extra"].get("request_id", "")
        request_id_str = f"[{request_id_str}] - " if request_id_str else ""
        format_string = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | " \
                        "<level>{level: <8}</level> | " \
                        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - " \
                        + request_id_str + \
                        "<level>{message}</level>"
        if record["extra"].get("payload") is not None:
            record["extra"]["payload"] = pformat(
                record["extra"]["payload"], indent=4, compact=True, width=88
            )
            format_string += "\n<level>{extra[payload]}</level>"

        format_string += "{exception}\n"
        return format_string

    class InterceptHandler(logging.Handler):
        def emit(self, record: logging.LogRecord):
            try:
                level = logger.level(record.levelname).name
            except ValueError:
                level = record.levelno

            frame, depth = logging.currentframe(), 2
            while frame.f_code.co_filename == logging.__file__:
                frame = frame.f_back
                depth += 1
            log = logger.bind(request_id='app')

            log.opt(depth=depth, exception=record.exc_info).log(
                level, record.getMessage()
            )


slogger = CustomLogger()
logger = slogger.logger
