# Medidas DAX

O modelo contém **71 medidas, todas com descrição**. Os cálculos respeitam o contexto de filtro do relatório, salvo as remoções de filtro explicitadas nas respectivas fórmulas.

## Indicadores principais

### Total Receita

Soma a receita líquida de desconto: unidades × preço de varejo × (1 − desconto). Respeita os filtros ativos.

```dax
Total Receita =
SUM('fact_Vendas'[Receita])
```

### Total Custo

Soma o custo: unidades × custo padrão × fator de custo. Respeita os filtros ativos.

```dax
Total Custo =
SUM('fact_Vendas'[Custo])
```

### Total Lucro

Soma o lucro bruto calculado como receita menos custo de produto; despesas operacionais não fazem parte desta base.

```dax
Total Lucro =
SUM('fact_Vendas'[Lucro])
```

### Total Unidades

Soma as unidades vendidas nos registros selecionados.

```dax
Total Unidades =
SUM('fact_Vendas'[Unidades])
```

### Margem Bruta %

Indicador de rentabilidade: lucro bruto dividido pela receita líquida de desconto. Retorna vazio quando não existe receita na seleção. Não inclui despesas operacionais.

```dax
Margem Bruta % =
DIVIDE([Total Lucro], [Total Receita])
```

### Receita YTD

Receita acumulada desde 1º de janeiro até a última data da seleção, no ano dessa data. Mantém os filtros de produto e geografia.

```dax
Receita YTD =
TOTALYTD([Total Receita], 'DimDate'[Date])
```

### Receita YTD Ano Anterior

Receita acumulada no mesmo intervalo anual do ano anterior. É a base de comparação do crescimento da receita acumulada. Sem histórico retorna vazio.

```dax
Receita YTD Ano Anterior =
CALCULATE([Receita YTD], SAMEPERIODLASTYEAR('DimDate'[Date]))
```

### Crescimento Receita %

Indicador de crescimento: compara a receita acumulada no ano da última data selecionada com o mesmo intervalo do ano anterior. No período completo compara 2017 com 2016. Sem base de comparação retorna vazio.

```dax
Crescimento Receita % =
DIVIDE([Receita YTD] - [Receita YTD Ano Anterior], [Receita YTD Ano Anterior])
```

### Participação na Receita %

Participação da geografia na receita da seleção visível. Remove apenas o detalhamento por geografia para obter o denominador; preserva os filtros externos. Mede distribuição interna da receita, não market share.

```dax
Participação na Receita % =
DIVIDE([Total Receita], CALCULATE([Total Receita], ALLSELECTED('dim_Geografia')))
```

## Interpretação

- **Margem bruta:** usa a razão entre os totais de lucro e receita; não é a média simples das margens por venda.
- **Crescimento da receita:** compara o acumulado no ano da última data selecionada com o mesmo intervalo do ano anterior. No período completo, a comparação é 2017 × 2016. Sem base anterior, o resultado fica vazio.
- **Participação na receita:** mede a participação dentro da seleção do relatório. Não representa participação de mercado.
- **Variações mensais em valor:** comparam o último mês completo selecionado com o mês completo anterior; são diferenças absolutas, não percentuais. Sem histórico, retornam vazio.
- **Títulos dinâmicos:** refletem o contexto da seleção para explicar os recortes apresentados.

## Catálogo completo

Cada medida abaixo reproduz a expressão e a descrição extraídas do PBIX final.

<details>
<summary>Custo Change vs Prior Month</summary>

**Tabela:** `fact_Vendas` · **Pasta:** `Comparações temporais`

Diferença absoluta de custo entre o último mês selecionado e o mês anterior, ambos completos. Remove somente o filtro de calendário para alcançar o mês anterior. Sem histórico retorna vazio; não é uma taxa percentual.

```dax
Custo Change vs Prior Month =
VAR UltimaData = MAX('DimDate'[Date])
VAR InicioAtual = DATE(YEAR(UltimaData), MONTH(UltimaData), 1)
VAR InicioAnterior = EDATE(InicioAtual, -1)
VAR Atual = CALCULATE([Total Custo], FILTER(ALL('DimDate'), 'DimDate'[Date] >= InicioAtual && 'DimDate'[Date] <= EOMONTH(InicioAtual, 0)))
VAR Anterior = CALCULATE([Total Custo], FILTER(ALL('DimDate'), 'DimDate'[Date] >= InicioAnterior && 'DimDate'[Date] <= EOMONTH(InicioAnterior, 0)))
RETURN IF(ISBLANK(Anterior), BLANK(), Atual - Anterior)
```

