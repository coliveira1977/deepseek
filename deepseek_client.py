import os
import requests
import json
from typing import List, Dict, Any, Optional
import logging
from config import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL, DEFAULT_MODEL, MAX_TOKENS, TEMPERATURE

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DeepSeekClient:
    """Cliente para integração com a API do DeepSeek"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or DEEPSEEK_API_KEY
        self.base_url = DEEPSEEK_BASE_URL
        self.model = DEFAULT_MODEL
        
        if not self.api_key:
            raise ValueError("API key do DeepSeek é obrigatória")
        
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def chat_completion(self, messages: List[Dict[str, str]], 
                       model: Optional[str] = None,
                       max_tokens: Optional[int] = None,
                       temperature: Optional[float] = None) -> Dict[str, Any]:
        """Envia mensagem para o chat do DeepSeek"""
        try:
            url = f"{self.base_url}/v1/chat/completions"
            
            payload = {
                "model": model or self.model,
                "messages": messages,
                "max_tokens": max_tokens or MAX_TOKENS,
                "temperature": temperature or TEMPERATURE,
                "stream": False
            }
            
            response = requests.post(url, headers=self.headers, json=payload, timeout=60)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro na requisição para DeepSeek: {e}")
            return {"error": f"Erro de conexão: {str(e)}"}
        except Exception as e:
            logger.error(f"Erro inesperado: {e}")
            return {"error": f"Erro interno: {str(e)}"}
    
    def analyze_document(self, document_text: str, analysis_prompt: str = None) -> str:
        """Analisa um documento usando a API do DeepSeek"""
        if not document_text.strip():
            return "❌ Nenhum texto encontrado no documento para análise."
        
        # Prompt padrão para análise de documentos
        default_prompt = """Analise o seguinte documento e forneça:
1. Um resumo executivo (2-3 parágrafos)
2. Principais pontos e insights
3. Recomendações ou observações relevantes
4. Palavras-chave importantes

Documento:
{text}

Por favor, seja conciso mas abrangente na análise."""

        prompt = analysis_prompt or default_prompt.format(text=document_text[:4000])  # Limita o tamanho
        
        messages = [
            {"role": "system", "content": "Você é um assistente especializado em análise de documentos. Forneça análises claras, estruturadas e úteis."},
            {"role": "user", "content": prompt}
        ]
        
        response = self.chat_completion(messages)
        
        if "error" in response:
            return f"❌ Erro na análise: {response['error']}"
        
        try:
            return response["choices"][0]["message"]["content"]
        except (KeyError, IndexError) as e:
            logger.error(f"Erro ao processar resposta: {e}")
            return "❌ Erro ao processar resposta da API"
    
    def generate_response(self, user_message: str, chat_history: List[Dict[str, str]] = None) -> str:
        """Gera resposta para uma mensagem do usuário"""
        messages = []
        
        # Adiciona histórico do chat se disponível
        if chat_history:
            messages.extend(chat_history[-10:])  # Últimas 10 mensagens
        
        # Adiciona mensagem atual
        messages.append({"role": "user", "content": user_message})
        
        response = self.chat_completion(messages)
        
        if "error" in response:
            return f"❌ Erro: {response['error']}"
        
        try:
            return response["choices"][0]["message"]["content"]
        except (KeyError, IndexError) as e:
            logger.error(f"Erro ao processar resposta: {e}")
            return "❌ Erro ao processar resposta da API"
    
    def test_connection(self) -> bool:
        """Testa a conexão com a API do DeepSeek"""
        try:
            messages = [{"role": "user", "content": "Olá, teste de conexão."}]
            response = self.chat_completion(messages, max_tokens=10)
            return "error" not in response
        except Exception as e:
            logger.error(f"Erro no teste de conexão: {e}")
            return False
