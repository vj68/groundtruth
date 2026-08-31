"""Google Cloud Functions entry point for the GroundTruth FastAPI application.

Cloud Functions supplies a Flask request object.  The small adapter below forwards
that request to the exact same ASGI app used by Cloud Run, preserving one product
implementation and one set of routes.
"""

from __future__ import annotations

from collections.abc import Iterator

import functions_framework
import httpx
from flask import Request, Response

from app.main import app


def _headers(request: Request) -> Iterator[tuple[str, str]]:
    """Forward end-to-end headers while allowing the test transport to set Host."""

    for name, value in request.headers.items():
        if name.lower() not in {"content-length", "host"}:
            yield name, value


@functions_framework.http
def groundtruth_web(request: Request) -> Response:
    """Serve GroundTruth through a first-generation HTTP function."""

    transport = httpx.ASGITransport(app=app)
    path = request.full_path.rstrip("?")

    async def invoke() -> httpx.Response:
        async with httpx.AsyncClient(
            transport=transport,
            base_url="https://groundtruth.local",
            follow_redirects=False,
        ) as client:
            return await client.request(
                request.method,
                path,
                content=request.get_data(),
                headers=dict(_headers(request)),
            )

    import asyncio

    upstream = asyncio.run(invoke())
    excluded = {"content-encoding", "content-length", "transfer-encoding", "connection"}
    response_headers = [
        (name, value)
        for name, value in upstream.headers.multi_items()
        if name.lower() not in excluded
    ]
    return Response(upstream.content, status=upstream.status_code, headers=response_headers)
