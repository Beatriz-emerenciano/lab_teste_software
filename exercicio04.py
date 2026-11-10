 def fechar(item, qtd, preco, peso_kg, uf, estoque, frete):
2 if not estoque.reservar(item, qtd):
3 return {"status": "sem estoque"}
4 total = preco * qtd + frete(uf, peso_kg)
5 return {"status": "fechado", "total": total}
def calcular(peso_kg, uf):
2 """Devolve o frete em centavos."""
3 base = 1500 + 200 * peso_kg
4 return base if uf == "SP" else base + 1000

class SemEstoque(Exception):
2 pass
3
4 class Estoque:
5 def __init__(self, itens):
6 self.itens = dict(itens)
7 def reservar(self, item, qtd):
8 if self.itens.get(item, 0) < qtd:
9 raise SemEstoque(item)
10 self.itens[item] -= qtd

from unittest.mock import Mock
2 from pedido import fechar
3 def test_fecha_com_frete():
4 estoque = Mock()
5 estoque.reservar.return_value = True
6 frete = Mock(return_value=15.0)
7 r = fechar("livro", 2, 40.0, 1, "SP", estoque, frete)
8 assert r == {"status": "fechado", "total": 95.0}
9
10 def test_sem_estoque():
11 estoque = Mock()
12 estoque.reservar.return_value = False
13 r = fechar("livro", 2, 40.0, 1, "SP", estoque, Mock())
14 assert r == {"status": "sem estoque"}
