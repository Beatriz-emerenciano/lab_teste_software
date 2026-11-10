import pytest

from exercicio03 import EmailDuplicado, FakeFiel, FakeIngenuo, RepoSqlite


@pytest.fixture(
    params=[RepoSqlite, FakeIngenuo, FakeFiel],
    ids=["sqlite", "fake-ingenuo", "fake-fiel"],
)
def repositorio(request):
    repositorio = request.param()
    yield repositorio
    if isinstance(repositorio, RepoSqlite):
        repositorio.fechar()


def test_buscar_usuario_salvo(repositorio) -> None:
    repositorio.salvar("ana@example.com", "Ana")

    assert repositorio.buscar("ana@example.com") == "Ana"


def test_buscar_ignora_maiusculas_e_minusculas(repositorio) -> None:
    repositorio.salvar("ana@example.com", "Ana")
    resultado = repositorio.buscar("ANA@EXAMPLE.COM")

    if isinstance(repositorio, FakeIngenuo) and resultado != "Ana":
        pytest.xfail("FakeIngenuo usa a chave original e diferencia maiusculas")
    assert resultado == "Ana"


def test_salvar_email_duplicado_ignora_maiusculas(repositorio) -> None:
    repositorio.salvar("ana@example.com", "Ana")

    try:
        repositorio.salvar("ANA@EXAMPLE.COM", "Outra Ana")
    except EmailDuplicado:
        return

    if isinstance(repositorio, FakeIngenuo):
        pytest.xfail("FakeIngenuo nao detecta duplicatas com caixa diferente")
    pytest.fail("Salvar novamente o mesmo email deve levantar EmailDuplicado")


def test_buscar_email_nao_cadastrado_retorna_none(repositorio) -> None:
    assert repositorio.buscar("ausente@example.com") is None