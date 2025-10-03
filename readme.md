# Laboratório 02 - Análise de Qualidade de Sistemas Java

## Objetivo

No processo de desenvolvimento de sistemas open-source, em que diversos desenvolvedores contribuem em partes diferentes do código, um dos riscos a serem gerenciados diz respeito à evolução dos seus atributos de qualidade interna. Isto é, ao se adotar uma abordagem colaborativa, corre-se o risco de tornar vulnerável aspectos como modularidade, manutenibilidade, ou legibilidade do software produzido.

Neste contexto, o objetivo deste laboratório é analisar aspectos da qualidade de repositórios desenvolvidos na linguagem Java, correlacionando-os com características do seu processo de desenvolvimento, sob a perspectiva de métricas de produto calculadas através da ferramenta CK.

## Metodologia

### 1. Seleção de Repositórios

Com o objetivo de analisar repositórios relevantes, escritos na linguagem estudada, coletaremos os top-1.000 repositórios Java mais populares do GitHub, calculando cada uma das métricas definidas.

### 2. Questões de Pesquisa

- **RQ01**: Qual a relação entre a popularidade dos repositórios e as suas características de qualidade?
- **RQ02**: Qual a relação entre a maturidade dos repositórios e as suas características de qualidade?
- **RQ03**: Qual a relação entre a atividade dos repositórios e as suas características de qualidade?
- **RQ04**: Qual a relação entre o tamanho dos repositórios e as suas características de qualidade?

### 3. Definição de Métricas

**Métricas de Processo:**

- **Popularidade**: Número de estrelas
- **Tamanho**: Linhas de código (LOC) e linhas de comentários
- **Atividade**: Número de releases
- **Maturidade**: Idade (em anos) de cada repositório coletado

**Métricas de Qualidade (CK):**

- **CBO**: Coupling between objects
- **DIT**: Depth Inheritance Tree
- **LCOM**: Lack of Cohesion of Methods

## Como executar

### Opção 1: Execução Completa (Recomendado)

```bash
python3 analise_completa.py
```

Este script executa todo o pipeline:

1. **Coleta via GitHub API** - Top-1.000 repositórios Java mais populares
2. **Análise de Métricas CK** - Cálculo de CBO, DIT, LCOM, WMC, RFC
3. **Correlações Estatísticas** - Pearson e Spearman
4. **Geração de Gráficos** - Gráficos de pizza coloridos
5. **Relatório Final** - Análise completa em texto

### Opção 2: Execução Individual

1. **Instalar dependências:**

```bash
pip install pandas numpy matplotlib seaborn scipy requests
```

2. **Executar análise:**

```bash
python3 analise_completa.py
```

## Arquivos Gerados

### 📊 Dados

- `dataset/dataset_repositorios_completo.csv` - 1000 repositórios da API GitHub
- `dataset/dataset_repositorios_analise.csv` - 100 repositórios com métricas CK
- `dataset/dataset_metricas_ck.csv` - Métricas de qualidade

### 🍕 Gráficos

- `graficos_pizza/distribuicao_popularidade.png` - Distribuição por estrelas
- `graficos_pizza/niveis_qualidade_cbo.png` - Níveis de qualidade
- `graficos_pizza/distribuicao_tamanho.png` - Distribuição por tamanho
- `graficos_pizza/resumo_correlacoes.png` - Resumo das correlações

### 📄 Relatório

- `relatorio_pdf/relatorio_qualidade_java.pdf` - Relatório final em PDF

## Tecnologias Utilizadas

- **Python 3** - Linguagem principal
- **GitHub API** - Coleta de repositórios
- **Pandas** - Manipulação de dados
- **Matplotlib/Seaborn** - Visualizações
- **SciPy** - Análise estatística
- **ReportLab** - Geração de PDF

## Resultados Esperados

### Hipóteses Informais

- **H1**: Repositórios mais populares tendem a ter melhor qualidade (menor CBO, maior DIT)
- **H2**: Repositórios mais maduros mostram padrões de qualidade mais consistentes
- **H3**: Repositórios maiores tendem a ter maior acoplamento (CBO)
- **H4**: Projetos com mais releases apresentam melhor coesão (LCOM)

### Análises Realizadas

- **Correlações de Pearson e Spearman** entre métricas de processo e qualidade
- **Análise de distribuição** por categorias de popularidade, tamanho e idade
- **Visualizações em gráficos de pizza** para análise exploratória
- **Medidas centrais** (mediana, média, desvio padrão) para cada métrica

## Estrutura do Relatório

1. **Introdução** - Contexto e hipóteses informais
2. **Metodologia** - Processo de coleta e análise
3. **Resultados** - Análise de cada questão de pesquisa
4. **Discussão** - Comparação entre hipóteses e resultados obtidos
