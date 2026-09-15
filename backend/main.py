import os

from acustica import router as acustica_router
from catalogo import router as catalogo_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import router
from seed import seed_database

# Cria as tabelas e, se o banco estiver vazio, popula o catálogo. Na Vercel o
# banco começa vazio (e o SQLite temporário de /tmp some quando a função
# reinicia): sem isso a calculadora não teria sistemas para oferecer.
seed_database()

# Na Vercel o site e a API dividem o mesmo domínio e a API atende em /api. A
# Vercel entrega o caminho com o /api, então as rotas precisam existir com o
# prefixo. No computador a API continua sem prefixo, em localhost:8000.
PREFIXO_API = "/api" if os.getenv("VERCEL") else ""


def montar_app(prefixo: str = PREFIXO_API) -> FastAPI:
    app = FastAPI(
        title="AcousticBuild API",
        version="1.0.0",
        docs_url=f"{prefixo}/docs",
        redoc_url=f"{prefixo}/redoc",
        openapi_url=f"{prefixo}/openapi.json",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:5173",
            "http://127.0.0.1:5173",
            "http://localhost:3000",
            "http://127.0.0.1:3000",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(router, prefix=prefixo)
    app.include_router(acustica_router, prefix=prefixo)
    app.include_router(catalogo_router, prefix=prefixo)

    @app.get(f"{prefixo}/")
    def root():
        return {"message": "AcousticBuild API está no ar."}

    return app


app = montar_app()
