import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# Configuração da API DeepSeek
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")

# Configurações do modelo
DEFAULT_MODEL = "deepseek-chat"
MAX_TOKENS = 4096
TEMPERATURE = 0.7

# Configurações de arquivo
UPLOAD_FOLDER = "uploads"
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_EXTENSIONS = {'.pdf', '.doc', '.docx', '.txt', '.csv'}

# Configurações do chat
CHAT_HISTORY_LIMIT = 50
