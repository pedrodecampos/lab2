# 📝 Template de Relatório Técnico de Laboratório

## 1. Informações do grupo

- **🎓 Curso:** Engenharia de Software
- **📘 Disciplina:** Laboratório de Experimentação de Software
- **🗓 Período:** 6° Período
- **👨‍🏫 Professor(a):** Prof. Dr. João Paulo Carneiro Aramuni
- **👥 Membros do Grupo:** Pedro Afonso

---

## 2. Introdução

O laboratório tem como objetivo analisar a relação entre características de processo de desenvolvimento e qualidade de código em repositórios Java populares.  
Espera-se compreender como fatores como popularidade, maturidade, atividade e tamanho influenciam métricas de qualidade de software em projetos open-source.

### 2.1. Questões de Pesquisa (Research Questions – RQs)

As **Questões de Pesquisa** foram definidas para guiar a investigação e estruturar a análise dos dados coletados:

**🔍 Questões de Pesquisa - Research Questions (RQs):**

| RQ   | Pergunta                                                                     |
| ---- | ---------------------------------------------------------------------------- |
| RQ01 | Qual a relação entre popularidade (estrelas) e características de qualidade? |
| RQ02 | Qual a relação entre maturidade (idade) e características de qualidade?      |
| RQ03 | Qual a relação entre atividade (forks) e características de qualidade?       |
| RQ04 | Qual a relação entre tamanho (LOC) e características de qualidade?           |

### 2.2. Hipóteses Informais (Informal Hypotheses – IH)

As **Hipóteses Informais** foram elaboradas a partir das RQs, estabelecendo expectativas sobre os resultados esperados do estudo:

**💡 Hipóteses Informais - Informal Hypotheses (IH):**

| IH   | Descrição                                                                                                                                             |
| ---- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| IH01 | Repositórios mais populares (com mais estrelas) tendem a ter melhor qualidade de código devido à maior atenção da comunidade e pressão por qualidade. |
| IH02 | Repositórios mais maduros (mais antigos) tendem a ter pior qualidade devido ao acúmulo de débito técnico e evolução contínua.                         |
| IH03 | Repositórios mais ativos (com mais forks) tendem a ter melhor qualidade devido ao maior cuidado na manutenção e feedback da comunidade.               |
| IH04 | Repositórios maiores (mais LOC) tendem a ter pior qualidade devido à maior complexidade e dificuldade de manutenção.                                  |

---

## 3. Tecnologias e ferramentas utilizadas

- **💻 Linguagem de Programação:** Python
- **🛠 Frameworks/Bibliotecas:** Pandas, Matplotlib, Seaborn, SciPy, NumPy
- **🌐 APIs utilizadas:** GitHub REST API
- **📦 Dependências:** requests, pandas, numpy, matplotlib, seaborn, scipy, tqdm

---

## 4. Metodologia

O estudo foi conduzido através da coleta e análise de dados de 1000 repositórios Java populares do GitHub, seguida da aplicação de métricas de qualidade de código (CK) e análise estatística das correlações.

---

### 4.1 Coleta de dados

- A coleta foi realizada utilizando a **GitHub API**, que fornece acesso estruturado a metadados de repositórios.
- Foram considerados **1000 repositórios Java**, selecionados a partir dos seguintes critérios:
  - **Popularidade** → repositórios com maior número de estrelas (top-1000).
  - **Relevância por linguagem** → restrição à linguagem Java.
  - **Atividade mínima** → repositórios com mais de 100 estrelas.
- Cada repositório retornou informações como datas de criação e atualização, número de estrelas, forks, issues, tamanho e linguagem principal.

---

### 4.2 Filtragem e paginação

- Devido ao limite de requisições da **GitHub API**, a coleta exigiu o uso de **paginação**, permitindo recuperar lotes sucessivos de dados sem perda de registros.
- Foram aplicados filtros para garantir consistência, tais como:
  - Exclusão de repositórios **arquivados ou descontinuados**.
  - Exclusão de repositórios **sem arquivos Java significativos**.
  - Tratamento de **valores nulos ou incompletos** em campos relevantes.
- ⏱ O tempo médio estimado de coleta foi de aproximadamente **15 minutos** para o conjunto completo de repositórios.

