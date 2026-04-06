import logging
import sys

def get_logger(name: str)->logging.Logger:
    '''
    Configura e retorna um logger padronizado para a aplicação
    '''

    logger = logging.getLogger(name)

    if not logger.handlers:
        logger.setLevel(logging.INFO) # nível mínimo de logger que será registrado

        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(name)s - %(message)s'
        )

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)

        logger.addHandler(console_handler)

    return logger