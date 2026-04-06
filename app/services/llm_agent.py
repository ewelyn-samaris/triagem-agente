import os
import json
from google import genai
from google.genai import types
from abc import ABC, abstractmethod
from app.core.logger import get_logger
from app.db.categoria_enum import Categoria
from app.db.urgencia_enum import Urgencia
from typing import TypedDict

logger = get_logger(__name__) # identifica a origem do log (se exec diretamente ou chamado)

class Classificacao(TypedDict):
    categoria: Categoria
    urgencia: Urgencia


class AIAgente(ABC):
    '''
    Interface abstrata que define comportamento esperado do agente de triagem 
    '''

    @abstractmethod
    def classificar_ticket(self, texto_solicitacao: str) -> Classificacao:
        pass


class GeminiAgente(AIAgente):
    '''
    Implementação concreta do agente de triagem utilizando API Google Gemini
    '''
    
    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY')
        self.model_name = os.getenv('MODEL_NAME')
        self.client = None
        self._configurar_api(self.api_key)
    
    def _configurar_api(self, api_key: str):
        if api_key:
            self.client=genai.Client(api_key=api_key)
        else:
            logger.warning('API_key não fornecida para o Agente Gemini')

    def _construir_prompt(self, texto_solicitacao):
        return f'''
        Você é um agente de triagem de suporte de TI altamente preciso.
        Analise o texto da solicitação do usuário e classifique-o ESTRITAMENTE usando as opções abaixo:
    
        Categorias permitidas: "FINANCEIRO", "SUPORTE_TECNICO", "DUVIDA_GERAL", "OUTRO".
        Urgências permitidas: "ALTA", "MEDIA", "BAIXA".
        
        Texto: {texto_solicitacao}
        '''
    
    def classificar_ticket(self, texto_solicitacao: str) -> Classificacao:
        fallback = {'categoria': Categoria.NAO_CLASSIFICADO, 'urgencia': Urgencia.MEDIA}
        
        if not self.client:
            return fallback
        
        logger.info(f'Classificando ticket via {self.model_name}....')
        
        try:
            prompt = self._construir_prompt(texto_solicitacao)

            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(response_mime_type="application/json")
            )

            try:
                if not response.text:
                    logger.error('IA não retornou resposta')
                    return fallback
                
                # convertendo json text em python dict
                resultado = json.loads(response.text)
            except json.JSONDecodeError:
                logger.error('Resposta de IA não é JSON válido')
                return fallback

            logger.info(f'Ticket classificado com sucesso por IA segundo regras definidas: {resultado}')

            return {
                'categoria': Categoria(resultado.get('categoria', Categoria.NAO_CLASSIFICADO.value)),
                'urgencia': Urgencia(resultado.get('urgencia', Urgencia.MEDIA.value))
            }
        
        except Exception as e:
            logger.error(f'Falha na integração com LLM. Assumindo classificação de fallback. Erro: {str(e)}')
            return fallback
        
