import os
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

def configure_session(app: FastAPI):
    secret_key = os.getenv("SESSION_SECRET_KEY")

    if not secret_key:
        raise RuntimeError("Chave de sessão não configurada")

    app.add_middleware(
        SessionMiddleware,
        secret_key=secret_key,
        same_site="lax",
        https_only=False
    )