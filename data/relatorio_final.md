# Análise de Qualidade de Sistemas Java: Relação entre Processo de Desenvolvimento e Características de Qualidade

**Autores:** Pedro Afonso  
**Data:** 2025-09-20  
**Versão:** 1.0

## Resumo Executivo

**Objetivo:** Análise da relação entre características de processo de desenvolvimento e qualidade de código em repositórios Java

**Metodologia:** Análise de correlação entre métricas de processo (popularidade, maturidade, atividade, tamanho) e métricas de qualidade CK (CBO, DIT, LCOM)

**Amostra:**
- Total de repositórios coletados: 1000
- Repositórios analisados: 750
- Taxa de sucesso: 75.0%

**Principais Achados:**

- **Relação entre popularidade (estrelas) e características de qualidade:** cbo_mean: -0.116, lcom_mean: -0.185
- **Relação entre maturidade (idade) e características de qualidade:** dit_mean: 0.156
- **Relação entre atividade (forks) e características de qualidade:** cbo_mean: -0.086, dit_mean: 0.074, lcom_mean: -0.178

## 1. Introdução

### 1.1 Contexto
A qualidade de software é um fator crítico para o sucesso de projetos de desenvolvimento

### 1.2 Problema de Pesquisa
Como características do processo de desenvolvimento influenciam a qualidade do código?

### 1.3 Objetivos

1. Analisar relação entre popularidade e qualidade
2. Investigar impacto da maturidade na qualidade
3. Examinar correlação entre atividade e qualidade
4. Avaliar influência do tamanho na qualidade

### 1.4 Questões de Pesquisa

- RQ 01: Qual a relação entre popularidade e qualidade?
- RQ 02: Qual a relação entre maturidade e qualidade?
- RQ 03: Qual a relação entre atividade e qualidade?
- RQ 04: Qual a relação entre tamanho e qualidade?

## 2. Metodologia

### 2.1 Coleta de Dados
- **Fonte:** GitHub API
- **Critério de Seleção:** Top 1000 repositórios Java mais populares (stars > 100)
- **Período:** 2024
- **Ferramentas:** GitHub Search API, Git, CK Tool

### 2.2 Métricas de Processo

- **Popularidade:** Número de estrelas (stars)
- **Maturidade:** Idade do repositório em anos
- **Atividade:** Número de forks
- **Tamanho:** Linhas de código (LOC) e número de arquivos Java

### 2.3 Métricas de Qualidade

- **CBO:** Coupling Between Objects - Mede acoplamento entre classes
- **DIT:** Depth Inheritance Tree - Profundidade da árvore de herança
- **LCOM:** Lack of Cohesion of Methods - Falta de coesão dos métodos

### 2.4 Análise Estatística

- **Correlacoes:** Spearman (não-paramétrica), Pearson (paramétrica), Kendall
- **Testes_Hipotese:** Mann-Whitney U para comparação de grupos
- **Normalidade:** Shapiro-Wilk para amostras pequenas
- **Significancia:** p < 0.05

## 3. Resultados

### 3.1 Estatísticas Descritivas

[Ver arquivo `advanced_analysis_results.json` para detalhes completos]

### 3.2 Análise de Correlações

[Ver arquivo `advanced_analysis_results.json` para detalhes completos]

### 3.3 Questões de Pesquisa

[Ver arquivo `advanced_analysis_results.json` para detalhes completos]

## 4. Discussão

### 4.1 Interpretação dos Resultados

[Baseado nos resultados da análise estatística]

### 4.2 Comparação com Hipóteses

[Comparação dos achados com as hipóteses formuladas]

### 4.3 Implicações Práticas

[Relevância dos resultados para desenvolvedores e gerentes]

### 4.4 Limitações

[Limitações do estudo e suas implicações]

## 5. Conclusões

### 5.1 Principais Achados

[Resumo dos principais resultados]

### 5.2 Contribuições


- Evidências empíricas sobre relação entre processo e qualidade em projetos Java
- Metodologia para análise de qualidade em repositórios open source
- Insights para desenvolvedores e gerentes de projeto
- Base para estudos futuros sobre qualidade de software

### 5.3 Recomendações


- Desenvolvedores devem considerar popularidade e atividade como indicadores de qualidade
- Projetos maduros podem se beneficiar de refatorações regulares
- Tamanho do projeto deve ser monitorado para evitar degradação da qualidade
- Ferramentas de análise estática devem ser integradas ao processo de desenvolvimento

## 6. Referências


- Chidamber, S. R., & Kemerer, C. F. (1994). A metrics suite for object oriented design
- GitHub API Documentation. https://docs.github.com/en/rest
- CK Tool. https://github.com/mauricioaniche/ck

## 7. Apêndices

- **Métricas Detalhadas:** Ver arquivo `consolidated_data.csv`
- **Visualizações:** Ver diretório `data/plots/`
- **Código Fonte:** Ver diretório `scripts/`

---

*Relatório gerado automaticamente em 20/09/2025 20:53:03*
