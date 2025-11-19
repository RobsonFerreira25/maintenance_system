# 📄 utils/validators.py
"""
VALIDAÇÕES DO SISTEMA - VERSÃO MELHORADA
Validações centralizadas para todo o sistema com mais robustez
"""

import re
from datetime import datetime

class Validators:
    """Classe com métodos de validação melhorados"""
    
    @staticmethod
    def validar_cnpj(cnpj):
        """
        Valida formato de CNPJ (apenas formato, não dígitos verificadores)
        VERSÃO MELHORADA: Mais validações
        """
        if not cnpj or not isinstance(cnpj, str):
            return False
        
        # Remove caracteres não numéricos
        cnpj_limpo = re.sub(r'[^0-9]', '', cnpj)
        
        # Verifica se tem 14 dígitos
        if len(cnpj_limpo) != 14:
            return False
        
        # Verifica se não é uma sequência de números iguais
        if cnpj_limpo == cnpj_limpo[0] * 14:
            return False
        
        return True
    
    @staticmethod
    def validar_matricula(matricula):
        """
        Valida se a matrícula é um número positivo
        VERSÃO MELHORADA: Aceita string ou inteiro
        """
        try:
            if isinstance(matricula, str):
                matricula = matricula.strip()
                if not matricula:
                    return False
            
            matricula_int = int(matricula)
            return matricula_int > 0 and matricula_int < 1000000  # Limite razoável
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def validar_data(data_str):
        """
        Valida formato de data (DD/MM/AAAA)
        VERSÃO MELHORADA: Verifica se data é real
        """
        try:
            data = datetime.strptime(data_str, '%d/%m/%Y')
            # Verifica se a data não é no futuro (para datas de abertura)
            if data > datetime.now():
                return False
            return True
        except ValueError:
            return False
    
    @staticmethod
    def validar_email(email):
        """
        Valida formato de email
        VERSÃO MELHORADA: Regex mais robusto
        """
        if not email:
            return True  # Email é opcional
        
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def validar_texto(texto, max_length=1000, min_length=1):
        """
        Valida texto com limites de tamanho
        """
        if not texto or not isinstance(texto, str):
            return False
        
        texto_limpo = texto.strip()
        return min_length <= len(texto_limpo) <= max_length
    
    @staticmethod
    def validar_telefone(telefone):
        """
        Valida formato de telefone brasileiro
        """
        if not telefone:
            return True  # Telefone é opcional
        
        # Remove caracteres não numéricos
        telefone_limpo = re.sub(r'[^0-9]', '', telefone)
        
        # Verifica se tem entre 10 e 11 dígitos
        return 10 <= len(telefone_limpo) <= 11
    
    @staticmethod
    def formatar_cnpj(cnpj):
        """
        Formata CNPJ para exibição: XX.XXX.XXX/XXXX-XX
        """
        cnpj_limpo = re.sub(r'[^0-9]', '', str(cnpj))
        if len(cnpj_limpo) == 14:
            return f"{cnpj_limpo[:2]}.{cnpj_limpo[2:5]}.{cnpj_limpo[5:8]}/{cnpj_limpo[8:12]}-{cnpj_limpo[12:]}"
        return cnpj
    
    @staticmethod
    def validar_solicitacao_dados(area, responsavel, descricao):
        """
        Valida dados completos de uma solicitação
        """
        errors = []
        
        if not area or not Validators.validar_texto(area, 50):
            errors.append("Área é obrigatória e deve ter até 50 caracteres")
        
        if not responsavel or not Validators.validar_texto(responsavel, 100):
            errors.append("Responsável é obrigatório e deve ter até 100 caracteres")
        
        if not descricao or not Validators.validar_texto(descricao, 1000, 10):
            errors.append("Descrição é obrigatória e deve ter entre 10 e 1000 caracteres")
        
        return errors