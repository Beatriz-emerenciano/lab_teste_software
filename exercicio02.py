"""Confirmacao de pedidos com retentativas de cobranca."""


def confirmar(pedido, centavos, gateway, email, tentativas=3):
    """Cobra um pedido, notificando o cliente conforme o resultado."""
    if tentativas < 1:
        raise ValueError("tentativas deve ser maior ou igual a 1")

    for tentativa in range(tentativas):
        try:
            status = gateway.cobrar(pedido, centavos)
        except ConnectionError:
            if tentativa == tentativas - 1:
                email.enviar(pedido, "falha na cobranca")
                raise
        else:
            if status == "aprovado":
                email.enviar(pedido, "pedido confirmado")
            return status