</details>

<details>
<summary>Custo Direction</summary>

**Tabela:** `fact_Vendas` · **Pasta:** `Comparações temporais`

Seta que indica se custo cresceu, caiu ou ficou estável em relação ao mês anterior. Sem comparação disponível retorna vazio.

```dax
Custo Direction =
VAR Variacao = [Custo Change vs Prior Month]
RETURN IF(ISBLANK(Variacao), BLANK(), IF(Variacao > 0, UNICHAR(9650), IF(Variacao < 0, UNICHAR(9660), UNICHAR(9658))))
```

</details>

<details>
<summary>Custo Running Total</summary>

**Tabela:** `fact_Vendas` · **Pasta:** `Comparações temporais`

Acumula custo até a data do ponto atual, dentro do período selecionado; mantém os filtros de produto, representante e geografia.

```dax
Custo Running Total =
VAR Limite = MAX('DimDate'[Date])
RETURN CALCULATE([Total Custo], FILTER(ALLSELECTED('DimDate'[Date]), 'DimDate'[Date] <= Limite))
```

</details>

<details>
<summary>Custo Sign</summary>

**Tabela:** `fact_Vendas` · **Pasta:** `Comparações temporais`

Sinal da variação mensal de custo: 1 para aumento, -1 para queda e 0 para estabilidade. Sem histórico retorna vazio.

```dax
Custo Sign =
VAR Variacao = [Custo Change vs Prior Month]
RETURN IF(ISBLANK(Variacao), BLANK(), SIGN(Variacao))
```

</details>

<details>
<summary>Lucro Change vs Prior Month</summary>

**Tabela:** `fact_Vendas` · **Pasta:** `Comparações temporais`

Diferença absoluta de lucro entre o último mês selecionado e o mês anterior, ambos completos. Remove somente o filtro de calendário para alcançar o mês anterior. Sem histórico retorna vazio; não é uma taxa percentual.

```dax
Lucro Change vs Prior Month =
VAR UltimaData = MAX('DimDate'[Date])
VAR InicioAtual = DATE(YEAR(UltimaData), MONTH(UltimaData), 1)
VAR InicioAnterior = EDATE(InicioAtual, -1)
VAR Atual = CALCULATE([Total Lucro], FILTER(ALL('DimDate'), 'DimDate'[Date] >= InicioAtual && 'DimDate'[Date] <= EOMONTH(InicioAtual, 0)))
VAR Anterior = CALCULATE([Total Lucro], FILTER(ALL('DimDate'), 'DimDate'[Date] >= InicioAnterior && 'DimDate'[Date] <= EOMONTH(InicioAnterior, 0)))
RETURN IF(ISBLANK(Anterior), BLANK(), Atual - Anterior)
```

</details>

<details>
<summary>Lucro Direction</summary>

**Tabela:** `fact_Vendas` · **Pasta:** `Comparações temporais`

Seta que indica se lucro cresceu, caiu ou ficou estável em relação ao mês anterior. Sem comparação disponível retorna vazio.

```dax
Lucro Direction =
VAR Variacao = [Lucro Change vs Prior Month]
RETURN IF(ISBLANK(Variacao), BLANK(), IF(Variacao > 0, UNICHAR(9650), IF(Variacao < 0, UNICHAR(9660), UNICHAR(9658))))
```

</details>

<details>
<summary>Lucro Running Total</summary>

**Tabela:** `fact_Vendas` · **Pasta:** `Comparações temporais`

Acumula lucro até a data do ponto atual, dentro do período selecionado; mantém os filtros de produto, representante e geografia.

```dax
Lucro Running Total =
VAR Limite = MAX('DimDate'[Date])
RETURN CALCULATE([Total Lucro], FILTER(ALLSELECTED('DimDate'[Date]), 'DimDate'[Date] <= Limite))
```

</details>

<details>
<summary>Lucro Sign</summary>

**Tabela:** `fact_Vendas` · **Pasta:** `Comparações temporais`

Sinal da variação mensal de lucro: 1 para aumento, -1 para queda e 0 para estabilidade. Sem histórico retorna vazio.

```dax
Lucro Sign =
VAR Variacao = [Lucro Change vs Prior Month]
RETURN IF(ISBLANK(Variacao), BLANK(), SIGN(Variacao))
```

</details>

<details>
<summary>Receita Change vs Prior Month</summary>

**Tabela:** `fact_Vendas` · **Pasta:** `Comparações temporais`

