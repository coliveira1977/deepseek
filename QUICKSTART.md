# 🚀 Início Rápido - DeepSeek Chat Local

## ⚡ Instalação em 3 Passos

### 1. **Instalar Dependências**
```bash
# Linux/Mac
./install.sh

# Windows
install.bat

# Manual
pip install -r requirements.txt
```

### 2. **Configurar API Key**
```bash
# Copie o arquivo de exemplo
cp env_example.txt .env

# Edite com sua API key
nano .env  # ou use seu editor preferido
```

**Conteúdo do .env:**
```bash
DEEPSEEK_API_KEY=sua_chave_real_aqui
```

### 3. **Executar Aplicação**
```bash
# Opção 1: Script automático
python run.py

# Opção 2: Direto
streamlit run app.py
```

## 🔑 Obter API Key

1. Acesse [DeepSeek Platform](https://platform.deepseek.com/)
2. Faça login/cadastro
3. Vá em "API Keys"
4. Crie uma nova chave

## 📱 Primeiro Uso

1. **Abra a aplicação** no navegador
2. **Configure sua API key** na barra lateral
3. **Teste a conexão** com o botão "Testar Conexão"
4. **Faça upload de um documento** na aba "Documentos"
5. **Analise o documento** ou **inicie um chat** na aba "Chat"

## 🧪 Testar Instalação

```bash
python test_setup.py
```

## 📁 Estrutura do Projeto

```
deepseek-chat-local/
├── app.py              # 🚀 Aplicação principal
├── run.py              # ⚡ Script de execução
├── install.sh          # 🔧 Instalador Linux/Mac
├── install.bat         # 🔧 Instalador Windows
├── test_setup.py       # 🧪 Teste de instalação
├── requirements.txt    # 📦 Dependências
└── README.md          # 📖 Documentação completa
```

## 🆘 Problemas Comuns

### ❌ "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### ❌ "API key inválida"
- Verifique se copiou a chave completa
- Confirme se não há espaços extras
- Teste a conexão na interface

### ❌ "Porta já em uso"
```bash
# Mude a porta no arquivo .streamlit/config.toml
port = 8502
```

## 🎯 Próximos Passos

- 📖 Leia o [README.md](README.md) completo
- 🔍 Explore as funcionalidades na interface
- 📄 Teste com diferentes tipos de documentos
- 💬 Experimente o chat com IA

---

**🎉 Pronto! Você tem um chat local com IA funcionando!**
