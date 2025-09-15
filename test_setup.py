#!/usr/bin/env python3

import sys
import subprocess
from pathlib import Path

def test_python_version():
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 8:
        print("✅ Versão do Python adequada")
        return True
    else:
        print("❌ Python 3.8+ é necessário")
        return False

def test_dependencies():
    required_packages = [
        'requests', 'pandas', 'numpy', 
        'matplotlib', 'seaborn', 'scipy', 'tqdm'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package}")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n❌ Pacotes não encontrados: {', '.join(missing_packages)}")
        print("Execute: pip install -r requirements.txt")
        return False
    else:
        print("✅ Todas as dependências estão instaladas")
        return True

def test_git():
    try:
        result = subprocess.run(['git', '--version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Git disponível: {result.stdout.strip()}")
            return True
        else:
            print("❌ Git não está funcionando")
            return False
    except FileNotFoundError:
        print("❌ Git não encontrado no sistema")
        return False

def test_java():
    try:
        result = subprocess.run(['java', '-version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Java disponível")
            return True
        else:
            print("❌ Java não está funcionando")
            return False
    except FileNotFoundError:
        print("❌ Java não encontrado no sistema")
        print("   Java é necessário para executar a ferramenta CK")
        return False

def test_project_structure():
    required_files = [
        'requirements.txt',
        'README.md',
        'scripts/collect_repos.py',
        'scripts/clone_repos.py',
        'scripts/run_ck_analysis.py',
        'scripts/process_results.py',
        'scripts/demo_single_repo.py',
        'run_sprint1.py'
    ]
    
    missing_files = []
    
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path}")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n❌ Arquivos não encontrados: {', '.join(missing_files)}")
        return False
    else:
        print("✅ Estrutura do projeto está correta")
        return True

def main():
    print("🧪 TESTE DE CONFIGURAÇÃO DO AMBIENTE")
    print("="*50)
    
    tests = [
        ("Python Version", test_python_version),
        ("Dependencies", test_dependencies),
        ("Git", test_git),
        ("Java", test_java),
        ("Project Structure", test_project_structure)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Testando {test_name}...")
        if test_func():
            passed += 1
    
    print(f"\n{'='*50}")
    print(f"RESULTADO: {passed}/{total} testes passaram")
    
    if passed == total:
        print("🎉 Ambiente configurado corretamente!")
        print("   Você pode executar: python run_sprint1.py")
        return True
    else:
        print("⚠️  Alguns problemas foram encontrados.")
        print("   Corrija os problemas antes de executar a Sprint 1.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)