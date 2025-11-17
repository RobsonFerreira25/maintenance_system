# 📄 database/models.py
"""
MODELS.PY - Definição das classes do sistema
Aqui criamos 'representações' das tabelas em Python
"""

class Empresa:
    def __init__(self, cnpj, razao_social):
        self.cnpj = cnpj
        self.razao_social = razao_social
    
    def to_dict(self):
        return {'cnpj': self.cnpj, 'razao_social': self.razao_social}

class Filial:
    def __init__(self, cnpj_ind, nome):
        self.cnpj_ind = cnpj_ind
        self.nome = nome
    
    def to_dict(self):
        return {'cnpj_ind': self.cnpj_ind, 'nome': self.nome}

class Endereco:
    def __init__(self, id_endereco, rua, numero, bairro):
        self.id_endereco = id_endereco
        self.rua = rua
        self.numero = numero
        self.bairro = bairro
    
    def to_dict(self):
        return {
            'id_endereco': self.id_endereco,
            'rua': self.rua,
            'numero': self.numero,
            'bairro': self.bairro
        }

class Colaborador:
    def __init__(self, matricula, nome, cargo):
        self.matricula = matricula
        self.nome = nome
        self.cargo = cargo
    
    def to_dict(self):
        return {
            'matricula': self.matricula,
            'nome': self.nome,
            'cargo': self.cargo
        }

class Solicitacao:
    def __init__(self, n_solicitacao, dt_abertura, area, status, responsavel, descricao, dt_conclusao=None):
        self.n_solicitacao = n_solicitacao
        self.dt_abertura = dt_abertura
        self.area = area
        self.status = status
        self.responsavel = responsavel
        self.descricao = descricao
        self.dt_conclusao = dt_conclusao
    
    def to_dict(self):
        return {
            'n_solicitacao': self.n_solicitacao,
            'dt_abertura': self.dt_abertura,
            'area': self.area,
            'status': self.status,
            'responsavel': self.responsavel,
            'descricao': self.descricao,
            'dt_conclusao': self.dt_conclusao
        }