from unittest.mock import Mock, call

import pytest

from exercicio02 import confirmar


def test_confirmar_aprovado_cobra_e_envia_confirmacao() -> None:
    gateway = Mock()
    gateway.cobrar.return_value = "aprovado"
    email = Mock()

    resultado = confirmar("pedido-1", 2500, gateway, email)

    assert resultado == "aprovado"
    gateway.cobrar.assert_called_once_with("pedido-1", 2500)
    email.enviar.assert_called_once_with("pedido-1", "pedido confirmado")


def test_confirmar_negado_nao_envia_email() -> None:
    gateway = Mock()
    gateway.cobrar.return_value = "negado"
    email = Mock()

    resultado = confirmar("pedido-2", 900, gateway, email)

    assert resultado == "negado"
    gateway.cobrar.assert_called_once_with("pedido-2", 900)
    email.enviar.assert_not_called()


def test_confirmar_repete_apos_connection_error_e_entao_aprova() -> None:
    gateway = Mock()
    gateway.cobrar.side_effect = [ConnectionError("conexao perdida"), "aprovado"]
    email = Mock()

    resultado = confirmar("pedido-3", 1200, gateway, email, tentativas=2)

    assert resultado == "aprovado"
    assert gateway.cobrar.call_args_list == [
        call("pedido-3", 1200),
        call("pedido-3", 1200),
    ]
    email.enviar.assert_called_once_with("pedido-3", "pedido confirmado")


def test_confirmar_apos_ultima_falha_notifica_e_relanca_excecao() -> None:
    gateway = Mock()
    erro = ConnectionError("gateway indisponivel")
    gateway.cobrar.side_effect = erro
    email = Mock()

    with pytest.raises(ConnectionError) as capturada:
        confirmar("pedido-4", 1800, gateway, email, tentativas=3)

    assert capturada.value is erro
    assert gateway.cobrar.call_args_list == [
        call("pedido-4", 1800),
        call("pedido-4", 1800),
        call("pedido-4", 1800),
    ]
    email.enviar.assert_called_once_with("pedido-4", "falha na cobranca")


def test_confirmar_com_uma_tentativa_nao_repete_a_cobranca() -> None:
    gateway = Mock()
    gateway.cobrar.side_effect = ConnectionError("conexao perdida")
    email = Mock()

    with pytest.raises(ConnectionError):
        confirmar("pedido-5", 500, gateway, email, tentativas=1)

    gateway.cobrar.assert_called_once_with("pedido-5", 500)
    email.enviar.assert_called_once_with("pedido-5", "falha na cobranca")


@pytest.mark.parametrize("tentativas", [0, -1])
def test_confirmar_rejeita_numero_de_tentativas_invalido(tentativas: int) -> None:
    gateway = Mock()
    email = Mock()

    with pytest.raises(ValueError):
        confirmar("pedido-6", 100, gateway, email, tentativas=tentativas)

    gateway.cobrar.assert_not_called()
    email.enviar.assert_not_called()
