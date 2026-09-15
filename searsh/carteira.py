import unittest # módulo usado para executar testes python


class SaldoInsuficienteError(Exception):
	# Exceção usada quando o saque é maior que o saldo disponível.
	pass


# classes que representa a carteira digital 
class CarteiraDigital:
	def __init__(self, saldo_inicial=0, log_path="carteira.log"):  # construtor da classe.
		self.saldo = saldo_inicial
		self.log_path = log_path

	def depositar(self, valor): # método para somar valores ao saldo atual
		self.saldo += valor
		# Registra cada depósito em uma nova linha do arquivo de log.
		with open(self.log_path, "a") as arquivo_log:
			arquivo_log.write(f"deposito:{valor}\n")

	def sacar(self, valor): # método ára subtrair valores do saldo atual 
		# Impede o saque e mantém o saldo inalterado quando não há saldo suficiente.
		if valor > self.saldo:
			raise SaldoInsuficienteError("saldo insuficiente")
		self.saldo -= valor


def transferir(origem, destino, valor):
	origem.sacar(valor)
	destino.depositar(valor)

