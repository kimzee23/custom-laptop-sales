from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from src.domain.exception.base import DomainException
from src.domain.exception.exceptions import UserAlreadyExistsException

async def domain_exception_handler(request: Request, exc: DomainException):
    if isinstance(exc, UserAlreadyExistsException):
        return JSONResponse(
            status_code=200,
            content={
                "statusCode": 200,
                "message": exc.message,
                "data": exc.data,
                "successful": True
            }
        )
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "statusCode": exc.status_code,
            "message": exc.message,
            "data": exc.data,
            "successful": exc.status_code < 400
        }
    )

async def http_exception_handler(request: Request, exc: HTTPException):
    if isinstance(exc.detail, dict):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "statusCode": exc.status_code,
                "message": exc.detail.get("message", "Request failed"),
                "data": exc.detail.get("data", {}),
                "successful": exc.detail.get("successful", False),
                **exc.detail
            }
        )
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "statusCode": exc.status_code,
            "message": str(exc.detail),
            "data": {},
            "successful": False
        }
    )

async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "statusCode": 500,
            "message": "An unexpected internal server error occurred.",
            "data": {"error": str(exc)},
            "successful": False
        }
    )
