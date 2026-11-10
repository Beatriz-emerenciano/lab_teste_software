"""Controle de estoque para os pedidos."""


class SemEstoque(Exception):
    """Indica que nao ha unidades suficientes para reservar."""


class Estoque:
    def __init__(self, itens: dict[str, int]) -> None:
        self.itens = dict(itens)

    def reservar(self, item: str, qtd: int) -> None:
        if self.itens.get(item, 0) < qtd:
            raise SemEstoque(item)
        self.itens[item] -= qtd
