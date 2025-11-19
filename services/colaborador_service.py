# 📄 services/colaborador_service.py (VERSÃO CORRIGIDA)
"""
SERVIÇO DE COLABORADORES - Gerencia técnicos e suas habilidades
VERSÃO CORRIGIDA - Problema de tipagem
"""

from database.database import get_connection, DatabaseConnection  # ← ADICIONAR DatabaseConnection
from database.models import Colaborador

class ColaboradorService:
    """Serviço para gerenciar colaboradores e suas aptidões"""
    
    @staticmethod
    def criar_colaborador(matricula, nome, cargo):
        """
        Cadastra um novo colaborador
        VERSÃO MELHORADA: Usa context manager para conexão
        """
        try:
            # CORREÇÃO: Garantir que matrícula seja inteiro
            matricula_int = int(matricula)
        
            # USANDO CONTEXT MANAGER - conexão fechada automaticamente
            with DatabaseConnection() as conn:
                if conn is None:
                    return False
            
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
            return False
    
    @staticmethod
    def deletar_colaborador(matricula):
        """
        Deleta um colaborador pela matrícula
        VERSÃO CORRIGIDA: Melhor tratamento de erros
        """
        try:
            # CORREÇÃO: Garantir que matrícula seja inteiro
            matricula_int = int(matricula)
            
            # USANDO CONTEXT MANAGER CORRIGIDO
            with DatabaseConnection() as conn:
                if conn is None:
                    return False
                
                cur = conn.cursor()
                cur.execute("DELETE FROM COLABORADORES WHERE MATRICULA = %s", (matricula_int,))
                conn.commit()  # Commit dentro do context manager
                
                if cur.rowcount > 0:
                    print(f"✅ Colaborador {matricula_int} deletado com sucesso!")
                    return True
                else:
                    print(f"⚠️ Colaborador {matricula_int} não encontrado")
                    return False
                
        except Exception as e:
            print(f"❌ Erro ao deletar colaborador: {e}")
            # NÃO PRECISA DE rollback - o context manager cuida disso
            return False
        
    
    @staticmethod
    def listar_colaboradores():
        """
        Lista todos os colaboradores
        VERSÃO MELHORADA: Conexão automática
        """
        try:
            with DatabaseConnection() as conn:
                if conn is None:
                    return []
            
                cur = conn.cursor()
                cur.execute("SELECT MATRICULA, NOME, CARGO FROM COLABORADORES ORDER BY NOME")
            
                colaboradores = []
                for matricula, nome, cargo in cur.fetchall():
                    colaboradores.append(Colaborador(matricula, nome, cargo))
            
                return colaboradores
            
        except Exception as e:
            print(f"❌ Erro ao listar colaboradores: {e}")
            return []
    
    @staticmethod
    def listar_nomes_colaboradores():
        """
        Retorna apenas os nomes dos colaboradores
        VERSÃO MELHORADA: Mais simples e segura
        """
        try:
            with DatabaseConnection() as conn:
                if conn is None:
                    return []
                
                cur = conn.cursor()
                cur.execute("SELECT NOME FROM COLABORADORES ORDER BY NOME")
                
                # Retorna lista simples com apenas os nomes
                nomes = [row[0] for row in cur.fetchall()]
                return nomes
                
        except Exception as e:
            print(f"❌ Erro ao listar nomes de colaboradores: {e}")
            return []
    
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