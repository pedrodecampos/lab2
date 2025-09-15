#!/usr/bin/env python3

import os
import sys
import subprocess
import json
from pathlib import Path
from datetime import datetime

def run_script(script_name, description):
    print(f"\n{'='*60}")
    print(f"EXECUTANDO: {description}")
    print(f"Script: {script_name}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run([sys.executable, script_name], 
                              capture_output=False, 
                              text=True, 
                              cwd=Path(__file__).parent)
        
        if result.returncode == 0:
            print(f"✅ {description} - CONCLUÍDO COM SUCESSO")
            return True
        else:
            print(f"❌ {description} - FALHOU (código: {result.returncode})")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao executar {script_name}: {e}")
        return False

def check_dependencies():
    print("Verificando dependências...")
    
    try:
        import requests
        import pandas
        import numpy
        import matplotlib
        import seaborn
        import scipy
        import tqdm
        print("✅ Todas as dependências Python estão disponíveis")
        return True
    except ImportError as e:
        print(f"❌ Dependência não encontrada: {e}")
        print("Execute: pip install -r requirements.txt")
        return False

def create_project_structure():
    directories = [
        "data",
        "data/metrics", 
        "data/plots",
        "tools",
        "repositories"
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
    
    print("✅ Estrutura de diretórios criada")

def main():
    print("🚀 LABORATÓRIO 2 - SPRINT 1: ANÁLISE DE QUALIDADE DE SISTEMAS JAVA")
    print(f"📅 Iniciado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📁 Diretório de trabalho: {Path.cwd()}")
    
    if not check_dependencies():
        print("\n❌ DEPENDÊNCIAS NÃO ATENDIDAS")
        print("Instale as dependências com: pip install -r requirements.txt")
        return False
    
    create_project_structure()
    
    scripts = [
        {
            "script": "scripts/collect_repos.py",
            "description": "Coleta dos top 1000 repositórios Java do GitHub"
        },
        {
            "script": "scripts/demo_single_repo.py", 
            "description": "Demonstração: Análise de um repositório (geração de CSV)"
        },
        {
            "script": "scripts/clone_repos.py",
            "description": "Clone dos repositórios coletados"
        },
        {
            "script": "scripts/run_ck_analysis.py",
            "description": "Análise CK dos repositórios clonados"
        },
        {
            "script": "scripts/process_results.py",
            "description": "Processamento e consolidação dos dados"
        }
    ]
    
    successful_steps = 0
    total_steps = len(scripts)
    
    for i, script_info in enumerate(scripts, 1):
        print(f"\n📋 PASSO {i}/{total_steps}")
        
        success = run_script(script_info["script"], script_info["description"])
        
        if success:
            successful_steps += 1
        else:
            print(f"\n⚠️  AVISO: {script_info['description']} falhou.")
            print("Continuando com os próximos passos...")
            
            if script_info["script"] == "scripts/collect_repos.py":
                print("❌ ERRO CRÍTICO: Não foi possível coletar repositórios.")
                print("Abortando execução.")
                return False
    
    print(f"\n{'='*60}")
    print("RESUMO DA EXECUÇÃO")
    print(f"{'='*60}")
    print(f"📊 Passos executados com sucesso: {successful_steps}/{total_steps}")
    print(f"📁 Diretórios criados:")
    
    data_dir = Path("data")
    if data_dir.exists():
        print(f"   📂 {data_dir.absolute()}")
        for file in data_dir.rglob("*"):
            if file.is_file():
                size = file.stat().st_size
                print(f"      📄 {file.name} ({size:,} bytes)")
    
    expected_files = [
        "data/repositories.json",
        "data/demo_repo_summary.csv", 
        "data/consolidated_data.csv",
        "data/final_report.json"
    ]
    
    print(f"\n✅ ARQUIVOS ESPERADOS:")
    for file_path in expected_files:
        if Path(file_path).exists():
            print(f"   ✅ {file_path}")
        else:
            print(f"   ❌ {file_path} (não encontrado)")
    
    if successful_steps >= 3:
        print(f"\n🎉 SPRINT 1 CONCLUÍDA COM SUCESSO!")
        print(f"📋 Próximos passos para a Sprint 2:")
        print(f"   1. Analise os resultados em data/final_report.json")
        print(f"   2. Execute análises adicionais conforme necessário")
        print(f"   3. Prepare apresentação dos resultados")
        return True
    else:
        print(f"\n⚠️  SPRINT 1 CONCLUÍDA COM PROBLEMAS")
        print(f"   Apenas {successful_steps}/{total_steps} passos foram executados com sucesso.")
        print(f"   Verifique os logs acima para identificar problemas.")
        return False

if __name__ == "__main__":
    success = main()
    exit_code = 0 if success else 1
    sys.exit(exit_code)