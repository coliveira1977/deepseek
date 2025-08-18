#!/usr/bin/env python3
"""
Script de teste para verificar a instalação do DeepSeek Chat Local
"""

import sys
import importlib

def test_imports():
    """Testa se todas as dependências podem ser importadas"""
    print("🧪 Testando importações...")
    
    required_modules = [
        'streamlit',
        'PyPDF2', 
        'pandas',
        'docx',
        'requests'
    ]
    
    failed_imports = []
    
    for module in required_modules:
        try:
            importlib.import_module(module)
            print(f"   ✅ {module}")
        except ImportError as e:
            print(f"   ❌ {module}: {e}")
            failed_imports.append(module)
    
    if failed_imports:
        print(f"\n❌ Falharam {len(failed_imports)} importações:")
        for module in failed_imports:
            print(f"   - {module}")
        return False
    
    print("\n✅ Todas as importações funcionaram!")
    return True

def test_local_modules():
    """Testa se os módulos locais podem ser importados"""
    print("\n🔧 Testando módulos locais...")
    
    local_modules = [
        'config',
        'document_processor',
        'deepseek_client',
        'chat_manager'
    ]
    
    failed_imports = []
    
    for module in local_modules:
        try:
            importlib.import_module(module)
            print(f"   ✅ {module}")
        except ImportError as e:
            print(f"   ❌ {module}: {e}")
            failed_imports.append(module)
    
    if failed_imports:
        print(f"\n❌ Falharam {len(failed_imports)} módulos locais:")
        for module in failed_imports:
            print(f"   - {module}")
        return False
    
    print("\n✅ Todos os módulos locais funcionaram!")
    return True

def test_config():
    """Testa se a configuração está acessível"""
    print("\n⚙️ Testando configuração...")
    
    try:
        import config
        
        print(f"   ✅ Configuração carregada")
        print(f"   📍 Pasta de uploads: {config.UPLOAD_FOLDER}")
        print(f"   🔑 API Key configurada: {'Sim' if config.DEEPSEEK_API_KEY else 'Não'}")
        print(f"   🌐 URL base: {config.DEEPSEEK_BASE_URL}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Erro na configuração: {e}")
        return False

def main():
    """Função principal de teste"""
    print("🤖 Teste de Instalação - DeepSeek Chat Local")
    print("=" * 50)
    
    # Testa importações de dependências
    deps_ok = test_imports()
    
    # Testa módulos locais
    modules_ok = test_local_modules()
    
    # Testa configuração
    config_ok = test_config()
    
    # Resumo
    print("\n" + "=" * 50)
    print("📊 RESUMO DOS TESTES:")
    print(f"   Dependências: {'✅ OK' if deps_ok else '❌ FALHOU'}")
    print(f"   Módulos locais: {'✅ OK' if modules_ok else '❌ FALHOU'}")
    print(f"   Configuração: {'✅ OK' if config_ok else '❌ FALHOU'}")
    
    if deps_ok and modules_ok and config_ok:
        print("\n🎉 TODOS OS TESTES PASSARAM!")
        print("\n🚀 Para iniciar a aplicação:")
        print("   python run.py")
        print("   # ou")
        print("   streamlit run app.py")
    else:
        print("\n❌ ALGUNS TESTES FALHARAM!")
        print("\n🔧 Para resolver:")
        print("   # Linux/Mac:")
        print("   ./install.sh")
        print("   # Windows:")
        print("   install.bat")
        print("   # Manual:")
        print("   pip install -r requirements.txt")

if __name__ == "__main__":
    main()
