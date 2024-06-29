import uvicorn
from fastapi import FastAPI
from app.crud.user import auth
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response


class CrossOriginResourcePolicyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        response = await call_next(request)
        response.headers["Cross-Origin-Resource-Policy"] = "strict-origin-when-cross-origin"
        return response


app = FastAPI()
origins = [
    # List of allowed origins, you can add more origins as needed
    "*",
]

# CORSMiddleware to allow all origins, methods, headers, and credentials
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
    expose_headers=["Content-Disposition"]
)


app.include_router(auth)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
