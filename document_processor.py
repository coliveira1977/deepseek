import os
import PyPDF2
import pandas as pd
from docx import Document
from typing import List, Dict, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DocumentProcessor:
    """Classe para processar diferentes tipos de documentos"""
    
    def __init__(self):
        self.supported_extensions = {'.pdf', '.doc', '.docx', '.txt', '.csv'}
    
    def extract_text_from_pdf(self, file_path: str) -> str:
        """Extrai texto de arquivos PDF"""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                return text.strip()
        except Exception as e:
            logger.error(f"Erro ao processar PDF {file_path}: {e}")
            return ""
    
    def extract_text_from_docx(self, file_path: str) -> str:
        """Extrai texto de arquivos DOCX"""
        try:
            doc = Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text.strip()
        except Exception as e:
            logger.error(f"Erro ao processar DOCX {file_path}: {e}")
            return ""
    
    def extract_text_from_txt(self, file_path: str) -> str:
        """Extrai texto de arquivos TXT"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read().strip()
        except Exception as e:
            logger.error(f"Erro ao processar TXT {file_path}: {e}")
            return ""
    
    def extract_text_from_csv(self, file_path: str) -> str:
        """Extrai texto de arquivos CSV"""
        try:
            df = pd.read_csv(file_path)
            # Converte DataFrame para texto estruturado
            text = f"Arquivo CSV com {len(df)} linhas e {len(df.columns)} colunas\n\n"
            text += "Colunas: " + ", ".join(df.columns.tolist()) + "\n\n"
            text += "Primeiras 10 linhas:\n"
            text += df.head(10).to_string(index=False)
            
            if len(df) > 10:
                text += f"\n\n... e mais {len(df) - 10} linhas"
            
            return text
        except Exception as e:
            logger.error(f"Erro ao processar CSV {file_path}: {e}")
            return ""
    
    def process_document(self, file_path: str) -> Dict[str, Any]:
        """Processa um documento e retorna informações extraídas"""
        if not os.path.exists(file_path):
            return {"error": "Arquivo não encontrado"}
        
        file_extension = os.path.splitext(file_path)[1].lower()
        
        if file_extension not in self.supported_extensions:
            return {"error": f"Formato de arquivo não suportado: {file_extension}"}
        
        file_info = {
            "filename": os.path.basename(file_path),
            "extension": file_extension,
            "size": os.path.getsize(file_path),
            "path": file_path
        }
        
        # Extrai texto baseado no tipo de arquivo
        if file_extension == '.pdf':
            text = self.extract_text_from_pdf(file_path)
        elif file_extension == '.docx':
            text = self.extract_text_from_docx(file_path)
        elif file_extension == '.txt':
            text = self.extract_text_from_txt(file_path)
        elif file_extension == '.csv':
            text = self.extract_text_from_csv(file_path)
        else:
            text = ""
        
        file_info["text"] = text
        file_info["word_count"] = len(text.split()) if text else 0
        
        return file_info
    
    def get_document_summary(self, file_info: Dict[str, Any]) -> str:
        """Gera um resumo do documento processado"""
        if "error" in file_info:
            return f"Erro: {file_info['error']}"
        
        summary = f"📄 **{file_info['filename']}**\n"
        summary += f"📊 Tipo: {file_info['extension'].upper()}\n"
        summary += f"📏 Tamanho: {file_info['size'] / 1024:.1f} KB\n"
        summary += f"📝 Palavras: {file_info['word_count']}\n"
        
        if file_info['text']:
            preview = file_info['text'][:200] + "..." if len(file_info['text']) > 200 else file_info['text']
            summary += f"\n📖 Prévia:\n{preview}"
        
        return summary
