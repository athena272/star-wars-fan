"""Star Wars Fan API - FastAPI app and Cloud Functions (2nd gen) entrypoint."""

from fastapi import FastAPI

from api.routers import films, people, planets, starships

app = FastAPI(
    title="Star Wars Fan API",
    description="API for Star Wars data (SWAPI) with filters, sort, and correlated queries.",
    version="1.0.0",
)

app.include_router(films.router)
app.include_router(people.router)
app.include_router(planets.router)
app.include_router(starships.router)


@app.get("/")
def root() -> dict:
    """Health and API info."""
    return {
        "name": "Star Wars Fan API",
        "version": "1.0.0",
        "docs": "/docs",
        "resources": ["/films", "/people", "/planets", "/starships"],
    }


@app.get("/health")
def health() -> dict:
    """Health check for API Gateway / load balancer."""
    return {"status": "ok"}


def cloud_function_handler(request):
    """Entrypoint for Google Cloud Functions (2nd gen) HTTP trigger.
    Forwards Flask-like request to FastAPI app via ASGI and returns response.
    """
    from starlette.testclient import TestClient
    path = (request.path or "/").strip()
    if not path.startswith("/"):
        path = "/" + path
    if request.query_string:
        path += "?" + request.query_string
    body = request.get_data()
    headers = {k: v for k, v in request.headers}
    client = TestClient(app)
    response = client.request(
        request.method,
        path,
        content=body,
        headers=headers,
    )
    # Return tuple (body, status_code, headers) for Functions Framework
    resp_headers = dict(response.headers)
    resp_headers.pop("content-length", None)
    resp_headers.pop("transfer-encoding", None)
    return (response.content, response.status_code, resp_headers)


# For local run: uvicorn api.main:app --reload
# For Cloud Functions: set main.py as entrypoint and use functions_framework
# Alternative: use Request/Response adapter so a single function receives the request
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.main:app", host="0.0.0.0", port=8080)
