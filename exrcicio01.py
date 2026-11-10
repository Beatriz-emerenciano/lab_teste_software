"""Conversao de valores de frete de centavos de dolar para reais."""

from typing import Protocol


class Cotacao(Protocol):
    """Interface esperada pelo conversor."""

    def dolar(self) -> float:
        """Retorna o valor de um dolar em reais."""
        ...


class CotacaoIndisponivel(Exception):
    """Indica que nao foi possivel consultar a cotacao do dolar."""


class ConversorFrete:
    """Converte centavos de dolar para centavos de real."""

    def __init__(self, cotacao: Cotacao) -> None:
        self.cotacao = cotacao

    def em_centavos_de_real(self, centavos_de_dolar: int) -> int:
        """Converte o valor usando a cotacao atual e arredondamento usual."""
        try:
            taxa = self.cotacao.dolar()
        except TimeoutError as erro:
            raise CotacaoIndisponivel(
                "A cotacao do dolar esta indisponivel."
            ) from erro

        if taxa <= 0:
            raise ValueError("A taxa do dolar deve ser maior que zero.")

        return round(centavos_de_dolar * taxa)