#!/usr/bin/env python3

import os
import sys
import subprocess
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

def check_sprint1_completed():
    required_files = [
        "data/consolidated_data.csv",
        "data/repositories.json"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Arquivos da Sprint 1 não encontrados: {', '.join(missing_files)}")
        print("Execute primeiro: python run_sprint1.py")
        return False
    
    print("✅ Sprint 1 completada - arquivos necessários encontrados")
    return True

def check_dependencies():
    print("Verificando dependências...")
    
    try:
        import pandas
        import numpy
        import matplotlib
        import seaborn
        import scipy
        print("✅ Todas as dependências Python estão disponíveis")
        return True
    except ImportError as e:
        print(f"❌ Dependência não encontrada: {e}")
        print("Execute: pip install -r requirements.txt")
        return False

def create_sprint2_structure():
    directories = [
        "data/plots",
        "data/reports"
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
    
    print("✅ Estrutura da Sprint 2 criada")

def main():
    print("🚀 LABORATÓRIO 2 - SPRINT 2: ANÁLISE E VISUALIZAÇÃO DE DADOS")
    print(f"📅 Iniciado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📁 Diretório de trabalho: {Path.cwd()}")
    
    # Verificar se Sprint 1 foi completada
    if not check_sprint1_completed():
        return False
    
    # Verificar dependências
    if not check_dependencies():
        print("\n❌ DEPENDÊNCIAS NÃO ATENDIDAS")
        print("Instale as dependências com: pip install -r requirements.txt")
        return False
    
    # Criar estrutura
    create_sprint2_structure()
    
    # Lista de scripts da Sprint 2
    scripts = [
        {
            "script": "scripts/advanced_analysis.py",
            "description": "Análise estatística avançada e testes de correlação"
        },
        {
            "script": "scripts/create_visualizations.py",
            "description": "Criação de visualizações detalhadas dos dados"
        },
        {
            "script": "scripts/generate_final_report.py",
            "description": "Geração do relatório final completo"
        }
    ]
    
    # Executar scripts em sequência
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
    
    # Resumo final
    print(f"\n{'='*60}")
    print("RESUMO DA EXECUÇÃO - SPRINT 2")
    print(f"{'='*60}")
    print(f"📊 Passos executados com sucesso: {successful_steps}/{total_steps}")
    
    # Verificar arquivos gerados
    expected_files = [
        "data/advanced_analysis_results.json",
        "data/relatorio_final_completo.json",
        "data/relatorio_final.md"
    ]
    
    print(f"\n✅ ARQUIVOS ESPERADOS:")
    for file_path in expected_files:
        if Path(file_path).exists():
            print(f"   ✅ {file_path}")
        else:
            print(f"   ❌ {file_path} (não encontrado)")
    
    # Verificar visualizações
    plots_dir = Path("data/plots")
    if plots_dir.exists():
        plot_files = list(plots_dir.glob("*.png"))
        print(f"\n📊 VISUALIZAÇÕES CRIADAS: {len(plot_files)}")
        for file in sorted(plot_files):
            print(f"   • {file.name}")
    
    if successful_steps >= 2:  # Pelo menos análise e relatório
        print(f"\n🎉 SPRINT 2 CONCLUÍDA COM SUCESSO!")
        print(f"📋 Entregáveis gerados:")
        print(f"   • Análise estatística avançada")
        print(f"   • Visualizações dos dados")
        print(f"   • Relatório final completo")
        print(f"   • Material para apresentação")
        return True
    else:
        print(f"\n⚠️  SPRINT 2 CONCLUÍDA COM PROBLEMAS")
        print(f"   Apenas {successful_steps}/{total_steps} passos foram executados com sucesso.")
        print(f"   Verifique os logs acima para identificar problemas.")
        return False

if __name__ == "__main__":
    success = main()
    exit_code = 0 if success else 1
    sys.exit(exit_code)

