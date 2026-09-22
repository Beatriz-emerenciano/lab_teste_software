import pytest

from Search.exercicio04 import tem_frete_gratis


# Tabela completa: V = valor >= 200, P = cliente premium,
# K = peso <= 30 kg.
@pytest.mark.parametrize(
    ("valor_compra", "cliente_premium", "peso", "resultado"),
    [
        pytest.param(199.99, False, 30.01, False, id="R1"),
        pytest.param(199.99, False, 30.00, False, id="R2"),
        pytest.param(199.99, True, 30.01, False, id="R3"),
        pytest.param(199.99, True, 30.00, False, id="R4"),
        pytest.param(200.00, False, 30.01, False, id="R5"),
        pytest.param(200.00, False, 30.00, False, id="R6"),
        pytest.param(200.00, True, 30.01, False, id="R7"),
        pytest.param(200.00, True, 30.00, True, id="R8"),
    ],
)
def test_tabela_de_decisao_completa(
    valor_compra, cliente_premium, peso, resultado
):
    assert tem_frete_gratis(valor_compra, cliente_premium, peso) is resultado


# Tabela reduzida por don't care:
# R1: V=N, pois uma compra insuficiente ja impede o beneficio;
# P e K nao importam.
# R2: V=S e P=N, pois a falta de assinatura impede o beneficio;
# K nao importa.
# R3: V=S, P=S e K=N, pois o peso excede o limite.
# R4: V=S, P=S e K=S, unica combinacao com frete gratis.
@pytest.mark.parametrize(
    ("valor_compra", "cliente_premium", "peso", "resultado"),
    [
        pytest.param(199.99, True, 30.00, False, id="R1-reduzida"),
        pytest.param(200.00, False, 1.00, False, id="R2-reduzida"),
        pytest.param(200.00, True, 30.01, False, id="R3-reduzida"),
        pytest.param(200.00, True, 30.00, True, id="R4-reduzida"),
    ],
)
def test_tabela_de_decisao_reduzida(
    valor_compra, cliente_premium, peso, resultado
):
    assert tem_frete_gratis(valor_compra, cliente_premium, peso) is resultado
