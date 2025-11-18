# 📄 config/settings.py
"""
CONFIGURAÇÕES DO SISTEMA
Centraliza todas as configurações em um único lugar
"""

import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configurações do Banco de Dados
DB_CONFIG = {
    'dbname': os.getenv("DB_NAME", "gestao_manutencao"),
    'user': os.getenv("DB_USER", "postgres"),
    'password': os.getenv("DB_PASSWORD", "password"),
    'host': os.getenv("DB_HOST", "localhost"),
    'port': os.getenv("DB_PORT", "5432")
}

# Configurações da Aplicação
APP_CONFIG = {
    'name': 'Sistema de Gestão de Manutenção',
    'version': '1.0.0',
    'developer': 'O Arquiteto',
    'description': 'Sistema profissional para gestão de manutenções'
}

# Cores do Sistema
COLORS = {
    'primary': '#3498DB',
    'success': '#2ECC71',
    'danger': '#E74C3C',
    'warning': '#F39C12',
    'dark': '#2C3E50',
    'light': '#ECF0F1'
}