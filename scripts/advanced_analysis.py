#!/usr/bin/env python3

import pandas as pd
import numpy as np
import json
from scipy import stats
from scipy.stats import spearmanr, pearsonr, kendalltau
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

class AdvancedAnalyzer:
    def __init__(self, data_file="data/consolidated_data.csv"):
        self.data_file = data_file
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
    
    def filter_analyzed_repos(self):
        if self.df is None:
            return None
        return self.df[self.df['analyzed'] == True].copy()
    
    def calculate_descriptive_statistics(self):
        analyzed_df = self.filter_analyzed_repos()
        if analyzed_df is None or len(analyzed_df) == 0:
            return {}
        
        print("Calculando estatísticas descritivas...")
        
        metrics = {
            'process': ['stars', 'forks', 'age_years', 'size_kb'],
            'quality': ['cbo_mean', 'dit_mean', 'lcom_mean', 'total_classes', 'loc_total']
        }
        
        stats_results = {}
        
        for category, metric_list in metrics.items():
            stats_results[category] = {}
            for metric in metric_list:
                if metric in analyzed_df.columns:
                    values = analyzed_df[metric].dropna()
                    if len(values) > 0:
                        stats_results[category][metric] = {
                            'count': len(values),
                            'mean': float(values.mean()),
                            'median': float(values.median()),
                            'std': float(values.std()),
                            'min': float(values.min()),
                            'max': float(values.max()),
                            'q25': float(values.quantile(0.25)),
                            'q75': float(values.quantile(0.75)),
                            'skewness': float(stats.skew(values)),
                            'kurtosis': float(stats.kurtosis(values))
                        }
        
        self.analysis_results['descriptive'] = stats_results
        return stats_results
    
    def perform_correlation_analysis(self):
        analyzed_df = self.filter_analyzed_repos()
        if analyzed_df is None or len(analyzed_df) < 3:
            return {}
        
        print("Realizando análise de correlação...")
        
        process_metrics = ['stars', 'forks', 'age_years', 'size_kb']
        quality_metrics = ['cbo_mean', 'dit_mean', 'lcom_mean', 'total_classes', 'loc_total']
        
        correlations = {}
        
        for process_metric in process_metrics:
            if process_metric not in analyzed_df.columns:
                continue
                
            correlations[process_metric] = {}
            
            for quality_metric in quality_metrics:
                if quality_metric not in analyzed_df.columns:
                    continue
                
                valid_data = analyzed_df[[process_metric, quality_metric]].dropna()
                
                if len(valid_data) >= 3:
                    try:
                        # Spearman (não-paramétrica)
                        spearman_corr, spearman_p = spearmanr(valid_data[process_metric], valid_data[quality_metric])
                        
                        # Pearson (paramétrica)
                        pearson_corr, pearson_p = pearsonr(valid_data[process_metric], valid_data[quality_metric])
                        
                        # Kendall (não-paramétrica)
                        kendall_corr, kendall_p = kendalltau(valid_data[process_metric], valid_data[quality_metric])
                        
                        correlations[process_metric][quality_metric] = {
                            'spearman': {
                                'correlation': float(spearman_corr),
                                'p_value': float(spearman_p),
                                'significant': bool(spearman_p < 0.05)
                            },
                            'pearson': {
                                'correlation': float(pearson_corr),
                                'p_value': float(pearson_p),
                                'significant': bool(pearson_p < 0.05)
                            },
                            'kendall': {
                                'correlation': float(kendall_corr),
                                'p_value': float(kendall_p),
                                'significant': bool(kendall_p < 0.05)
                            },
                            'sample_size': int(len(valid_data))
                        }
                    except Exception as e:
                        print(f"Erro ao calcular correlação {process_metric} vs {quality_metric}: {e}")
        
        self.analysis_results['correlations'] = correlations
        return correlations
    
    def perform_hypothesis_testing(self):
        analyzed_df = self.filter_analyzed_repos()
        if analyzed_df is None or len(analyzed_df) < 3:
            return {}
        
        print("Realizando testes de hipóteses...")
        
        # Teste de normalidade (Shapiro-Wilk para amostras pequenas)
        normality_tests = {}
        
        metrics = ['stars', 'forks', 'age_years', 'cbo_mean', 'dit_mean', 'lcom_mean']
        
        for metric in metrics:
            if metric in analyzed_df.columns:
                values = analyzed_df[metric].dropna()
                if len(values) >= 3 and len(values) <= 5000:  # Shapiro-Wilk limit
                    try:
                        stat, p_value = stats.shapiro(values)
                        normality_tests[metric] = {
                            'statistic': float(stat),
                            'p_value': float(p_value),
                            'is_normal': bool(p_value > 0.05)
                        }
                    except Exception as e:
                        print(f"Erro no teste de normalidade para {metric}: {e}")
        
        # Teste de diferenças entre grupos (baseado em popularidade)
        if 'stars' in analyzed_df.columns:
            median_stars = analyzed_df['stars'].median()
            high_popularity = analyzed_df[analyzed_df['stars'] >= median_stars]
            low_popularity = analyzed_df[analyzed_df['stars'] < median_stars]
            
            group_tests = {}
            quality_metrics = ['cbo_mean', 'dit_mean', 'lcom_mean']
            
            for metric in quality_metrics:
                if metric in analyzed_df.columns:
                    high_values = high_popularity[metric].dropna()
                    low_values = low_popularity[metric].dropna()
                    
                    if len(high_values) >= 3 and len(low_values) >= 3:
                        try:
                            # Mann-Whitney U test (não-paramétrico)
                            stat, p_value = stats.mannwhitneyu(high_values, low_values, alternative='two-sided')
                            
                            group_tests[metric] = {
                                'test': 'Mann-Whitney U',
                                'statistic': float(stat),
                                'p_value': float(p_value),
                                'significant': bool(p_value < 0.05),
                                'high_pop_mean': float(high_values.mean()),
                                'low_pop_mean': float(low_values.mean()),
                                'high_pop_median': float(high_values.median()),
                                'low_pop_median': float(low_values.median())
                            }
                        except Exception as e:
                            print(f"Erro no teste de grupos para {metric}: {e}")
        
        hypothesis_results = {
            'normality_tests': normality_tests,
            'group_tests': group_tests
        }
        
        self.analysis_results['hypothesis_tests'] = hypothesis_results
        return hypothesis_results
    
    def analyze_research_questions(self):
        correlations = self.analysis_results.get('correlations', {})
        
        rq_analysis = {}
        
        # RQ 01: Popularidade vs Qualidade
        if 'stars' in correlations:
            rq_analysis['RQ01'] = {
                'question': 'Relação entre popularidade (estrelas) e características de qualidade',
                'hypothesis': 'Repositórios mais populares tendem a ter melhor qualidade',
                'results': {}
            }
            
            for quality_metric in ['cbo_mean', 'dit_mean', 'lcom_mean']:
                if quality_metric in correlations['stars']:
                    result = correlations['stars'][quality_metric]
                    rq_analysis['RQ01']['results'][quality_metric] = {
                        'spearman_correlation': float(result['spearman']['correlation']),
                        'p_value': float(result['spearman']['p_value']),
                        'significant': bool(result['spearman']['significant']),
                        'interpretation': self.interpret_correlation(
                            result['spearman']['correlation'], 
                            result['spearman']['p_value'],
                            'stars', quality_metric
                        )
                    }
        
        # RQ 02: Maturidade vs Qualidade
        if 'age_years' in correlations:
            rq_analysis['RQ02'] = {
                'question': 'Relação entre maturidade (idade) e características de qualidade',
                'hypothesis': 'Repositórios mais maduros tendem a ter pior qualidade',
                'results': {}
            }
            
            for quality_metric in ['cbo_mean', 'dit_mean', 'lcom_mean']:
                if quality_metric in correlations['age_years']:
                    result = correlations['age_years'][quality_metric]
                    rq_analysis['RQ02']['results'][quality_metric] = {
                        'spearman_correlation': float(result['spearman']['correlation']),
                        'p_value': float(result['spearman']['p_value']),
                        'significant': bool(result['spearman']['significant']),
                        'interpretation': self.interpret_correlation(
                            result['spearman']['correlation'], 
                            result['spearman']['p_value'],
                            'age_years', quality_metric
                        )
                    }
        
        # RQ 03: Atividade vs Qualidade
        if 'forks' in correlations:
            rq_analysis['RQ03'] = {
                'question': 'Relação entre atividade (forks) e características de qualidade',
                'hypothesis': 'Repositórios mais ativos tendem a ter melhor qualidade',
                'results': {}
            }
            
            for quality_metric in ['cbo_mean', 'dit_mean', 'lcom_mean']:
                if quality_metric in correlations['forks']:
                    result = correlations['forks'][quality_metric]
                    rq_analysis['RQ03']['results'][quality_metric] = {
                        'spearman_correlation': float(result['spearman']['correlation']),
                        'p_value': float(result['spearman']['p_value']),
                        'significant': bool(result['spearman']['significant']),
                        'interpretation': self.interpret_correlation(
                            result['spearman']['correlation'], 
                            result['spearman']['p_value'],
                            'forks', quality_metric
                        )
                    }
        
        # RQ 04: Tamanho vs Qualidade
        if 'loc_total' in correlations:
            rq_analysis['RQ04'] = {
                'question': 'Relação entre tamanho (LOC) e características de qualidade',
                'hypothesis': 'Repositórios maiores tendem a ter pior qualidade',
                'results': {}
            }
            
            for quality_metric in ['cbo_mean', 'dit_mean', 'lcom_mean']:
                if quality_metric in correlations['loc_total']:
                    result = correlations['loc_total'][quality_metric]
                    rq_analysis['RQ04']['results'][quality_metric] = {
                        'spearman_correlation': float(result['spearman']['correlation']),
                        'p_value': float(result['spearman']['p_value']),
                        'significant': bool(result['spearman']['significant']),
                        'interpretation': self.interpret_correlation(
                            result['spearman']['correlation'], 
                            result['spearman']['p_value'],
                            'loc_total', quality_metric
                        )
                    }
        
        self.analysis_results['research_questions'] = rq_analysis
        return rq_analysis
    
    def interpret_correlation(self, correlation, p_value, process_metric, quality_metric):
        strength = "forte" if abs(correlation) > 0.7 else "moderada" if abs(correlation) > 0.3 else "fraca"
        direction = "positiva" if correlation > 0 else "negativa"
        significance = "significativa" if p_value < 0.05 else "não significativa"
        
        interpretation = f"Correlação {strength} {direction} ({correlation:.3f})"
        if significance == "significativa":
            interpretation += f" e estatisticamente {significance} (p={p_value:.3f})"
        else:
            interpretation += f" mas não estatisticamente {significance} (p={p_value:.3f})"
        
        return interpretation
    
    def generate_summary_report(self):
        if not self.analysis_results:
            return {}
        
        summary = {
            'metadata': {
                'total_repositories': len(self.df) if self.df is not None else 0,
                'analyzed_repositories': len(self.filter_analyzed_repos()) if self.df is not None else 0,
                'analysis_timestamp': pd.Timestamp.now().isoformat()
            },
            'descriptive_statistics': self.analysis_results.get('descriptive', {}),
            'correlation_analysis': self.analysis_results.get('correlations', {}),
            'hypothesis_tests': self.analysis_results.get('hypothesis_tests', {}),
            'research_questions': self.analysis_results.get('research_questions', {})
        }
        
        return summary
    
    def save_results(self, filename="data/advanced_analysis_results.json"):
        results = self.generate_summary_report()
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"Resultados da análise avançada salvos em {filename}")
        return results

def main():
    print("=== ANÁLISE AVANÇADA DE DADOS - SPRINT 2 ===\n")
    
    analyzer = AdvancedAnalyzer()
    
    if not analyzer.load_data():
        print("Erro ao carregar dados. Execute primeiro a Sprint 1.")
        return
    
    print("Iniciando análises avançadas...")
    
    analyzer.calculate_descriptive_statistics()
    analyzer.perform_correlation_analysis()
    analyzer.perform_hypothesis_testing()
    analyzer.analyze_research_questions()
    
    results = analyzer.save_results()
    
    print("\n=== ANÁLISE AVANÇADA CONCLUÍDA ===")
    print("Próximos passos:")
    print("1. Execute: python scripts/create_visualizations.py")
    print("2. Execute: python scripts/generate_final_report.py")

if __name__ == "__main__":
    main()

