'''SERVIÇO DE COLABORADORES - Gerencia técnico e suas habilidades'''

import sys
import os

# Adiciona o diretório raiz do projeto ao Python Path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.database import get_connection
from database.models import Colaborador


class ColaboradorService:
    '''Serviço para gerenciar colaboradores e suas aptidões'''
    
    @staticmethod
    def criar_colaborador(matricula, nome, cargo):
        '''Cadastra um novo colaborador'''
        
        conn = get_connection()
        if conn is None:
            return False
        
        try:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO COLABORADORES (MATRICULA, NOME, CARGO) VALUES (%s, %s, %s)",
                (matricula, nome, cargo)
            )
            conn.commit()
            
            print(f"Colaborador {nome} cadastrado com sucesso!")
            return True
        
        except Exception as e:
            print(f"Erro ao cadastrar colaborador: {e}")
            conn.rollback()
            return False
        
        finally:
            cur.close()
            conn.close()
            
            
    @staticmethod
    def listar_colaboradores():
        '''Lista todos os colaboradores'''
        
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
            print(f"Erro ao listar colaboradores: {e}")
            return []
        
        finally:
            cur.close()
            conn.close()
            
            
            
    @staticmethod
    def adicinar_aptidao_colaborador(matricula, id_aptidao):
        '''Adiciona uma aptidão a um colaborador'''
        
        conn = get_connection()
        if conn is None:
            return False
        
        try:
            cur = conn.cursor()
            cur.execute(
                """
                INSERT INTO POSSUI_COLABORADOR_APTIDAO
                (FK_COLABORADORES_MATRICULA, FK_APTIDOES_ID_APTIDAO)
                VALUES (%s, %s)""",
                (matricula, id_aptidao)
            )
            conn.commit()
            print(f"Aptidão {id_aptidao} adicionado ao colaborador {matricula}")
            return True
        
        except Exception as e:
            print(f"Erro ao adicionar aptidão: {e}")
            conn.rollback()
            return False
        
        finally:
            cur.close()
            conn.close()
            
    @staticmethod
    def listar_aptidoes_disponiveis():
        '''Lista todas as aptidoes disponiveis no sistema'''
        
        conn = get_connection()
        if conn is None:
            return []
        
        try:
            cur = conn.cursor()
            cur.execute("SELECT ID_APTIDAO FROM APTIDOES ORDER BY ID_APTIDAO")
            
            aptidoes = [row[0] for row in cur.fetchall()]
            return aptidoes
        
        except Exception as e:
            print(f"Erro ao lista aptidoes: {e}")
            return []
        finally:
            cur.close()
            conn.close()
            
            
# Teste rápido
if __name__ =="__main__":
    print("🧪 Testando Serviço de Colaboradores...")
    
    
    # Teste d criação de colaboradores
    ColaboradorService.criar_colaborador(1001, "Robson Ferreira", "Técnico Eletricista")
    
    
    # Teste de listagem
    colaboradores = ColaboradorService.listar_colaboradores()
    print(f"👥 Colaboradores cadastrados: {len(colaboradores)}")
    for colab in colaboradores:
        print(f"  - {colab.nome} (Mat: {colab.matricula}) - {colab.cargo}")