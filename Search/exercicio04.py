"""Regra de frete gratis de uma loja."""


def tem_frete_gratis(
    valor_compra: float,
    cliente_premium: bool,
    peso: float,
) -> bool:
    """Retorna True somente quando as tres condicoes sao satisfeitas."""
    return valor_compra >= 200 and cliente_premium and peso <= 30
