from typing import TypeVar, Generic

from pydantic import BaseModel, Field
from pydantic.generics import GenericModel

DataT = TypeVar('DataT')

default_error_message = "Default error message"


class Error(BaseModel):
    id: int = Field(0, description="Error id")
    message: str = Field(default_error_message, description="Human readable error message")


class ResponseModel(GenericModel, Generic[DataT]):
    success: bool = Field(True, description="If the request was a success")


class ResponseErrorModel(ResponseModel, Generic[DataT]):
    error: Error = Field(Error(), description="Error details")


class ResponseSuccessModel(ResponseModel, Generic[DataT]):
    data: DataT


class ResponseError(ResponseErrorModel, Generic[DataT]):
    success = False


class ResponseSuccess(ResponseSuccessModel, Generic[DataT]):
    pass
