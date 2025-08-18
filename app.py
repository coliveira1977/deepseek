import streamlit as st
import os
import tempfile
from datetime import datetime
import logging
from chat_manager import ChatManager
from config import DEEPSEEK_API_KEY

# Configuração da página
st.set_page_config(
    page_title="DeepSeek Chat Local",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def initialize_session_state():
    """Inicializa variáveis de estado da sessão"""
    if 'chat_manager' not in st.session_state:
        st.session_state.chat_manager = None
    if 'api_key' not in st.session_state:
        st.session_state.api_key = ""
    if 'connection_tested' not in st.session_state:
        st.session_state.connection_tested = False

def main():
    """Função principal da aplicação"""
    initialize_session_state()
    
    # Sidebar para configurações
    with st.sidebar:
        st.title("🤖 DeepSeek Chat")
        st.markdown("---")
        
        # Configuração da API
        st.subheader("🔑 Configuração da API")
        
        # Tenta usar API key do arquivo de configuração primeiro
        if not st.session_state.api_key and DEEPSEEK_API_KEY:
            st.session_state.api_key = DEEPSEEK_API_KEY
        
        api_key = st.text_input(
            "API Key DeepSeek",
            value=st.session_state.api_key,
            type="password",
            help="Insira sua chave da API do DeepSeek"
        )
        
        if api_key != st.session_state.api_key:
            st.session_state.api_key = api_key
            st.session_state.connection_tested = False
            st.session_state.chat_manager = None
        
        # Botão para testar conexão
        if st.button("🧪 Testar Conexão", type="primary"):
            if api_key:
                with st.spinner("Testando conexão..."):
                    try:
                        temp_manager = ChatManager(api_key)
                        if temp_manager.test_connection():
                            st.success("✅ Conexão estabelecida!")
                            st.session_state.connection_tested = True
                            st.session_state.chat_manager = temp_manager
                        else:
                            st.error("❌ Falha na conexão. Verifique sua API key.")
                    except Exception as e:
                        st.error(f"❌ Erro: {str(e)}")
            else:
                st.warning("⚠️ Insira uma API key primeiro")
        
        # Status da conexão
        if st.session_state.connection_tested:
            st.success("🟢 Conectado")
        else:
            st.warning("🟡 Não conectado")
        
        st.markdown("---")
        
        # Informações sobre formatos suportados
        st.subheader("📁 Formatos Suportados")
        st.markdown("""
        - **PDF** (.pdf)
        - **Word** (.doc, .docx)
        - **Texto** (.txt)
        - **CSV** (.csv)
        """)
        
        # Botões de controle
        st.markdown("---")
        if st.button("🗑️ Limpar Chat", type="secondary"):
            if st.session_state.chat_manager:
                st.session_state.chat_manager.clear_chat_history()
                st.rerun()
        
        if st.button("🔄 Reiniciar Sessão", type="secondary"):
            st.session_state.chat_manager = None
            st.session_state.connection_tested = False
            st.rerun()
    
    # Área principal
    if not st.session_state.api_key:
        st.error("⚠️ Por favor, configure sua API key do DeepSeek na barra lateral.")
        st.info("💡 Você pode obter uma API key em: https://platform.deepseek.com/")
        return
    
    if not st.session_state.connection_tested:
        st.warning("⚠️ Por favor, teste a conexão com a API antes de continuar.")
        return
    
    # Inicializa chat manager se necessário
    if not st.session_state.chat_manager:
        try:
            st.session_state.chat_manager = ChatManager(st.session_state.api_key)
        except Exception as e:
            st.error(f"❌ Erro ao inicializar chat: {str(e)}")
            return
    
    chat_manager = st.session_state.chat_manager
    
    # Header principal
    st.title("🤖 DeepSeek Chat Local")
    st.markdown("Chat inteligente com análise de documentos usando a API do DeepSeek")
    
    # Tabs principais
    tab1, tab2, tab3 = st.tabs(["💬 Chat", "📄 Documentos", "⚙️ Configurações"])
    
    with tab1:
        # Área de chat
        st.subheader("💬 Conversa com IA")
        
        # Exibe histórico do chat
        chat_history = chat_manager.get_chat_history()
        
        # Container para mensagens
        chat_container = st.container()
        
        with chat_container:
            for message in chat_history:
                if message["role"] == "user":
                    with st.chat_message("user"):
                        st.write(message["content"])
                        if message.get("document_info"):
                            st.info(f"📎 Referência ao documento: {message['document_info'].get('document', 'N/A')}")
                elif message["role"] == "assistant":
                    with st.chat_message("assistant"):
                        st.markdown(message["content"])
                elif message["role"] == "system":
                    with st.chat_message("system"):
                        st.info(message["content"])
        
        # Área de input
        st.markdown("---")
        user_input = st.chat_input("Digite sua mensagem aqui...")
        
        if user_input:
            with st.spinner("🤔 Processando..."):
                response = chat_manager.chat_with_ai(user_input)
                st.rerun()
    
    with tab2:
        # Área de documentos
        st.subheader("📄 Gerenciamento de Documentos")
        
        # Upload de arquivo
        st.markdown("### 📤 Upload de Documento")
        uploaded_file = st.file_uploader(
            "Escolha um arquivo para análise",
            type=['pdf', 'doc', 'docx', 'txt', 'csv'],
            help="Arraste um arquivo ou clique para selecionar"
        )
        
        if uploaded_file is not None:
            if st.button("📥 Processar Documento", type="primary"):
                with st.spinner("Processando documento..."):
                    result = chat_manager.upload_document(uploaded_file)
                    
                    if "error" in result:
                        st.error(f"❌ {result['error']}")
                    else:
                        st.success("✅ Documento processado com sucesso!")
                        st.markdown(result["summary"])
                        st.rerun()
        
        # Lista de documentos carregados
        st.markdown("### 📁 Documentos Carregados")
        if chat_manager.uploaded_documents:
            for filename, doc_info in chat_manager.uploaded_documents.items():
                with st.expander(f"📄 {filename}"):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.markdown(f"**Tipo:** {doc_info['extension'].upper()}")
                        st.markdown(f"**Tamanho:** {doc_info['size'] / 1024:.1f} KB")
                        st.markdown(f"**Palavras:** {doc_info['word_count']}")
                        st.markdown(f"**Carregado:** {doc_info['upload_time'][:19]}")
                    
                    with col2:
                        if st.button(f"🔍 Analisar", key=f"analyze_{filename}"):
                            with st.spinner("Analisando documento..."):
                                analysis = chat_manager.analyze_document(filename)
                                st.markdown("### 📊 Análise do Documento")
                                st.markdown(analysis)
                                st.rerun()
        else:
            st.info("📁 Nenhum documento carregado ainda.")
    
    with tab3:
        # Área de configurações
        st.subheader("⚙️ Configurações e Status")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🔗 Status da API")
            if chat_manager.test_connection():
                st.success("✅ API DeepSeek funcionando")
            else:
                st.error("❌ Problema com a API")
            
            st.markdown("### 📊 Estatísticas da Sessão")
            st.metric("Mensagens", len(chat_manager.get_chat_history()))
            st.metric("Documentos", len(chat_manager.uploaded_documents))
        
        with col2:
            st.markdown("### 🗂️ Informações do Sistema")
            st.info(f"**Sessão:** {chat_manager.session_id}")
            st.info(f"**Modelo:** DeepSeek Chat")
            st.info(f"**Limite de histórico:** {len(chat_manager.get_chat_history())}/{50}")
        
        # Botões de controle avançados
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📋 Exportar Histórico", type="secondary"):
                # Implementar exportação do histórico
                st.info("Funcionalidade de exportação em desenvolvimento")
        
        with col2:
            if st.button("💾 Salvar Sessão", type="secondary"):
                # Implementar salvamento da sessão
                st.info("Funcionalidade de salvamento em desenvolvimento")
        
        with col3:
            if st.button("📖 Documentação", type="secondary"):
                st.info("""
                ### 📖 Como usar:
                1. **Configure sua API key** na barra lateral
                2. **Teste a conexão** com o botão "Testar Conexão"
                3. **Faça upload de documentos** na aba Documentos
                4. **Chat com a IA** na aba Chat
                5. **Analise documentos** usando os botões de análise
                """)

if __name__ == "__main__":
    main()
