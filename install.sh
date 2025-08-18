#!/bin/bash

echo "🤖 DeepSeek Chat Local - Instalador"
echo "====================================="

# Verifica se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado. Por favor, instale Python 3.8+ primeiro."
    exit 1
fi

# Verifica versão do Python
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python $python_version encontrado. Python $required_version+ é necessário."
    exit 1
fi

echo "✅ Python $python_version encontrado"

# Cria ambiente virtual
echo "🔧 Criando ambiente virtual..."
python3 -m venv .venv

# Ativa ambiente virtual
echo "🔌 Ativando ambiente virtual..."
source .venv/bin/activate

# Atualiza pip
echo "📦 Atualizando pip..."
pip install --upgrade pip

# Instala dependências
echo "📚 Instalando dependências..."
pip install -r requirements.txt

# Cria arquivo .env se não existir
if [ ! -f .env ]; then
    echo "🔧 Criando arquivo .env..."
    cp env_example.txt .env
    echo "⚠️  IMPORTANTE: Edite o arquivo .env e adicione sua API key do DeepSeek"
fi

# Cria pasta uploads
mkdir -p uploads

echo ""
echo "✅ Instalação concluída!"
echo ""
echo "🚀 Para iniciar a aplicação:"
echo "   source .venv/bin/activate"
echo "   python run.py"
echo ""
echo "🔑 Configure sua API key do DeepSeek no arquivo .env"
echo "   ou diretamente na interface da aplicação"
echo ""
echo "📖 Consulte o README.md para mais informações"
