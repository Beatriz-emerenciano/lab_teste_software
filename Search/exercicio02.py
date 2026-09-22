"""Classificacao generica por faixas e classificacao de vento."""

from collections.abc import Sequence
from typing import TypeAlias


Faixa: TypeAlias = tuple[float | None, str]


FAIXAS_VENTO: list[Faixa] = [
	(20.0, "calmo"),
	(40.0, "moderado"),
	(60.0, "forte"),
	(None, "tempestade"),
]


def classificar_por_faixas(valor: float, faixas: Sequence[Faixa]) -> str:
	"""Retorna o rotulo da primeira faixa cujo limite nao foi atingido."""
	for limite_superior, rotulo in faixas:
		if limite_superior is None or valor < limite_superior:
			return rotulo
	raise ValueError("valor nao pertence a nenhuma faixa")


def classificar_vento(velocidade: float) -> str:
	"""Classifica o vento conforme sua velocidade."""
	return classificar_por_faixas(velocidade, FAIXAS_VENTO)
