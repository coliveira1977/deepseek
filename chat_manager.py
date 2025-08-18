import os
import tempfile
import shutil
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging
from deepseek_client import DeepSeekClient
from document_processor import DocumentProcessor
from config import UPLOAD_FOLDER, CHAT_HISTORY_LIMIT

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ChatManager:
    """Gerenciador principal do chat com IA"""
    
    def __init__(self, api_key: str):
        self.deepseek_client = DeepSeekClient(api_key)
        self.document_processor = DocumentProcessor()
        self.chat_history = []
        self.uploaded_documents = {}
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Cria pasta de uploads se não existir
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    
    def add_message(self, role: str, content: str, document_info: Optional[Dict] = None) -> None:
        """Adiciona uma mensagem ao histórico do chat"""
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "document_info": document_info
        }
        
        self.chat_history.append(message)
        
        # Limita o histórico
        if len(self.chat_history) > CHAT_HISTORY_LIMIT:
            self.chat_history = self.chat_history[-CHAT_HISTORY_LIMIT:]
    
    def get_chat_history(self) -> List[Dict[str, Any]]:
        """Retorna o histórico do chat"""
        return self.chat_history
    
    def upload_document(self, uploaded_file) -> Dict[str, Any]:
        """Processa upload de documento"""
        try:
            if uploaded_file is None:
                return {"error": "Nenhum arquivo foi enviado"}
            
            # Verifica extensão
            file_extension = os.path.splitext(uploaded_file.name)[1].lower()
            if file_extension not in ['.pdf', '.doc', '.docx', '.txt', '.csv']:
                return {"error": f"Formato não suportado: {file_extension}"}
            
            # Salva arquivo temporariamente
            with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as tmp_file:
                shutil.copyfileobj(uploaded_file, tmp_file)
                temp_path = tmp_file.name
            
            # Processa o documento
            document_info = self.document_processor.process_document(temp_path)
            
            if "error" not in document_info:
                # Move para pasta de uploads com nome único
                final_filename = f"{self.session_id}_{uploaded_file.name}"
                final_path = os.path.join(UPLOAD_FOLDER, final_filename)
                shutil.move(temp_path, final_path)
                
                document_info["path"] = final_path
                document_info["upload_time"] = datetime.now().isoformat()
                
                # Armazena no dicionário de documentos
                self.uploaded_documents[final_filename] = document_info
                
                # Adiciona mensagem de confirmação
                summary = self.document_processor.get_document_summary(document_info)
                self.add_message("system", f"📄 Documento carregado com sucesso!\n\n{summary}")
                
                return {
                    "success": True,
                    "document_info": document_info,
                    "summary": summary
                }
            else:
                # Remove arquivo temporário em caso de erro
                if os.path.exists(temp_path):
                    os.unlink(temp_path)
                return document_info
                
        except Exception as e:
            logger.error(f"Erro no upload: {e}")
            return {"error": f"Erro interno: {str(e)}"}
    
    def analyze_document(self, filename: str, custom_prompt: Optional[str] = None) -> str:
        """Analisa um documento específico"""
        if filename not in self.uploaded_documents:
            return "❌ Documento não encontrado. Por favor, faça upload primeiro."
        
        document_info = self.uploaded_documents[filename]
        
        if not document_info.get("text"):
            return "❌ Nenhum texto extraído do documento para análise."
        
        # Adiciona mensagem de análise em andamento
        self.add_message("user", f"Analise o documento: {filename}")
        
        # Realiza análise usando DeepSeek
        analysis = self.deepseek_client.analyze_document(
            document_info["text"], 
            custom_prompt
        )
        
        # Adiciona resposta da IA
        self.add_message("assistant", analysis, {"document": filename})
        
        return analysis
    
    def chat_with_ai(self, user_message: str) -> str:
        """Processa mensagem do usuário e retorna resposta da IA"""
        if not user_message.strip():
            return "❌ Por favor, digite uma mensagem."
        
        # Adiciona mensagem do usuário
        self.add_message("user", user_message)
        
        # Gera resposta usando DeepSeek
        response = self.deepseek_client.generate_response(
            user_message, 
            self.get_formatted_history()
        )
        
        # Adiciona resposta da IA
        self.add_message("assistant", response)
        
        return response
    
    def get_formatted_history(self) -> List[Dict[str, str]]:
        """Retorna histórico formatado para a API"""
        formatted_history = []
        
        for message in self.chat_history[-20:]:  # Últimas 20 mensagens
            if message["role"] in ["user", "assistant"]:
                formatted_history.append({
                    "role": message["role"],
                    "content": message["content"]
                })
        
        return formatted_history
    
    def get_documents_summary(self) -> str:
        """Retorna resumo de todos os documentos carregados"""
        if not self.uploaded_documents:
            return "📁 Nenhum documento carregado ainda."
        
        summary = f"📁 **Documentos Carregados ({len(self.uploaded_documents)})**\n\n"
        
        for filename, doc_info in self.uploaded_documents.items():
            summary += f"📄 **{filename}**\n"
            summary += f"   Tipo: {doc_info['extension'].upper()}\n"
            summary += f"   Tamanho: {doc_info['size'] / 1024:.1f} KB\n"
            summary += f"   Palavras: {doc_info['word_count']}\n"
            summary += f"   Carregado: {doc_info['upload_time'][:19]}\n\n"
        
        return summary
    
    def clear_chat_history(self) -> None:
        """Limpa o histórico do chat"""
        self.chat_history = []
        logger.info("Histórico do chat limpo")
    
    def test_connection(self) -> bool:
        """Testa conexão com a API do DeepSeek"""
        return self.deepseek_client.test_connection()
