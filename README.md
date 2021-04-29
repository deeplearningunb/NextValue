# NextValue

## Aluno

| Matrícula | Nome |
| -- | -- |
| 17/0050394 | Henrique Martins de Messias |

## Descrição

Projeto de Deep Learning que tem como objetivo tentar prever o valor de várias criptomoedas. As previsões são feitas com base:
- Nos valores anteriores da criptomoeda
- Nos valores de outras criptomoedas

As criptomoedas disponíveis para fazer a previsão e treinar são:
- Bitcoin
- Bitcoin Cash
- Cardano
- EOS
- Ethereum
- IOTA
- Lisk
- Litecoin
- Monero
- NEO
- Qtum
- Stellar
- Tron
- XRP
- Zcash

## O que é RNN?

Uma rede neural recorrente (RNN) é uma classe de redes neurais artificiais onde as conexões entre os nós formam um gráfico direcionado ao longo de uma sequência temporal.
No projeto é usado uma RNN para fazer as previsões. Além de usar o valor de um dia para prever o dia seguinte, valores de dias anteriores também são usados (além de valores de outras criptomoedas).

## O Notebook

O notebook tem como objetivo explicar passo-a-passo o funcionamento do algoritmo usado para prever o valor das criptomoedas. O algoritmo está dividido em:
- Processamento dos Dados
- Construção da Rede Neural
- Treino da Rede Neural
- Teste e Visualização de resultados

## A Aplicação

A aplicação tem como objetivo providenciar uma interface para o usuário. Na aplicação é possível:
- Treinar uma rede neural criada por você mesmo (ou usar a rede padrão)
- Escolher a criptomoeda que deseja fazer a previsão
- Prever o valor para um dia específico
- Prever o valor para um intervalo de dias

## Instalações necessárias

```bash
  $ sudo apt-get install python3-tk
  $ pip3 install -r requirements.txt
```

## Como executar o Notebook

No diretório do projeto, use o seguinte comando:

```bash
  $ jupyter notebook NextValue.ipynb
```

## Como executar a Aplicação

No diretório do projeto, use os seguintes comandos:

```bash
  $ cd src
  $ python3 main.py
```

## Fonte dos dados

[Coindesk](https://www.coindesk.com)

## Referências

[Wikipedia - Recurrent neural network](https://en.wikipedia.org/wiki/Recurrent_neural_network)
