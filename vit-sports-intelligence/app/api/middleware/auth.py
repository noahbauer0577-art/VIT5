# app/api/middleware/auth.py
import os
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY", "dev_api_key_12345")
_auth_env = os.getenv("AUTH_ENABLED", "").lower()
# Auto-enable auth when a real API key has been configured and AUTH_ENABLED is not
# explicitly set to "false"
if _auth_env == "true":
    AUTH_ENABLED = True
elif _auth_env == "false":
    AUTH_ENABLED = False
else:
    # Auto-detect: enable if the key is non-default
    AUTH_ENABLED = API_KEY not in ("dev_api_key_12345", "", "your_api_key_here")

# Only enforce auth on these API route prefixes — everything else is static frontend
_PROTECTED_PREFIXES = (
    "/analytics", "/history", "/predict", "/result",
    "/training", "/ai", "/odds", "/ai-feed",
)


class APIKeyMiddleware(BaseHTTPMiddleware):
    """
    API Key authentication middleware.
    Only enforces on known API routes — never on static frontend files.
    """

    async def dispatch(self, request: Request, call_next):
        if not AUTH_ENABLED:
            return await call_next(request)

        path = request.url.path

        # Always allow: health probes, docs, admin (has own _verify_key), and
        # anything that is NOT a known API route (i.e. static frontend files)
        always_open = ("/health", "/docs", "/openapi.json", "/redoc", "/favicon.ico")
        if path in always_open or path.startswith("/admin"):
            return await call_next(request)

        # Pass static frontend assets through without auth
        if not any(path.startswith(pfx) for pfx in _PROTECTED_PREFIXES):
            return await call_next(request)

        api_key = request.headers.get("x-api-key")

        if not api_key:
            raise HTTPException(
                status_code=401,
                detail="Missing API key. Please provide x-api-key header"
            )

        if api_key != API_KEY:
            raise HTTPException(
                status_code=401,
                detail="Invalid API key"
            )

        return await call_next(request)


async def verify_api_key(request: Request):
    """Dependency for route-level API key validation"""
    if not AUTH_ENABLED:
        return True

    api_key = request.headers.get("x-api-key")

    if not api_key:
        raise HTTPException(status_code=401, detail="Missing API key")

    if api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

    return True
