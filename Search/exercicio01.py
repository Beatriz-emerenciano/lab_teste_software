"""Calculo e classificacao do indice de massa corporal (IMC)."""

from Search.exercicio02 import classificar_por_faixas


FAIXAS_IMC = [
	(18.5, "abaixo do peso"),
	(25.0, "peso normal"),
	(30.0, "sobrepeso"),
	(None, "obesidade"),
]


def calcular_imc(peso: float, altura: float) -> float:
	"""Retorna o IMC calculado a partir do peso e da altura."""
	if peso <= 0 or altura <= 0:
		raise ValueError("peso e altura devem ser positivos")
	return peso / altura**2


def categorizar_imc(imc: float) -> str:
	"""Retorna a categoria correspondente ao valor do IMC."""
	return classificar_por_faixas(imc, FAIXAS_IMC)


def classificar_pessoa(peso: float, altura: float) -> str:
	"""Calcula o IMC e retorna a categoria da pessoa."""
	return categorizar_imc(calcular_imc(peso, altura))
