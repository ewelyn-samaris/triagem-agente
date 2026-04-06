import pytest
import json
from app.services.llm_agent import GeminiAgente
from app.db.categoria_enum import Categoria
from app.db.urgencia_enum import Urgencia

class TestLLMAgente:
    '''
    Suíte de testes para garantir que o agente de IA lide corretamente com a API
    e seus possíveis cenários de falha
    '''

    @pytest.fixture(scope='function', autouse=True)
    def mock_env(self, mocker):
        # mockamos variáveis de ambiente
        mocker.patch.dict('os.environ', {
            'GEMINI_API_KEY': 'Fake_API_Key_1234567890',
            'MODEL_NAME': 'Fake_model-name'
        })

    def test_classifica_ticket_com_sucesso(self, mocker, mock_env):
        agente = GeminiAgente()

        mock_response = mocker.MagicMock()
        mock_response.text = json.dumps({'categoria':'FINANCEIRO', 'urgencia':'ALTA'})

        # substituo o método verdadeiro (generate_content) pelo mock
        mocker.patch.object(agente.client.models, 'generate_content', return_value=mock_response)

        resultado = agente.classificar_ticket('Faturamento travado')

        assert resultado['categoria'] == Categoria.FINANCEIRO
        assert resultado['urgencia'] == Urgencia.ALTA

    def test_fallback_quando_api_key_nao_fornecida(self, mocker):
        mocker.patch.dict('os.environ', clear=True)

        agente = GeminiAgente()
        resultado = agente.classificar_ticket('Texto solicitação ticket.')

        assert resultado['categoria'] == Categoria.NAO_CLASSIFICADO
        assert resultado['urgencia'] == Urgencia.MEDIA
    
    def test_fallback_quando_llm_retorna_json_invalido(self, mocker, mock_env):
        agente = GeminiAgente()

        mock_response = mocker.MagicMock()
        mock_response.text = 'Com base nos dados fornecidos, é provável que a categoria deste ticket seja FINANCEIRO.'

        mocker.patch.object(agente.client.models, 'generate_content', return_value=mock_response)

        resultado = agente.classificar_ticket('Faturamento interrompido há uma hora')

        assert resultado['categoria'] == Categoria.NAO_CLASSIFICADO
        assert resultado['urgencia'] == Urgencia.MEDIA
    
    def test_fallback_quando_api_sofre_excecao_de_rede(self, mocker):
        agente = GeminiAgente()

        mocker.patch.object(agente.client.models, 'generate_content', side_effect=Exception('Timeout'))

        resultado = agente.classificar_ticket('Texto solicitação ticket.')

        assert resultado['categoria'] == Categoria.NAO_CLASSIFICADO
        assert resultado['urgencia'] == Urgencia.MEDIA