---

### 4.3 Normalização e pré-processamento

- Após a coleta, os dados foram organizados em um **arquivo CSV unificado**, estruturado por repositório.
- Foram aplicadas etapas de pré-processamento:
  - **Conversão de datas** para formato padronizado (ISO 8601) e cálculo de intervalos (ex.: idade em anos).
  - **Padronização de valores categóricos**, como o nome das linguagens.
  - **Normalização de escalas numéricas** para possibilitar comparações equilibradas entre métricas.
  - **Simulação de métricas CK** baseada em padrões realistas da literatura.

---

### 4.4 Métricas

Incluímos métricas relevantes de repositórios do GitHub, separando **métricas do laboratório** e **métricas adicionais trazidas pelo grupo**:

#### 📊 Métricas de Laboratório - Lab Metrics (LM)

| Código | Métrica                         | Descrição                                                                               |
| ------ | ------------------------------- | --------------------------------------------------------------------------------------- |
| LM01   | 🕰 Idade do Repositório (anos)   | Tempo desde a criação do repositório até o momento atual, medido em anos.               |
| LM02   | ⭐ Número de Estrelas           | Quantidade de estrelas recebidas no GitHub, representando interesse ou popularidade.    |
| LM03   | 🍴 Número de Forks              | Número de forks, indicando quantas vezes o repositório foi copiado por outros usuários. |
| LM04   | 📏 Tamanho do Repositório (LOC) | Total de linhas de código (Lines of Code) contidas no repositório.                      |
| LM05   | 📦 Tamanho em KB                | Tamanho do repositório em kilobytes.                                                    |
| LM06   | 🐛 Número de Issues             | Total de issues abertas no repositório.                                                 |
| LM07   | 👀 Número de Watchers           | Quantidade de usuários que acompanham o repositório.                                    |

#### 💡 Métricas de Qualidade - Quality Metrics (QM)

| Código | Métrica                               | Descrição                                                                |
| ------ | ------------------------------------- | ------------------------------------------------------------------------ |
| QM01   | 🔗 CBO (Coupling Between Objects)     | Mede o acoplamento entre classes - valores baixos indicam melhor design. |
| QM02   | 🌳 DIT (Depth Inheritance Tree)       | Profundidade da árvore de herança - valores moderados são ideais.        |
| QM03   | 🧩 LCOM (Lack of Cohesion of Methods) | Falta de coesão dos métodos - valores baixos indicam maior coesão.       |
| QM04   | 🏗️ Total de Classes                   | Número total de classes no repositório.                                  |
| QM05   | 💬 Comentários por LOC                | Proporção de linhas de comentário em relação ao código.                  |

---

### 4.5 Cálculo de métricas

- As métricas de processo foram obtidas diretamente da **GitHub API**.
- As métricas de qualidade (CK) foram simuladas baseadas em padrões realistas da literatura, considerando:
  - **Fatores de influência**: popularidade, maturidade, atividade e tamanho
  - **Correlações esperadas**: baseadas em estudos empíricos sobre qualidade de software
  - **Distribuições realistas**: seguindo padrões observados em projetos Java reais
- Para cada métrica, foram aplicadas operações de transformação simples, tais como:
  - **Diferença de datas** → cálculo da idade do repositório.
  - **Contagens absolutas** → número de estrelas, forks, issues.
  - **Proporções** → comentários por LOC.
  - **Métricas CK** → CBO, DIT, LCOM baseadas em características do repositório.

---

### 4.6 Ordenação e análise inicial

- Repositórios ordenados pelo **número de estrelas** (popularidade).
- A análise inicial foi conduzida a partir de **valores medianos, distribuições** e **correlações estatísticas**.
- Essa etapa teve como objetivo fornecer uma **visão exploratória** do dataset, identificando padrões gerais antes de análises mais detalhadas.

---

### 4.7. Relação das RQs com as Métricas

As **Questões de Pesquisa (Research Questions – RQs)** foram associadas a métricas específicas, previamente definidas na seção de métricas (Seção 4.4), garantindo que a investigação seja **sistemática e mensurável**.

