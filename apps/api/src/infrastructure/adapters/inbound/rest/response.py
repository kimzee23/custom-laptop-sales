from typing import Any, Optional, Dict
from fastapi.responses import JSONResponse

def api_response(
    data: Any = None,
    message: str = "Operation completed successfully.",
    status_code: int = 200,
    successful: bool = True
) -> Dict[str, Any]:
    return {
        "statusCode": status_code,
        "message": message,
        "data": data if data is not None else {},
        "successful": successful
    }

def json_envelope_response(
    data: Any = None,
    message: str = "Operation completed successfully.",
    status_code: int = 200,
    successful: bool = True
) -> JSONResponse:
    content = api_response(data=data, message=message, status_code=status_code, successful=successful)
    return JSONResponse(status_code=status_code, content=content)
