#!/usr/bin/env python3
"""
Script de execução para o DeepSeek Chat Local
"""

import os
import sys
import subprocess
import logging

def check_dependencies():
    """Verifica se as dependências estão instaladas"""
    try:
        import streamlit
        import requests
        import PyPDF2
        import pandas
        import docx
        return True
    except ImportError as e:
        print(f"❌ Dependência não encontrada: {e}")
        return False

def install_dependencies():
    """Instala as dependências necessárias"""
    print("📦 Instalando dependências...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependências instaladas com sucesso!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao instalar dependências: {e}")
        return False

def create_env_file():
    """Cria arquivo .env se não existir"""
    if not os.path.exists(".env"):
        print("🔧 Criando arquivo .env...")
        try:
            with open("env_example.txt", "r") as example:
                content = example.read()
            
            with open(".env", "w") as env_file:
                env_file.write(content)
            
            print("✅ Arquivo .env criado!")
            print("⚠️  IMPORTANTE: Edite o arquivo .env e adicione sua API key do DeepSeek")
        except Exception as e:
            print(f"❌ Erro ao criar arquivo .env: {e}")

def main():
    """Função principal"""
    print("🤖 DeepSeek Chat Local")
    print("=" * 40)
    
    # Verifica se estamos no diretório correto
    if not os.path.exists("app.py"):
        print("❌ Erro: Execute este script no diretório do projeto")
        sys.exit(1)
    
    # Verifica dependências
    if not check_dependencies():
        print("📦 Dependências não encontradas. Instalando...")
        if not install_dependencies():
            print("❌ Falha ao instalar dependências")
            sys.exit(1)
    
    # Cria arquivo .env se necessário
    create_env_file()
    
    # Verifica se a API key está configurada
    if not os.path.exists(".env") or "DEEPSEEK_API_KEY=sua_api_key_aqui" in open(".env").read():
        print("⚠️  ATENÇÃO: Configure sua API key do DeepSeek no arquivo .env")
        print("   Ou configure diretamente na interface da aplicação")
    
    print("\n🚀 Iniciando aplicação...")
    print("📱 A aplicação será aberta no seu navegador")
    print("🔑 Configure sua API key na barra lateral")
    print("\n" + "=" * 40)
    
    try:
        # Inicia a aplicação Streamlit
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])
    except KeyboardInterrupt:
        print("\n👋 Aplicação encerrada pelo usuário")
    except Exception as e:
        print(f"❌ Erro ao iniciar aplicação: {e}")

if __name__ == "__main__":
    main()
