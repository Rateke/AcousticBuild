"""Configuração central do backend.

Todo valor sensível (chave de assinatura de login, string de conexão do
banco, credenciais de e-mail) é lido daqui — nunca fixo no código-fonte.

- Em desenvolvimento: os valores vêm do arquivo `.env` (na pasta backend/),
  que o `.gitignore` já bloqueia de ir para o Git. Copie `.env.example`
  para `.env` e preencha.
- Em produção (Vercel): não existe `.env` nenhum publicado. As mesmas
  variáveis são cadastradas em Settings → Environment Variables, e chegam
  aqui exatamente da mesma forma (`os.getenv`), sem mudar nada no código.

Nenhuma variável ausente derruba a aplicação: cada uma tem um padrão seguro
e declarado. Sem SECRET_KEY, a chave é sorteada e os logins caem a cada
reinício. Sem DATABASE_URL, o banco é um SQLite temporário. Sem SMTP_*, o
link de recuperação de senha é impresso no log em vez de enviado por
e-mail. Em todos os casos o aviso aparece no log do servidor.

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


# True quando a chave desta execução foi sorteada em vez de configurada.
# Quem precisar avisar o usuário de que a sessão pode cair consulta isto.
CHAVE_EFEMERA = False


def _carregar_secret_key() -> str:
    """Chave de assinatura dos tokens de login.

    Configurada no ambiente, é estável e as sessões sobrevivem a reinícios.
    Ausente, é SORTEADA a cada execução — inclusive em produção.

    Sortear não é a insegurança que o código precisava evitar: o problema
    era a chave fixa e pública no repositório, que deixaria qualquer pessoa
    assinar um token válido para qualquer conta. Uma chave sorteada na hora
    ninguém conhece, logo ninguém forja. O que se perde é permanecer logado:
    ao hibernar, o servidor sorteia outra e os tokens antigos deixam de
    valer. Antes isto era um erro de import, o que derrubava a API inteira
    — incluindo a calculadora, que não precisa de login — para proteger um
    cadastro que, sem DATABASE_URL, já é apagado junto com o /tmp.
    """
    global CHAVE_EFEMERA
    chave = os.getenv("SECRET_KEY")
    if chave:
        return chave

    CHAVE_EFEMERA = True
    onde = (
        "nas variáveis de ambiente da Vercel" if IS_VERCEL
        else "no backend/.env (veja backend/.env.example)"
    )
    print(
        "[config] SECRET_KEY não definida — sorteando uma chave aleatória só "
        "para esta execução. A API funciona normalmente; o que cai são os "
        "logins a cada reinício do servidor. Para manter as sessões, defina "
        "SECRET_KEY " + onde + ".",
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
