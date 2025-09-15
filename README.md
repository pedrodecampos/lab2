# Laboratório 2 - Sprint 1: Análise de Qualidade de Sistemas Java

## Objetivo

Este projeto implementa um estudo das características de qualidade de sistemas Java, analisando os top-1000 repositórios mais populares do GitHub. O objetivo é correlacionar métricas de processo de desenvolvimento com métricas de qualidade de código usando a ferramenta CK.

## Estrutura do Projeto

```
lab2/
├── scripts/
│   ├── collect_repos.py          # Coleta top 1000 repositórios Java do GitHub
│   ├── clone_repos.py            # Automação de clone dos repositórios
│   ├── run_ck_analysis.py        # Execução da análise CK
│   ├── process_results.py        # Processamento e consolidação dos dados
│   └── demo_single_repo.py       # Demonstração com um repositório
├── data/
│   ├── repositories.json         # Lista dos repositórios coletados
│   ├── clone_results.json        # Resultados do processo de clone
│   ├── ck_analysis_results.json  # Resultados da análise CK
│   ├── consolidated_data.csv     # Dataset consolidado final
│   ├── final_report.json         # Relatório final com todas as análises
│   ├── metrics/                  # Arquivos CSV das métricas CK por repositório
│   └── plots/                    # Visualizações geradas
├── tools/
│   └── ck.jar                    # Ferramenta CK para análise estática
├── repositories/                 # Diretório com repositórios clonados
├── requirements.txt              # Dependências Python
├── run_sprint1.py               # Script principal para executar toda a Sprint 1
└── README.md                    # Este arquivo
```

## Questões de Pesquisa

- **RQ 01**: Qual a relação entre a popularidade dos repositórios e as suas características de qualidade?
- **RQ 02**: Qual a relação entre a maturidade dos repositórios e as suas características de qualidade?
- **RQ 03**: Qual a relação entre a atividade dos repositórios e as suas características de qualidade?
- **RQ 04**: Qual a relação entre o tamanho dos repositórios e as suas características de qualidade?

## Métricas Analisadas

### Métricas de Processo:

- **Popularidade**: Número de estrelas (stars)
- **Tamanho**: Linhas de código (LOC) e número de arquivos Java
- **Atividade**: Número de forks e releases
- **Maturidade**: Idade (em anos) do repositório

### Métricas de Qualidade (CK):

- **CBO**: Coupling Between Objects - Mede o acoplamento entre classes
- **DIT**: Depth Inheritance Tree - Profundidade da árvore de herança
- **LCOM**: Lack of Cohesion of Methods - Falta de coesão dos métodos
- **RFC**: Response For a Class - Resposta de uma classe
- **WMC**: Weighted Methods per Class - Métodos ponderados por classe

## Como Executar

### Opção 1: Execução Automática (Recomendada)

```bash
# Instalar dependências
pip install -r requirements.txt

# Executar toda a Sprint 1 automaticamente
python run_sprint1.py
```

### Opção 2: Execução Manual Passo a Passo

1. **Instalar dependências:**

```bash
pip install -r requirements.txt
```

2. **Coletar repositórios:**

```bash
python scripts/collect_repos.py
```

3. **Demonstração com um repositório:**

```bash
python scripts/demo_single_repo.py
```

4. **Clonar repositórios:**

```bash
python scripts/clone_repos.py
```

5. **Executar análise CK:**

```bash
python scripts/run_ck_analysis.py
```

6. **Processar resultados:**

```bash
python scripts/process_results.py
```

## Resultados Esperados

Após a execução, você terá:

- **`data/repositories.json`**: Lista dos 1000 repositórios Java mais populares
- **`data/demo_repo_summary.csv`**: Exemplo de métricas de um repositório
- **`data/consolidated_data.csv`**: Dataset completo com todas as métricas
- **`data/final_report.json`**: Relatório detalhado com correlações e análises
- **`data/plots/`**: Gráficos de correlação e distribuições

## Configuração Opcional

Para melhor performance na coleta de dados do GitHub, você pode configurar um token de acesso:

```bash
export GITHUB_TOKEN=seu_token_github_aqui
```

## Entregáveis da Sprint 1

✅ **Lista dos 1.000 repositórios Java** - `data/repositories.json`  
✅ **Script de Automação de clone e Coleta de Métricas** - Scripts em `scripts/`  
✅ **Arquivo .csv com resultado das medições de 1 repositório** - `data/demo_repo_summary.csv`

## Análise dos Resultados

O sistema calcula automaticamente:

- Correlações de Spearman entre métricas de processo e qualidade
- Estatísticas descritivas (média, mediana, desvio padrão)
- Testes de significância estatística
- Visualizações para interpretação dos dados

## Referências

- **CK Tool**: https://github.com/mauricioaniche/ck
- **GitHub API**: https://docs.github.com/en/rest
- **Métricas CK**: Chidamber, S. R., & Kemerer, C. F. (1994). A metrics suite for object oriented design