Diferença absoluta de receita entre o último mês selecionado e o mês anterior, ambos completos. Remove somente o filtro de calendário para alcançar o mês anterior. Sem histórico retorna vazio; não é uma taxa percentual.

```dax
Receita Change vs Prior Month =
VAR UltimaData = MAX('DimDate'[Date])
VAR InicioAtual = DATE(YEAR(UltimaData), MONTH(UltimaData), 1)
VAR InicioAnterior = EDATE(InicioAtual, -1)
VAR Atual = CALCULATE([Total Receita], FILTER(ALL('DimDate'), 'DimDate'[Date] >= InicioAtual && 'DimDate'[Date] <= EOMONTH(InicioAtual, 0)))
VAR Anterior = CALCULATE([Total Receita], FILTER(ALL('DimDate'), 'DimDate'[Date] >= InicioAnterior && 'DimDate'[Date] <= EOMONTH(InicioAnterior, 0)))
RETURN IF(ISBLANK(Anterior), BLANK(), Atual - Anterior)
```

</details>

<details>
<summary>Receita Direction</summary>

**Tabela:** `fact_Vendas` · **Pasta:** `Comparações temporais`

Seta que indica se receita cresceu, caiu ou ficou estável em relação ao mês anterior. Sem comparação disponível retorna vazio.

```dax
Receita Direction =
VAR Variacao = [Receita Change vs Prior Month]
RETURN IF(ISBLANK(Variacao), BLANK(), IF(Variacao > 0, UNICHAR(9650), IF(Variacao < 0, UNICHAR(9660), UNICHAR(9658))))
```

</details>

<details>
<summary>Receita Running Total</summary>

**Tabela:** `fact_Vendas` · **Pasta:** `Comparações temporais`

Acumula receita até a data do ponto atual, dentro do período selecionado; mantém os filtros de produto, representante e geografia.

```dax
Receita Running Total =
VAR Limite = MAX('DimDate'[Date])
RETURN CALCULATE([Total Receita], FILTER(ALLSELECTED('DimDate'[Date]), 'DimDate'[Date] <= Limite))
```

</details>

<details>
<summary>Receita Sign</summary>

**Tabela:** `fact_Vendas` · **Pasta:** `Comparações temporais`

Sinal da variação mensal de receita: 1 para aumento, -1 para queda e 0 para estabilidade. Sem histórico retorna vazio.

```dax
Receita Sign =
VAR Variacao = [Receita Change vs Prior Month]
RETURN IF(ISBLANK(Variacao), BLANK(), SIGN(Variacao))
```

</details>

<details>
<summary>Receita YTD</summary>

**Tabela:** `fact_Vendas` · **Pasta:** `Comparações temporais`

Receita acumulada desde 1º de janeiro até a última data da seleção, no ano dessa data. Mantém os filtros de produto e geografia.

```dax
Receita YTD =
TOTALYTD([Total Receita], 'DimDate'[Date])
```

</details>

<details>
<summary>Receita YTD Ano Anterior</summary>

**Tabela:** `fact_Vendas` · **Pasta:** `Comparações temporais`

Receita acumulada no mesmo intervalo anual do ano anterior. É a base de comparação do crescimento da receita acumulada. Sem histórico retorna vazio.

```dax
Receita YTD Ano Anterior =
CALCULATE([Receita YTD], SAMEPERIODLASTYEAR('DimDate'[Date]))
```

</details>

<details>
<summary>Unidades Change vs Prior Month</summary>

**Tabela:** `fact_Vendas` · **Pasta:** `Comparações temporais`

Diferença absoluta de unidades entre o último mês selecionado e o mês anterior, ambos completos. Remove somente o filtro de calendário para alcançar o mês anterior. Sem histórico retorna vazio; não é uma taxa percentual.

```dax
Unidades Change vs Prior Month =
VAR UltimaData = MAX('DimDate'[Date])
VAR InicioAtual = DATE(YEAR(UltimaData), MONTH(UltimaData), 1)
VAR InicioAnterior = EDATE(InicioAtual, -1)
VAR Atual = CALCULATE([Total Unidades], FILTER(ALL('DimDate'), 'DimDate'[Date] >= InicioAtual && 'DimDate'[Date] <= EOMONTH(InicioAtual, 0)))
VAR Anterior = CALCULATE([Total Unidades], FILTER(ALL('DimDate'), 'DimDate'[Date] >= InicioAnterior && 'DimDate'[Date] <= EOMONTH(InicioAnterior, 0)))
RETURN IF(ISBLANK(Anterior), BLANK(), Atual - Anterior)
```

