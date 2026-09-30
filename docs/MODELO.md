# Modelo e preparação dos dados

## Granularidade e tabelas

Cada linha de `fact_Vendas` representa um registro de venda identificado por `VendaID`. A base contém 54.530 identificadores de venda únicos.

| Tabela | Linhas | Chave | Função |
| :--- | ---: | :--- | :--- |
| `fact_Vendas` | 54.530 | `VendaID` | Data, quantidades, desconto, fator de custo, receita, custo e lucro. |
| `dim_Produto` | 13 | `ProdutoID` | Produto, cor, categoria, subcategoria, preço de varejo e custo padrão. |
| `dim_Representante` | 7 | `RepresentanteID` | Representante comercial. |
| `dim_Geografia` | 7 | `LocalizacaoID` | País e cidade. |
| `DimDate` | 1.461 | `Date` | Calendário diário de 01/01/2014 a 31/12/2017. |

## Relacionamentos

| Dimensão · lado 1 | Fato · lado muitos | Estado | Filtro |
| :--- | :--- | :--- | :--- |
| `dim_Produto[ProdutoID]` | `fact_Vendas[ProdutoID]` | Ativo | Dimensão → fato |
| `dim_Representante[RepresentanteID]` | `fact_Vendas[RepresentanteID]` | Ativo | Dimensão → fato |
| `dim_Geografia[LocalizacaoID]` | `fact_Vendas[LocalizacaoID]` | Ativo | Dimensão → fato |
| `DimDate[Date]` | `fact_Vendas[Data]` | Ativo | Dimensão → fato |

As chaves das dimensões são únicas e não há chaves órfãs na fato. Os produtos 12 e 13 permanecem no cadastro mesmo sem vendas: eles representam produtos cadastrados, não registros duplicados da fato.

## Power Query

As cinco consultas M estão na definição do modelo semântico. As fontes de produtos, representantes, geografia e vendas são CSVs comprimidos incorporados à consulta; o calendário é gerado a partir do intervalo de datas das vendas.

A preparação inclui interpretação do CSV, conversão explícita de tipos, padronização de chaves, preservação dos atributos dimensionais, cálculos auxiliares e geração do calendário com ano, número do mês, nome do mês e ano-mês. Os registros da fato verificada não contêm valores nulos nas suas 13 colunas.

Os cálculos financeiros por venda seguem:

```text
Receita = Unidades × Preço de varejo × (1 − Desconto)
Custo   = Unidades × Custo padrão × Fator de custo
Lucro   = Receita − Custo
```

Os preços e custos vêm de `dim_Produto`. Os totais DAX agregam as colunas calculadas da fato, e a margem é a razão entre lucro total e receita total.

## Organização dos arquivos

`projeto/pratique_powerbi.pbip` aponta para o relatório em `pratique_powerbi.Report`; o arquivo `definition.pbir` referencia `../pratique_powerbi.SemanticModel`. O `model.bim` contém as tabelas, consultas M, relacionamentos e medidas.

As definições do relatório foram copiadas da versão final salva no Power BI Desktop. O modelo editável acompanha as mesmas tabelas, medidas e fontes incorporadas da versão corrigida. O PBIX em `dashboard/` é a entrega principal.
