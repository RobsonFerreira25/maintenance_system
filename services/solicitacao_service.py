# 📄 services/solicitacao_service.py (VERSÃO CORRIGIDA)
"""
SERVIÇO DE SOLICITAÇÕES - O coração do sistema de manutenção
VERSÃO CORRIGIDA - Problema de tipagem
"""

from database.database import get_connection
from database.models import Solicitacao
from datetime import datetime

class SolicitacaoService:
    """Serviço para gerenciar solicitações de manutenção"""
    
    @staticmethod
    def criar_solicitacao(n_solicitacao, area, responsavel, descricao, status="Aberta"):
        """
        Cria uma nova solicitação de manutenção
        CORREÇÃO: Garantir tipos corretos
        """
        conn = get_connection()
        if conn is None:
            return False
        
        try:
            # CORREÇÃO: Garantir que número seja inteiro
            n_solicitacao_int = int(n_solicitacao)
            data_abertura = datetime.now().date()
            
            cur = conn.cursor()
            cur.execute(
                """INSERT INTO SOLICITACAO 
                (N_SOLICITACAO, DT_ABERTURA, AREA, STATUS, RESPONSAVEL, DESCRICAO) 
                VALUES (%s, %s, %s, %s, %s, %s)""",
                (n_solicitacao_int, data_abertura, area, status, responsavel, descricao)
            )
            conn.commit()
            print(f"✅ Solicitação #{n_solicitacao_int} criada com sucesso!")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao criar solicitação: {e}")
            conn.rollback()
            return False
        finally:
            cur.close()
            conn.close()
    
    @staticmethod
    def deletar_solicitacao(n_solicitacao):
        """
        Deleta uma solicitação pelo número
        CORREÇÃO: Garantir tipo inteiro
        """
        conn = get_connection()
        if conn is None:
            return False
        
        try:
            # CORREÇÃO: Garantir que número seja inteiro
            n_solicitacao_int = int(n_solicitacao)
            
            cur = conn.cursor()
            cur.execute("DELETE FROM SOLICITACAO WHERE N_SOLICITACAO = %s", (n_solicitacao_int,))
            conn.commit()
            
            if cur.rowcount > 0:
                print(f"✅ Solicitação #{n_solicitacao_int} deletada com sucesso!")
                return True
            else:
                print(f"⚠️ Solicitação #{n_solicitacao_int} não encontrada")
                return False
                
        except Exception as e:
            print(f"❌ Erro ao deletar solicitação: {e}")
            conn.rollback()
            return False
        finally:
            cur.close()
            conn.close()
    
    @staticmethod
    def listar_solicitacoes():
        """
        Lista todas as solicitações
        """
        conn = get_connection()
        if conn is None:
            return []
        
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT N_SOLICITACAO, DT_ABERTURA, AREA, STATUS, RESPONSAVEL, DESCRICAO, DT_CONCLUSAO 
                FROM SOLICITACAO 
                ORDER BY DT_ABERTURA DESC
            """)
            
            solicitacoes = []
            for n_solicitacao, dt_abertura, area, status, responsavel, descricao, dt_conclusao in cur.fetchall():
                solicitacoes.append(Solicitacao(
                    n_solicitacao, dt_abertura, area, status, responsavel, descricao, dt_conclusao
                ))
            
            return solicitacoes
            
        except Exception as e:
            print(f"❌ Erro ao listar solicitações: {e}")
            return []
        finally:
            cur.close()
            conn.close()
    
    @staticmethod
    def atualizar_status_solicitacao(n_solicitacao, novo_status):
        """
        Atualiza o status de uma solicitação
        CORREÇÃO: Garantir tipo inteiro
        """
        conn = get_connection()
        if conn is None:
            return False
        
        try:
            # CORREÇÃO: Garantir que número seja inteiro
            n_solicitacao_int = int(n_solicitacao)
            
            cur = conn.cursor()
            
            if novo_status.lower() == "concluída":
                data_conclusao = datetime.now().date()
                cur.execute(
                    "UPDATE SOLICITACAO SET STATUS = %s, DT_CONCLUSAO = %s WHERE N_SOLICITACAO = %s",
                    (novo_status, data_conclusao, n_solicitacao_int)
                )
            else:
                cur.execute(
                    "UPDATE SOLICITACAO SET STATUS = %s, DT_CONCLUSAO = NULL WHERE N_SOLICITACAO = %s",
                    (novo_status, n_solicitacao_int)
                )
            
            conn.commit()
            print(f"✅ Status da solicitação #{n_solicitacao_int} atualizado para: {novo_status}")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao atualizar solicitação: {e}")
            conn.rollback()
            return False
        finally:
            cur.close()
            conn.close()
    
    @staticmethod
    def buscar_solicitacao_por_numero(n_solicitacao):
        """
        Busca uma solicitação específica pelo número
        CORREÇÃO: Garantir tipo inteiro
        """
        conn = get_connection()
        if conn is None:
            return None
        
        try:
            # CORREÇÃO: Garantir que número seja inteiro
            n_solicitacao_int = int(n_solicitacao)
            
            cur = conn.cursor()
            cur.execute(
                "SELECT N_SOLICITACAO, DT_ABERTURA, AREA, STATUS, RESPONSAVEL, DESCRICAO, DT_CONCLUSAO FROM SOLICITACAO WHERE N_SOLICITACAO = %s",
                (n_solicitacao_int,)
            )
            
            resultado = cur.fetchone()
            if resultado:
                return Solicitacao(*resultado)
            return None
            
        except Exception as e:
            print(f"❌ Erro ao buscar solicitação: {e}")
            return None
        finally:
            cur.close()
            conn.close()