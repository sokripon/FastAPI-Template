from typing import Optional

from requests import Response

from ProjectName.app.response.schema import Error, ResponseSuccess, ResponseError, default_error_message


def set_response_success(response: Response, data, status_code: Optional[int] = 200) -> ResponseSuccess:
    response.status_code = status_code
    return ResponseSuccess(data=data, success=True)


def set_response_error(response: Response, status_code: Optional[int] = 404, error_code: Optional[int] = 0,
                       error_message: Optional[str] = default_error_message) -> ResponseError:
    response.status_code = status_code
    error = Error(id=error_code, message=error_message)
    return ResponseError(error=error, success=False)
