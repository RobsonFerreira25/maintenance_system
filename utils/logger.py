# 📄 utils/logger.py
"""
SISTEMA DE LOGS DO SISTEMA
Registra todas as atividades importantes
"""

import logging
from datetime import datetime
import os

def setup_logger():
    """
    Configura o sistema de logs
    """
    # Criar pasta de logs se não existir
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # Configurar logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(f'logs/sistema_{datetime.now().strftime("%Y%m%d")}.log'),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger(__name__)

# Logger global
logger = setup_logger()

def log_activity(usuario, acao, detalhes=""):
    """
    Registra atividade importante do sistema
    """
    mensagem = f"USUÁRIO: {usuario} | AÇÃO: {acao} | DETALHES: {detalhes}"
    logger.info(mensagem)

def log_error(usuario, erro, modulo=""):
    """
    Registra erros do sistema
    """
    mensagem = f"ERRO - USUÁRIO: {usuario} | MÓDULO: {modulo} | ERRO: {erro}"
    logger.error(mensagem)