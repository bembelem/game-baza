import json
import logging
from pathlib import Path
from typing import Callable

from openapi_core import OpenAPI
from openapi_core.contrib.starlette import StarletteOpenAPIRequest, StarletteOpenAPIResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

logger = logging.getLogger(__name__)


class ContractViolationError(Exception):
    """Raised when a response violates the API contract."""
    pass


class OpenAPIValidationMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, spec_path: Path, strict: bool = True):
        super().__init__(app)
        self.openapi = OpenAPI.from_file_path(str(spec_path))
        self.strict = strict

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Validate request
        openapi_request = StarletteOpenAPIRequest(request)
        request_result = self.openapi.unmarshal_request(openapi_request)

        if request_result.errors:
            if self.strict:
                error_messages = [str(e) for e in request_result.errors]
                return Response(
                    content=json.dumps({
                        "code": "VALIDATION_ERROR",
                        "message": "Request validation failed",
                        "details": {"errors": error_messages}
                    }),
                    status_code=400,
                    media_type="application/json"
                )
            else:
                # Log but continue in non-strict mode
                logger.warning(f"Request validation errors: {request_result.errors}")

        # Process the request
        response = await call_next(request)

        # Validate response
        openapi_response = StarletteOpenAPIResponse(response)
        response_result = self.openapi.unmarshal_response(
            openapi_request, openapi_response
        )

        if response_result.errors:
            # Response validation failures are always bugs in our code
            logger.error(f"Response validation failed: {response_result.errors}")
            if self.strict:
                raise ContractViolationError(
                    f"Response does not match spec: {response_result.errors}"
                )

        return response