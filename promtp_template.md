# Instrucao 

Considere a imagem ou o .pdf, que é uma nota fiscal, para extrair as seguintes informações:
-Nome do Produto
-Valor do Produto
-data da compra

# Nome do Produto
Para o nome do produto, considere apena o nome do objeto, descartando medidas , marcas , peso e quantidade. Segue um exemplo:

{produtos}

## Valor Produto
Para valor unitário, em caso de unidades inteiras, considerar o valor unitário. Caso seja em kilogramas/gramas, considerar o valor total.

# Formato do Retorno
Retorne os dados em formato json, na sequinte estrutura:

{respostas}