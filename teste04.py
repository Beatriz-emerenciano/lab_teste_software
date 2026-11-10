from unittest.mock import Mock

import pytest

from ex4.src.estoque import Estoque, SemEstoque
from ex4.src.frete import calcular
from ex4.src.pedido import fechar


def test_fecha_com_stubs_que_respeitam_as_unidades_e_assinaturas() -> None:
    estoque = Mock()
    estoque.reservar.return_value = None
    frete = Mock(return_value=1700)

    resultado = fechar("livro", 2, 4000, 1, "SP", estoque, frete)

    assert resultado == {"status": "fechado", "total": 9700}
    estoque.reservar.assert_called_once_with("livro", 2)
    frete.assert_called_once_with(1, "SP")


def test_sem_estoque_com_stub_que_levanta_excecao_do_contrato() -> None:
    estoque = Mock()
    estoque.reservar.side_effect = SemEstoque("livro")
    frete = Mock()

    resultado = fechar("livro", 2, 4000, 1, "SP", estoque, frete)

    assert resultado == {"status": "sem estoque"}
    estoque.reservar.assert_called_once_with("livro", 2)
    frete.assert_not_called()


@pytest.mark.parametrize(
    ("peso_kg", "uf", "frete_esperado"),
    [
        pytest.param(1, "SP", 1700, id="sao-paulo"),
        pytest.param(1, "RJ", 2700, id="outro-estado"),
    ],
)
def test_fecha_com_estoque_e_frete_reais(
    peso_kg: float, uf: str, frete_esperado: float
) -> None:
    estoque = Estoque({"livro": 2})

    resultado = fechar(
        "livro", 2, 4000, peso_kg, uf, estoque, calcular
    )

    assert resultado == {
        "status": "fechado",
        "total": 8000 + frete_esperado,
    }
    assert estoque.itens["livro"] == 0


def test_tres_pedidos_sequenciais_ate_esgotar_estoque() -> None:
    estoque = Estoque({"livro": 2})

    resultados = [
        fechar("livro", 1, 4000, 0.5, "SP", estoque, calcular)
        for _ in range(3)
    ]

    assert resultados == [
        {"status": "fechado", "total": 5600},
        {"status": "fechado", "total": 5600},
        {"status": "sem estoque"},
    ]
    assert estoque.itens["livro"] == 0