</details>

<details>
<summary>Unidades Direction</summary>

**Tabela:** `fact_Vendas` · **Pasta:** `Comparações temporais`

Seta que indica se unidades cresceu, caiu ou ficou estável em relação ao mês anterior. Sem comparação disponível retorna vazio.

```dax
Unidades Direction =
VAR Variacao = [Unidades Change vs Prior Month]
RETURN IF(ISBLANK(Variacao), BLANK(), IF(Variacao > 0, UNICHAR(9650), IF(Variacao < 0, UNICHAR(9660), UNICHAR(9658))))
```

</details>

<details>
<summary>Unidades Running Total</summary>

**Tabela:** `fact_Vendas` · **Pasta:** `Comparações temporais`

Acumula unidades até a data do ponto atual, dentro do período selecionado; mantém os filtros de produto, representante e geografia.

```dax
Unidades Running Total =
VAR Limite = MAX('DimDate'[Date])
RETURN CALCULATE([Total Unidades], FILTER(ALLSELECTED('DimDate'[Date]), 'DimDate'[Date] <= Limite))
```

</details>

<details>
<summary>Unidades Sign</summary>

**Tabela:** `fact_Vendas` · **Pasta:** `Comparações temporais`

Sinal da variação mensal de unidades: 1 para aumento, -1 para queda e 0 para estabilidade. Sem histórico retorna vazio.

```dax
Unidades Sign =
VAR Variacao = [Unidades Change vs Prior Month]
RETURN IF(ISBLANK(Variacao), BLANK(), SIGN(Variacao))
```

</details>

<details>
<summary>Crescimento Receita %</summary>

**Tabela:** `fact_Vendas` · **Pasta:** `Indicadores`

Indicador de crescimento: compara a receita acumulada no ano da última data selecionada com o mesmo intervalo do ano anterior. No período completo compara 2017 com 2016. Sem base de comparação retorna vazio.

```dax
Crescimento Receita % =
DIVIDE([Receita YTD] - [Receita YTD Ano Anterior], [Receita YTD Ano Anterior])
```

</details>

<details>
<summary>Margem Bruta %</summary>

**Tabela:** `fact_Vendas` · **Pasta:** `Indicadores`

Indicador de rentabilidade: lucro bruto dividido pela receita líquida de desconto. Retorna vazio quando não existe receita na seleção. Não inclui despesas operacionais.

```dax
Margem Bruta % =
DIVIDE([Total Lucro], [Total Receita])
```

</details>

<details>
<summary>Participação na Receita %</summary>

**Tabela:** `fact_Vendas` · **Pasta:** `Indicadores`

Participação da geografia na receita da seleção visível. Remove apenas o detalhamento por geografia para obter o denominador; preserva os filtros externos. Mede distribuição interna da receita, não market share.

```dax
Participação na Receita % =
DIVIDE([Total Receita], CALCULATE([Total Receita], ALLSELECTED('dim_Geografia')))
```

</details>

<details>
<summary>Average Custo</summary>

**Tabela:** `fact_Vendas` · **Pasta:** `Medidas de apoio`

Média aritmética de fact_Vendas[Custo] nas linhas visíveis. Na fato é uma média por registro de venda, sem ponderação adicional; no cadastro é uma média por item.

```dax
Average Custo =
AVERAGE('fact_Vendas'[Custo])
```

</details>

<details>
<summary>Average CustoPadrao</summary>

**Tabela:** `dim_Produto` · **Pasta:** `Medidas de apoio`

Média aritmética de dim_Produto[CustoPadrao] nas linhas visíveis. Na fato é uma média por registro de venda, sem ponderação adicional; no cadastro é uma média por item.

```dax
Average CustoPadrao =
AVERAGE('dim_Produto'[CustoPadrao])
```

</details>

<details>
<summary>Average FatorCusto</summary>

**Tabela:** `fact_Vendas` · **Pasta:** `Medidas de apoio`

Média aritmética de fact_Vendas[FatorCusto] nas linhas visíveis. Na fato é uma média por registro de venda, sem ponderação adicional; no cadastro é uma média por item.

```dax
Average FatorCusto =
AVERAGE('fact_Vendas'[FatorCusto])
```

</details>

<details>
<summary>Average Lucro</summary>

**Tabela:** `fact_Vendas` · **Pasta:** `Medidas de apoio`

Média aritmética de fact_Vendas[Lucro] nas linhas visíveis. Na fato é uma média por registro de venda, sem ponderação adicional; no cadastro é uma média por item.

