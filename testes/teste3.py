 # O pytest fornece a parametrizacao dos cenarios da tabela de decisao.
import pytest

# Importa a funcao que sera validada pelas duas tabelas.
from Search.exercicio03 import tem_frete_gratis


# Tabela de decisao completa:
# V = valor da compra >= 200; P = cliente premium; K = peso <= 30 kg.
# A saida so e frete gratis quando V, P e K sao verdadeiros.
@pytest.mark.parametrize(
	# Cada linha representa uma combinacao das tres condicoes binarias.
    ("valor_compra", "cliente_premium", "peso", "frete_gratis"),
    [
		# R1: valor insuficiente, cliente nao premium e peso acima do limite.
        pytest.param(199.99, False, 30.01, False, id="R1"),
		# R2: valor insuficiente, cliente nao premium e peso permitido.
        pytest.param(199.99, False, 30.0, False, id="R2"),
		# R3: valor insuficiente, cliente premium e peso acima do limite.
        pytest.param(199.99, True, 30.01, False, id="R3"),
		# R4: valor insuficiente, cliente premium e peso permitido.
        pytest.param(199.99, True, 30.0, False, id="R4"),
		# R5: valor suficiente, cliente nao premium e peso acima do limite.
        pytest.param(200.0, False, 30.01, False, id="R5"),
		# R6: valor suficiente, cliente nao premium e peso permitido.
        pytest.param(200.0, False, 30.0, False, id="R6"),
		# R7: valor suficiente, cliente premium e peso acima do limite.
        pytest.param(200.0, True, 30.01, False, id="R7"),
		# R8: as tres condicoes sao verdadeiras e o frete e gratis.
        pytest.param(200.0, True, 30.0, True, id="R8"),
    ],
)
def test_tabela_de_decisao_completa(
    valor_compra, cliente_premium, peso, frete_gratis
):
	# Confirma a saida esperada para cada uma das oito regras.
    assert tem_frete_gratis(valor_compra, cliente_premium, peso) is frete_gratis


# Tabela reduzida por don't care:
# R1: V=N; P e K nao importam, pois a compra nao atingiu R$200.
# R2: V=S, P=N; K nao importa, pois o cliente nao e premium.
# R3: V=S, P=S, K=N; o peso acima de 30 kg impede o beneficio.
# R4: V=S, P=S, K=S; as tres condicoes sao satisfeitas.
@pytest.mark.parametrize(
	# O asterisco da tabela reduzida representa uma condicao irrelevante.
    ("valor_compra", "cliente_premium", "peso", "frete_gratis"),
    [
		# R1 reduzida: compra insuficiente; premium e peso nao importam.
        pytest.param(199.99, True, 30.0, False, id="R1-valor-nao-atingido"),
		# R2 reduzida: sem premium; o peso nao importa.
        pytest.param(200.0, False, 1.0, False, id="R2-sem-premium"),
		# R3 reduzida: peso excedido impede o frete gratis.
        pytest.param(200.0, True, 30.01, False, id="R3-peso-excedido"),
		# R4 reduzida: todas as condicoes precisam ser verdadeiras.
        pytest.param(200.0, True, 30.0, True, id="R4-todas-condicoes"),
    ],
)
def test_tabela_de_decisao_reduzida(
    valor_compra, cliente_premium, peso, frete_gratis
):
	# Confirma as regras apos a reducao por don't care.
    assert tem_frete_gratis(valor_compra, cliente_premium, peso) is frete_gratis
