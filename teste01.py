from unittest.mock import Mock

import pytest

from exrcicio01 import ConversorFrete, CotacaoIndisponivel


class CotacaoStub:
    def __init__(self, taxa: float) -> None:
        self.taxa = taxa

    def dolar(self) -> float:
        return self.taxa


@pytest.mark.parametrize(
    ("centavos_de_dolar", "taxa", "esperado"),
    [
        pytest.param(100, 5.25, 525, id="conversao-direta"),
        pytest.param(1, 2.5, 2, id="empate-arredonda-para-par-inferior"),
        pytest.param(1, 3.5, 4, id="empate-arredonda-para-par-superior"),
        pytest.param(0, 5.0, 0, id="valor-zero"),
    ],
)
def test_em_centavos_de_real_com_stub(
    centavos_de_dolar: int, taxa: float, esperado: int
) -> None:
    conversor = ConversorFrete(CotacaoStub(taxa))

    assert conversor.em_centavos_de_real(centavos_de_dolar) == esperado


@pytest.mark.parametrize("taxa", [0, -1], ids=["taxa-zero", "taxa-negativa"])
def test_em_centavos_de_real_rejeita_taxa_nao_positiva(taxa: float) -> None:
    conversor = ConversorFrete(CotacaoStub(taxa))

    with pytest.raises(ValueError):
        conversor.em_centavos_de_real(100)


def test_em_centavos_de_real_converte_timeout_em_cotacao_indisponivel() -> None:
    cotacao = Mock()
    cotacao.dolar.side_effect = TimeoutError("tempo esgotado")
    conversor = ConversorFrete(cotacao)

    with pytest.raises(CotacaoIndisponivel) as erro:
        conversor.em_centavos_de_real(100)

    cotacao.dolar.assert_called_once_with()
    assert isinstance(erro.value.__cause__, TimeoutError)