```dax
Average Lucro =
AVERAGE('fact_Vendas'[Lucro])
```

</details>

<details>
<summary>Average PrecoVarejo</summary>

**Tabela:** `dim_Produto` · **Pasta:** `Medidas de apoio`

Média aritmética de dim_Produto[PrecoVarejo] nas linhas visíveis. Na fato é uma média por registro de venda, sem ponderação adicional; no cadastro é uma média por item.

```dax
Average PrecoVarejo =
AVERAGE('dim_Produto'[PrecoVarejo])
```

</details>

<details>
<summary>Average Receita</summary>

**Tabela:** `fact_Vendas` · **Pasta:** `Medidas de apoio`

Média aritmética de fact_Vendas[Receita] nas linhas visíveis. Na fato é uma média por registro de venda, sem ponderação adicional; no cadastro é uma média por item.

```dax
Average Receita =
AVERAGE('fact_Vendas'[Receita])
```

</details>

<details>
<summary>Average Unidades</summary>

**Tabela:** `fact_Vendas` · **Pasta:** `Medidas de apoio`

Média aritmética de fact_Vendas[Unidades] nas linhas visíveis. Na fato é uma média por registro de venda, sem ponderação adicional; no cadastro é uma média por item.

```dax
Average Unidades =
AVERAGE('fact_Vendas'[Unidades])
```

</details>

<details>
<summary>Distinct CategoriaKey</summary>

**Tabela:** `dim_Produto` · **Pasta:** `Medidas de apoio`

Conta os valores distintos de CategoriaKey em dim_Produto, respeitando o contexto de filtro. No cadastro conta itens disponíveis; na fato conta itens com vendas na seleção.

```dax
Distinct CategoriaKey =
DISTINCTCOUNT('dim_Produto'[CategoriaKey])
```

</details>

<details>
<summary>Distinct LocalizacaoID (dim_Geografia)</summary>

**Tabela:** `dim_Geografia` · **Pasta:** `Medidas de apoio`

Conta os valores distintos de LocalizacaoID em dim_Geografia, respeitando o contexto de filtro. No cadastro conta itens disponíveis; na fato conta itens com vendas na seleção.

```dax
Distinct LocalizacaoID (dim_Geografia) =
DISTINCTCOUNT('dim_Geografia'[LocalizacaoID])
```

</details>

<details>
<summary>Distinct LocalizacaoID (fact_Vendas)</summary>

**Tabela:** `fact_Vendas` · **Pasta:** `Medidas de apoio`

Conta os valores distintos de LocalizacaoID em fact_Vendas, respeitando o contexto de filtro. No cadastro conta itens disponíveis; na fato conta itens com vendas na seleção.

```dax
Distinct LocalizacaoID (fact_Vendas) =
DISTINCTCOUNT('fact_Vendas'[LocalizacaoID])
```

</details>

<details>
<summary>Distinct ProdutoID (dim_Produto)</summary>

**Tabela:** `dim_Produto` · **Pasta:** `Medidas de apoio`

Conta os valores distintos de ProdutoID em dim_Produto, respeitando o contexto de filtro. No cadastro conta itens disponíveis; na fato conta itens com vendas na seleção.

```dax
Distinct ProdutoID (dim_Produto) =
DISTINCTCOUNT('dim_Produto'[ProdutoID])
```

</details>

<details>
<summary>Distinct ProdutoID (fact_Vendas)</summary>

**Tabela:** `fact_Vendas` · **Pasta:** `Medidas de apoio`

Conta os valores distintos de ProdutoID em fact_Vendas, respeitando o contexto de filtro. No cadastro conta itens disponíveis; na fato conta itens com vendas na seleção.

```dax
Distinct ProdutoID (fact_Vendas) =
DISTINCTCOUNT('fact_Vendas'[ProdutoID])
```

</details>

<details>
<summary>Distinct RepresentanteID (dim_Representante)</summary>

**Tabela:** `dim_Representante` · **Pasta:** `Medidas de apoio`

Conta os valores distintos de RepresentanteID em dim_Representante, respeitando o contexto de filtro. No cadastro conta itens disponíveis; na fato conta itens com vendas na seleção.

```dax
Distinct RepresentanteID (dim_Representante) =
DISTINCTCOUNT('dim_Representante'[RepresentanteID])
```

</details>

<details>
<summary>Distinct RepresentanteID (fact_Vendas)</summary>

**Tabela:** `fact_Vendas` · **Pasta:** `Medidas de apoio`

Conta os valores distintos de RepresentanteID em fact_Vendas, respeitando o contexto de filtro. No cadastro conta itens disponíveis; na fato conta itens com vendas na seleção.

