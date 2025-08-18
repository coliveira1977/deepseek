#!/usr/bin/env python3
"""
Exemplo de uso programático do DeepSeek Chat Local
"""

import os
import sys
from chat_manager import ChatManager
from document_processor import DocumentProcessor

def example_usage():
    """Exemplo de uso das funcionalidades principais"""
    
    # Verifica se a API key está configurada
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        print("❌ Configure a variável de ambiente DEEPSEEK_API_KEY")
        print("   export DEEPSEEK_API_KEY=sua_chave_aqui")
        return
    
    print("🤖 Exemplo de uso do DeepSeek Chat Local")
    print("=" * 50)
    
    try:
        # Inicializa o chat manager
        print("🔧 Inicializando chat manager...")
        chat_manager = ChatManager(api_key)
        
        # Testa conexão
        print("🧪 Testando conexão com a API...")
        if chat_manager.test_connection():
            print("✅ Conexão estabelecida!")
        else:
            print("❌ Falha na conexão")
            return
        
        # Exemplo de chat simples
        print("\n💬 Exemplo de chat:")
        user_message = "Olá! Como você pode me ajudar hoje?"
        print(f"👤 Usuário: {user_message}")
        
        response = chat_manager.chat_with_ai(user_message)
        print(f"🤖 IA: {response[:100]}...")
        
        # Exemplo de processamento de documento
        print("\n📄 Exemplo de processamento de documento:")
        
        # Cria um arquivo de exemplo
        example_content = """
        Este é um documento de exemplo para demonstrar as funcionalidades.
        
        Principais tópicos:
        1. Análise de documentos
        2. Chat inteligente
        3. Processamento de texto
        4. Integração com DeepSeek
        
        O sistema pode analisar diferentes tipos de arquivos e fornecer insights úteis.
        """
        
        example_file_path = "example_document.txt"
        with open(example_file_path, "w", encoding="utf-8") as f:
            f.write(example_content)
        
        print(f"📝 Arquivo de exemplo criado: {example_file_path}")
        
        # Processa o documento
        document_processor = DocumentProcessor()
        doc_info = document_processor.process_document(example_file_path)
        
        if "error" not in doc_info:
            print("✅ Documento processado com sucesso!")
            print(f"   Palavras: {doc_info['word_count']}")
            print(f"   Tamanho: {doc_info['size']} bytes")
            
            # Analisa o documento
            print("\n🔍 Analisando documento...")
            analysis = chat_manager.deepseek_client.analyze_document(doc_info["text"])
            print(f"📊 Análise: {analysis[:200]}...")
        else:
            print(f"❌ Erro no processamento: {doc_info['error']}")
        
        # Limpa arquivo de exemplo
        if os.path.exists(example_file_path):
            os.remove(example_file_path)
            print(f"🗑️ Arquivo de exemplo removido")
        
        print("\n✅ Exemplo concluído com sucesso!")
        print("\n💡 Para usar a interface web:")
        print("   streamlit run app.py")
        
    except Exception as e:
        print(f"❌ Erro durante o exemplo: {e}")
        import traceback
        traceback.print_exc()

def test_document_processing():
    """Testa o processamento de diferentes tipos de documentos"""
    
    print("\n🧪 Testando processamento de documentos...")
    
    # Cria documentos de exemplo
    examples = {
        "example.txt": "Este é um arquivo de texto simples para teste.",
        "example.csv": "Nome,Idade,Cidade\nJoão,25,São Paulo\nMaria,30,Rio de Janeiro\nPedro,35,Belo Horizonte"
    }
    
    processor = DocumentProcessor()
    
    for filename, content in examples.items():
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(content)
            
            print(f"\n📄 Testando: {filename}")
            doc_info = processor.process_document(filename)
            
            if "error" not in doc_info:
                print(f"   ✅ Sucesso: {doc_info['word_count']} palavras")
                print(f"   📊 Resumo: {processor.get_document_summary(doc_info)[:100]}...")
            else:
                print(f"   ❌ Erro: {doc_info['error']}")
            
            # Remove arquivo de teste
            os.remove(filename)
            
        except Exception as e:
            print(f"   ❌ Exceção: {e}")

if __name__ == "__main__":
    print("🚀 Iniciando exemplos...")
    
    # Testa processamento de documentos
    test_document_processing()
    
    # Executa exemplo principal
    example_usage()
    
    print("\n🎉 Todos os exemplos foram executados!")
