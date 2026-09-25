"""Configuração central do backend.

Todo valor sensível (chave de assinatura de login, string de conexão do
banco, credenciais de e-mail) é lido daqui — nunca fixo no código-fonte.

- Em desenvolvimento: os valores vêm do arquivo `.env` (na pasta backend/),
  que o `.gitignore` já bloqueia de ir para o Git. Copie `.env.example`
  para `.env` e preencha.
- Em produção (Vercel): não existe `.env` nenhum publicado. As mesmas
  variáveis são cadastradas em Settings → Environment Variables, e chegam
  aqui exatamente da mesma forma (`os.getenv`), sem mudar nada no código.

Importar este módulo é o que garante que o `.env` seja carregado antes de
qualquer outro módulo (database.py, auth.py, recuperacao.py) ler uma
variável de ambiente — por isso ele é importado antes dos outros em main.py.
"""
from __future__ import annotations

import os
import secrets

from dotenv import load_dotenv

# Carrega backend/.env para dentro de os.environ. Se o arquivo não existir
# (ex.: em produção na Vercel), não faz nada — as variáveis já vêm do
# ambiente real, configuradas no painel.
load_dotenv()

IS_VERCEL = bool(os.getenv("VERCEL"))


def _carregar_secret_key() -> str:
    chave = os.getenv("SECRET_KEY")
    if chave:
        return chave

    if IS_VERCEL:
        # Em produção não existe fallback: sem SECRET_KEY configurada, o
        # deploy não deve nem subir — uma chave pública e fixa no código
        # permitiria forjar um login válido para qualquer conta.
        raise RuntimeError(
            "SECRET_KEY não configurada. Cadastre essa variável em "
            "Settings → Environment Variables no painel da Vercel."
        )

    # Em desenvolvimento local, gera uma chave aleatória a cada execução em
    # vez de usar um valor fixo e público no código-fonte. Definir SECRET_KEY
    # no seu .env evita que sessões sejam derrubadas a cada reinício.
    print(
        "[config] SECRET_KEY não definida no .env — usando uma chave "
        "aleatória só para esta execução (logins serão invalidados ao "
        "reiniciar o servidor). Veja backend/.env.example.",
        flush=True,
    )
    return secrets.token_hex(32)


SECRET_KEY = _carregar_secret_key()

# DATABASE_URL, as variáveis SMTP_* e FRONTEND_URL continuam lidas com
# os.getenv() diretamente em database.py e recuperacao.py — cada uma no
# momento em que é usada, para poderem mudar em tempo de execução (é assim
# que a suíte de testes simula diferentes ambientes). O que importa é que
# ambos os módulos importam este config.py primeiro, o que garante que o
# .env já foi carregado antes dessas leituras.