```dax
Distinct RepresentanteID (fact_Vendas) =
DISTINCTCOUNT('fact_Vendas'[RepresentanteID])
```

</details>

<details>
<summary>Distinct SubcategoriaID</summary>

**Tabela:** `dim_Produto` · **Pasta:** `Medidas de apoio`

Conta os valores distintos de SubcategoriaID em dim_Produto, respeitando o contexto de filtro. No cadastro conta itens disponíveis; na fato conta itens com vendas na seleção.

```dax
Distinct SubcategoriaID =
DISTINCTCOUNT('dim_Produto'[SubcategoriaID])
```

</details>

<details>
<summary>Distinct VendaID</summary>

**Tabela:** `fact_Vendas` · **Pasta:** `Medidas de apoio`

Conta os valores distintos de VendaID em fact_Vendas, respeitando o contexto de filtro. No cadastro conta itens disponíveis; na fato conta itens com vendas na seleção.

```dax
Distinct VendaID =
DISTINCTCOUNT('fact_Vendas'[VendaID])
```

</details>

<details>
<summary>Max Custo</summary>

**Tabela:** `fact_Vendas` · **Pasta:** `Medidas de apoio`

Maior valor de fact_Vendas[Custo] no contexto de filtro atual.

```dax
Max Custo =
MAX('fact_Vendas'[Custo])
```

</details>

<details>
<summary>Max CustoPadrao</summary>

**Tabela:** `dim_Produto` · **Pasta:** `Medidas de apoio`

Maior valor de dim_Produto[CustoPadrao] no contexto de filtro atual.

```dax
Max CustoPadrao =
MAX('dim_Produto'[CustoPadrao])
```

</details>

<details>
<summary>Max FatorCusto</summary>

**Tabela:** `fact_Vendas` · **Pasta:** `Medidas de apoio`

Maior valor de fact_Vendas[FatorCusto] no contexto de filtro atual.

```dax
Max FatorCusto =
MAX('fact_Vendas'[FatorCusto])
```

</details>

<details>
<summary>Max Lucro</summary>

**Tabela:** `fact_Vendas` · **Pasta:** `Medidas de apoio`

Maior valor de fact_Vendas[Lucro] no contexto de filtro atual.

```dax
Max Lucro =
MAX('fact_Vendas'[Lucro])
```

</details>

<details>
<summary>Max PrecoVarejo</summary>

**Tabela:** `dim_Produto` · **Pasta:** `Medidas de apoio`

Maior valor de dim_Produto[PrecoVarejo] no contexto de filtro atual.

```dax
Max PrecoVarejo =
MAX('dim_Produto'[PrecoVarejo])
```

</details>

<details>
<summary>Max Receita</summary>

**Tabela:** `fact_Vendas` · **Pasta:** `Medidas de apoio`

Maior valor de fact_Vendas[Receita] no contexto de filtro atual.

```dax
Max Receita =
MAX('fact_Vendas'[Receita])
```

</details>

<details>
<summary>Max Unidades</summary>

**Tabela:** `fact_Vendas` · **Pasta:** `Medidas de apoio`

Maior valor de fact_Vendas[Unidades] no contexto de filtro atual.

```dax
Max Unidades =
MAX('fact_Vendas'[Unidades])
```

</details>

<details>
<summary>dim_Calendario Record Count</summary>

**Tabela:** `DimDate` · **Pasta:** `Medidas de apoio`

Conta as linhas de DimDate no contexto de filtro atual.

```dax
dim_Calendario Record Count =
COUNTROWS('DimDate')
```

</details>

<details>
<summary>dim_Geografia Record Count</summary>

**Tabela:** `dim_Geografia` · **Pasta:** `Medidas de apoio`

Conta as linhas de dim_Geografia no contexto de filtro atual.

```dax
dim_Geografia Record Count =
COUNTROWS('dim_Geografia')
```

</details>

<details>
<summary>dim_Produto Record Count</summary>

**Tabela:** `dim_Produto` · **Pasta:** `Medidas de apoio`

Conta as linhas de dim_Produto no contexto de filtro atual.

```dax
dim_Produto Record Count =
COUNTROWS('dim_Produto')
```

</details>

<details>
<summary>dim_Representante Record Count</summary>

**Tabela:** `dim_Representante` · **Pasta:** `Medidas de apoio`

Conta as linhas de dim_Representante no contexto de filtro atual.

```dax
dim_Representante Record Count =
COUNTROWS('dim_Representante')
```

