import logging
import re
from app.core.logger import get_logger

class TestLogger:
    '''
    Suíte de validação de objetos Logger gerados
    '''
    def test_get_logger_retorna_instancia_correta(self):
        logger = get_logger('é instancia de Logger')

        assert isinstance(logger, logging.Logger)
    
    def test_logger_comportamento_singleton(self):

        logger1 = get_logger('singleton_behavior_test')
        logger2 = get_logger('singleton_behavior_test')

        assert logger1 is logger2 # devem apontar para mesmo end de memória
        assert len(logger2.handlers) == 1
    
    def test_formato_log(self):
        logger = get_logger('test_logger')
        handler = logger.handlers[-1]
        formatter = handler.formatter

        record = logging.LogRecord(
            name='test_logger',
            level=logging.INFO,
            pathname=__file__,
            lineno=10,
            msg='message text',
            args=(),
            exc_info=None,
        )

        formatted = formatter.format(record)

        assert 'INFO' in formatted
        assert 'test_logger' in formatted
        assert 'message text' in formatted

        pattern = r'\d{4}-\d{2}-\d{2}'
        assert re.search(pattern, formatted)