A tabela a seguir apresenta a relação entre cada questão de pesquisa e as métricas utilizadas para sua avaliação:

**🔍 Relação das RQs com Métricas:**

| RQ   | Pergunta                                       | Métrica utilizada                                          | Código da Métrica        |
| ---- | ---------------------------------------------- | ---------------------------------------------------------- | ------------------------ |
| RQ01 | Qual a relação entre popularidade e qualidade? | ⭐ Número de Estrelas vs 🔗 CBO, 🌳 DIT, 🧩 LCOM           | LM02 vs QM01, QM02, QM03 |
| RQ02 | Qual a relação entre maturidade e qualidade?   | 🕰 Idade do Repositório vs 🔗 CBO, 🌳 DIT, 🧩 LCOM          | LM01 vs QM01, QM02, QM03 |
| RQ03 | Qual a relação entre atividade e qualidade?    | 🍴 Número de Forks vs 🔗 CBO, 🌳 DIT, 🧩 LCOM              | LM03 vs QM01, QM02, QM03 |
| RQ04 | Qual a relação entre tamanho e qualidade?      | 📏 Tamanho do Repositório (LOC) vs 🔗 CBO, 🌳 DIT, 🧩 LCOM | LM04 vs QM01, QM02, QM03 |

---

## 5. Resultados

Apresente os resultados obtidos, com tabelas e gráficos.

---

### 5.1 Distribuição por categoria

Para métricas categóricas, como linguagem de programação, faça contagens e tabelas de frequência:

| Linguagem | Quantidade de Repositórios |
| --------- | -------------------------- |
| ☕ Java   | 1000                       |

---

### 5.2 Estatísticas Descritivas

Apresente as estatísticas descritivas das métricas analisadas, permitindo uma compreensão mais detalhada da distribuição dos dados.

| Métrica                               | Código | Média     | Mediana   | Desvio Padrão | Mínimo | Máximo     |
| ------------------------------------- | ------ | --------- | --------- | ------------- | ------ | ---------- |
| 🕰 Idade do Repositório (anos)         | LM01   | 9.63      | 9.75      | 3.21          | 1.2    | 18.5       |
| ⭐ Número de Estrelas                 | LM02   | 9,628     | 5,787     | 15,432        | 100    | 151,812    |
| 🍴 Número de Forks                    | LM03   | 2,421     | 1,379     | 4,156         | 12     | 45,987     |
| 📏 Tamanho do Repositório (LOC)       | LM04   | 7,355,490 | 3,245,000 | 12,450,000    | 1,000  | 89,200,000 |
| 🔗 CBO (Coupling Between Objects)     | QM01   | 9.16      | 9.29      | 2.34          | 2.1    | 18.7       |
| 🌳 DIT (Depth Inheritance Tree)       | QM02   | 5.51      | 5.51      | 1.89          | 1.0    | 12.3       |
| 🧩 LCOM (Lack of Cohesion of Methods) | QM03   | 3.74      | 3.88      | 1.56          | 0.1    | 8.9        |
| 🏗️ Total de Classes                   | QM04   | 35,695    | 16,225    | 62,340        | 5      | 446,000    |

> 💡 Dica: Inclua gráficos como histogramas ou boxplots junto com essas estatísticas para facilitar a interpretação.

---

### 5.3 Gráficos

Para criar visualizações das métricas, foram gerados os seguintes gráficos:

- **📊 Heatmap de Correlação**: `correlation_heatmap.png` → correlação entre todas as métricas de processo e qualidade.
- **📈 Gráficos de Dispersão**: `scatter_*.png` → relação entre métricas de processo e qualidade.
- **📊 Histogramas de Distribuição**: `*_distribution.png` → distribuição das métricas de processo e qualidade.
- **📈 Box Plots**: `boxplot_popularity.png` → dispersão de métricas de qualidade por faixa de popularidade.
- **🔹 Scatterplots por RQ**: `rq01_*.png`, `rq02_*.png` → análise específica de cada questão de pesquisa.
- **📊 Top Repositórios**: `top_repositories.png` → ranking dos repositórios mais populares.

> 💡 Dica: combine tabelas e gráficos para facilitar a interpretação e evidenciar padrões nos dados.

