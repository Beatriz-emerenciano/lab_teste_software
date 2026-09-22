"""Regra de frete gratis de uma loja."""


def tem_frete_gratis(
    # Valor total da compra em reais.
    valor_compra: float,
    # Indica se o cliente possui assinatura premium.
    cliente_premium: bool,
    # Peso total do pedido em quilogramas.
    peso: float,
) -> bool:
    """Retorna True quando as tres condicoes do frete gratis sao atendidas."""
    # A compra deve atingir R$200 ou mais.
    # O cliente deve ter assinatura premium.
    # O pedido deve pesar no maximo 30 kg.
    # O operador and exige que as tres condicoes sejam verdadeiras ao mesmo tempo.
    return valor_compra >= 200 and cliente_premium and peso <= 30
