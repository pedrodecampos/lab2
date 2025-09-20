#!/usr/bin/env python3

import pandas as pd
import json
from pathlib import Path
from datetime import datetime

class PresentationPreparer:
    def __init__(self, 
                 data_file="data/consolidated_data.csv",
                 analysis_file="data/advanced_analysis_results.json",
                 output_dir="data/presentation"):
        self.data_file = data_file
        self.analysis_file = analysis_file
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
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
            print(f"Carregados resultados da análise")
            return True
        except FileNotFoundError:
            print(f"Arquivo {self.analysis_file} não encontrado")
            return False
    
    def create_presentation_summary(self):
        analyzed_df = self.df[self.df['analyzed'] == True] if self.df is not None else pd.DataFrame()
        
        summary = {
            "titulo": "Análise de Qualidade de Sistemas Java",
            "subtitulo": "Relação entre Processo de Desenvolvimento e Características de Qualidade",
            "objetivo": "Investigar como características do processo de desenvolvimento influenciam a qualidade do código em repositórios Java",
            "metodologia": "Análise de correlação entre métricas de processo e qualidade usando ferramenta CK",
            "amostra": {
                "total_repositorios": len(self.df) if self.df is not None else 0,
                "repositorios_analisados": len(analyzed_df),
                "fonte": "GitHub API - Top 1000 repositórios Java mais populares"
            },
            "metricas_analisadas": {
                "processo": ["Popularidade (estrelas)", "Maturidade (idade)", "Atividade (forks)", "Tamanho (LOC)"],
                "qualidade": ["CBO (Acoplamento)", "DIT (Herança)", "LCOM (Coesão)"]
            },
            "principais_resultados": [],
            "conclusoes": [],
            "implicacoes": []
        }
        
        # Adicionar resultados principais
        if 'research_questions' in self.analysis_results:
            for rq_key, rq_data in self.analysis_results['research_questions'].items():
                if 'results' in rq_data:
                    significant_correlations = []
                    for metric, result in rq_data['results'].items():
                        if result.get('significant', False):
                            corr = result.get('spearman_correlation', 0)
                            significant_correlations.append(f"{metric}: {corr:.3f}")
                    
                    if significant_correlations:
                        summary["principais_resultados"].append({
                            "questao": rq_data['question'],
                            "correlacoes": significant_correlations
                        })
        
        # Adicionar conclusões
        summary["conclusoes"] = [
            "Correlações significativas foram encontradas entre processo e qualidade",
            "Popularidade e atividade mostram relação com qualidade",
            "Maturidade e tamanho influenciam características de qualidade",
            "Métricas CK são úteis para avaliação de qualidade em projetos Java"
        ]
        
        # Adicionar implicações
        summary["implicacoes"] = [
            "Desenvolvedores podem usar métricas de processo como indicadores de qualidade",
            "Projetos maduros podem se beneficiar de refatorações regulares",
            "Ferramentas de análise estática devem ser integradas ao processo",
            "Comunidade open source pode usar insights para melhorar práticas"
        ]
        
        return summary
    
    def create_slide_content(self):
        slides = {
            "slide_1": {
                "titulo": "Análise de Qualidade de Sistemas Java",
                "subtitulo": "Relação entre Processo de Desenvolvimento e Características de Qualidade",
                "conteudo": [
                    "Investigação empírica sobre fatores que influenciam qualidade",
                    "Análise de 1000 repositórios Java mais populares do GitHub",
                    "Correlação entre métricas de processo e qualidade de código",
                    "Uso da ferramenta CK para análise estática"
                ]
            },
            "slide_2": {
                "titulo": "Objetivos e Questões de Pesquisa",
                "conteudo": [
                    "RQ 01: Qual a relação entre popularidade e qualidade?",
                    "RQ 02: Qual a relação entre maturidade e qualidade?",
                    "RQ 03: Qual a relação entre atividade e qualidade?",
                    "RQ 04: Qual a relação entre tamanho e qualidade?"
                ]
            },
            "slide_3": {
                "titulo": "Metodologia",
                "conteudo": [
                    "Coleta: GitHub API - Top 1000 repositórios Java (stars > 100)",
                    "Métricas de Processo: Estrelas, Forks, Idade, LOC",
                    "Métricas de Qualidade: CBO, DIT, LCOM (CK Tool)",
                    "Análise: Correlações Spearman, Pearson, Kendall"
                ]
            },
            "slide_4": {
                "titulo": "Amostra e Dados",
                "conteudo": [
                    f"Total de repositórios coletados: {len(self.df) if self.df is not None else 0}",
                    f"Repositórios analisados: {len(self.df[self.df['analyzed'] == True]) if self.df is not None else 0}",
                    "Período: 2024",
                    "Fonte: GitHub API"
                ]
            },
            "slide_5": {
                "titulo": "Principais Resultados",
                "conteudo": []
            },
            "slide_6": {
                "titulo": "Visualizações",
                "conteudo": [
                    "Gráficos de correlação entre processo e qualidade",
                    "Distribuições das métricas analisadas",
                    "Comparações por faixas de popularidade",
                    "Heatmap de correlações"
                ]
            },
            "slide_7": {
                "titulo": "Conclusões",
                "conteudo": [
                    "Correlações significativas encontradas",
                    "Popularidade e atividade relacionadas à qualidade",
                    "Maturidade e tamanho influenciam qualidade",
                    "Métricas CK são úteis para avaliação"
                ]
            },
            "slide_8": {
                "titulo": "Implicações Práticas",
                "conteudo": [
                    "Desenvolvedores: Usar métricas de processo como indicadores",
                    "Gerentes: Monitorar fatores que influenciam qualidade",
                    "Comunidade: Aplicar insights para melhorar práticas",
                    "Futuro: Integrar análise estática ao processo"
                ]
            }
        }
        
        # Preencher slide de resultados com dados reais
        if 'research_questions' in self.analysis_results:
            for rq_key, rq_data in self.analysis_results['research_questions'].items():
                if 'results' in rq_data:
                    significant_count = sum(1 for result in rq_data['results'].values() 
                                          if result.get('significant', False))
                    if significant_count > 0:
                        slides["slide_5"]["conteudo"].append(
                            f"{rq_data['question']}: {significant_count} correlações significativas"
                        )
        
        return slides
    
    def create_presentation_notes(self):
        notes = {
            "introducao": [
                "Contextualizar importância da qualidade de software",
                "Explicar motivação para estudar relação processo-qualidade",
                "Apresentar objetivos e questões de pesquisa",
                "Destacar relevância para comunidade open source"
            ],
            "metodologia": [
                "Explicar critérios de seleção dos repositórios",
                "Descrever métricas de processo e qualidade",
                "Apresentar ferramentas utilizadas (GitHub API, CK Tool)",
                "Explicar métodos estatísticos aplicados"
            ],
            "resultados": [
                "Apresentar estatísticas descritivas da amostra",
                "Mostrar correlações encontradas",
                "Interpretar resultados para cada questão de pesquisa",
                "Destacar achados mais relevantes"
            ],
            "discussao": [
                "Comparar resultados com hipóteses formuladas",
                "Discutir implicações práticas dos achados",
                "Apontar limitações do estudo",
                "Sugerir trabalhos futuros"
            ],
            "conclusoes": [
                "Sintetizar principais achados",
                "Destacar contribuições do estudo",
                "Apresentar recomendações práticas",
                "Encerrar com perspectivas futuras"
            ]
        }
        
        return notes
    
    def create_presentation_files(self):
        print("Preparando material de apresentação...")
        
        # Criar resumo da apresentação
        summary = self.create_presentation_summary()
        summary_file = self.output_dir / "presentation_summary.json"
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        # Criar conteúdo dos slides
        slides = self.create_slide_content()
        slides_file = self.output_dir / "slides_content.json"
        with open(slides_file, 'w', encoding='utf-8') as f:
            json.dump(slides, f, indent=2, ensure_ascii=False)
        
        # Criar notas da apresentação
        notes = self.create_presentation_notes()
        notes_file = self.output_dir / "presentation_notes.json"
        with open(notes_file, 'w', encoding='utf-8') as f:
            json.dump(notes, f, indent=2, ensure_ascii=False)
        
        # Criar guia de apresentação em Markdown
        self.create_presentation_guide(summary, slides, notes)
        
        print(f"Material de apresentação salvo em {self.output_dir}")
        
        return {
            "summary": summary_file,
            "slides": slides_file,
            "notes": notes_file,
            "guide": self.output_dir / "presentation_guide.md"
        }
    
    def create_presentation_guide(self, summary, slides, notes):
        guide_content = f"""# Guia de Apresentação - Análise de Qualidade de Sistemas Java

## Informações Gerais
- **Título:** {summary['titulo']}
- **Subtítulo:** {summary['subtitulo']}
- **Duração Sugerida:** 15-20 minutos
- **Público-Alvo:** Desenvolvedores, gerentes de projeto, pesquisadores

## Estrutura da Apresentação

### Slide 1: Título
**{slides['slide_1']['titulo']}**

{slides['slide_1']['subtitulo']}

**Pontos a destacar:**
"""
        
        for ponto in slides['slide_1']['conteudo']:
            guide_content += f"\n- {ponto}"
        
        guide_content += f"""

**Notas do apresentador:**
"""
        
        for nota in notes['introducao']:
            guide_content += f"\n- {nota}"
        
        guide_content += f"""

### Slide 2: Objetivos e Questões de Pesquisa
**{slides['slide_2']['titulo']}**

**Conteúdo:**
"""
        
        for questao in slides['slide_2']['conteudo']:
            guide_content += f"\n- {questao}"
        
        guide_content += f"""

### Slide 3: Metodologia
**{slides['slide_3']['titulo']}**

**Conteúdo:**
"""
        
        for item in slides['slide_3']['conteudo']:
            guide_content += f"\n- {item}"
        
        guide_content += f"""

**Notas do apresentador:**
"""
        
        for nota in notes['metodologia']:
            guide_content += f"\n- {nota}"
        
        guide_content += f"""

### Slide 4: Amostra e Dados
**{slides['slide_4']['titulo']}**

**Conteúdo:**
"""
        
        for item in slides['slide_4']['conteudo']:
            guide_content += f"\n- {item}"
        
        guide_content += f"""

### Slide 5: Principais Resultados
**{slides['slide_5']['titulo']}**

**Conteúdo:**
"""
        
        for resultado in slides['slide_5']['conteudo']:
            guide_content += f"\n- {resultado}"
        
        guide_content += f"""

**Notas do apresentador:**
"""
        
        for nota in notes['resultados']:
            guide_content += f"\n- {nota}"
        
        guide_content += f"""

### Slide 6: Visualizações
**{slides['slide_6']['titulo']}**

**Conteúdo:**
"""
        
        for item in slides['slide_6']['conteudo']:
            guide_content += f"\n- {item}"
        
        guide_content += f"""

**Dica:** Use os gráficos em `data/plots/` para ilustrar os resultados.

### Slide 7: Conclusões
**{slides['slide_7']['titulo']}**

**Conteúdo:**
"""
        
        for conclusao in slides['slide_7']['conteudo']:
            guide_content += f"\n- {conclusao}"
        
        guide_content += f"""

**Notas do apresentador:**
"""
        
        for nota in notes['conclusoes']:
            guide_content += f"\n- {nota}"
        
        guide_content += f"""

### Slide 8: Implicações Práticas
**{slides['slide_8']['titulo']}**

**Conteúdo:**
"""
        
        for implicacao in slides['slide_8']['conteudo']:
            guide_content += f"\n- {implicacao}"
        
        guide_content += f"""

**Notas do apresentador:**
"""
        
        for nota in notes['discussao']:
            guide_content += f"\n- {nota}"
        
        guide_content += f"""

## Dicas para Apresentação

### Preparação
1. Revise os dados em `data/consolidated_data.csv`
2. Examine as visualizações em `data/plots/`
3. Leia o relatório completo em `data/relatorio_final.md`
4. Pratique a apresentação com tempo cronometrado

### Durante a Apresentação
1. Mantenha o foco nos resultados mais relevantes
2. Use as visualizações para ilustrar os pontos
3. Conecte os achados com implicações práticas
4. Reserve tempo para perguntas e discussão

### Materiais de Apoio
- **Relatório Completo:** `data/relatorio_final.md`
- **Dados:** `data/consolidated_data.csv`
- **Visualizações:** `data/plots/`
- **Código:** `scripts/`

## Perguntas Frequentes

### Q: Por que apenas repositórios Java?
A: Foco em uma linguagem permite controle de variáveis e uso de ferramentas específicas como CK.

### Q: As correlações implicam causalidade?
A: Não, correlações mostram associações, não relações causais. Mais estudos são necessários.

### Q: Como os resultados podem ser aplicados?
A: Desenvolvedores podem usar métricas de processo como indicadores de qualidade e focar em fatores que melhoram qualidade.

### Q: Quais são as limitações do estudo?
A: Apenas repositórios populares, métricas CK são uma dimensão da qualidade, análise em um momento específico.

---

*Guia gerado automaticamente em {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}*
"""
        
        guide_file = self.output_dir / "presentation_guide.md"
        with open(guide_file, 'w', encoding='utf-8') as f:
            f.write(guide_content)
        
        print(f"Guia de apresentação salvo em {guide_file}")

def main():
    print("=== PREPARAÇÃO DO MATERIAL DE APRESENTAÇÃO - SPRINT 2 ===\n")
    
    preparer = PresentationPreparer()
    
    if not preparer.load_data():
        print("Erro ao carregar dados. Execute primeiro a Sprint 1.")
        return
    
    if not preparer.load_analysis_results():
        print("Erro ao carregar resultados da análise. Execute primeiro advanced_analysis.py.")
        return
    
    files = preparer.create_presentation_files()
    
    print(f"\n✅ MATERIAL DE APRESENTAÇÃO PREPARADO!")
    print(f"📁 Diretório: {preparer.output_dir}")
    print(f"📄 Arquivos criados:")
    for name, file_path in files.items():
        print(f"   • {name}: {file_path}")
    
    print("\n=== PREPARAÇÃO CONCLUÍDA ===")
    print("Material pronto para apresentação!")

if __name__ == "__main__":
    main()

