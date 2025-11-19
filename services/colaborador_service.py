# 📄 services/colaborador_service.py - ADICIONAR CACHE

from database.database import get_connection, DatabaseConnection
from database.models import Colaborador
from utils.cache_manager import cache_manager  # ← NOVO IMPORT

class ColaboradorService:
    """Serviço para gerenciar colaboradores e suas aptidões"""
    
    @staticmethod
    def criar_colaborador(matricula, nome, cargo):
        """
        Cadastra um novo colaborador
        VERSÃO MELHORADA: Invalida cache após criação
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
                
                # INVALIDAR CACHE - dados mudaram
                cache_manager.delete('colaboradores_lista')
                cache_manager.delete('colaboradores_nomes')
                
                return True
                
        except Exception as e:
            print(f"❌ Erro ao criar colaborador: {e}")
            return False
    
    @staticmethod
    def listar_colaboradores():
        """
        Lista todos os colaboradores
        VERSÃO COM CACHE: Reduz queries ao banco
        """
        # Tentar obter do cache primeiro
        cache_key = 'colaboradores_lista'
        cached_data = cache_manager.get(cache_key)
        
        if cached_data is not None:
            print("📦 Colaboradores carregados do cache")
            return cached_data
        
        try:
            with DatabaseConnection() as conn:
                if conn is None:
                    return []
                
                cur = conn.cursor()
                cur.execute("SELECT MATRICULA, NOME, CARGO FROM COLABORADORES ORDER BY NOME")
                
                colaboradores = []
                for matricula, nome, cargo in cur.fetchall():
                    colaboradores.append(Colaborador(matricula, nome, cargo))
                
                # Armazenar no cache
                cache_manager.set(cache_key, colaboradores, cache_manager.TTL_COLABORADORES)
                print(f"✅ {len(colaboradores)} colaboradores carregados do banco e armazenados no cache")
                
                return colaboradores
                
        except Exception as e:
            print(f"❌ Erro ao listar colaboradores: {e}")
            return []
    
    @staticmethod
    def listar_nomes_colaboradores():
        """
        Retorna apenas os nomes dos colaboradores
        VERSÃO COM CACHE: Otimizado para combobox
        """
        # Tentar obter do cache primeiro
        cache_key = 'colaboradores_nomes'
        cached_data = cache_manager.get(cache_key)
        
        if cached_data is not None:
            print("📦 Nomes de colaboradores carregados do cache")
            return cached_data
        
        try:
            with DatabaseConnection() as conn:
                if conn is None:
                    return []
                
                cur = conn.cursor()
                cur.execute("SELECT NOME FROM COLABORADORES ORDER BY NOME")
                
                # Retorna lista simples com apenas os nomes
                nomes = [row[0] for row in cur.fetchall()]
                
                # Armazenar no cache
                cache_manager.set(cache_key, nomes, cache_manager.TTL_COLABORADORES)
                print(f"✅ {len(nomes)} nomes de colaboradores carregados do banco e armazenados no cache")
                
                return nomes
                
        except Exception as e:
            print(f"❌ Erro ao listar nomes de colaboradores: {e}")
            return []
    
    @staticmethod
    def deletar_colaborador(matricula):
        """
        Deleta um colaborador pela matrícula
        VERSÃO MELHORADA: Invalida cache após deleção
        """
        try:
            # CORREÇÃO: Garantir que matrícula seja inteiro
            matricula_int = int(matricula)
            
            with DatabaseConnection() as conn:
                if conn is None:
                    return False
                
                cur = conn.cursor()
                cur.execute("DELETE FROM COLABORADORES WHERE MATRICULA = %s", (matricula_int,))
                conn.commit()
                
                if cur.rowcount > 0:
                    print(f"✅ Colaborador {matricula_int} deletado com sucesso!")
                    
                    # INVALIDAR CACHE - dados mudaram
                    cache_manager.delete('colaboradores_lista')
                    cache_manager.delete('colaboradores_nomes')
                    
                    return True
                else:
                    print(f"⚠️ Colaborador {matricula_int} não encontrado")
                    return False
                    
        except Exception as e:
            print(f"❌ Erro ao deletar colaborador: {e}")
            return False