</details>

<details>
<summary>fact_Vendas Record Count</summary>

**Tabela:** `fact_Vendas` · **Pasta:** `Medidas de apoio`

Conta as linhas de fact_Vendas no contexto de filtro atual.

```dax
fact_Vendas Record Count =
COUNTROWS('fact_Vendas')
```

</details>

<details>
<summary>Total Custo</summary>

**Tabela:** `fact_Vendas` · **Pasta:** `Totais`

Soma o custo: unidades × custo padrão × fator de custo. Respeita os filtros ativos.

```dax
Total Custo =
SUM('fact_Vendas'[Custo])
```

</details>

<details>
<summary>Total Lucro</summary>

**Tabela:** `fact_Vendas` · **Pasta:** `Totais`

Soma o lucro bruto calculado como receita menos custo de produto; despesas operacionais não fazem parte desta base.

```dax
Total Lucro =
SUM('fact_Vendas'[Lucro])
```

</details>

<details>
<summary>Total Receita</summary>

**Tabela:** `fact_Vendas` · **Pasta:** `Totais`

Soma a receita líquida de desconto: unidades × preço de varejo × (1 − desconto). Respeita os filtros ativos.

```dax
Total Receita =
SUM('fact_Vendas'[Receita])
```

</details>

<details>
<summary>Total Unidades</summary>

**Tabela:** `fact_Vendas` · **Pasta:** `Totais`

Soma as unidades vendidas nos registros selecionados.

```dax
Total Unidades =
SUM('fact_Vendas'[Unidades])
```

</details>

<details>
<summary>Contexto dos Filtros</summary>

**Tabela:** `fact_Vendas` · **Pasta:** `Títulos dinâmicos`

Texto usado nos títulos dinâmicos. Mostra o intervalo de datas e as seleções de cidade e subcategoria. É recalculado quando o usuário altera os filtros.

```dax
Contexto dos Filtros =
VAR Inicio = MIN('DimDate'[Date])
VAR Fim = MAX('DimDate'[Date])
VAR Cidade = IF(HASONEVALUE('dim_Geografia'[Cidade]), SELECTEDVALUE('dim_Geografia'[Cidade]), IF(ISFILTERED('dim_Geografia'[Cidade]), FORMAT(COUNTROWS(VALUES('dim_Geografia'[Cidade])), "0") & " cidades", "Todas as cidades"))
VAR Produto = IF(HASONEVALUE('dim_Produto'[SubCategoriaNome]), SELECTEDVALUE('dim_Produto'[SubCategoriaNome]), IF(ISFILTERED('dim_Produto'[SubCategoriaNome]), "Subcategorias selecionadas", "Todas as subcategorias"))
RETURN IF(ISBLANK(Inicio), "Sem dados para os filtros", FORMAT(Inicio, "dd/MM/yy") & "–" & FORMAT(Fim, "dd/MM/yy") & " · " & Cidade & " · " & Produto)
```

</details>

<details>
<summary>Título p1_kpi_3</summary>

**Tabela:** `fact_Vendas` · **Pasta:** `Títulos dinâmicos`

Título do visual: Margem bruta. Inclui período, cidade e subcategoria da seleção.

```dax
Título p1_kpi_3 =
"Margem bruta | " & [Contexto dos Filtros]
```

</details>

<details>
<summary>Título p1_kpi_4</summary>

**Tabela:** `fact_Vendas` · **Pasta:** `Títulos dinâmicos`

Título do visual: Receita YTD: variação anual. Inclui período, cidade e subcategoria da seleção.

```dax
Título p1_kpi_4 =
"Receita YTD: variação anual | " & [Contexto dos Filtros]
```

</details>

<details>
<summary>Título p1_v1</summary>

**Tabela:** `fact_Vendas` · **Pasta:** `Títulos dinâmicos`

Título do visual: Lucro bruto. Inclui período, cidade e subcategoria da seleção.

```dax
Título p1_v1 =
"Lucro bruto | " & [Contexto dos Filtros]
```

</details>

<details>
<summary>Título p1_v2</summary>

**Tabela:** `fact_Vendas` · **Pasta:** `Títulos dinâmicos`

Título do visual: Lucro bruto ao longo do tempo. Inclui período, cidade e subcategoria da seleção.

```dax
Título p1_v2 =
"Lucro bruto ao longo do tempo | " & [Contexto dos Filtros]
```

</details>

<details>
<summary>Título p1_v3</summary>

**Tabela:** `fact_Vendas` · **Pasta:** `Títulos dinâmicos`

