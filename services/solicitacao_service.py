'''
SERVIÇO DE SOLICITAÇÕES - O coração do sistema de manutenção
Gerencia as ordens de serviço e seu ciclo de vida
'''
import sys
import os

# Adiciona o diretório raiz do projeto ao Python Path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.database import get_connection
from database.models import Solicitacao
from datetime import datetime


class SolicitacaoService:
    '''Serviço para Gerenciar solicitações de manutenção'''
    
    @staticmethod
    def criar_solicitação(n_solicitacao, area, responsavel, descricao, status="Aberta"):
        '''Cria uma nova solicitação de manutenção'''
        
        conn = get_connection()
        if conn is None:
            return False
        
        try:
            cur = conn.cursor()
            data_abertura = datetime.now().date()
            
            cur.execute(
                """INSERT INTO SOLICITACAO
                (N_SOLICITACAO, DT_ABERTURA, AREA, STATUS, RESPONSAVEL, DESCRICAO)
                VALUES (%s, %s, %s, %s, %s, %s)""",
                (n_solicitacao, data_abertura, area, status, responsavel, descricao)
            )
            conn.commit()
            print(f"Solicitação #{n_solicitacao} criada com sucesso!")
            return True
        
        except Exception as e:
            print(f"Erro ao criar solicitação: {e}")
            conn.rollback()
            return False
        finally:
            cur.close()
            conn.close()
            
            
            
    @staticmethod
    def listar_solicitacoes():
        '''Lista todas as solicitações no sistema'''
        
        conn = get_connection()
        if conn is None:
            return []
        
        try:
            cur = conn.cursor()
            cur.execute('''
                SELECT N_SOLICITACAO, DT_ABERTURA, AREA, STATUS, 
                RESPONSAVEL, DESCRICAO, DT_CONCLUSAO
                FROM SOLICITACAO ORDER BY DT_ABERTURA DESC
            ''')
            solicitacoes = []
            for n_solicitacao, dt_abertura, area, status, responsavel, descricao, dt_conclusao in cur.fetchall():
                solicitacoes.append(Solicitacao(dt_abertura, area, status, responsavel, descricao, dt_conclusao))
                
            return solicitacoes
        
        except Exception as e:
            print(f"Erro ao listar solicitações: {e}")
            return []
        
        finally:
            cur.close()
            conn.close()
            
            
            
    @staticmethod
    def atualizar_status_solicitacao(n_solicitacao, novo_status):
        '''Atualiza o status da solicitação'''
        
        conn = get_connection()
        if conn is None:
            return False
        
        try:
            cur = conn.cursor()
            
            if novo_status.lower() == "concluída":
                data_conclusao = datetime.now().date()
                cur.execute(
                    "UPDATE SOLICITACAO SET STATUS = %s, DT_CONCLUSAO = %s, WHERE N_SOLICITACAO = %s",
                    (novo_status, data_conclusao, n_solicitacao)
                )
            else:
                cur.execute(
                    "UPDATE SOLICITACAO SET STATUS = %s, DT_CONCLUSAO = NULL WHERE N_SOLICITACAO = %s",
                    (novo_status, n_solicitacao)
                )
            
            conn.commit()
            print(f"Status da solicitação #{n_solicitacao} atualizado para: {novo_status}")
            return True
        
        except Exception as e:
            print(f"Erro ao atualizar o status da solicitação: {e}")
            conn.rollback()
            return False
        finally:
            cur.close()
            conn.close()
            
            
            
    @staticmethod
    def buscar_solicitacao_por_numero(n_solicitacao):
        '''Busca uma solicitação especifica por numero'''
        
        conn = get_connection()
        if conn is None:
            return None
        
        try:
            cur = conn.cursor()
            cur.execute(
                "SELECT N_SOLICITACAO, DT_ABERTURA, AREA, STATUS, RESPONSAVEL, DESCRICAO, DT_CONCLUSAO FROM SOLICITACAO WHERE N_SOLICITACAO = %s",
                (n_solicitacao)
            )
            
            resultado = cur.fetchone()
            if resultado:
                return Solicitacao(*resultado)
            return None
        
        except Exception as e:
            print(f"Erro ao buscar solicitação: {e}")
            return None
        finally:
            cur.close()
            conn.close()
            
            
# Teste rápido
if __name__ == "__main__":
    print("🧪 Testando Serviço de Solicitações...")
    
    # Teste de criação de solicitação
    SolicitacaoService.criar_solicitação(
        1001,
        "Elétrica",
        "Robson Ferreira",
        "Trocar lâmpadas queimadas oficina piso 1"
    )
    
    # Teste de listagem
    solicitacoes = SolicitacaoService.listar_solicitacoes()
    print(f"📋 Solicitações cadastradas: {len(solicitacoes)}")
    for sol in solicitacoes:
        print(f"  - #{sol.n_solicitacao}: {sol.descricao} [{sol.status}]")
