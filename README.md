# lab_teste_software

## Classificador de IMC

`calcular_imc(peso, altura)` calcula `peso / altura**2` e levanta `ValueError`
quando peso ou altura sao menores ou iguais a zero.

`classificar_por_faixas(valor, faixas)` e a funcao generica: a tabela recebe
tuplas `(limite_superior, rotulo)` ordenadas. A primeira faixa cujo valor seja
menor que o limite e escolhida; `None` representa a ultima faixa, sem limite.

`categorizar_imc(imc, faixas=FAIXAS_IMC)` e `classificar_vento(velocidade)`
reutilizam essa funcao generica com suas respectivas tabelas.

`classificar_pessoa(peso, altura)` combina o calculo do IMC com a
classificacao e retorna uma destas categorias: `abaixo do peso`, `peso normal`,
`sobrepeso` ou `obesidade`.

### Tabela de decisao reduzida

| Peso positivo | Altura positiva | Decisao |
|---|---|---|
| Nao | * | Rejeitar com `ValueError` |
| Sim | Nao | Rejeitar com `ValueError` |
| Sim | Sim | Calcular o IMC |

O `*` e um don’t care: quando o peso ja e invalido, o valor da altura nao
altera a decisao.

## Frete gratis

`tem_frete_gratis(valor_compra, cliente_premium, peso)` retorna `True` apenas
quando o valor da compra e pelo menos R$200, o cliente e premium e o pedido
pesa no maximo 30 kg.

### Tabela de decisao completa

| Regra | V: compra >= 200 | P: premium | K: peso <= 30 kg | Resultado |
|---|---|---|---|---|
| R1 | Nao | Nao | Nao | Cobrado |
| R2 | Nao | Nao | Sim | Cobrado |
| R3 | Nao | Sim | Nao | Cobrado |
| R4 | Nao | Sim | Sim | Cobrado |
| R5 | Sim | Nao | Nao | Cobrado |
| R6 | Sim | Nao | Sim | Cobrado |
| R7 | Sim | Sim | Nao | Cobrado |
| R8 | Sim | Sim | Sim | Gratis |

### Tabela reduzida por don’t care

| Regra | V | P | K | Resultado | Justificativa |
|---|---|---|---|---|---|
| R1 | Nao | * | * | Cobrado | Compra abaixo de R$200 ja impede o beneficio. |
| R2 | Sim | Nao | * | Cobrado | Sem assinatura premium, o beneficio nao se aplica. |
| R3 | Sim | Sim | Nao | Cobrado | Peso acima de 30 kg impede o beneficio. |
| R4 | Sim | Sim | Sim | Gratis | As tres condicoes sao satisfeitas. |