#!/usr/bin/env python3

import json
import os
import subprocess
import time
import shutil
from pathlib import Path

class RepositoryCloner:
    def __init__(self, repos_file="data/repositories.json", clone_dir="repositories"):
        self.repos_file = repos_file
        self.clone_dir = Path(clone_dir)
        self.clone_dir.mkdir(exist_ok=True)
        
        self.repositories = []
        self.clone_results = {
            "successful": [],
            "failed": [],
            "skipped": []
        }
    
    def load_repositories(self):
        try:
            with open(self.repos_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.repositories = data.get("repositories", [])
            
            print(f"Carregados {len(self.repositories)} repositórios de {self.repos_file}")
            return True
            
        except FileNotFoundError:
            print(f"Erro: Arquivo {self.repos_file} não encontrado.")
            print("Execute primeiro: python scripts/collect_repos.py")
            return False
        except json.JSONDecodeError as e:
            print(f"Erro ao decodificar JSON: {e}")
            return False
    
    def is_repository_cloned(self, repo_name):
        repo_path = self.clone_dir / repo_name.replace("/", "_")
        return repo_path.exists() and (repo_path / ".git").exists()
    
    def clone_repository(self, repo_info, max_retries=3):
        repo_name = repo_info["full_name"]
        clone_url = repo_info["clone_url"]
        
        dir_name = repo_name.replace("/", "_")
        repo_path = self.clone_dir / dir_name
        
        if self.is_repository_cloned(repo_name):
            self.clone_results["skipped"].append({
                "repo": repo_name,
                "reason": "já existe"
            })
            return True
        
        cmd = [
            "git", "clone",
            "--depth", "1",
            "--single-branch",
            clone_url,
            str(repo_path)
        ]
        
        for attempt in range(max_retries):
            try:
                print(f"Clonando {repo_name} (tentativa {attempt + 1}/{max_retries})...")
                
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=300
                )
                
                if result.returncode == 0:
                    self.clone_results["successful"].append({
                        "repo": repo_name,
                        "path": str(repo_path),
                        "stars": repo_info["stars"]
                    })
                    print(f"✓ {repo_name} clonado com sucesso")
                    return True
                else:
                    print(f"✗ Erro ao clonar {repo_name}: {result.stderr}")
                    
            except subprocess.TimeoutExpired:
                print(f"✗ Timeout ao clonar {repo_name}")
            except Exception as e:
                print(f"✗ Erro inesperado ao clonar {repo_name}: {e}")
            
            if repo_path.exists():
                shutil.rmtree(repo_path, ignore_errors=True)
            
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
        
        self.clone_results["failed"].append({
            "repo": repo_name,
            "url": clone_url,
            "stars": repo_info["stars"]
        })
        return False
    
    def clone_all_repositories(self, max_repos=None, start_from=0):
        if not self.repositories:
            print("Nenhum repositório carregado. Execute load_repositories() primeiro.")
            return
        
        repos_to_clone = self.repositories[start_from:]
        if max_repos:
            repos_to_clone = repos_to_clone[:max_repos]
        
        print(f"Clonando {len(repos_to_clone)} repositórios...")
        print(f"Diretório de destino: {self.clone_dir}")
        
        for i, repo in enumerate(repos_to_clone):
            self.clone_repository(repo)
            
            if (i + 1) % 10 == 0:
                time.sleep(2)
            
            if (i + 1) % 50 == 0:
                print(f"\nPausa após {i + 1} clones...")
                time.sleep(10)
    
    def get_java_files_count(self, repo_path):
        try:
            result = subprocess.run(
                ["find", str(repo_path), "-name", "*.java", "-type", "f"],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                return len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0
            else:
                return 0
        except:
            return 0
    
    def validate_cloned_repositories(self):
        print("Validando repositórios clonados...")
        
        validation_stats = {
            "total_cloned": 0,
            "with_java_files": 0,
            "total_java_files": 0,
            "repositories_with_java": []
        }
        
        for success_info in self.clone_results["successful"]:
            repo_path = Path(success_info["path"])
            
            if repo_path.exists():
                validation_stats["total_cloned"] += 1
                
                java_files = self.get_java_files_count(repo_path)
                
                if java_files > 0:
                    validation_stats["with_java_files"] += 1
                    validation_stats["total_java_files"] += java_files
                    validation_stats["repositories_with_java"].append({
                        "repo": success_info["repo"],
                        "path": success_info["path"],
                        "java_files": java_files,
                        "stars": success_info["stars"]
                    })
        
        return validation_stats
    
    def save_clone_results(self, filename="data/clone_results.json"):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        data = {
            "metadata": {
                "clone_dir": str(self.clone_dir),
                "total_repositories": len(self.repositories),
                "successful_clones": len(self.clone_results["successful"]),
                "failed_clones": len(self.clone_results["failed"]),
                "skipped_clones": len(self.clone_results["skipped"])
            },
            "results": self.clone_results
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"Resultados do clone salvos em {filename}")
    
    def print_summary(self):
        total = len(self.repositories)
        successful = len(self.clone_results["successful"])
        failed = len(self.clone_results["failed"])
        skipped = len(self.clone_results["skipped"])
        
        print("\n=== RESUMO DO CLONE ===")
        print(f"Total de repositórios: {total}")
        print(f"Clonados com sucesso: {successful}")
        print(f"Falharam: {failed}")
        print(f"Pulados (já existiam): {skipped}")
        print(f"Taxa de sucesso: {(successful/total)*100:.1f}%" if total > 0 else "N/A")
        
        if failed > 0:
            print(f"\nRepositórios que falharam:")
            for fail_info in self.clone_results["failed"][:10]:
                print(f"  - {fail_info['repo']} ({fail_info['stars']} estrelas)")


def main():
    print("=== AUTOMAÇÃO DE CLONE DE REPOSITÓRIOS JAVA ===\n")
    
    cloner = RepositoryCloner()
    
    if not cloner.load_repositories():
        return
    
    print("Iniciando clone dos repositórios...")
    print("NOTA: Para teste, vamos clonar apenas os primeiros 10 repositórios.")
    print("Para clonar todos, modifique o parâmetro max_repos no código.")
    
    cloner.clone_all_repositories(max_repos=10)
    
    validation_stats = cloner.validate_cloned_repositories()
    
    cloner.save_clone_results()
    
    cloner.print_summary()
    
    print(f"\nRepositórios com arquivos Java: {validation_stats['with_java_files']}")
    print(f"Total de arquivos Java encontrados: {validation_stats['total_java_files']}")
    
    print("\n=== CLONE CONCLUÍDO ===")
    print("Próximos passos:")
    print("1. Execute: python scripts/run_ck_analysis.py")


if __name__ == "__main__":
    main()