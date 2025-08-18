@echo off
chcp 65001 >nul

echo 🤖 DeepSeek Chat Local - Instalador
echo =====================================

REM Verifica se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python não encontrado. Por favor, instale Python 3.8+ primeiro.
    pause
    exit /b 1
)

echo ✅ Python encontrado

REM Cria ambiente virtual
echo 🔧 Criando ambiente virtual...
python -m venv .venv

REM Ativa ambiente virtual
echo 🔌 Ativando ambiente virtual...
call .venv\Scripts\activate.bat

REM Atualiza pip
echo 📦 Atualizando pip...
python -m pip install --upgrade pip

REM Instala dependências
echo 📚 Instalando dependências...
pip install -r requirements.txt

REM Cria arquivo .env se não existir
if not exist .env (
    echo 🔧 Criando arquivo .env...
    copy env_example.txt .env
    echo ⚠️  IMPORTANTE: Edite o arquivo .env e adicione sua API key do DeepSeek
)

REM Cria pasta uploads
if not exist uploads mkdir uploads

echo.
echo ✅ Instalação concluída!
echo.
echo 🚀 Para iniciar a aplicação:
echo    .venv\Scripts\activate.bat
echo    python run.py
echo.
echo 🔑 Configure sua API key do DeepSeek no arquivo .env
echo    ou diretamente na interface da aplicação
echo.
echo 📖 Consulte o README.md para mais informações
pause
