"""
Sistema de logging do PDV
Baseado na prática do SISUSF com logs detalhados
"""
import logging
import os
from datetime import datetime

# Criar diretório de logs
LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
os.makedirs(LOG_DIR, exist_ok=True)

# Nome do arquivo de log com data
LOG_FILE = os.path.join(LOG_DIR, f'pdv_{datetime.now().strftime("%Y%m%d")}.log')

# Configuração do logger
def setup_logger(name='PDV'):
    """Configura e retorna um logger"""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # Evitar duplicação de handlers
    if logger.handlers:
        return logger
    
    # Handler para arquivo
    file_handler = logging.FileHandler(LOG_FILE, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    
    # Handler para console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # Formato detalhado
    formatter = logging.Formatter(
        '%(asctime)s | %(name)s | %(levelname)s | %(funcName)s:%(lineno)d | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

# Logger padrão do sistema
logger = setup_logger()

def log_venda(venda_dict):
    """Log especializado para vendas"""
    logger.info(f"VENDA REGISTRADA | Nº {venda_dict['numero_venda']} | "
                f"Total: R$ {venda_dict['valor_final']:.2f} | "
                f"Pagamento: {venda_dict['forma_pagamento']}")

def log_erro_fiscal(mensagem, detalhes=None):
    """Log especializado para erros fiscais"""
    logger.error(f"ERRO FISCAL | {mensagem}")
    if detalhes:
        logger.error(f"Detalhes: {detalhes}")

def log_produto_cadastrado(produto_dict):
    """Log de cadastro de produto"""
    logger.info(f"PRODUTO CADASTRADO | {produto_dict['codigo_barras']} | "
                f"{produto_dict['descricao']} | "
                f"R$ {produto_dict['preco_venda']:.2f}")