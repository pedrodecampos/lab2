#!/usr/bin/env python3

import pandas as pd
import numpy as np
import json
from pathlib import Path
from datetime import datetime

class FinalReportGenerator:
    def __init__(self, 
                 data_file="data/consolidated_data.csv",
                 analysis_file="data/advanced_analysis_results.json",
                 output_dir="data"):
        self.data_file = data_file
        self.analysis_file = analysis_file
        self.output_dir = Path(output_dir)
        self.df = None
        self.analysis_results = {}
        
    def load_data(self):
        try:
            self.df = pd.read_csv(self.data_file)
            print(f"Carregados {len(self.df)} repositórios")
            return True
        except FileNotFoundError:
            print(f"Arquivo {self.data_file} não encontrado")
            return False
    
    def load_analysis_results(self):
        try:
            with open(self.analysis_file, 'r', encoding='utf-8') as f:
                self.analysis_results = json.load(f)
            print(f"Carregados resultados da análise avançada")
            return True
        except FileNotFoundError:
            print(f"Arquivo {self.analysis_file} não encontrado")
            return False
    
    def generate_executive_summary(self):
        analyzed_df = self.df[self.df['analyzed'] == True] if self.df is not None else pd.DataFrame()
        
        summary = {
            "objetivo": "Análise da relação entre características de processo de desenvolvimento e qualidade de código em repositórios Java",
            "metodologia": "Análise de correlação entre métricas de processo (popularidade, maturidade, atividade, tamanho) e métricas de qualidade CK (CBO, DIT, LCOM)",
            "amostra": {
                "total_repositorios_coletados": len(self.df) if self.df is not None else 0,
                "repositorios_analisados": len(analyzed_df),
                "taxa_sucesso": f"{(len(analyzed_df)/len(self.df)*100):.1f}%" if self.df is not None and len(self.df) > 0 else "0%"
            },
            "principais_achados": []
        }
        
        # Adicionar achados principais baseados na análise
        if 'research_questions' in self.analysis_results:
            for rq_key, rq_data in self.analysis_results['research_questions'].items():
                if 'results' in rq_data:
                    significant_correlations = []
                    for metric, result in rq_data['results'].items():
                        if result.get('significant', False):
                            corr = result.get('spearman_correlation', 0)
                            significant_correlations.append(f"{metric}: {corr:.3f}")
                    
                    if significant_correlations:
                        summary["principais_achados"].append({
                            "questao": rq_data['question'],
                            "correlacoes_significativas": significant_correlations
                        })
        
        return summary
    
    def generate_methodology_section(self):
        methodology = {
            "coleta_dados": {
                "fonte": "GitHub API",
                "criterio_selecao": "Top 1000 repositórios Java mais populares (stars > 100)",
                "periodo_coleta": "2024",
                "ferramentas": ["GitHub Search API", "Git", "CK Tool"]
            },
            "metricas_processo": {
                "popularidade": "Número de estrelas (stars)",
                "maturidade": "Idade do repositório em anos",
                "atividade": "Número de forks",
                "tamanho": "Linhas de código (LOC) e número de arquivos Java"
            },
            "metricas_qualidade": {
                "cbo": "Coupling Between Objects - Mede acoplamento entre classes",
                "dit": "Depth Inheritance Tree - Profundidade da árvore de herança",
                "lcom": "Lack of Cohesion of Methods - Falta de coesão dos métodos"
            },
            "analise_estatistica": {
                "correlacoes": "Spearman (não-paramétrica), Pearson (paramétrica), Kendall",
                "testes_hipotese": "Mann-Whitney U para comparação de grupos",
                "normalidade": "Shapiro-Wilk para amostras pequenas",
                "significancia": "p < 0.05"
            }
        }
        
        return methodology
    
    def generate_results_section(self):
        analyzed_df = self.df[self.df['analyzed'] == True] if self.df is not None else pd.DataFrame()
        
        results = {
            "estatisticas_descritivas": {},
            "correlacoes": {},
            "questoes_pesquisa": {}
        }
        
        # Estatísticas descritivas
        if 'descriptive_statistics' in self.analysis_results:
            results["estatisticas_descritivas"] = self.analysis_results['descriptive_statistics']
        
        # Correlações
        if 'correlation_analysis' in self.analysis_results:
            results["correlacoes"] = self.analysis_results['correlation_analysis']
        
        # Questões de pesquisa
        if 'research_questions' in self.analysis_results:
            results["questoes_pesquisa"] = self.analysis_results['research_questions']
        
        # Estatísticas adicionais
        if len(analyzed_df) > 0:
            results["estatisticas_gerais"] = {
                "repositorios_analisados": len(analyzed_df),
                "media_estrelas": float(analyzed_df['stars'].mean()) if 'stars' in analyzed_df.columns else 0,
                "media_idade_anos": float(analyzed_df['age_years'].mean()) if 'age_years' in analyzed_df.columns else 0,
                "media_loc": float(analyzed_df['loc_total'].mean()) if 'loc_total' in analyzed_df.columns else 0,
                "media_cbo": float(analyzed_df['cbo_mean'].mean()) if 'cbo_mean' in analyzed_df.columns else 0,
                "media_dit": float(analyzed_df['dit_mean'].mean()) if 'dit_mean' in analyzed_df.columns else 0,
                "media_lcom": float(analyzed_df['lcom_mean'].mean()) if 'lcom_mean' in analyzed_df.columns else 0
            }
        
        return results
    
    def generate_discussion_section(self):
        discussion = {
            "interpretacao_resultados": {},
            "comparacao_hipoteses": {},
            "implicacoes_praticas": {},
            "limitacoes": {},
            "trabalhos_futuros": {}
        }
        
        # Interpretação dos resultados
        if 'research_questions' in self.analysis_results:
            for rq_key, rq_data in self.analysis_results['research_questions'].items():
                if 'results' in rq_data:
                    significant_findings = []
                    for metric, result in rq_data['results'].items():
                        if result.get('significant', False):
                            corr = result.get('spearman_correlation', 0)
                            interpretation = result.get('interpretation', '')
                            significant_findings.append({
                                "metrica": metric,
                                "correlacao": corr,
                                "interpretacao": interpretation
                            })
                    
                    discussion["interpretacao_resultados"][rq_key] = {
                        "questao": rq_data['question'],
                        "hipotese": rq_data.get('hypothesis', ''),
                        "achados_significativos": significant_findings
                    }
        
        # Comparação com hipóteses
        discussion["comparacao_hipoteses"] = {
            "rq01": "Hipótese: Repositórios populares têm melhor qualidade. Resultado: [A ser preenchido com base nos dados]",
            "rq02": "Hipótese: Repositórios maduros têm pior qualidade. Resultado: [A ser preenchido com base nos dados]",
            "rq03": "Hipótese: Repositórios ativos têm melhor qualidade. Resultado: [A ser preenchido com base nos dados]",
            "rq04": "Hipótese: Repositórios grandes têm pior qualidade. Resultado: [A ser preenchido com base nos dados]"
        }
        
        # Implicações práticas
        discussion["implicacoes_praticas"] = {
            "desenvolvedores": "Os resultados podem orientar práticas de desenvolvimento",
            "gerentes_projeto": "Insights sobre fatores que influenciam qualidade",
            "comunidade_opensource": "Entendimento sobre padrões de qualidade em projetos colaborativos"
        }
        
        # Limitações
        discussion["limitacoes"] = {
            "amostra": "Apenas repositórios Java populares foram analisados",
            "metricas": "Métricas CK são apenas uma dimensão da qualidade",
            "causalidade": "Correlações não implicam relações causais",
            "temporal": "Análise em um momento específico no tempo"
        }
        
        # Trabalhos futuros
        discussion["trabalhos_futuros"] = {
            "metricas_adicionais": "Incluir outras métricas de qualidade e processo",
            "analise_temporal": "Estudar evolução da qualidade ao longo do tempo",
            "outras_linguagens": "Estender análise para outras linguagens de programação",
            "fatores_contextuais": "Considerar fatores como domínio, equipe, metodologia"
        }
        
        return discussion
    
    def generate_conclusions(self):
        conclusions = {
            "resumo_principais_achados": [],
            "contribuicoes": [],
            "recomendacoes": []
        }
        
        # Resumo dos principais achados
        if 'research_questions' in self.analysis_results:
            for rq_key, rq_data in self.analysis_results['research_questions'].items():
                if 'results' in rq_data:
                    significant_count = sum(1 for result in rq_data['results'].values() 
                                          if result.get('significant', False))
                    conclusions["resumo_principais_achados"].append({
                        "questao": rq_data['question'],
                        "correlacoes_significativas": significant_count,
                        "total_metricas": len(rq_data['results'])
                    })
        
        # Contribuições
        conclusions["contribuicoes"] = [
            "Evidências empíricas sobre relação entre processo e qualidade em projetos Java",
            "Metodologia para análise de qualidade em repositórios open source",
            "Insights para desenvolvedores e gerentes de projeto",
            "Base para estudos futuros sobre qualidade de software"
        ]
        
        # Recomendações
        conclusions["recomendacoes"] = [
            "Desenvolvedores devem considerar popularidade e atividade como indicadores de qualidade",
            "Projetos maduros podem se beneficiar de refatorações regulares",
            "Tamanho do projeto deve ser monitorado para evitar degradação da qualidade",
            "Ferramentas de análise estática devem ser integradas ao processo de desenvolvimento"
        ]
        
        return conclusions
    
    def generate_full_report(self):
        print("Gerando relatório final completo...")
        
        report = {
            "metadata": {
                "titulo": "Análise de Qualidade de Sistemas Java: Relação entre Processo de Desenvolvimento e Características de Qualidade",
                "autores": ["Pedro Afonso"],
                "data_geracao": datetime.now().isoformat(),
                "versao": "1.0"
            },
            "resumo_executivo": self.generate_executive_summary(),
            "introducao": {
                "contexto": "A qualidade de software é um fator crítico para o sucesso de projetos de desenvolvimento",
                "problema": "Como características do processo de desenvolvimento influenciam a qualidade do código?",
                "objetivos": [
                    "Analisar relação entre popularidade e qualidade",
                    "Investigar impacto da maturidade na qualidade",
                    "Examinar correlação entre atividade e qualidade",
                    "Avaliar influência do tamanho na qualidade"
                ],
                "questoes_pesquisa": [
                    "RQ 01: Qual a relação entre popularidade e qualidade?",
                    "RQ 02: Qual a relação entre maturidade e qualidade?",
                    "RQ 03: Qual a relação entre atividade e qualidade?",
                    "RQ 04: Qual a relação entre tamanho e qualidade?"
                ]
            },
            "metodologia": self.generate_methodology_section(),
            "resultados": self.generate_results_section(),
            "discussao": self.generate_discussion_section(),
            "conclusoes": self.generate_conclusions(),
            "referencias": [
                "Chidamber, S. R., & Kemerer, C. F. (1994). A metrics suite for object oriented design",
                "GitHub API Documentation. https://docs.github.com/en/rest",
                "CK Tool. https://github.com/mauricioaniche/ck"
            ],
            "apendices": {
                "metricas_detalhadas": "Ver arquivo consolidated_data.csv",
                "visualizacoes": "Ver diretório data/plots/",
                "codigo_fonte": "Ver diretório scripts/"
            }
        }
        
        return report
    
    def save_report(self, report, filename="data/relatorio_final_completo.json"):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"Relatório final salvo em {filename}")
        return filename
    
    def generate_markdown_report(self, report, filename="data/relatorio_final.md"):
        md_content = f"""# {report['metadata']['titulo']}

**Autores:** {', '.join(report['metadata']['autores'])}  
**Data:** {report['metadata']['data_geracao'][:10]}  
**Versão:** {report['metadata']['versao']}

## Resumo Executivo

**Objetivo:** {report['resumo_executivo']['objetivo']}

**Metodologia:** {report['resumo_executivo']['metodologia']}

**Amostra:**
- Total de repositórios coletados: {report['resumo_executivo']['amostra']['total_repositorios_coletados']}
- Repositórios analisados: {report['resumo_executivo']['amostra']['repositorios_analisados']}
- Taxa de sucesso: {report['resumo_executivo']['amostra']['taxa_sucesso']}

**Principais Achados:**
"""
        
        for achado in report['resumo_executivo']['principais_achados']:
            md_content += f"\n- **{achado['questao']}:** {', '.join(achado['correlacoes_significativas'])}"
        
        md_content += f"""

## 1. Introdução

### 1.1 Contexto
{report['introducao']['contexto']}

### 1.2 Problema de Pesquisa
{report['introducao']['problema']}

### 1.3 Objetivos
"""
        
        for i, objetivo in enumerate(report['introducao']['objetivos'], 1):
            md_content += f"\n{i}. {objetivo}"
        
        md_content += f"""

### 1.4 Questões de Pesquisa
"""
        
        for questao in report['introducao']['questoes_pesquisa']:
            md_content += f"\n- {questao}"
        
        md_content += f"""

## 2. Metodologia

### 2.1 Coleta de Dados
- **Fonte:** {report['metodologia']['coleta_dados']['fonte']}
- **Critério de Seleção:** {report['metodologia']['coleta_dados']['criterio_selecao']}
- **Período:** {report['metodologia']['coleta_dados']['periodo_coleta']}
- **Ferramentas:** {', '.join(report['metodologia']['coleta_dados']['ferramentas'])}

### 2.2 Métricas de Processo
"""
        
        for metrica, descricao in report['metodologia']['metricas_processo'].items():
            md_content += f"\n- **{metrica.title()}:** {descricao}"
        
        md_content += f"""

### 2.3 Métricas de Qualidade
"""
        
        for metrica, descricao in report['metodologia']['metricas_qualidade'].items():
            md_content += f"\n- **{metrica.upper()}:** {descricao}"
        
        md_content += f"""

### 2.4 Análise Estatística
"""
        
        for tipo, descricao in report['metodologia']['analise_estatistica'].items():
            md_content += f"\n- **{tipo.title()}:** {descricao}"
        
        md_content += f"""

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

"""
        
        for contribuicao in report['conclusoes']['contribuicoes']:
            md_content += f"\n- {contribuicao}"
        
        md_content += f"""

### 5.3 Recomendações

"""
        
        for recomendacao in report['conclusoes']['recomendacoes']:
            md_content += f"\n- {recomendacao}"
        
        md_content += f"""

## 6. Referências

"""
        
        for ref in report['referencias']:
            md_content += f"\n- {ref}"
        
        md_content += f"""

## 7. Apêndices

- **Métricas Detalhadas:** Ver arquivo `consolidated_data.csv`
- **Visualizações:** Ver diretório `data/plots/`
- **Código Fonte:** Ver diretório `scripts/`

---

*Relatório gerado automaticamente em {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}*
"""
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        print(f"Relatório Markdown salvo em {filename}")
        return filename

def main():
    print("=== GERAÇÃO DO RELATÓRIO FINAL - SPRINT 2 ===\n")
    
    generator = FinalReportGenerator()
    
    if not generator.load_data():
        print("Erro ao carregar dados. Execute primeiro a Sprint 1.")
        return
    
    if not generator.load_analysis_results():
        print("Erro ao carregar resultados da análise. Execute primeiro advanced_analysis.py.")
        return
    
    print("Gerando relatório final completo...")
    
    report = generator.generate_full_report()
    
    # Salvar relatório JSON
    json_file = generator.save_report(report)
    
    # Gerar relatório Markdown
    md_file = generator.generate_markdown_report(report)
    
    print(f"\n✅ RELATÓRIO FINAL GERADO COM SUCESSO!")
    print(f"📄 JSON: {json_file}")
    print(f"📄 Markdown: {md_file}")
    
    print("\n=== SPRINT 2 CONCLUÍDA ===")
    print("Todos os entregáveis da Sprint 2 foram gerados!")

if __name__ == "__main__":
    main()

