import unittest
from pathlib import Path

import pytest

from searsh.carteira import CarteiraDigital, SaldoInsuficienteError, transferir
from searsh.transacoes import classificar_transacao


@pytest.fixture
def carteira_com_log(tmp_path):
	# Arrange: define um arquivo isolado para o teste.
	log_path = tmp_path / "carteira.log"
	if log_path.exists():
		log_path.unlink()

	carteira = CarteiraDigital(log_path=log_path)
	yield carteira

	# Teardown: remove o log mesmo quando o teste falha.
	if log_path.exists():
		log_path.unlink()


@pytest.fixture
def carteiras_para_transferencia(tmp_path):
	# Arrange: cria uma carteira de origem com saldo e uma carteira de destino vazia.
	origem = CarteiraDigital(1000, log_path=tmp_path / "origem.log")
	destino = CarteiraDigital(log_path=tmp_path / "destino.log")
	return origem, destino


# classe de testes 

class TestCarteiraDigital(unittest.TestCase):
	def test_saldo_inicial_padrao(self):    # verifica se uma carteira criada sem valor começa com saldo 
		# Arrange
		carteira = CarteiraDigital()

		# Act
		saldo = carteira.saldo

		# Assert
		self.assertEqual(saldo, 0)

	def test_saldo_inicial_informado(self): # verifica se  o saldo informado é armazenado corretamente 
		# Arrange
		carteira = CarteiraDigital(100)

		# Act
		saldo = carteira.saldo

		# Assert
		self.assertEqual(saldo, 100)

	def test_depositar_soma_valor_ao_saldo(self):
		# Arrange
		carteira = CarteiraDigital(50)

		# Act
		carteira.depositar(25)

		# Assert
		self.assertEqual(carteira.saldo, 75)

	def test_sacar_subtrai_valor_com_saldo_disponivel(self):
		# Arrange
		carteira = CarteiraDigital(100)

		# Act
		carteira.sacar(40)

		# Assert
		self.assertEqual(carteira.saldo, 60)

	def test_sacar_sem_saldo_suficiente_levanta_excecao(self):
		# Arrange
		# Cria uma carteira com saldo menor que o valor do saque.
		carteira = CarteiraDigital(50)

		# Act e Assert
		# Verifica o tipo e a mensagem da exceção levantada.
		with pytest.raises(SaldoInsuficienteError, match="^saldo insuficiente$"):
			carteira.sacar(60)

	def test_sacar_sem_saldo_suficiente_nao_altera_saldo(self):
		# Arrange
		# Guarda uma carteira com saldo conhecido antes da tentativa.
		carteira = CarteiraDigital(50)

		# Act
		# A exceção é esperada, então ela é capturada para continuar o teste.
		try:
			carteira.sacar(60)
		except SaldoInsuficienteError:
			pass

		# Assert
		# Confirma que a tentativa de saque não modificou o saldo.
		self.assertEqual(carteira.saldo, 50)


if __name__ == "__main__":
	unittest.main()


def test_deposito_registra_linha_no_log(carteira_com_log):
	# Act
	carteira_com_log.depositar(25)

	# Assert
	conteudo = Path(carteira_com_log.log_path).read_text()
	assert conteudo == "deposito:25\n"


@pytest.mark.parametrize(
	"valor, categoria_esperada",
	[
		pytest.param(0, "pequena", id="valor-zero-e-pequeno"),
		pytest.param(99, "pequena", id="limite-antes-da-media"),
		pytest.param(100, "media", id="limite-inicial-da-media"),
		pytest.param(500, "media", id="valor-no-meio-da-media"),
		pytest.param(1000, "grande", id="limite-inicial-da-grande"),
		pytest.param(1001, "grande", id="valor-acima-do-limite-da-grande"),
	],
)
def test_classificar_transacao(valor, categoria_esperada):
	# Act
	categoria = classificar_transacao(valor)

	# Assert
	assert categoria == categoria_esperada


@pytest.mark.parametrize(
	"valor", 
	[
		pytest.param(1, id="transferencia-de-um-real"),
		pytest.param(250, id="transferencia-de-duzentos-e-cinquenta-reais"),
		pytest.param(1000, id="transferencia-do-saldo-total"),
	],
)
def test_transferencia_bem_sucedida(carteiras_para_transferencia, valor):
	# Arrange
	origem, destino = carteiras_para_transferencia
	saldo_inicial_origem = origem.saldo

	# Act
	transferir(origem, destino, valor)

	# Assert
	assert origem.saldo == saldo_inicial_origem - valor
	assert destino.saldo == valor


def test_transferencia_maior_que_saldo_nao_altera_nenhuma_carteira(
	carteiras_para_transferencia,
):
	# Arrange
	origem, destino = carteiras_para_transferencia
	saldo_inicial_origem = origem.saldo
	saldo_inicial_destino = destino.saldo

	# Act e Assert
	with pytest.raises(SaldoInsuficienteError):
		transferir(origem, destino, saldo_inicial_origem + 1)

	assert origem.saldo == saldo_inicial_origem
	assert destino.saldo == saldo_inicial_destino
