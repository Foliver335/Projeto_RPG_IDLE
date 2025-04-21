import os
import pytest
import openai
from dotenv import load_dotenv

# Carrega variáveis do arquivo .env
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

@pytest.mark.skipif(API_KEY is None, reason="OPENAI_API_KEY não definida")
def test_openai_api_response():
    """
    Testa se a chamada à API do OpenAI retorna uma resposta válida.
    Caso exceda a cota, o teste será pulado.
    """
    openai.api_key = API_KEY
    try:
        # nova forma de chamar o chat no SDK >=1.0.0
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Diga olá em forma de poema curto."}]
        )
    except openai.RateLimitError as e:
        pytest.skip(f"Quota excedida, pulando teste de API: {e}")
    # Validações básicas
    assert hasattr(response, "choices"), "Resposta não contém 'choices'"
    assert len(response.choices) > 0, "Nenhuma escolha retornada pela API"
    content = response.choices[0].message.content
    assert isinstance(content, str) and content.strip(), "Conteúdo da resposta inválido"
