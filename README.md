# 🤖 DeepSeek Chat Local

Um chat local inteligente com análise de documentos usando a API do DeepSeek. Esta aplicação permite conversar com IA e analisar documentos em diversos formatos.

## ✨ Funcionalidades

- **💬 Chat Inteligente**: Conversa com IA usando a API do DeepSeek
- **📄 Análise de Documentos**: Suporte para PDF, DOC, DOCX, TXT e CSV
- **🔍 Processamento Inteligente**: Extração e análise automática de conteúdo
- **🌐 Interface Web**: Interface moderna e responsiva com Streamlit
- **🔐 Segurança**: Gerenciamento seguro de API keys
- **📊 Histórico**: Manutenção de histórico de conversas

## 🚀 Instalação

### Pré-requisitos

- Python 3.8+
- API key do DeepSeek

### Passos de Instalação

1. **Clone o repositório**
```bash
git clone <url-do-repositorio>
cd deepseek-chat-local
```

2. **Crie um ambiente virtual**
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate  # Windows
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

4. **Configure sua API key**
   - Copie o arquivo `env_example.txt` para `.env`
   - Edite o arquivo `.env` e adicione sua API key do DeepSeek
   - Ou configure diretamente na interface da aplicação

## 🔑 Configuração da API

### Obter API Key

1. Acesse [DeepSeek Platform](https://platform.deepseek.com/)
2. Crie uma conta ou faça login
3. Vá para a seção de API Keys
4. Crie uma nova chave de API

### Configuração

**Opção 1: Arquivo .env (Recomendado)**
```bash
cp env_example.txt .env
# Edite o arquivo .env com sua API key
```

**Opção 2: Interface da Aplicação**
- Execute a aplicação
- Configure a API key na barra lateral
- Teste a conexão

## 🎯 Como Usar

### 1. Iniciar a Aplicação
```bash
streamlit run app.py
```

### 2. Configurar API
- Abra a aplicação no navegador
- Insira sua API key na barra lateral
- Clique em "Testar Conexão"

### 3. Upload de Documentos
- Vá para a aba "Documentos"
- Arraste ou selecione um arquivo
- Clique em "Processar Documento"
- Aguarde o processamento

### 4. Análise de Documentos
- Após o upload, clique em "Analisar"
- A IA analisará o conteúdo automaticamente
- Visualize insights e recomendações

### 5. Chat com IA
- Use a aba "Chat" para conversas
- Faça perguntas sobre os documentos
- A IA manterá contexto das conversas

## 📁 Formatos Suportados

| Formato | Extensão | Descrição |
|---------|----------|-----------|
| **PDF** | `.pdf` | Documentos PDF com extração de texto |
| **Word** | `.doc`, `.docx` | Documentos do Microsoft Word |
| **Texto** | `.txt` | Arquivos de texto simples |
| **CSV** | `.csv` | Dados tabulares com análise estruturada |

## 🏗️ Arquitetura do Projeto

```
deepseek-chat-local/
├── app.py                 # Aplicação principal Streamlit
├── chat_manager.py        # Gerenciador de chat e documentos
├── deepseek_client.py     # Cliente da API DeepSeek
├── document_processor.py  # Processamento de documentos
├── config.py             # Configurações e constantes
├── requirements.txt      # Dependências Python
├── env_example.txt      # Exemplo de variáveis de ambiente
├── README.md            # Esta documentação
└── uploads/             # Pasta para documentos carregados
```

## 🔧 Configurações Avançadas

### Variáveis de Ambiente

```bash
# API DeepSeek
DEEPSEEK_API_KEY=sua_chave_aqui
DEEPSEEK_BASE_URL=https://api.deepseek.com

# Configurações do Modelo
MAX_TOKENS=4096
TEMPERATURE=0.7

# Configurações de Arquivo
MAX_FILE_SIZE=10485760  # 10MB
```

### Personalização

Edite o arquivo `config.py` para ajustar:
- Limites de tokens
- Temperatura do modelo
- Tamanho máximo de arquivo
- Extensões permitidas

## 🚨 Solução de Problemas

### Erro de Conexão
- Verifique se a API key está correta
- Confirme se há conexão com a internet
- Teste a conexão na interface

### Erro no Upload
- Verifique o formato do arquivo
- Confirme o tamanho (máximo 10MB)
- Verifique permissões da pasta uploads

### Erro de Processamento
- Verifique se o arquivo não está corrompido
- Confirme se o formato é suportado
- Verifique os logs da aplicação

## 📊 Recursos da API DeepSeek

Esta aplicação utiliza a API oficial do DeepSeek para:
- **Chat Completions**: Conversas em tempo real
- **Análise de Texto**: Processamento inteligente de documentos
- **Contexto**: Manutenção de histórico de conversas
- **Modelos Avançados**: Acesso aos melhores modelos de IA

## 🤝 Contribuição

Contribuições são bem-vindas! Para contribuir:

1. Faça um fork do projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para detalhes.

## 🆘 Suporte

Para suporte:
- Abra uma issue no GitHub
- Consulte a documentação da API DeepSeek
- Verifique os logs da aplicação

## 🔮 Roadmap

- [ ] Exportação de histórico
- [ ] Salvamento de sessões
- [ ] Suporte a mais formatos
- [ ] Análise em lote
- [ ] Integração com bancos de dados
- [ ] API REST para integração

---

**Desenvolvido com ❤️ usando Python e DeepSeek AI**
