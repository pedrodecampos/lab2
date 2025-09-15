#!/usr/bin/env python3

import json
import os
import subprocess
import pandas as pd
import numpy as np
from pathlib import Path
import shutil

class CKAnalyzer:
    def __init__(self, clone_results_file="data/clone_results.json", 
                 ck_jar_path="tools/ck.jar", output_dir="data/metrics"):
        self.clone_results_file = clone_results_file
        self.ck_jar_path = Path(ck_jar_path)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        self.repositories = []
        self.analysis_results = {
            "successful": [],
            "failed": [],
            "skipped": []
        }
    
    def download_ck_tool(self):
        if self.ck_jar_path.exists():
            print(f"Ferramenta CK encontrada em {self.ck_jar_path}")
            return True
        
        print("Baixando ferramenta CK...")
        self.ck_jar_path.parent.mkdir(exist_ok=True)
        
        ck_url = "https://github.com/mauricioaniche/ck/releases/download/v0.7.1/ck-0.7.1-SNAPSHOT-jar-with-dependencies.jar"
        
        try:
            import requests
            
            response = requests.get(ck_url, stream=True)
            response.raise_for_status()
            
            with open(self.ck_jar_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"CK baixado com sucesso em {self.ck_jar_path}")
            return True
            
        except Exception as e:
            print(f"Erro ao baixar CK: {e}")
            print("Baixe manualmente o CK de: https://github.com/mauricioaniche/ck/releases")
            return False
    
    def load_clone_results(self):
        try:
            with open(self.clone_results_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.repositories = data.get("results", {}).get("successful", [])
            
            print(f"Carregados {len(self.repositories)} repositórios clonados de {self.clone_results_file}")
            return True
            
        except FileNotFoundError:
            print(f"Erro: Arquivo {self.clone_results_file} não encontrado.")
            print("Execute primeiro: python scripts/clone_repos.py")
            return False
        except json.JSONDecodeError as e:
            print(f"Erro ao decodificar JSON: {e}")
            return False
    
    def find_java_files(self, repo_path):
        java_files = []
        
        try:
            for java_file in repo_path.rglob("*.java"):
                java_files.append(java_file)
        except Exception as e:
            print(f"Erro ao buscar arquivos Java em {repo_path}: {e}")
        
        return java_files
    
    def run_ck_analysis(self, repo_path, repo_name):
        if not self.ck_jar_path.exists():
            print(f"Erro: Ferramenta CK não encontrada em {self.ck_jar_path}")
            return None
        
        output_file = self.output_dir / f"{repo_name.replace('/', '_')}_ck.csv"
        
        cmd = [
            "java", "-jar", str(self.ck_jar_path),
            str(repo_path),
            "true",
            "0",
            "false",
            str(output_file)
        ]
        
        try:
            print(f"Executando CK em {repo_name}...")
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=600
            )
            
            if result.returncode == 0 and output_file.exists():
                print(f"✓ CK executado com sucesso em {repo_name}")
                return str(output_file)
            else:
                print(f"✗ Erro ao executar CK em {repo_name}: {result.stderr}")
                return None
                
        except subprocess.TimeoutExpired:
            print(f"✗ Timeout ao executar CK em {repo_name}")
            return None
        except Exception as e:
            print(f"✗ Erro inesperado ao executar CK em {repo_name}: {e}")
            return None
    
    def analyze_ck_results(self, csv_file, repo_name):
        try:
            df = pd.read_csv(csv_file)
            
            if df.empty:
                return {
                    "repo": repo_name,
                    "total_classes": 0,
                    "cbo_median": 0,
                    "cbo_mean": 0,
                    "cbo_std": 0,
                    "dit_median": 0,
                    "dit_mean": 0,
                    "dit_std": 0,
                    "lcom_median": 0,
                    "lcom_mean": 0,
                    "lcom_std": 0,
                    "loc_total": 0,
                    "comments_loc": 0
                }
            
            metrics = {
                "repo": repo_name,
                "total_classes": len(df),
                "cbo_median": float(df['cbo'].median()) if 'cbo' in df.columns else 0,
                "cbo_mean": float(df['cbo'].mean()) if 'cbo' in df.columns else 0,
                "cbo_std": float(df['cbo'].std()) if 'cbo' in df.columns else 0,
                "dit_median": float(df['dit'].median()) if 'dit' in df.columns else 0,
                "dit_mean": float(df['dit'].mean()) if 'dit' in df.columns else 0,
                "dit_std": float(df['dit'].std()) if 'dit' in df.columns else 0,
                "lcom_median": float(df['lcom'].median()) if 'lcom' in df.columns else 0,
                "lcom_mean": float(df['lcom'].mean()) if 'lcom' in df.columns else 0,
                "lcom_std": float(df['lcom'].std()) if 'lcom' in df.columns else 0,
                "loc_total": int(df['loc'].sum()) if 'loc' in df.columns else 0,
                "comments_loc": int(df['cbo'].sum()) if 'cbo' in df.columns else 0
            }
            
            if 'rfc' in df.columns:
                metrics['rfc_median'] = float(df['rfc'].median())
                metrics['rfc_mean'] = float(df['rfc'].mean())
            
            if 'wmc' in df.columns:
                metrics['wmc_median'] = float(df['wmc'].median())
                metrics['wmc_mean'] = float(df['wmc'].mean())
            
            return metrics
            
        except Exception as e:
            print(f"Erro ao analisar resultados CK para {repo_name}: {e}")
            return {
                "repo": repo_name,
                "total_classes": 0,
                "cbo_median": 0, "cbo_mean": 0, "cbo_std": 0,
                "dit_median": 0, "dit_mean": 0, "dit_std": 0,
                "lcom_median": 0, "lcom_mean": 0, "lcom_std": 0,
                "loc_total": 0,
                "comments_loc": 0
            }
    
    def analyze_repository(self, repo_info):
        repo_name = repo_info["repo"]
        repo_path = Path(repo_info["path"])
        
        if not repo_path.exists():
            self.analysis_results["failed"].append({
                "repo": repo_name,
                "reason": "diretório não existe"
            })
            return {}
        
        java_files = self.find_java_files(repo_path)
        if not java_files:
            self.analysis_results["skipped"].append({
                "repo": repo_name,
                "reason": "nenhum arquivo Java encontrado"
            })
            return {}
        
        csv_file = self.run_ck_analysis(repo_path, repo_name)
        if not csv_file:
            self.analysis_results["failed"].append({
                "repo": repo_name,
                "reason": "falha na execução do CK"
            })
            return {}
        
        metrics = self.analyze_ck_results(csv_file, repo_name)
        
        metrics.update({
            "stars": repo_info["stars"],
            "java_files_count": len(java_files),
            "analysis_file": csv_file
        })
        
        self.analysis_results["successful"].append(metrics)
        return metrics
    
    def analyze_all_repositories(self, max_repos=None):
        if not self.repositories:
            print("Nenhum repositório carregado. Execute load_clone_results() primeiro.")
            return
        
        repos_to_analyze = self.repositories
        if max_repos:
            repos_to_analyze = repos_to_analyze[:max_repos]
        
        print(f"Analisando {len(repos_to_analyze)} repositórios...")
        
        for repo_info in repos_to_analyze:
            self.analyze_repository(repo_info)
    
    def save_analysis_results(self, filename="data/ck_analysis_results.json"):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        data = {
            "metadata": {
                "total_repositories": len(self.repositories),
                "successful_analyses": len(self.analysis_results["successful"]),
                "failed_analyses": len(self.analysis_results["failed"]),
                "skipped_analyses": len(self.analysis_results["skipped"]),
                "output_directory": str(self.output_dir)
            },
            "results": self.analysis_results
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"Resultados da análise salvos em {filename}")
    
    def create_summary_csv(self, filename="data/metrics_summary.csv"):
        if not self.analysis_results["successful"]:
            print("Nenhum resultado de análise disponível.")
            return
        
        df = pd.DataFrame(self.analysis_results["successful"])
        df.to_csv(filename, index=False)
        print(f"Resumo das métricas salvo em {filename}")
        
        return df
    
    def print_summary(self):
        total = len(self.repositories)
        successful = len(self.analysis_results["successful"])
        failed = len(self.analysis_results["failed"])
        skipped = len(self.analysis_results["skipped"])
        
        print("\n=== RESUMO DA ANÁLISE CK ===")
        print(f"Total de repositórios: {total}")
        print(f"Analisados com sucesso: {successful}")
        print(f"Falharam: {failed}")
        print(f"Pulados: {skipped}")
        print(f"Taxa de sucesso: {(successful/total)*100:.1f}%" if total > 0 else "N/A")
        
        if successful > 0:
            cbo_values = [r["cbo_mean"] for r in self.analysis_results["successful"] if r["cbo_mean"] > 0]
            dit_values = [r["dit_mean"] for r in self.analysis_results["successful"] if r["dit_mean"] > 0]
            lcom_values = [r["lcom_mean"] for r in self.analysis_results["successful"] if r["lcom_mean"] > 0]
            
            if cbo_values:
                print(f"\nMétricas de Qualidade (médias):")
                print(f"CBO - Média: {np.mean(cbo_values):.2f}, Mediana: {np.median(cbo_values):.2f}")
                print(f"DIT - Média: {np.mean(dit_values):.2f}, Mediana: {np.median(dit_values):.2f}")
                print(f"LCOM - Média: {np.mean(lcom_values):.2f}, Mediana: {np.median(lcom_values):.2f}")


