# Laboratório 02 - Análise de Qualidade de Sistemas Java

## Objetivo

Analisar aspectos da qualidade de repositórios desenvolvidos na linguagem Java, correlacionando-os com características do processo de desenvolvimento através de métricas CK.

## Questões de Pesquisa

- **RQ01**: Qual a relação entre a popularidade dos repositórios e as suas características de qualidade?
- **RQ02**: Qual a relação entre a maturidade dos repositórios e as suas características de qualidade?
- **RQ03**: Qual a relação entre a atividade dos repositórios e as suas características de qualidade?
- **RQ04**: Qual a relação entre o tamanho dos repositórios e as suas características de qualidade?

## Métricas de Processo

- **Popularidade**: Número de estrelas
- **Tamanho**: Linhas de código (LOC) e linhas de comentários
- **Atividade**: Número de releases
- **Maturidade**: Idade (em anos)

## Métricas de Qualidade (CK)

- **CBO**: Coupling between objects
- **DIT**: Depth Inheritance Tree
- **LCOM**: Lack of Cohesion of Methods

## Como executar

1. Instalar dependências:

```bash
pip install -r dependencias.txt
```

2. Executar coleta de dados:

```bash
python3 coletor_github.py
```

3. Executar análise de métricas:

```bash
python3 analisador_clones.py
```

4. Gerar relatório:

```bash
python3 gerador_relatorio.py
```

5. Gerar relatório PDF:

```bash
python3 gerador_pdf.py
```

6. Executar pipeline completo:

```bash
python3 gerar_tudo.py
```