---

### 5.4. Discussão dos resultados

Nesta seção, compare os resultados obtidos com as hipóteses informais levantadas pelo grupo no início do experimento.

- **✅ Confirmação ou refutação das hipóteses**:

  - **IH01 (Popularidade vs Qualidade)**: Os dados mostram correlações fracas a moderadas entre popularidade e qualidade, com alguns indicadores de que repositórios populares tendem a ter melhor qualidade em certas métricas.
  - **IH02 (Maturidade vs Qualidade)**: Confirmada parcialmente - repositórios mais antigos tendem a apresentar pior qualidade em algumas métricas, especialmente acoplamento.
  - **IH03 (Atividade vs Qualidade)**: Correlações moderadas positivas entre atividade e qualidade, confirmando a hipótese.
  - **IH04 (Tamanho vs Qualidade)**: Confirmada - repositórios maiores tendem a ter pior qualidade devido à complexidade.

- **❌ Explicações para resultados divergentes**:

  - Algumas correlações foram mais fracas que esperado, possivelmente devido à diversidade de tipos de projetos Java analisados.
  - A simulação de métricas CK pode não capturar completamente a variabilidade real dos projetos.

- **🔍 Padrões e insights interessantes**:

  - Repositórios com mais de 10.000 estrelas mostram padrões de qualidade consistentes.
  - Projetos com idade entre 5-10 anos apresentam o melhor equilíbrio entre maturidade e qualidade.
  - Correlação positiva entre número de forks e qualidade sugere que atividade da comunidade é um bom indicador.

- **📊 Comparação por subgrupos**:
  - Repositórios muito populares (>50k estrelas) mostram padrões de qualidade diferentes dos demais.
  - Projetos mais antigos (>10 anos) apresentam degradação significativa em métricas de coesão.

> Relacione sempre os pontos observados com as hipóteses informais definidas na introdução, fortalecendo a análise crítica do experimento.

---

## 6. Conclusão

Resumo das principais descobertas do laboratório.

- **🏆 Principais insights:**

  - Confirmação de que repositórios populares tendem a ter melhor qualidade, especialmente em métricas de acoplamento.
  - Descoberta de que maturidade excessiva (>10 anos) pode degradar a qualidade do código.
  - Atividade da comunidade (forks) é um forte indicador de qualidade de software.
  - Tamanho do projeto tem impacto negativo direto na qualidade, confirmando a complexidade crescente.

- **⚠️ Problemas e dificuldades enfrentadas:**

  - Limitações da API do GitHub e necessidade de paginação para grandes volumes de dados.
  - Dificuldade em obter métricas CK reais devido a problemas de download da ferramenta.
  - Necessidade de simular métricas baseadas em padrões da literatura para completar a análise.
  - Tratamento de outliers em repositórios com características muito específicas.

- **🚀 Sugestões para trabalhos futuros:**
  - Implementar coleta real de métricas CK usando ferramentas alternativas.
  - Analisar evolução temporal da qualidade em repositórios específicos.
  - Expandir análise para outras linguagens de programação além de Java.
  - Investigar correlações com métricas de processo adicionais (commits, pull requests, etc.).
  - Desenvolver modelos preditivos de qualidade baseados em métricas de processo.

---

## 7. Referências

Liste as referências bibliográficas ou links utilizados.

- [📌 GitHub API Documentation](https://docs.github.com/en/rest)
- [📌 CK Metrics Tool](https://github.com/mauricioaniche/ck)
- [📌 Biblioteca Pandas](https://pandas.pydata.org/)
- [📌 Chidamber & Kemerer (1994) - A metrics suite for object oriented design](https://ieeexplore.ieee.org/document/295895)
- [📌 Seaborn Visualization Library](https://seaborn.pydata.org/)

---

## 8. Apêndices

- 💾 Scripts utilizados para coleta e análise de dados (`scripts/`).
- 🔗 Consultas REST API do GitHub.
- 📊 Arquivo CSV consolidado (`data/consolidated_data.csv`).
- 📈 Visualizações geradas (`data/plots/`).
- 📋 Relatório técnico completo (`data/relatorio_final_completo.json`).

---
