# Conferência técnica da entrega

Referência: `dashboard/pratique_powerbi.pbix`, versão final atualizada e salva no Power BI Desktop pelo autor.

## Identificação do arquivo

- Tamanho: **2,229,309 bytes**.
- SHA-256: `9fb5f871cadfccae9a114f00caa26eeba1418e17d155b2cb1b585a266347b460`.
- A cópia publicada preserva exatamente os bytes dessa entrega final.

## Dados e modelo

| Conferência | Resultado |
| :--- | :--- |
| Tabelas carregadas | 5 |
| Consultas Power Query | 5 |
| Registros de venda | 54.530 |
| `VendaID` únicos | 54.530 |
| Valores nulos nas colunas da fato | 0 |
| Chaves das dimensões | Únicas e sem valores nulos |
| Chaves órfãs na fato | 0 |
| Calendário | 1.461 datas únicas, cobrindo todas as vendas |
| Relacionamentos | 4 ativos, muitos para um, direção única |
| Medidas DAX | 71 |
| Medidas com descrição | 71 |
| Mensagens de erro armazenadas nas medidas | Nenhuma |
| Referências inexistentes nos visuais | Nenhuma |

## Totais recalculados a partir da fato

| Cálculo | Valor |
| :--- | ---: |
| Receita | 73.651.617,5850 |
| Custo | 37.993.700,7677 |
| Lucro bruto | 35.657.916,8173 |
| Unidades | 4.026.277 |
| Lucro / receita | 48,414302% |
| Receita 2017 / receita 2016 − 1 | 37,219466% |

A receita menos o custo coincide com o lucro, dentro da tolerância numérica. Os resumos em `dados/` foram extraídos dessa mesma fato, sem acrescentar observações externas.

## Relatório

- Seis páginas visíveis e uma página oculta de tooltip.
- Cinco cartões, duas tabelas visuais e gráficos de linhas, barras, rosca e dispersão.
- Filtros sincronizados de data, cidade e subcategoria nas páginas analíticas.
- Títulos dinâmicos e páginas de conclusões e documentação das medidas.

## Escopo da conferência

A conferência técnica utiliza leitura dos metadados, das definições do relatório e dos dados importados no PBIX final. O arquivo foi atualizado e salvo pelo autor no Desktop. A imagem do README é um resumo analítico produzido a partir da base, não uma captura da interface do Power BI.

A visualização e o teste manual de cliques e filtros devem ser feitos no Power BI Desktop. Esta documentação não representa uma publicação do relatório no Power BI Service.
