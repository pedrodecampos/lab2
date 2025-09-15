# Hipóteses para Análise de Qualidade de Sistemas Java

## Hipóteses Iniciais

Baseadas na literatura sobre qualidade de software e métricas de código, formulamos as seguintes hipóteses para cada questão de pesquisa:

### RQ 01: Relação entre Popularidade e Qualidade

**Hipótese**: Repositórios mais populares (com mais estrelas) tendem a ter melhor qualidade de código.

**Justificativa**:

- Repositórios populares recebem mais atenção da comunidade
- Maior número de contribuidores pode resultar em melhor revisão de código
- Projetos populares têm maior pressão para manter qualidade para atrair desenvolvedores

**Métricas esperadas**:

- Correlação negativa entre estrelas e CBO (menos acoplamento)
- Correlação negativa entre estrelas e LCOM (maior coesão)
- Relação neutra ou positiva entre estrelas e DIT (herança bem estruturada)

### RQ 02: Relação entre Maturidade e Qualidade

**Hipótese**: Repositórios mais maduros (mais antigos) tendem a ter pior qualidade devido à evolução contínua.

**Justificativa**:

- Código legado pode acumular débito técnico
- Refatorações podem não acompanhar o crescimento do projeto
- Pressão por funcionalidades pode comprometer qualidade

**Métricas esperadas**:

- Correlação positiva entre idade e CBO (maior acoplamento)
- Correlação positiva entre idade e LCOM (menor coesão)
- Correlação positiva entre idade e DIT (herança mais profunda)

### RQ 03: Relação entre Atividade e Qualidade

**Hipótese**: Repositórios mais ativos (mais forks) tendem a ter melhor qualidade devido ao maior cuidado na manutenção.

**Justificativa**:

- Projetos ativos recebem mais feedback da comunidade
- Maior número de forks indica interesse e pode resultar em melhor manutenção
- Atividade pode indicar equipe dedicada à qualidade

**Métricas esperadas**:

- Correlação negativa entre forks e CBO
- Correlação negativa entre forks e LCOM
- Relação neutra entre forks e DIT

### RQ 04: Relação entre Tamanho e Qualidade

**Hipótese**: Repositórios maiores (mais LOC) tendem a ter pior qualidade devido à complexidade.

**Justificativa**:

- Projetos grandes são mais difíceis de manter
- Maior complexidade pode resultar em maior acoplamento
- Dificuldade em manter coesão em projetos extensos

**Métricas esperadas**:

- Correlação positiva entre LOC e CBO
- Correlação positiva entre LOC e LCOM
- Correlação positiva entre LOC e DIT

## Interpretação das Métricas CK

### CBO (Coupling Between Objects)

- **Valores baixos (< 5)**: Bom acoplamento, classes bem isoladas
- **Valores médios (5-10)**: Acoplamento moderado, aceitável
- **Valores altos (> 10)**: Alto acoplamento, pode indicar problemas de design

### DIT (Depth Inheritance Tree)

- **Valores baixos (< 3)**: Herança simples e clara
- **Valores médios (3-5)**: Herança moderada, aceitável
- **Valores altos (> 5)**: Herança profunda, pode ser difícil de manter

### LCOM (Lack of Cohesion of Methods)

- **Valores baixos (< 1)**: Alta coesão, métodos bem relacionados
- **Valores médios (1-2)**: Coesão moderada
- **Valores altos (> 2)**: Baixa coesão, classe pode ter responsabilidades demais

## Análise Estatística

### Correlações de Spearman

- **Correlação forte**: |r| > 0.7
- **Correlação moderada**: 0.3 < |r| < 0.7
- **Correlação fraca**: |r| < 0.3

### Significância Estatística

- **p < 0.05**: Correlação estatisticamente significativa
- **p < 0.01**: Correlação altamente significativa
- **p >= 0.05**: Correlação não significativa

## Critérios de Sucesso

### Para RQ 01 (Popularidade):

- Se correlação negativa significativa entre estrelas e CBO/LCOM
- Se correlação positiva ou neutra entre estrelas e DIT

### Para RQ 02 (Maturidade):

- Se correlação positiva significativa entre idade e CBO/LCOM
- Se correlação positiva entre idade e DIT

### Para RQ 03 (Atividade):

- Se correlação negativa significativa entre forks e CBO/LCOM
- Se correlação neutra entre forks e DIT

### Para RQ 04 (Tamanho):

- Se correlação positiva significativa entre LOC e CBO/LCOM
- Se correlação positiva entre LOC e DIT

## Limitações e Considerações

1. **Correlação não implica causalidade**: As correlações encontradas podem não indicar relações causais diretas
2. **Contexto do projeto**: Diferentes tipos de projetos podem ter padrões diferentes
3. **Qualidade subjetiva**: As métricas CK são apenas uma dimensão da qualidade de software
4. **Amostra**: Os 1000 repositórios podem não ser representativos de todos os projetos Java

## Próximos Passos

Após a análise dos dados, será necessário:

1. Comparar resultados com as hipóteses formuladas
2. Identificar padrões inesperados
3. Discutir implicações práticas dos achados
4. Propor melhorias metodológicas para estudos futuros