Título do visual: Lucro bruto por subcategoria. Inclui período, cidade e subcategoria da seleção.

```dax
Título p1_v3 =
"Lucro bruto por subcategoria | " & [Contexto dos Filtros]
```

</details>

<details>
<summary>Título p1_v4</summary>

**Tabela:** `fact_Vendas` · **Pasta:** `Títulos dinâmicos`

Título do visual: Receita líquida. Inclui período, cidade e subcategoria da seleção.

```dax
Título p1_v4 =
"Receita líquida | " & [Contexto dos Filtros]
```

</details>

<details>
<summary>Título p1_v5</summary>

**Tabela:** `fact_Vendas` · **Pasta:** `Títulos dinâmicos`

Título do visual: Quantidade de vendas. Inclui período, cidade e subcategoria da seleção.

```dax
Título p1_v5 =
"Quantidade de vendas | " & [Contexto dos Filtros]
```

</details>

<details>
<summary>Título p2_v1</summary>

**Tabela:** `fact_Vendas` · **Pasta:** `Títulos dinâmicos`

Título do visual: Receita por país. Inclui período, cidade e subcategoria da seleção.

```dax
Título p2_v1 =
"Receita por país | " & [Contexto dos Filtros]
```

</details>

<details>
<summary>Título p2_v2</summary>

**Tabela:** `fact_Vendas` · **Pasta:** `Títulos dinâmicos`

Título do visual: Receita ao longo do tempo. Inclui período, cidade e subcategoria da seleção.

```dax
Título p2_v2 =
"Receita ao longo do tempo | " & [Contexto dos Filtros]
```

</details>

<details>
<summary>Título p2_v3</summary>

**Tabela:** `fact_Vendas` · **Pasta:** `Títulos dinâmicos`

Título do visual: Receita por subcategoria. Inclui período, cidade e subcategoria da seleção.

```dax
Título p2_v3 =
"Receita por subcategoria | " & [Contexto dos Filtros]
```

</details>

<details>
<summary>Título p3_v1</summary>

**Tabela:** `fact_Vendas` · **Pasta:** `Títulos dinâmicos`

Título do visual: Vendas por cidade. Inclui período, cidade e subcategoria da seleção.

```dax
Título p3_v1 =
"Vendas por cidade | " & [Contexto dos Filtros]
```

</details>

<details>
<summary>Título p3_v2</summary>

**Tabela:** `fact_Vendas` · **Pasta:** `Títulos dinâmicos`

Título do visual: Vendas por cor ao longo do tempo. Inclui período, cidade e subcategoria da seleção.

```dax
Título p3_v2 =
"Vendas por cor ao longo do tempo | " & [Contexto dos Filtros]
```

</details>

<details>
<summary>Título p3_v3</summary>

**Tabela:** `fact_Vendas` · **Pasta:** `Títulos dinâmicos`

Título do visual: Vendas por país e cidade. Inclui período, cidade e subcategoria da seleção.

```dax
Título p3_v3 =
"Vendas por país e cidade | " & [Contexto dos Filtros]
```

</details>

<details>
<summary>Título p4_v1</summary>

**Tabela:** `fact_Vendas` · **Pasta:** `Títulos dinâmicos`

Título do visual: Cidades com mais unidades vendidas. Inclui período, cidade e subcategoria da seleção.

```dax
Título p4_v1 =
"Cidades com mais unidades vendidas | " & [Contexto dos Filtros]
```

</details>

<details>
<summary>Título p4_v2</summary>

**Tabela:** `fact_Vendas` · **Pasta:** `Títulos dinâmicos`

Título do visual: Custo e lucro bruto por cidade. Inclui período, cidade e subcategoria da seleção.

```dax
Título p4_v2 =
"Custo e lucro bruto por cidade | " & [Contexto dos Filtros]
```

</details>

<details>
<summary>Título p4_v3</summary>

**Tabela:** `fact_Vendas` · **Pasta:** `Títulos dinâmicos`

Título do visual: Detalhamento das vendas. Inclui período, cidade e subcategoria da seleção.

```dax
Título p4_v3 =
"Detalhamento das vendas | " & [Contexto dos Filtros]
```

</details>

<details>
<summary>Título tooltip-trend</summary>

**Tabela:** `fact_Vendas` · **Pasta:** `Títulos dinâmicos`

Título do visual: Evolução do lucro bruto. Inclui período, cidade e subcategoria da seleção.

```dax
Título tooltip-trend =
"Evolução do lucro bruto | " & [Contexto dos Filtros]
```

</details>
