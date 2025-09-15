#!/usr/bin/env python3

import json
import subprocess
import pandas as pd
import numpy as np
from pathlib import Path
import shutil
import requests
import os

class SingleRepoAnalyzer:
    def __init__(self, output_dir="data"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.ck_jar_path = Path("tools/ck.jar")
        self.demo_repo_path = Path("demo_repo")
    
    def download_ck_tool(self):
        if self.ck_jar_path.exists():
            print(f"Ferramenta CK encontrada em {self.ck_jar_path}")
            return True
        
        print("Baixando ferramenta CK...")
        self.ck_jar_path.parent.mkdir(exist_ok=True)
        
        ck_url = "https://github.com/mauricioaniche/ck/releases/download/v0.7.1/ck-0.7.1-SNAPSHOT-jar-with-dependencies.jar"
        
        try:
            response = requests.get(ck_url, stream=True)
            response.raise_for_status()
            
            with open(self.ck_jar_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"CK baixado com sucesso em {self.ck_jar_path}")
            return True
            
        except Exception as e:
            print(f"Erro ao baixar CK: {e}")
            return False
    
    def clone_demo_repository(self, repo_url="https://github.com/spring-projects/spring-boot.git"):
        if self.demo_repo_path.exists():
            shutil.rmtree(self.demo_repo_path)
        
        print(f"Clonando repositório de demonstração: {repo_url}")
        
        cmd = [
            "git", "clone",
            "--depth", "1",
            "--single-branch",
            repo_url,
            str(self.demo_repo_path)
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                print(f"✓ Repositório clonado com sucesso em {self.demo_repo_path}")
                return True
            else:
                print(f"✗ Erro ao clonar repositório: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            print("✗ Timeout ao clonar repositório")
            return False
        except Exception as e:
            print(f"✗ Erro inesperado: {e}")
            return False
    
    def run_ck_analysis(self):
        if not self.ck_jar_path.exists():
            print(f"Erro: Ferramenta CK não encontrada em {self.ck_jar_path}")
            return None
        
        output_file = self.output_dir / "demo_repo_ck_metrics.csv"
        
        cmd = [
            "java", "-jar", str(self.ck_jar_path),
            str(self.demo_repo_path),
            "true",
            "0",
            "false",
            str(output_file)
        ]
        
        try:
            print("Executando análise CK...")
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
            
            if result.returncode == 0 and output_file.exists():
                print(f"✓ Análise CK executada com sucesso")
                print(f"  Resultados salvos em: {output_file}")
                return str(output_file)
            else:
                print(f"✗ Erro ao executar CK: {result.stderr}")
                return None
                
        except subprocess.TimeoutExpired:
            print("✗ Timeout ao executar CK")
            return None
        except Exception as e:
            print(f"✗ Erro inesperado: {e}")
            return None
    
    def analyze_ck_results(self, csv_file):
        try:
            df = pd.read_csv(csv_file)
            
            if df.empty:
                print("Arquivo CSV vazio ou sem dados.")
                return {}
            
            print(f"Analisando {len(df)} classes Java...")
            
            stats = {
                "total_classes": len(df),
                "total_methods": df['cbo'].sum() if 'cbo' in df.columns else 0,
                "total_loc": df['loc'].sum() if 'loc' in df.columns else 0,
            }
            
            if 'cbo' in df.columns:
                stats['cbo'] = {
                    "mean": float(df['cbo'].mean()),
                    "median": float(df['cbo'].median()),
                    "std": float(df['cbo'].std()),
                    "min": float(df['cbo'].min()),
                    "max": float(df['cbo'].max())
                }
            
            if 'dit' in df.columns:
                stats['dit'] = {
                    "mean": float(df['dit'].mean()),
                    "median": float(df['dit'].median()),
                    "std": float(df['dit'].std()),
                    "min": float(df['dit'].min()),
                    "max": float(df['dit'].max())
                }
            
            if 'lcom' in df.columns:
                stats['lcom'] = {
                    "mean": float(df['lcom'].mean()),
                    "median": float(df['lcom'].median()),
                    "std": float(df['lcom'].std()),
                    "min": float(df['lcom'].min()),
                    "max": float(df['lcom'].max())
                }
            
            if 'rfc' in df.columns:
                stats['rfc'] = {
                    "mean": float(df['rfc'].mean()),
                    "median": float(df['rfc'].median())
                }
            
            if 'wmc' in df.columns:
                stats['wmc'] = {
                    "mean": float(df['wmc'].mean()),
                    "median": float(df['wmc'].median())
                }
            
            return stats
            
        except Exception as e:
            print(f"Erro ao analisar resultados: {e}")
            return {}
    
    def create_summary_csv(self, stats, original_csv):
        summary_file = self.output_dir / "demo_repo_summary.csv"
        
        df = pd.read_csv(original_csv)
        
        summary_data = []
        for _, row in df.iterrows():
            summary_data.append({
                "class": row.get('class', 'Unknown'),
                "file": row.get('file', 'Unknown'),
                "cbo": row.get('cbo', 0),
                "dit": row.get('dit', 0),
                "lcom": row.get('lcom', 0),
                "rfc": row.get('rfc', 0),
                "wmc": row.get('wmc', 0),
                "loc": row.get('loc', 0)
            })
        
        summary_df = pd.DataFrame(summary_data)
        summary_df.to_csv(summary_file, index=False)
        
        print(f"✓ Resumo por classe salvo em: {summary_file}")
        
        general_stats_file = self.output_dir / "demo_repo_general_stats.csv"
        
        general_stats_data = []
        
        general_stats_data.append({
            "metric": "total_classes",
            "value": stats.get("total_classes", 0),
            "description": "Total de classes analisadas"
        })
        
        general_stats_data.append({
            "metric": "total_loc",
            "value": stats.get("total_loc", 0),
            "description": "Total de linhas de código"
        })
        
        if "cbo" in stats:
            cbo_stats = stats["cbo"]
            general_stats_data.extend([
                {
                    "metric": "cbo_mean",
                    "value": cbo_stats["mean"],
                    "description": "Média de Coupling Between Objects"
                },
                {
                    "metric": "cbo_median",
                    "value": cbo_stats["median"],
                    "description": "Mediana de Coupling Between Objects"
                },
                {
                    "metric": "cbo_std",
                    "value": cbo_stats["std"],
                    "description": "Desvio padrão de Coupling Between Objects"
                }
            ])
        
        if "dit" in stats:
            dit_stats = stats["dit"]
            general_stats_data.extend([
                {
                    "metric": "dit_mean",
                    "value": dit_stats["mean"],
                    "description": "Média de Depth Inheritance Tree"
                },
                {
                    "metric": "dit_median",
                    "value": dit_stats["median"],
                    "description": "Mediana de Depth Inheritance Tree"
                },
                {
                    "metric": "dit_std",
                    "value": dit_stats["std"],
                    "description": "Desvio padrão de Depth Inheritance Tree"
                }
            ])
        
        if "lcom" in stats:
            lcom_stats = stats["lcom"]
            general_stats_data.extend([
                {
                    "metric": "lcom_mean",
                    "value": lcom_stats["mean"],
                    "description": "Média de Lack of Cohesion of Methods"
                },
                {
                    "metric": "lcom_median",
                    "value": lcom_stats["median"],
                    "description": "Mediana de Lack of Cohesion of Methods"
                },
                {
                    "metric": "lcom_std",
                    "value": lcom_stats["std"],
                    "description": "Desvio padrão de Lack of Cohesion of Methods"
                }
            ])
        
        general_stats_df = pd.DataFrame(general_stats_data)
        general_stats_df.to_csv(general_stats_file, index=False)
        
        print(f"✓ Estatísticas gerais salvas em: {general_stats_file}")
        
        return str(summary_file)
    
    def print_analysis_summary(self, stats):
        print("\n" + "="*60)
        print("RESUMO DA ANÁLISE DE QUALIDADE - REPOSITÓRIO DE DEMONSTRAÇÃO")
        print("="*60)
        
        print(f"\n📊 DADOS GERAIS:")
        print(f"   • Total de classes analisadas: {stats.get('total_classes', 0)}")
        print(f"   • Total de linhas de código: {stats.get('total_loc', 0):,}")
        
        if "cbo" in stats:
            cbo = stats["cbo"]
            print(f"\n🔗 CBO (Coupling Between Objects):")
            print(f"   • Média: {cbo['mean']:.2f}")
            print(f"   • Mediana: {cbo['median']:.2f}")
            print(f"   • Desvio padrão: {cbo['std']:.2f}")
            print(f"   • Mínimo: {cbo['min']}")
            print(f"   • Máximo: {cbo['max']}")
        
        if "dit" in stats:
            dit = stats["dit"]
            print(f"\n🌳 DIT (Depth Inheritance Tree):")
            print(f"   • Média: {dit['mean']:.2f}")
            print(f"   • Mediana: {dit['median']:.2f}")
            print(f"   • Desvio padrão: {dit['std']:.2f}")
            print(f"   • Mínimo: {dit['min']}")
            print(f"   • Máximo: {dit['max']}")
        
        if "lcom" in stats:
            lcom = stats["lcom"]
            print(f"\n🧩 LCOM (Lack of Cohesion of Methods):")
            print(f"   • Média: {lcom['mean']:.2f}")
            print(f"   • Mediana: {lcom['median']:.2f}")
            print(f"   • Desvio padrão: {lcom['std']:.2f}")
            print(f"   • Mínimo: {lcom['min']}")
            print(f"   • Máximo: {lcom['max']}")
        
        print(f"\n✅ ARQUIVOS GERADOS:")
        print(f"   • data/demo_repo_ck_metrics.csv - Métricas detalhadas por classe")
        print(f"   • data/demo_repo_summary.csv - Resumo por classe")
        print(f"   • data/demo_repo_general_stats.csv - Estatísticas gerais")
        
        print("\n" + "="*60)


def main():
    print("=== DEMONSTRAÇÃO: ANÁLISE DE QUALIDADE DE UM REPOSITÓRIO JAVA ===\n")
    
    analyzer = SingleRepoAnalyzer()
    
    if not analyzer.download_ck_tool():
        print("Não foi possível obter a ferramenta CK. Abortando.")
        return
    
    demo_repo_url = "https://github.com/spring-projects/spring-boot.git"
    print(f"Usando repositório de demonstração: Spring Boot")
    
    if not analyzer.clone_demo_repository(demo_repo_url):
        print("Não foi possível clonar o repositório de demonstração.")
        return
    
    ck_csv_file = analyzer.run_ck_analysis()
    if not ck_csv_file:
        print("Falha na análise CK.")
        return
    
    stats = analyzer.analyze_ck_results(ck_csv_file)
    if not stats:
        print("Não foi possível analisar os resultados.")
        return
    
    summary_file = analyzer.create_summary_csv(stats, ck_csv_file)
    
    analyzer.print_analysis_summary(stats)
    
    if analyzer.demo_repo_path.exists():
        shutil.rmtree(analyzer.demo_repo_path)
        print(f"\n🧹 Repositório de demonstração removido: {analyzer.demo_repo_path}")
    
    print("\n=== DEMONSTRAÇÃO CONCLUÍDA ===")
    print("Este exemplo mostra como o sistema analisa um repositório Java")
    print("e gera métricas de qualidade usando a ferramenta CK.")


if __name__ == "__main__":
    main()