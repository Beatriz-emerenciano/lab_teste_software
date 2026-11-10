"""Implementacoes de repositorio para usuarios."""

import sqlite3


class EmailDuplicado(Exception):
    """Indica que ja existe um usuario com esse endereco de email."""


class RepoSqlite:
    """Repositorio em memoria que trata emails sem diferenciar caixa."""

    def __init__(self) -> None:
        self._conexao = sqlite3.connect(":memory:")
        self._conexao.execute(
            """
            CREATE TABLE usuarios (
                email TEXT COLLATE NOCASE PRIMARY KEY,
                nome TEXT NOT NULL
            )
            """
        )

    def salvar(self, email: str, nome: str) -> None:
        try:
            self._conexao.execute(
                "INSERT INTO usuarios (email, nome) VALUES (?, ?)",
                (email, nome),
            )
        except sqlite3.IntegrityError as erro:
            raise EmailDuplicado(email) from erro

    def buscar(self, email: str) -> str | None:
        resultado = self._conexao.execute(
            "SELECT nome FROM usuarios WHERE email = ?",
            (email,),
        ).fetchone()
        return resultado[0] if resultado is not None else None

    def fechar(self) -> None:
        self._conexao.close()


class FakeIngenuo:
    """Fake simples que usa o email original como chave do dicionario."""

    def __init__(self) -> None:
        self._usuarios: dict[str, str] = {}

    def salvar(self, email: str, nome: str) -> None:
        if email in self._usuarios:
            raise EmailDuplicado(email)
        self._usuarios[email] = nome

    def buscar(self, email: str) -> str | None:
        return self._usuarios.get(email)


class FakeFiel:
    """Fake em memoria que respeita o contrato de comparacao de emails."""

    def __init__(self) -> None:
        self._usuarios: dict[str, str] = {}

    def salvar(self, email: str, nome: str) -> None:
        chave = email.lower()
        if chave in self._usuarios:
            raise EmailDuplicado(email)
        self._usuarios[chave] = nome

    def buscar(self, email: str) -> str | None:
        return self._usuarios.get(email.lower())