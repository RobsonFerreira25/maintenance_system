# 📄 services/solicitacao_service.py (VERSÃO COM NÚMERO AUTOMÁTICO)
"""
SERVIÇO DE SOLICITAÇÕES - O coração do sistema de manutenção
VERSÃO COM NÚMERO AUTOMÁTICO E FUNÇÕES DE RELATÓRIO
"""

from database.database import get_connection
from database.models import Solicitacao
from datetime import datetime

class SolicitacaoService:
    """Serviço para gerenciar solicitações de manutenção"""
    
    @staticmethod
    def obter_proximo_numero_os():
        """
        NOVO: Obtém o próximo número de OS automaticamente
        """
        conn = get_connection()
        if conn is None:
            return 1  # Retorna 1 se não conseguir conectar
        
        try:
            cur = conn.cursor()
            cur.execute("SELECT MAX(N_SOLICITACAO) FROM SOLICITACAO")
            resultado = cur.fetchone()
            
            if resultado[0] is None:
                return 1  # Primeira OS
            else:
                return resultado[0] + 1  # Próximo número
                
        except Exception as e:
            print(f"❌ Erro ao obter próximo número: {e}")
            return 1
        finally:
            cur.close()
            conn.close()
    
    @staticmethod
    def criar_solicitacao_automatica(area, responsavel, descricao, filial=None, status="Aberta"):
        """
        NOVO: Cria solicitação com número automático
        """
        n_solicitacao = SolicitacaoService.obter_proximo_numero_os()
        return SolicitacaoService.criar_solicitacao(n_solicitacao, area, responsavel, descricao, filial, status)
    
    @staticmethod
    def criar_solicitacao(n_solicitacao, area, responsavel, descricao, filial=None, status="Aberta"):
        """
        Cria uma nova solicitação de manutenção
        """
        conn = get_connection()
        if conn is None:
            return False
        
        try:
            # Garantir que número seja inteiro
            n_solicitacao_int = int(n_solicitacao)
            data_abertura = datetime.now().date()
            
            cur = conn.cursor()
            cur.execute(
                """INSERT INTO SOLICITACAO 
                (N_SOLICITACAO, DT_ABERTURA, AREA, STATUS, RESPONSAVEL, DESCRICAO, FILIAL) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                (n_solicitacao_int, data_abertura, area, status, responsavel, descricao, filial)
            )
            
            conn.commit()
            print(f"✅ Solicitação #{n_solicitacao_int} criada com sucesso!")
            return n_solicitacao_int  # Retorna o número da OS criada
            
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
        """
        conn = get_connection()
        if conn is None:
            return False
        
        try:
            # Garantir que número seja inteiro
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
        VERSÃO SIMPLIFICADA: Busca direto da tabela SOLICITACAO
        """
        conn = get_connection()
        if conn is None:
            return []
        
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT N_SOLICITACAO, DT_ABERTURA, AREA, STATUS, 
                       RESPONSAVEL, DESCRICAO, DT_CONCLUSAO, FILIAL
                FROM SOLICITACAO 
                ORDER BY DT_ABERTURA DESC
            """)
            
            solicitacoes = []
            for (n_solicitacao, dt_abertura, area, status, responsavel, 
                 descricao, dt_conclusao, filial) in cur.fetchall():
                
                # Buscar nome da filial se existir CNPJ
                nome_filial = None
                if filial:
                    try:
                        cur_filial = conn.cursor()
                        cur_filial.execute("SELECT NOME FROM FILIAIS WHERE CNPJ_IND_ = %s", (filial,))
                        resultado_filial = cur_filial.fetchone()
                        if resultado_filial:
                            nome_filial = resultado_filial[0]
                        cur_filial.close()
                    except:
                        nome_filial = filial  # Usa o CNPJ se não encontrar nome
                
                solicitacoes.append(Solicitacao(
                    n_solicitacao, dt_abertura, area, status, responsavel, 
                    descricao, dt_conclusao, filial, nome_filial
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
        """
        conn = get_connection()
        if conn is None:
            return False
        
        try:
            # Garantir que número seja inteiro
            n_solicitacao_int = int(n_solicitacao)
            
            cur = conn.cursor()
            
            # Status que exigem data de conclusão
            status_com_conclusao = ["concluída", "cancelada"]
            
            if novo_status.lower() in status_com_conclusao:
                data_conclusao = datetime.now().date()
                cur.execute(
                    "UPDATE SOLICITACAO SET STATUS = %s, DT_CONCLUSAO = %s WHERE N_SOLICITACAO = %s",
                    (novo_status, data_conclusao, n_solicitacao_int)
                )
            else:
                # Status que não tem data de conclusão
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
        """
        conn = get_connection()
        if conn is None:
            return None
        
        try:
            # Garantir que número seja inteiro
            n_solicitacao_int = int(n_solicitacao)
            
            cur = conn.cursor()
            cur.execute(
                """SELECT N_SOLICITACAO, DT_ABERTURA, AREA, STATUS, 
                          RESPONSAVEL, DESCRICAO, DT_CONCLUSAO, FILIAL
                   FROM SOLICITACAO 
                   WHERE N_SOLICITACAO = %s""",
                (n_solicitacao_int,)
            )
            
            resultado = cur.fetchone()
            if resultado:
                # Buscar nome da filial
                nome_filial = None
                if resultado[7]:  # FILIAL
                    try:
                        cur_filial = conn.cursor()
                        cur_filial.execute("SELECT NOME FROM FILIAIS WHERE CNPJ_IND_ = %s", (resultado[7],))
                        resultado_filial = cur_filial.fetchone()
                        if resultado_filial:
                            nome_filial = resultado_filial[0]
                        cur_filial.close()
                    except:
                        nome_filial = resultado[7]
                
                return Solicitacao(*resultado[:7], resultado[7], nome_filial)
            return None
            
        except Exception as e:
            print(f"❌ Erro ao buscar solicitação: {e}")
            return None
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def obter_estatisticas_solicitacoes():
        """
        Retorna estatísticas detalhadas das solicitações
        Para usar no dashboard
        """
        conn = get_connection()
        if conn is None:
            return {}
        
        try:
            cur = conn.cursor()
            
            # Contagem por status
            cur.execute("""
                SELECT STATUS, COUNT(*) as quantidade 
                FROM SOLICITACAO 
                GROUP BY STATUS
            """)
            
            estatisticas = {}
            for status, quantidade in cur.fetchall():
                estatisticas[status.lower()] = quantidade
            
            # Total geral
            cur.execute("SELECT COUNT(*) FROM SOLICITACAO")
            estatisticas['total'] = cur.fetchone()[0]
            
            return estatisticas
            
        except Exception as e:
            print(f"❌ Erro ao obter estatísticas: {e}")
            return {}
        finally:
            cur.close()
            conn.close()