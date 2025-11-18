# 📄 services/colaborador_service.py (VERSÃO CORRIGIDA)
"""
SERVIÇO DE COLABORADORES - Gerencia técnicos e suas habilidades
VERSÃO CORRIGIDA - Problema de tipagem
"""

from database.database import get_connection
from database.models import Colaborador

class ColaboradorService:
    """Serviço para gerenciar colaboradores e suas aptidões"""
    
    @staticmethod
    def criar_colaborador(matricula, nome, cargo):
        """
        Cadastra um novo colaborador
        CORREÇÃO: Garantir tipo inteiro para matrícula
        """
        conn = get_connection()
        if conn is None:
            return False
        
        try:
            # CORREÇÃO: Garantir que matrícula seja inteiro
            matricula_int = int(matricula)
            
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO COLABORADORES (MATRICULA, NOME, CARGO) VALUES (%s, %s, %s)",
                (matricula_int, nome, cargo)
            )
            conn.commit()
            print(f"✅ Colaborador {nome} cadastrado com sucesso!")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao criar colaborador: {e}")
            conn.rollback()
            return False
        finally:
            cur.close()
            conn.close()
    
    @staticmethod
    def deletar_colaborador(matricula):
        """
        Deleta um colaborador pela matrícula
        CORREÇÃO: Garantir tipo inteiro
        """
        conn = get_connection()
        if conn is None:
            return False
        
        try:
            # CORREÇÃO: Garantir que matrícula seja inteiro
            matricula_int = int(matricula)
            
            cur = conn.cursor()
            cur.execute("DELETE FROM COLABORADORES WHERE MATRICULA = %s", (matricula_int,))
            conn.commit()
            
            if cur.rowcount > 0:
                print(f"✅ Colaborador {matricula_int} deletado com sucesso!")
                return True
            else:
                print(f"⚠️ Colaborador {matricula_int} não encontrado")
                return False
                
        except Exception as e:
            print(f"❌ Erro ao deletar colaborador: {e}")
            conn.rollback()
            return False
        finally:
            cur.close()
            conn.close()
    
    @staticmethod
    def listar_colaboradores():
        """
        Lista todos os colaboradores
        """
        conn = get_connection()
        if conn is None:
            return []
        
        try:
            cur = conn.cursor()
            cur.execute("SELECT MATRICULA, NOME, CARGO FROM COLABORADORES ORDER BY NOME")
            
            colaboradores = []
            for matricula, nome, cargo in cur.fetchall():
                colaboradores.append(Colaborador(matricula, nome, cargo))
            
            return colaboradores
            
        except Exception as e:
            print(f"❌ Erro ao listar colaboradores: {e}")
            return []
        finally:
            cur.close()
            conn.close()
    
    @staticmethod
    def listar_nomes_colaboradores():
        """
        Retorna apenas os nomes dos colaboradores
        Para usar no combobox de responsáveis
        """
        conn = get_connection()
        if conn is None:
            return []
        
        try:
            cur = conn.cursor()
            cur.execute("SELECT NOME FROM COLABORADORES ORDER BY NOME")
            
            # Retorna lista simples com apenas os nomes
            nomes = [row[0] for row in cur.fetchall()]
            return nomes
            
        except Exception as e:
            print(f"❌ Erro ao listar nomes de colaboradores: {e}")
            return []
        finally:
            cur.close()
            conn.close()
    
    @staticmethod
    def buscar_colaborador_por_nome(nome):
        """
        Busca um colaborador pelo nome exato
        """
        conn = get_connection()
        if conn is None:
            return None
        
        try:
            cur = conn.cursor()
            cur.execute(
                "SELECT MATRICULA, NOME, CARGO FROM COLABORADORES WHERE NOME = %s",
                (nome,)
            )
            
            resultado = cur.fetchone()
            if resultado:
                return Colaborador(*resultado)
            return None
            
        except Exception as e:
            print(f"❌ Erro ao buscar colaborador: {e}")
            return None
        finally:
            cur.close()
            conn.close()
    
    @staticmethod
    def adicionar_aptidao_colaborador(matricula, id_aptidao):
        """
        Adiciona uma aptidão a um colaborador
        CORREÇÃO: Garantir tipo inteiro para matrícula
        """
        conn = get_connection()
        if conn is None:
            return False
        
        try:
            # CORREÇÃO: Garantir que matrícula seja inteiro
            matricula_int = int(matricula)
            
            cur = conn.cursor()
            cur.execute(
                """INSERT INTO POSSUI_COLABORADOR_APTIDAO 
                (FK_COLABORADORES_MATRICULA, FK_APTIDOES_ID_APTIDAO) 
                VALUES (%s, %s)""",
                (matricula_int, id_aptidao)
            )
            conn.commit()
            print(f"✅ Aptidão {id_aptidao} adicionada ao colaborador {matricula_int}")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao adicionar aptidão: {e}")
            conn.rollback()
            return False
        finally:
            cur.close()
            conn.close()
    
    @staticmethod
    def listar_aptidoes_disponiveis():
        """
        Lista todas as aptidões disponíveis no sistema
        """
        conn = get_connection()
        if conn is None:
            return []
        
        try:
            cur = conn.cursor()
            cur.execute("SELECT ID_APTIDAO FROM APTIDOES ORDER BY ID_APTIDAO")
            
            aptidoes = [row[0] for row in cur.fetchall()]
            return aptidoes
            
        except Exception as e:
            print(f"❌ Erro ao listar aptidões: {e}")
            return []
        finally:
            cur.close()
            conn.close()