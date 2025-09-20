#!/usr/bin/env python3

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import json

class VisualizationGenerator:
    def __init__(self, data_file="data/consolidated_data.csv", output_dir="data/plots"):
        self.data_file = data_file
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.df = None
        
        # Configurar estilo
        plt.style.use('default')
        sns.set_palette("husl")
        plt.rcParams['figure.figsize'] = (12, 8)
        plt.rcParams['font.size'] = 10
        
    def load_data(self):
        try:
            self.df = pd.read_csv(self.data_file)
            analyzed_df = self.df[self.df['analyzed'] == True].copy()
            print(f"Carregados {len(analyzed_df)} repositórios analisados")
            return analyzed_df
        except FileNotFoundError:
            print(f"Arquivo {self.data_file} não encontrado")
            return None
    
    def create_correlation_heatmap(self, df):
        print("Criando heatmap de correlações...")
        
        numeric_cols = ['stars', 'forks', 'age_years', 'cbo_mean', 'dit_mean', 'lcom_mean', 'total_classes', 'loc_total']
        correlation_data = df[numeric_cols].dropna()
        
        if len(correlation_data) == 0:
            print("Nenhum dado disponível para heatmap")
            return
        
        plt.figure(figsize=(12, 10))
        correlation_matrix = correlation_data.corr()
        
        mask = np.triu(np.ones_like(correlation_matrix, dtype=bool))
        
        sns.heatmap(correlation_matrix, 
                   mask=mask,
                   annot=True, 
                   cmap='RdBu_r', 
                   center=0,
                   square=True, 
                   fmt='.3f',
                   cbar_kws={"shrink": .8})
        
        plt.title('Matriz de Correlação - Métricas de Processo e Qualidade', fontsize=14, pad=20)
        plt.tight_layout()
        plt.savefig(self.output_dir / 'correlation_heatmap.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def create_scatter_plots(self, df):
        print("Criando gráficos de dispersão...")
        
        process_metrics = ['stars', 'forks', 'age_years', 'loc_total']
        quality_metrics = ['cbo_mean', 'dit_mean', 'lcom_mean']
        
        for process_metric in process_metrics:
            if process_metric not in df.columns:
                continue
                
            fig, axes = plt.subplots(1, 3, figsize=(18, 6))
            fig.suptitle(f'Relação entre {process_metric.replace("_", " ").title()} e Métricas de Qualidade', fontsize=16)
            
            for i, quality_metric in enumerate(quality_metrics):
                if quality_metric not in df.columns:
                    continue
                    
                ax = axes[i]
                valid_data = df[[process_metric, quality_metric]].dropna()
                
                if len(valid_data) > 0:
                    ax.scatter(valid_data[process_metric], valid_data[quality_metric], 
                             alpha=0.6, s=50, edgecolors='black', linewidth=0.5)
                    
                    # Linha de tendência
                    z = np.polyfit(valid_data[process_metric], valid_data[quality_metric], 1)
                    p = np.poly1d(z)
                    ax.plot(valid_data[process_metric], p(valid_data[process_metric]), 
                           "r--", alpha=0.8, linewidth=2)
                    
                    # Calcular correlação
                    from scipy.stats import spearmanr
                    corr, p_val = spearmanr(valid_data[process_metric], valid_data[quality_metric])
                    
                    ax.set_xlabel(process_metric.replace('_', ' ').title())
                    ax.set_ylabel(quality_metric.replace('_', ' ').title())
                    ax.set_title(f'{quality_metric.replace("_", " ").title()}\n(r={corr:.3f}, p={p_val:.3f})')
                    
                    # Grid
                    ax.grid(True, alpha=0.3)
            
            plt.tight_layout()
            plt.savefig(self.output_dir / f'scatter_{process_metric}.png', dpi=300, bbox_inches='tight')
            plt.close()
    
    def create_distribution_plots(self, df):
        print("Criando gráficos de distribuição...")
        
        # Distribuição das métricas de processo
        process_metrics = ['stars', 'forks', 'age_years', 'loc_total']
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Distribuição das Métricas de Processo', fontsize=16)
        
        for i, metric in enumerate(process_metrics):
            if metric not in df.columns:
                continue
                
            ax = axes[i//2, i%2]
            values = df[metric].dropna()
            
            if len(values) > 0:
                # Histograma
                ax.hist(values, bins=30, alpha=0.7, edgecolor='black', density=True)
                
                # Curva de densidade
                from scipy.stats import gaussian_kde
                if len(values) > 1:
                    kde = gaussian_kde(values)
                    x_range = np.linspace(values.min(), values.max(), 100)
                    ax.plot(x_range, kde(x_range), 'r-', linewidth=2)
                
                ax.set_xlabel(metric.replace('_', ' ').title())
                ax.set_ylabel('Densidade')
                ax.set_title(f'Distribuição de {metric.replace("_", " ").title()}')
                ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'process_metrics_distribution.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # Distribuição das métricas de qualidade
        quality_metrics = ['cbo_mean', 'dit_mean', 'lcom_mean', 'total_classes']
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Distribuição das Métricas de Qualidade', fontsize=16)
        
        for i, metric in enumerate(quality_metrics):
            if metric not in df.columns:
                continue
                
            ax = axes[i//2, i%2]
            values = df[metric].dropna()
            
            if len(values) > 0:
                ax.hist(values, bins=30, alpha=0.7, edgecolor='black', density=True)
                
                from scipy.stats import gaussian_kde
                if len(values) > 1:
                    kde = gaussian_kde(values)
                    x_range = np.linspace(values.min(), values.max(), 100)
                    ax.plot(x_range, kde(x_range), 'r-', linewidth=2)
                
                ax.set_xlabel(metric.replace('_', ' ').title())
                ax.set_ylabel('Densidade')
                ax.set_title(f'Distribuição de {metric.replace("_", " ").title()}')
                ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'quality_metrics_distribution.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def create_box_plots(self, df):
        print("Criando gráficos de box plot...")
        
        # Box plots por faixa de popularidade
        if 'stars' in df.columns:
            df['popularity_group'] = pd.cut(df['stars'], 
                                          bins=[0, df['stars'].quantile(0.33), 
                                                df['stars'].quantile(0.67), 
                                                df['stars'].max()], 
                                          labels=['Baixa', 'Média', 'Alta'])
            
            quality_metrics = ['cbo_mean', 'dit_mean', 'lcom_mean']
            
            fig, axes = plt.subplots(1, 3, figsize=(18, 6))
            fig.suptitle('Métricas de Qualidade por Faixa de Popularidade', fontsize=16)
            
            for i, metric in enumerate(quality_metrics):
                if metric not in df.columns:
                    continue
                    
                ax = axes[i]
                valid_data = df[['popularity_group', metric]].dropna()
                
                if len(valid_data) > 0:
                    sns.boxplot(data=valid_data, x='popularity_group', y=metric, ax=ax)
                    ax.set_title(f'{metric.replace("_", " ").title()}')
                    ax.set_xlabel('Faixa de Popularidade')
                    ax.set_ylabel(metric.replace('_', ' ').title())
                    ax.grid(True, alpha=0.3)
            
            plt.tight_layout()
            plt.savefig(self.output_dir / 'boxplot_popularity.png', dpi=300, bbox_inches='tight')
            plt.close()
    
    def create_research_question_plots(self, df):
        print("Criando gráficos específicos para questões de pesquisa...")
        
        # RQ 01: Popularidade vs Qualidade
        if 'stars' in df.columns:
            fig, axes = plt.subplots(2, 2, figsize=(15, 12))
            fig.suptitle('RQ 01: Relação entre Popularidade e Qualidade', fontsize=16)
            
            quality_metrics = ['cbo_mean', 'dit_mean', 'lcom_mean', 'total_classes']
            
            for i, metric in enumerate(quality_metrics):
                if metric not in df.columns:
                    continue
                    
                ax = axes[i//2, i%2]
                valid_data = df[['stars', metric]].dropna()
                
                if len(valid_data) > 0:
                    # Scatter plot com linha de tendência
                    ax.scatter(valid_data['stars'], valid_data[metric], alpha=0.6, s=50)
                    
                    # Linha de tendência
                    z = np.polyfit(valid_data['stars'], valid_data[metric], 1)
                    p = np.poly1d(z)
                    ax.plot(valid_data['stars'], p(valid_data['stars']), "r--", alpha=0.8)
                    
                    # Correlação
                    from scipy.stats import spearmanr
                    corr, p_val = spearmanr(valid_data['stars'], valid_data[metric])
                    
                    ax.set_xlabel('Número de Estrelas')
                    ax.set_ylabel(metric.replace('_', ' ').title())
                    ax.set_title(f'Estrelas vs {metric.replace("_", " ").title()}\n(r={corr:.3f}, p={p_val:.3f})')
                    ax.grid(True, alpha=0.3)
            
            plt.tight_layout()
            plt.savefig(self.output_dir / 'rq01_popularity_quality.png', dpi=300, bbox_inches='tight')
            plt.close()
        
        # RQ 02: Maturidade vs Qualidade
        if 'age_years' in df.columns:
            fig, axes = plt.subplots(2, 2, figsize=(15, 12))
            fig.suptitle('RQ 02: Relação entre Maturidade e Qualidade', fontsize=16)
            
            for i, metric in enumerate(quality_metrics):
                if metric not in df.columns:
                    continue
                    
                ax = axes[i//2, i%2]
                valid_data = df[['age_years', metric]].dropna()
                
                if len(valid_data) > 0:
                    ax.scatter(valid_data['age_years'], valid_data[metric], alpha=0.6, s=50)
                    
                    z = np.polyfit(valid_data['age_years'], valid_data[metric], 1)
                    p = np.poly1d(z)
                    ax.plot(valid_data['age_years'], p(valid_data['age_years']), "r--", alpha=0.8)
                    
                    from scipy.stats import spearmanr
                    corr, p_val = spearmanr(valid_data['age_years'], valid_data[metric])
                    
                    ax.set_xlabel('Idade (anos)')
                    ax.set_ylabel(metric.replace('_', ' ').title())
                    ax.set_title(f'Idade vs {metric.replace("_", " ").title()}\n(r={corr:.3f}, p={p_val:.3f})')
                    ax.grid(True, alpha=0.3)
            
            plt.tight_layout()
            plt.savefig(self.output_dir / 'rq02_maturity_quality.png', dpi=300, bbox_inches='tight')
            plt.close()
    
    def create_summary_plots(self, df):
        print("Criando gráficos de resumo...")
        
        # Top 10 repositórios por estrelas
        if 'stars' in df.columns and 'full_name' in df.columns:
            top_repos = df.nlargest(10, 'stars')[['full_name', 'stars', 'cbo_mean', 'dit_mean', 'lcom_mean']]
            
            fig, ax = plt.subplots(figsize=(12, 8))
            
            x_pos = np.arange(len(top_repos))
            bars = ax.bar(x_pos, top_repos['stars'], alpha=0.7)
            
            ax.set_xlabel('Repositórios')
            ax.set_ylabel('Número de Estrelas')
            ax.set_title('Top 10 Repositórios por Popularidade')
            ax.set_xticks(x_pos)
            ax.set_xticklabels([name.split('/')[-1] for name in top_repos['full_name']], 
                              rotation=45, ha='right')
            
            # Adicionar valores nas barras
            for i, bar in enumerate(bars):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                       f'{int(height):,}', ha='center', va='bottom')
            
            plt.tight_layout()
            plt.savefig(self.output_dir / 'top_repositories.png', dpi=300, bbox_inches='tight')
            plt.close()
    
    def generate_all_visualizations(self):
        df = self.load_data()
        if df is None or len(df) == 0:
            print("Nenhum dado disponível para visualização")
            return
        
        print(f"Criando visualizações em {self.output_dir}")
        
        self.create_correlation_heatmap(df)
        self.create_scatter_plots(df)
        self.create_distribution_plots(df)
        self.create_box_plots(df)
        self.create_research_question_plots(df)
        self.create_summary_plots(df)
        
        print(f"\n✅ Visualizações criadas com sucesso!")
        print(f"📁 Diretório: {self.output_dir}")
        
        # Listar arquivos criados
        plot_files = list(self.output_dir.glob("*.png"))
        print(f"📊 Total de gráficos: {len(plot_files)}")
        for file in sorted(plot_files):
            print(f"   • {file.name}")

def main():
    print("=== CRIAÇÃO DE VISUALIZAÇÕES - SPRINT 2 ===\n")
    
    viz = VisualizationGenerator()
    viz.generate_all_visualizations()
    
    print("\n=== VISUALIZAÇÕES CONCLUÍDAS ===")
    print("Próximos passos:")
    print("1. Execute: python scripts/generate_final_report.py")

if __name__ == "__main__":
    main()

