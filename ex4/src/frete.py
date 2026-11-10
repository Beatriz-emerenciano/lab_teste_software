"""Calculo de frete em centavos."""


def calcular(peso_kg: float, uf: str) -> float:
    """Devolve o frete em centavos."""
    base = 1500 + 200 * peso_kg
    return base if uf == "SP" else base + 1000
