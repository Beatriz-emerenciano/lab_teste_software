import pytest

from Search.exercicio01 import calcular_imc, categorizar_imc, classificar_pessoa
from Search.exercicio02 import classificar_vento


@pytest.mark.parametrize(
	("imc", "categoria"),
	[
		pytest.param(18.49, "abaixo do peso", id="abaixo-da-fronteira-18-5"),
		pytest.param(18.5, "peso normal", id="fronteira-18-5"),
		pytest.param(24.99, "peso normal", id="antes-da-fronteira-25"),
		pytest.param(25.0, "sobrepeso", id="fronteira-25"),
		pytest.param(29.99, "sobrepeso", id="antes-da-fronteira-30"),
		pytest.param(30.0, "obesidade", id="fronteira-30"),
		pytest.param(30.01, "obesidade", id="acima-da-fronteira-30"),
	],
)
def test_categorizar_imc_nos_valores_limite(imc, categoria):
	assert categorizar_imc(imc) == categoria


def test_calcular_imc_rejeita_peso_nao_positivo():
	with pytest.raises(ValueError):
		calcular_imc(0, 1.70)


def test_calcular_imc_rejeita_altura_nao_positiva():
	with pytest.raises(ValueError):
		calcular_imc(70, 0)


@pytest.mark.parametrize(
	("peso", "altura", "categoria"),
	[
		pytest.param(50, 1.80, "abaixo do peso", id="abaixo-do-peso"),
		pytest.param(68, 1.75, "peso normal", id="peso-normal"),
		pytest.param(82, 1.75, "sobrepeso", id="sobrepeso"),
		pytest.param(100, 1.75, "obesidade", id="obesidade"),
	],
)
def test_classificar_pessoa_representa_cada_classe(peso, altura, categoria):
	assert classificar_pessoa(peso, altura) == categoria


@pytest.mark.parametrize(
	("velocidade", "categoria"),
	[
		pytest.param(19.99, "calmo", id="abaixo-da-fronteira-20"),
		pytest.param(20.0, "moderado", id="fronteira-20"),
		pytest.param(39.99, "moderado", id="abaixo-da-fronteira-40"),
		pytest.param(40.0, "forte", id="fronteira-40"),
		pytest.param(59.99, "forte", id="abaixo-da-fronteira-60"),
		pytest.param(60.0, "tempestade", id="fronteira-60"),
		pytest.param(80.0, "tempestade", id="acima-da-fronteira-60"),
	],
)
def test_classificar_vento_nas_classes_e_nos_limites(velocidade, categoria):
	assert classificar_vento(velocidade) == categoria
