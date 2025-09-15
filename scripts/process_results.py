#!/usr/bin/env python3

import json
import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

class DataProcessor:
    def __init__(self, 
                 repos_file="data/repositories.json",
                 clone_results_file="data/clone_results.json",
                 ck_results_file="data/ck_analysis_results.json"):
        self.repos_file = repos_file
        self.clone_results_file = clone_results_file
        self.ck_results_file = ck_results_file
        
        self.repositories_data = []
        self.clone_data = []
        self.ck_data = []
        self.consolidated_data = None
    
    def load_all_data(self):
        try:
            with open(self.repos_file, 'r', encoding='utf-8') as f:
                repos_json = json.load(f)
                self.repositories_data = repos_json.get("repositories", [])
            print(f"✓ Carregados {len(self.repositories_data)} repositórios")
            
            with open(self.clone_results_file, 'r', encoding='utf-8') as f:
                clone_json = json.load(f)
                self.clone_data = clone_json.get("results", {}).get("successful", [])
            print(f"✓ Carregados {len(self.clone_data)} repositórios clonados")
            
            with open(self.ck_results_file, 'r', encoding='utf-8') as f:
                ck_json = json.load(f)
                self.ck_data = ck_json.get("results", {}).get("successful", [])
            print(f"✓ Carregados {len(self.ck_data)} análises CK")
            
            return True
            
        except FileNotFoundError as e:
            print(f"✗ Arquivo não encontrado: {e}")
            return False
        except json.JSONDecodeError as e:
            print(f"✗ Erro ao decodificar JSON: {e}")
            return False
    
    def consolidate_data(self):
        print("Consolidando dados...")
        
        repos_df = pd.DataFrame(self.repositories_data)
        
        clone_dict = {repo["repo"]: repo for repo in self.clone_data}
        ck_dict = {repo["repo"]: repo for repo in self.ck_data}
        
        repos_df["cloned"] = repos_df["full_name"].isin(clone_dict.keys())
        repos_df["clone_path"] = repos_df["full_name"].map(lambda x: clone_dict.get(x, {}).get("path", ""))
        
        repos_df["analyzed"] = repos_df["full_name"].isin(ck_dict.keys())
        
        for metric in ["cbo_median", "cbo_mean", "cbo_std", 
                      "dit_median", "dit_mean", "dit_std",
                      "lcom_median", "lcom_mean", "lcom_std",
                      "total_classes", "loc_total", "java_files_count"]:
            repos_df[metric] = repos_df["full_name"].map(lambda x: ck_dict.get(x, {}).get(metric, np.nan))
        
        self.consolidated_data = repos_df
        return repos_df
    
    def calculate_correlation_analysis(self):
        if self.consolidated_data is None:
            return {}
        
        print("Calculando correlações...")
        
        analyzed_df = self.consolidated_data[self.consolidated_data["analyzed"] == True].copy()
        
        if len(analyzed_df) == 0:
            print("Nenhum repositório analisado encontrado.")
            return {}
        
        correlations = {}
        
        process_metrics = ["stars", "forks", "age_years", "size_kb"]
        quality_metrics = ["cbo_mean", "dit_mean", "lcom_mean", "total_classes", "loc_total"]
        
        for process_metric in process_metrics:
            correlations[process_metric] = {}
            
            for quality_metric in quality_metrics:
                valid_data = analyzed_df[[process_metric, quality_metric]].dropna()
                
                if len(valid_data) >= 3:
                    corr, p_value = stats.spearmanr(valid_data[process_metric], valid_data[quality_metric])
                    correlations[process_metric][quality_metric] = {
                        "correlation": corr,
                        "p_value": p_value,
                        "sample_size": len(valid_data)
                    }
        
        return correlations
    
    def generate_summary_statistics(self):
        if self.consolidated_data is None:
            return {}
        
        print("Gerando estatísticas resumo...")
        
        analyzed_df = self.consolidated_data[self.consolidated_data["analyzed"] == True]
        
        summary = {
            "total_repositories": len(self.consolidated_data),
            "cloned_repositories": len(self.consolidated_data[self.consolidated_data["cloned"] == True]),
            "analyzed_repositories": len(analyzed_df),
            "process_metrics": {},
            "quality_metrics": {}
        }
        
        process_metrics = ["stars", "forks", "age_years", "size_kb"]
        for metric in process_metrics:
            if metric in analyzed_df.columns:
                values = analyzed_df[metric].dropna()
                summary["process_metrics"][metric] = {
                    "mean": float(values.mean()),
                    "median": float(values.median()),
                    "std": float(values.std()),
                    "min": float(values.min()),
                    "max": float(values.max()),
                    "count": len(values)
                }
        
        quality_metrics = ["cbo_mean", "dit_mean", "lcom_mean", "total_classes", "loc_total"]
        for metric in quality_metrics:
            if metric in analyzed_df.columns:
                values = analyzed_df[metric].dropna()
                summary["quality_metrics"][metric] = {
                    "mean": float(values.mean()),
                    "median": float(values.median()),
                    "std": float(values.std()),
                    "min": float(values.min()),
                    "max": float(values.max()),
                    "count": len(values)
                }
        
        return summary
    
    def answer_research_questions(self):
        if self.consolidated_data is None:
            return {}
        
        print("Respondendo questões de pesquisa...")
        
        analyzed_df = self.consolidated_data[self.consolidated_data["analyzed"] == True].copy()
        
        if len(analyzed_df) == 0:
            return {"error": "Nenhum repositório analisado disponível"}
        
        answers = {}
        
        stars_quality = analyzed_df[["stars", "cbo_mean", "dit_mean", "lcom_mean"]].dropna()
        if len(stars_quality) >= 3:
            answers["RQ01"] = {
                "question": "Relação entre popularidade (estrelas) e características de qualidade",
                "sample_size": len(stars_quality),
                "correlations": {
                    "stars_vs_cbo": stats.spearmanr(stars_quality["stars"], stars_quality["cbo_mean"]),
                    "stars_vs_dit": stats.spearmanr(stars_quality["stars"], stars_quality["dit_mean"]),
                    "stars_vs_lcom": stats.spearmanr(stars_quality["stars"], stars_quality["lcom_mean"])
                }
            }
        
        age_quality = analyzed_df[["age_years", "cbo_mean", "dit_mean", "lcom_mean"]].dropna()
        if len(age_quality) >= 3:
            answers["RQ02"] = {
                "question": "Relação entre maturidade (idade) e características de qualidade",
                "sample_size": len(age_quality),
                "correlations": {
                    "age_vs_cbo": stats.spearmanr(age_quality["age_years"], age_quality["cbo_mean"]),
                    "age_vs_dit": stats.spearmanr(age_quality["age_years"], age_quality["dit_mean"]),
                    "age_vs_lcom": stats.spearmanr(age_quality["age_years"], age_quality["lcom_mean"])
                }
            }
        
        activity_quality = analyzed_df[["forks", "cbo_mean", "dit_mean", "lcom_mean"]].dropna()
        if len(activity_quality) >= 3:
            answers["RQ03"] = {
                "question": "Relação entre atividade (forks) e características de qualidade",
                "sample_size": len(activity_quality),
                "correlations": {
                    "forks_vs_cbo": stats.spearmanr(activity_quality["forks"], activity_quality["cbo_mean"]),
                    "forks_vs_dit": stats.spearmanr(activity_quality["forks"], activity_quality["dit_mean"]),
                    "forks_vs_lcom": stats.spearmanr(activity_quality["forks"], activity_quality["lcom_mean"])
                }
            }
        
        size_quality = analyzed_df[["loc_total", "cbo_mean", "dit_mean", "lcom_mean"]].dropna()
        if len(size_quality) >= 3:
            answers["RQ04"] = {
                "question": "Relação entre tamanho (LOC) e características de qualidade",
                "sample_size": len(size_quality),
                "correlations": {
                    "loc_vs_cbo": stats.spearmanr(size_quality["loc_total"], size_quality["cbo_mean"]),
                    "loc_vs_dit": stats.spearmanr(size_quality["loc_total"], size_quality["dit_mean"]),
                    "loc_vs_lcom": stats.spearmanr(size_quality["loc_total"], size_quality["lcom_mean"])
                }
            }
        
        return answers
    
    def create_visualizations(self, output_dir="data/plots"):
        if self.consolidated_data is None:
            return
        
        print("Criando visualizações...")
        
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        analyzed_df = self.consolidated_data[self.consolidated_data["analyzed"] == True].copy()
        
        if len(analyzed_df) == 0:
            print("Nenhum dado analisado para visualizar.")
            return
        
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Relação entre Popularidade (Estrelas) e Métricas de Qualidade', fontsize=16)
        
        metrics = [("cbo_mean", "CBO (Coupling Between Objects)"),
                  ("dit_mean", "DIT (Depth Inheritance Tree)"),
                  ("lcom_mean", "LCOM (Lack of Cohesion of Methods)"),
                  ("total_classes", "Número Total de Classes")]
        
        for i, (metric, title) in enumerate(metrics):
            ax = axes[i//2, i%2]
            valid_data = analyzed_df[["stars", metric]].dropna()
            
            if len(valid_data) > 0:
                ax.scatter(valid_data["stars"], valid_data[metric], alpha=0.6)
                ax.set_xlabel("Número de Estrelas")
                ax.set_ylabel(title)
                ax.set_title(f"Estrelas vs {title}")
                
                z = np.polyfit(valid_data["stars"], valid_data[metric], 1)
                p = np.poly1d(z)
                ax.plot(valid_data["stars"], p(valid_data["stars"]), "r--", alpha=0.8)
        
        plt.tight_layout()
        plt.savefig(output_path / "popularity_vs_quality.png", dpi=300, bbox_inches='tight')
        plt.close()
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Distribuição das Métricas de Qualidade', fontsize=16)
        
        quality_metrics = ["cbo_mean", "dit_mean", "lcom_mean", "total_classes"]
        
        for i, metric in enumerate(quality_metrics):
            ax = axes[i//2, i%2]
            values = analyzed_df[metric].dropna()
            
            if len(values) > 0:
                ax.hist(values, bins=20, alpha=0.7, edgecolor='black')
                ax.set_xlabel(metric.replace("_", " ").title())
                ax.set_ylabel("Frequência")
                ax.set_title(f"Distribuição de {metric.replace('_', ' ').title()}")
        
        plt.tight_layout()
        plt.savefig(output_path / "quality_metrics_distribution.png", dpi=300, bbox_inches='tight')
        plt.close()
        
        fig, ax = plt.subplots(figsize=(10, 8))
        
        numeric_cols = ["stars", "forks", "age_years", "cbo_mean", "dit_mean", "lcom_mean", "total_classes", "loc_total"]
        correlation_data = analyzed_df[numeric_cols].dropna()
        
        if len(correlation_data) > 0:
            correlation_matrix = correlation_data.corr()
            sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0, 
                       square=True, ax=ax, fmt='.3f')
            ax.set_title('Matriz de Correlação - Métricas de Processo e Qualidade')
        
        plt.tight_layout()
        plt.savefig(output_path / "correlation_heatmap.png", dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"Visualizações salvas em {output_path}")
    
    def save_final_report(self, filename="data/final_report.json"):
        print("Gerando relatório final...")
        
        if self.consolidated_data is None:
            self.consolidate_data()
        
        summary_stats = self.generate_summary_statistics()
        correlations = self.calculate_correlation_analysis()
        research_answers = self.answer_research_questions()
        
        final_report = {
            "metadata": {
                "report_generated_at": pd.Timestamp.now().isoformat(),
                "total_repositories_analyzed": len(self.consolidated_data[self.consolidated_data["analyzed"] == True]),
                "analysis_version": "1.0"
            },
            "summary_statistics": summary_stats,
            "correlation_analysis": correlations,
            "research_questions_answers": research_answers,
            "hypotheses_and_findings": self.generate_hypotheses_analysis(research_answers)
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(final_report, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"Relatório final salvo em {filename}")
        return final_report
    
    def generate_hypotheses_analysis(self, research_answers):
        hypotheses = {
            "RQ01_hypothesis": "Repositórios mais populares (mais estrelas) tendem a ter melhor qualidade de código",
            "RQ02_hypothesis": "Repositórios mais maduros (mais antigos) tendem a ter pior qualidade devido à evolução contínua",
            "RQ03_hypothesis": "Repositórios mais ativos (mais forks) tendem a ter melhor qualidade devido ao maior cuidado na manutenção",
            "RQ04_hypothesis": "Repositórios maiores (mais LOC) tendem a ter pior qualidade devido à complexidade",
            "findings": []
        }
        
        for rq_key, rq_data in research_answers.items():
            if isinstance(rq_data, dict) and "correlations" in rq_data:
                finding = f"{rq_data['question']}: "
                
                correlations = rq_data["correlations"]
                for corr_key, (corr_value, p_value) in correlations.items():
                    strength = "forte" if abs(corr_value) > 0.7 else "moderada" if abs(corr_value) > 0.3 else "fraca"
                    direction = "positiva" if corr_value > 0 else "negativa"
                    significance = "significativa" if p_value < 0.05 else "não significativa"
                    
                    finding += f"{corr_key}: correlação {strength} {direction} ({corr_value:.3f}, p={p_value:.3f}, {significance}). "
                
                hypotheses["findings"].append(finding)
        
        return hypotheses
    
    def print_final_summary(self):
        if self.consolidated_data is None:
            print("Nenhum dado consolidado disponível.")
            return
        
        analyzed_df = self.consolidated_data[self.consolidated_data["analyzed"] == True]
        
        print("\n" + "="*60)
        print("RESUMO FINAL DA ANÁLISE DE QUALIDADE DE SISTEMAS JAVA")
        print("="*60)
        
        print(f"\n📊 DADOS GERAIS:")
        print(f"   • Total de repositórios coletados: {len(self.consolidated_data)}")
        print(f"   • Repositórios clonados: {len(self.consolidated_data[self.consolidated_data['cloned'] == True])}")
        print(f"   • Repositórios analisados: {len(analyzed_df)}")
        
        if len(analyzed_df) > 0:
            print(f"\n📈 MÉTRICAS DE QUALIDADE (médias):")
            print(f"   • CBO (Coupling): {analyzed_df['cbo_mean'].mean():.2f}")
            print(f"   • DIT (Inheritance): {analyzed_df['dit_mean'].mean():.2f}")
            print(f"   • LCOM (Cohesion): {analyzed_df['lcom_mean'].mean():.2f}")
            print(f"   • Classes por repositório: {analyzed_df['total_classes'].mean():.0f}")
            print(f"   • LOC por repositório: {analyzed_df['loc_total'].mean():.0f}")
            
            print(f"\n🏆 TOP 3 REPOSITÓRIOS POR ESTRELAS:")
            top_repos = analyzed_df.nlargest(3, 'stars')[['full_name', 'stars', 'cbo_mean', 'dit_mean', 'lcom_mean']]
            for i, (_, row) in enumerate(top_repos.iterrows(), 1):
                print(f"   {i}. {row['full_name']} - {row['stars']} estrelas")
                print(f"      CBO: {row['cbo_mean']:.2f}, DIT: {row['dit_mean']:.2f}, LCOM: {row['lcom_mean']:.2f}")
        
        print(f"\n✅ ARQUIVOS GERADOS:")
        print(f"   • data/consolidated_data.csv - Dataset completo")
        print(f"   • data/final_report.json - Relatório detalhado")
        print(f"   • data/plots/ - Visualizações dos dados")
        
        print("\n" + "="*60)


def main():
    print("=== PROCESSAMENTO E CONSOLIDAÇÃO DE DADOS ===\n")
    
    processor = DataProcessor()
    
    if not processor.load_all_data():
        print("Erro ao carregar dados. Verifique se todos os arquivos existem.")
        return
    
    consolidated_df = processor.consolidate_data()
    
    consolidated_df.to_csv("data/consolidated_data.csv", index=False)
    print("✓ Dataset consolidado salvo em data/consolidated_data.csv")
    
    final_report = processor.save_final_report()
    
    processor.create_visualizations()
    
    processor.print_final_summary()
    
    print("\n=== PROCESSAMENTO CONCLUÍDO ===")
    print("Todos os dados foram processados e consolidados com sucesso!")


if __name__ == "__main__":
    main()