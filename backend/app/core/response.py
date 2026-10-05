"""统一异常与响应"""
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError


class AppException(Exception):
    def __init__(self, code: int = 400, message: str = "请求失败", data=None):
        self.code = code
        self.message = message
        self.data = data


def success(data=None, message: str = "操作成功", msg: str = None) -> dict:
    return {"code": 200, "message": msg or message, "data": data}


def fail(code: int = 400, message: str = "操作失败") -> dict:
    return {"code": code, "message": message, "data": None}


async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=200,
        content={"code": exc.code, "message": exc.message, "data": exc.data},
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=200,
        content={
            "code": 422,
            "message": "参数校验失败",
            "data": [
                {"field": ".".join(str(loc) for loc in e["loc"][1:]), "msg": e["msg"]}
                for e in exc.errors()
            ],
        },
    )
