# 📄 utils/validators.py
"""
VALIDAÇÕES DO SISTEMA
Validações centralizadas para todo o sistema
"""

import re
from datetime import datetime

class Validators:
    """Classe com métodos de validação"""
    
    @staticmethod
    def validar_cnpj(cnpj):
        """
        Valida formato de CNPJ (apenas formato, não dígitos verificadores)
        """
        if not cnpj:
            return False
        
        # Remove caracteres não numéricos
        cnpj_limpo = re.sub(r'[^0-9]', '', cnpj)
        
        # Verifica se tem 14 dígitos
        if len(cnpj_limpo) != 14:
            return False
        
        return True
    
    @staticmethod
    def validar_matricula(matricula):
        """
        Valida se a matrícula é um número positivo
        """
        try:
            matricula_int = int(matricula)
            return matricula_int > 0
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def validar_data(data_str):
        """
        Valida formato de data (DD/MM/AAAA)
        """
        try:
            datetime.strptime(data_str, '%d/%m/%Y')
            return True
        except ValueError:
            return False
    
    @staticmethod
    def validar_email(email):
        """
        Valida formato de email
        """
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email)) if email else True
    
    @staticmethod
    def formatar_cnpj(cnpj):
        """
        Formata CNPJ para exibição: XX.XXX.XXX/XXXX-XX
        """
        cnpj_limpo = re.sub(r'[^0-9]', '', cnpj)
        if len(cnpj_limpo) == 14:
            return f"{cnpj_limpo[:2]}.{cnpj_limpo[2:5]}.{cnpj_limpo[5:8]}/{cnpj_limpo[8:12]}-{cnpj_limpo[12:]}"
        return cnpj