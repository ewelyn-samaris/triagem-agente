import pytest
from uuid import UUID, uuid4
from pydantic import ValidationError
from app.schemas.ticket_schema import TicketCreate

class TestTicketCreate:
    '''
    Suíte de testes responsável por garantir as regras de negócio e validações
    da entrada do ticket
    '''

    @pytest.fixture(scope='function')
    def dados_validos(self):
        return {
            'id_cliente': uuid4(),
            'texto_solicitacao': 'Não consigo fazer logging mesmo com os dados corretos'
        }
    
    def test_validacao_ok_quando_regras_atendidas(self, dados_validos):
        ticket = TicketCreate(**dados_validos)

        assert ticket.id_cliente == dados_validos['id_cliente']
        assert ticket.texto_solicitacao == dados_validos['texto_solicitacao']

    def test_id_cliente_string_valida(self, dados_validos):
        dados = {**dados_validos, 'id_cliente': str(dados_validos['id_cliente'])}

        ticket = TicketCreate(**dados)

        assert ticket.id_cliente == dados_validos['id_cliente']
    
    @pytest.mark.parametrize(
            'texto_solicitacao, tamanho_esperado',
            [
                pytest.param('i' * 120, 120, id='max_length'),
                pytest.param('i' * 10, 10, id='min_length'),
            ],
    )
    def test_valores_de_borda_de_length_para_texto_solicitacao(self, dados_validos, texto_solicitacao, tamanho_esperado):
        dados = {**dados_validos, 'texto_solicitacao':texto_solicitacao}
        ticket = TicketCreate(**dados)

        assert len(ticket.texto_solicitacao) == tamanho_esperado
    
    @pytest.mark.parametrize(
        'id_cliente',
        [
            pytest.param(123, id='inteiro'),
            pytest.param('', id='string vazia'),
            pytest.param('uuid invalida', id='string invalida'),
            pytest.param(None, id='none')
        ],
    )
    def test_id_cliente_invalido(self, dados_validos, id_cliente):
        dados = {**dados_validos, 'id_cliente':id_cliente}
        with pytest.raises(ValidationError) as exc:
            TicketCreate(**dados)

        errors = exc.value.errors()
        assert errors[0]['loc'] == ('id_cliente',)

    @pytest.mark.parametrize(
            'texto_solicitacao',
            [
                pytest.param('', id='string vazia'),
                pytest.param(None, id='none'),
                pytest.param('k' * 9, id='texto muito curto'),
                pytest.param('f' * 121, id='texto muito longo')
            ],
    )
    def test_texto_solicitacao_invalido(self, dados_validos, texto_solicitacao):
        dados = {**dados_validos, 'texto_solicitacao':texto_solicitacao}
        with pytest.raises(ValidationError) as exc:
            TicketCreate(**dados)

        errors = exc.value.errors()
        assert errors[0]['loc'] == ('texto_solicitacao',)
    
    @pytest.mark.parametrize(
            'dados',
            [
                pytest.param({'id_cliente': uuid4()}, id='sem campo de texto_solicitacao'),
                pytest.param({'texto_colicitacao': 'o' * 12}, id='apenas texto, sem id_cliente')
            ],
    )
    def test_campos_ausentes(self, dados):
        with pytest.raises(ValidationError):
            TicketCreate(**dados)