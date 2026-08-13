from typing import Any
from uuid import uuid4

from fastapi import FastAPI, Request

from willimakeit.context import request_id_context


def register_request_id_middleware(app: FastAPI):
    app.middleware("http")(assign_request_id)


async def assign_request_id(request: Request, call_next: Any):
    request_id = str(uuid4())
    request.state.request_id = request_id
    request_id_context.set(request_id)
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response
