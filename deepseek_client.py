import os
import requests
import json
from typing import List, Dict, Any, Optional
import logging
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from config import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL, DEFAULT_MODEL, MAX_TOKENS, TEMPERATURE

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DeepSeekClient:
    """Cliente para integração com a API do DeepSeek"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or DEEPSEEK_API_KEY
        self.base_url = DEEPSEEK_BASE_URL.rstrip("/")
        self.model = DEFAULT_MODEL
        
        if not self.api_key:
            raise ValueError("API key do DeepSeek é obrigatória")
        
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # Sessão com retries
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        retries = Retry(
            total=5,
            connect=5,
            read=5,
            backoff_factor=1.5,
            status_forcelist=(429, 500, 502, 503, 504),
            allowed_methods=frozenset(["GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS"]),
            raise_on_status=False,
        )
        adapter = HTTPAdapter(max_retries=retries)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)
        
        # Permite ajustar timeout via env var
        self.connect_timeout = float(os.getenv("DEEPSEEK_CONNECT_TIMEOUT", "10"))
        self.read_timeout = float(os.getenv("DEEPSEEK_READ_TIMEOUT", "120"))
    
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
            
            response = self.session.post(
                url, json=payload, timeout=(self.connect_timeout, self.read_timeout)
            )
            
            # Trata alguns status comuns
            if response.status_code == 401:
                return {"error": "Não autorizado (401). Verifique sua API key."}
            if response.status_code == 404:
                return {"error": "Endpoint não encontrado (404). Verifique a URL base."}
            if response.status_code >= 500:
                logger.warning(f"Erro do servidor DeepSeek: {response.status_code}")
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.Timeout:
            logger.error("Timeout ao chamar DeepSeek")
            return {"error": "Tempo de resposta excedido. Tente novamente em instantes."}
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
        
        default_prompt = """Analise o seguinte documento e forneça:
1. Um resumo executivo (2-3 parágrafos)
2. Principais pontos e insights
3. Recomendações ou observações relevantes
4. Palavras-chave importantes

Documento:
{text}

Por favor, seja conciso mas abrangente na análise."""

        prompt = analysis_prompt or default_prompt.format(text=document_text[:4000])
        
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
        if chat_history:
            messages.extend(chat_history[-10:])
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
        """Testa a conexão com a API do DeepSeek usando endpoint leve."""
        try:
            url = f"{self.base_url}/v1/models"
            resp = self.session.get(url, timeout=(self.connect_timeout, 20))
            if resp.status_code == 401:
                logger.error("Não autorizado (401) ao listar modelos. Verifique a API key.")
                return False
            if resp.status_code >= 400:
                logger.error(f"Falha ao listar modelos: {resp.status_code} {resp.text[:200]}")
                return False
            return True
        except requests.exceptions.Timeout:
            logger.error("Timeout no teste de conexão (/v1/models)")
            return False
        except Exception as e:
            logger.error(f"Erro no teste de conexão: {e}")
            return False
