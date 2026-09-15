"""Publicação na Vercel.

Lá o site e a API dividem o mesmo domínio: a API atende em /api, e a Vercel
entrega o caminho original ao FastAPI, sem remover o /api. Estes testes
garantem que o mesmo código responde sem prefixo no computador e com /api na
Vercel, e que o banco e o link de senha seguem a configuração do ambiente.
"""
import importlib
import os
import sys

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import database  # type: ignore
import recuperacao  # type: ignore
from main import montar_app  # type: ignore

CALCULO = {
    "tipo_analise": "aereo", "cenario": "parede_entre_unidades", "sistema_codigo": "PAR-CER-014",
    "area_elemento": 15, "volume_receptor": 36, "reverberacao": 0.6, "l1": 85,
}


def test_na_vercel_as_rotas_ficam_em_api():
    client = TestClient(montar_app("/api"))
    assert client.get("/api/materiais").status_code == 200
    assert client.post("/api/acustica/calcular", json=CALCULO).status_code == 200
    assert client.get("/api/").status_code == 200
    # sem o prefixo não existe nada: o site é que atende esses caminhos lá
    assert client.get("/materiais").status_code == 404


def test_no_computador_continua_sem_prefixo():
    client = TestClient(montar_app(""))
    assert client.get("/materiais").status_code == 200
    assert client.post("/acustica/calcular", json=CALCULO).status_code == 200


def _limpar_ambiente(monkeypatch):
    for variavel in ("DATABASE_URL", "POSTGRES_URL", "VERCEL"):
        monkeypatch.delenv(variavel, raising=False)


@pytest.mark.parametrize("entrada,esperado", [
    ("postgres://u:s@host/db", "postgresql+psycopg://u:s@host/db"),
    ("postgresql://u:s@host/db?sslmode=require", "postgresql+psycopg://u:s@host/db?sslmode=require"),
    ("postgresql+psycopg://u:s@host/db", "postgresql+psycopg://u:s@host/db"),
])
def test_endereco_do_postgres_e_normalizado(monkeypatch, entrada, esperado):
    _limpar_ambiente(monkeypatch)
    monkeypatch.setenv("DATABASE_URL", entrada)
    assert database._url_do_banco() == esperado


def test_postgres_url_tambem_e_aceita(monkeypatch):
    _limpar_ambiente(monkeypatch)
    monkeypatch.setenv("POSTGRES_URL", "postgres://u:s@host/db")
    assert database._url_do_banco() == "postgresql+psycopg://u:s@host/db"


def test_vercel_sem_banco_usa_a_pasta_gravavel(monkeypatch):
    _limpar_ambiente(monkeypatch)
    monkeypatch.setenv("VERCEL", "1")
    assert database._url_do_banco() == "sqlite:////tmp/acoust.db"


def test_no_computador_usa_o_arquivo_ao_lado_do_codigo(monkeypatch):
    _limpar_ambiente(monkeypatch)
    url = database._url_do_banco()
    assert url.startswith("sqlite:///")
    assert url.endswith("acoust.db")
    assert os.path.dirname(os.path.abspath(database.__file__)) in url


def test_link_de_senha_usa_o_dominio_publicado(monkeypatch):
    monkeypatch.delenv("FRONTEND_URL", raising=False)
    monkeypatch.setenv("VERCEL_PROJECT_PRODUCTION_URL", "acousticbuild.vercel.app")
    try:
        importlib.reload(recuperacao)
        assert recuperacao.montar_link("abc") == "https://acousticbuild.vercel.app/redefinir-senha?token=abc"
    finally:
        monkeypatch.delenv("VERCEL_PROJECT_PRODUCTION_URL", raising=False)
        importlib.reload(recuperacao)
