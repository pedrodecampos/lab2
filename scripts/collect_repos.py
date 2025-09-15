#!/usr/bin/env python3

import requests
import json
import time
import os
from datetime import datetime

class GitHubRepositoryCollector:
    def __init__(self, github_token=None):
        self.base_url = "https://api.github.com"
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "Java-Repo-Analyzer/1.0"
        }
        
        if github_token:
            self.headers["Authorization"] = f"token {github_token}"
        
        self.repositories = []
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def search_repositories(self, query, sort="stars", per_page=100):
        url = f"{self.base_url}/search/repositories"
        params = {
            "q": query,
            "sort": sort,
            "per_page": per_page,
            "page": 1
        }
        
        all_repos = []
        page = 1
        
        while len(all_repos) < 1000:
            params["page"] = page
            print(f"Buscando página {page}...")
            
            try:
                response = self.session.get(url, params=params)
                response.raise_for_status()
                
                data = response.json()
                repos = data.get("items", [])
                
                if not repos:
                    break
                
                for repo in repos:
                    repo_info = self.extract_repository_info(repo)
                    all_repos.append(repo_info)
                    
                    if len(all_repos) >= 1000:
                        break
                
                print(f"Coletados {len(all_repos)} repositórios até agora...")
                
                if "X-RateLimit-Remaining" in response.headers:
                    remaining = int(response.headers["X-RateLimit-Remaining"])
                    if remaining <= 1:
                        reset_time = int(response.headers["X-RateLimit-Reset"])
                        wait_time = reset_time - time.time() + 10
                        print(f"Rate limit atingido. Aguardando {wait_time:.0f} segundos...")
                        time.sleep(wait_time)
                
                page += 1
                time.sleep(1)
                
            except requests.exceptions.RequestException as e:
                print(f"Erro na requisição: {e}")
                time.sleep(5)
                continue
            except Exception as e:
                print(f"Erro inesperado: {e}")
                time.sleep(5)
                continue
        
        return all_repos[:1000]
    
    def extract_repository_info(self, repo_data):
        created_at = datetime.strptime(repo_data["created_at"], "%Y-%m-%dT%H:%M:%SZ")
        age_years = (datetime.now() - created_at).days / 365.25
        
        repo_info = {
            "id": repo_data["id"],
            "name": repo_data["name"],
            "full_name": repo_data["full_name"],
            "owner": repo_data["owner"]["login"],
            "description": repo_data.get("description", ""),
            "html_url": repo_data["html_url"],
            "clone_url": repo_data["clone_url"],
            "ssh_url": repo_data["ssh_url"],
            "stars": repo_data["stargazers_count"],
            "forks": repo_data["forks_count"],
            "watchers": repo_data["watchers_count"],
            "open_issues": repo_data["open_issues_count"],
            "size_kb": repo_data["size"],
            "language": repo_data.get("language", "Java"),
            "created_at": repo_data["created_at"],
            "updated_at": repo_data["updated_at"],
            "pushed_at": repo_data["pushed_at"],
            "age_years": round(age_years, 2),
            "archived": repo_data["archived"],
            "disabled": repo_data["disabled"],
            "fork": repo_data["fork"],
            "private": repo_data["private"],
            "has_issues": repo_data["has_issues"],
            "has_projects": repo_data["has_projects"],
            "has_wiki": repo_data["has_wiki"],
            "has_pages": repo_data["has_pages"],
            "has_downloads": repo_data["has_downloads"],
            "cbo_median": None,
            "cbo_mean": None,
            "cbo_std": None,
            "dit_median": None,
            "dit_mean": None,
            "dit_std": None,
            "lcom_median": None,
            "lcom_mean": None,
            "lcom_std": None,
            "loc": None,
            "comments_loc": None,
            "releases_count": None
        }
        
        return repo_info
    
    def get_releases_count(self, owner, repo_name):
        url = f"{self.base_url}/repos/{owner}/{repo_name}/releases"
        
        try:
            response = self.session.get(url, params={"per_page": 100})
            response.raise_for_status()
            
            releases = response.json()
            return len(releases)
            
        except Exception as e:
            print(f"Erro ao obter releases para {owner}/{repo_name}: {e}")
            return 0
    
    def collect_top_java_repositories(self, max_repos=1000):
        print("Iniciando coleta dos repositórios Java mais populares...")
        
        query = "language:java stars:>100 sort:stars"
        repositories = self.search_repositories(query, sort="stars")
        
        print(f"Coletados {len(repositories)} repositórios iniciais")
        
        print("Obtendo informações adicionais...")
        for i, repo in enumerate(repositories[:100]):
            if i % 10 == 0:
                print(f"Processando repositório {i+1}/100...")
            
            releases_count = self.get_releases_count(repo["owner"], repo["name"])
            repo["releases_count"] = releases_count
            
            time.sleep(0.5)
        
        self.repositories = repositories
        return repositories
    
    def save_to_json(self, filename="data/repositories.json"):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        data = {
            "metadata": {
                "collected_at": datetime.now().isoformat(),
                "total_repositories": len(self.repositories),
                "query": "language:java stars:>100 sort:stars"
            },
            "repositories": self.repositories
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"Dados salvos em {filename}")
    
    def print_summary(self):
        if not self.repositories:
            print("Nenhum repositório coletado ainda.")
            return
        
        print("\n=== RESUMO DA COLETA ===")
        print(f"Total de repositórios: {len(self.repositories)}")
        
        stars = [r["stars"] for r in self.repositories]
        forks = [r["forks"] for r in self.repositories]
        ages = [r["age_years"] for r in self.repositories]
        
        print(f"Estrelas - Média: {sum(stars)/len(stars):.0f}, Mediana: {sorted(stars)[len(stars)//2]:.0f}")
        print(f"Forks - Média: {sum(forks)/len(forks):.0f}, Mediana: {sorted(forks)[len(forks)//2]:.0f}")
        print(f"Idade - Média: {sum(ages)/len(ages):.2f} anos, Mediana: {sorted(ages)[len(ages)//2]:.2f} anos")
        
        print("\n=== TOP 5 REPOSITÓRIOS ===")
        top_5 = sorted(self.repositories, key=lambda x: x["stars"], reverse=True)[:5]
        for i, repo in enumerate(top_5, 1):
            print(f"{i}. {repo['full_name']} - {repo['stars']} estrelas")


def main():
    print("=== COLETOR DE REPOSITÓRIOS JAVA - TOP 1000 ===\n")
    
    github_token = os.getenv("GITHUB_TOKEN")
    if not github_token:
        print("AVISO: Token GitHub não encontrado. Usando API sem autenticação.")
        print("Para melhor performance, defina a variável GITHUB_TOKEN.")
        print("Exemplo: export GITHUB_TOKEN=seu_token_aqui\n")
    
    collector = GitHubRepositoryCollector(github_token)
    repositories = collector.collect_top_java_repositories()
    collector.save_to_json()
    collector.print_summary()
    
    print("\n=== COLETA CONCLUÍDA ===")
    print("Próximos passos:")
    print("1. Execute: python scripts/clone_repos.py")
    print("2. Execute: python scripts/run_ck_analysis.py")


if __name__ == "__main__":
    main()