def main():
    print("=== ANÁLISE CK DE REPOSITÓRIOS JAVA ===\n")
    
    analyzer = CKAnalyzer()
    
    if not analyzer.download_ck_tool():
        print("Não foi possível obter a ferramenta CK. Abortando.")
        return
    
    if not analyzer.load_clone_results():
        return
    
    print("Iniciando análise CK...")
    print("NOTA: Para teste, vamos analisar apenas os primeiros 5 repositórios.")
    print("Para analisar todos, modifique o parâmetro max_repos no código.")
    
    analyzer.analyze_all_repositories(max_repos=5)
    
    analyzer.save_analysis_results()
    
    df = analyzer.create_summary_csv()
    
    analyzer.print_summary()
    
    if df is not None and not df.empty:
        print(f"\nTop 3 repositórios por estrelas:")
        top_repos = df.nlargest(3, 'stars')[['repo', 'stars', 'cbo_mean', 'dit_mean', 'lcom_mean']]
        for _, row in top_repos.iterrows():
            print(f"  {row['repo']} - {row['stars']} estrelas (CBO: {row['cbo_mean']:.2f}, DIT: {row['dit_mean']:.2f}, LCOM: {row['lcom_mean']:.2f})")
    
    print("\n=== ANÁLISE CK CONCLUÍDA ===")
    print("Próximos passos:")
    print("1. Execute: python scripts/process_results.py")


if __name__ == "__main__":
    main()