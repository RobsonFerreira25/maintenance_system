# 📄 services/empresa_service.py (ATUALIZADO COM DELETE)
"""
SERVIÇO DE EMPRESAS - Gerencia tudo relacionado a empresas e filiais
VERSÃO COM FUNÇÕES DE DELETE
"""

from database.database import get_connection, DatabaseConnection
from database.models import Empresa, Filial, Endereco

class EmpresaService:
    """Serviço para gerenciar empresas e filiais"""
    
    @staticmethod
    def criar_empresa(cnpj, razao_social):
        """
        Cria uma nova empresa no sistema
        Retorna True se sucesso, False se erro
        """
        conn = get_connection()
        if conn is None:
            return False# 📄 services/empresa_service.py (VERSÃO CORRIGIDA)
"""
SERVIÇO DE EMPRESAS - Gerencia tudo relacionado a empresas e filiais
VERSÃO CORRIGIDA - Problema de tipagem CNPJ
"""

from database.database import get_connection
from database.models import Empresa, Filial, Endereco

class EmpresaService:
    """Serviço para gerenciar empresas e filiais"""
    
    @staticmethod
    def criar_empresa(cnpj, razao_social):
        """
        Cria uma nova empresa no sistema
        CORREÇÃO: CNPJ sempre como string
        """
        conn = get_connection()
        if conn is None:
            return False
        
        try:
            # CORREÇÃO: Garantir que CNPJ seja string
            cnpj_str = str(cnpj).strip()
            
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO EMPRESA (CNPJ, RAZAO_SOCIAL) VALUES (%s, %s)",
                (cnpj_str, razao_social)
            )
            conn.commit()
            print(f"✅ Empresa {razao_social} criada com sucesso!")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao criar empresa: {e}")
            conn.rollback()
            return False
        finally:
            cur.close()
            conn.close()
    
    @staticmethod
    def deletar_empresa(cnpj):
        """
        Deleta uma empresa pelo CNPJ
        VERSÃO CORRIGIDA: Usa context manager
        """
        try:
            # CORREÇÃO: Garantir que CNPJ seja string
            cnpj_str = str(cnpj).strip()
            
            with DatabaseConnection() as conn:
                if conn is None:
                    return False
                
                cur = conn.cursor()
                cur.execute("DELETE FROM EMPRESA WHERE CNPJ = %s", (cnpj_str,))
                conn.commit()
                
                if cur.rowcount > 0:
                    print(f"✅ Empresa {cnpj_str} deletada com sucesso!")
                    return True
                else:
                    print(f"⚠️ Empresa {cnpj_str} não encontrada")
                    return False
                    
        except Exception as e:
            print(f"❌ Erro ao deletar empresa: {e}")
            return False
    
    @staticmethod
    def listar_empresas():
        """
        Lista todas as empresas do sistema
        """
        conn = get_connection()
        if conn is None:
            return []
        
        try:
            cur = conn.cursor()
            cur.execute("SELECT CNPJ, RAZAO_SOCIAL FROM EMPRESA ORDER BY RAZAO_SOCIAL")
            
            empresas = []
            for cnpj, razao_social in cur.fetchall():
                empresas.append(Empresa(cnpj, razao_social))
            
            return empresas
            
        except Exception as e:
            print(f"❌ Erro ao listar empresas: {e}")
            return []
        finally:
            cur.close()
            conn.close()
    
    @staticmethod
    def criar_filial(cnpj_ind, nome):
        """
        Cria uma nova filial
        CORREÇÃO: CNPJ sempre como string
        """
        conn = get_connection()
        if conn is None:
            return False
        
        try:
            # CORREÇÃO: Garantir que CNPJ seja string
            cnpj_ind_str = str(cnpj_ind).strip()
            
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO FILIAIS (CNPJ_IND_, NOME) VALUES (%s, %s)",
                (cnpj_ind_str, nome)
            )
            conn.commit()
            print(f"✅ Filial {nome} criada com sucesso!")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao criar filial: {e}")
            conn.rollback()
            return False
        finally:
            cur.close()
            conn.close()
    
    @staticmethod
    def deletar_filial(cnpj_ind):
        """
        Deleta uma filial pelo CNPJ
        CORREÇÃO: CNPJ sempre como string
        """
        
        try:
            # CORREÇÃO: Garantir que CNPJ seja string
            cnpj_ind_str = str(cnpj_ind).strip()
            
            with DatabaseConnection as conn:
                if conn is None:
                    return False
            
            cur = conn.cursor()
            cur.execute("DELETE FROM FILIAIS WHERE CNPJ_IND_ = %s", (cnpj_ind_str,))
            conn.commit()
            
            if cur.rowcount > 0:
                print(f"✅ Filial {cnpj_ind_str} deletada com sucesso!")
                return True
            else:
                print(f"⚠️ Filial {cnpj_ind_str} não encontrada")
                return False
                
        except Exception as e:
            print(f"❌ Erro ao deletar filial: {e}")
            return False
        
    
    @staticmethod
    def listar_filiais():
        """
        Lista todas as filiais
        """
        conn = get_connection()
        if conn is None:
            return []
        
        try:
            cur = conn.cursor()
            cur.execute("SELECT CNPJ_IND_, NOME FROM FILIAIS ORDER BY NOME")
            
            filiais = []
            for cnpj_ind, nome in cur.fetchall():
                filiais.append(Filial(cnpj_ind, nome))
            
            return filiais
            
        except Exception as e:
            print(f"❌ Erro ao listar filiais: {e}")
            return []
        finally:
            cur.close()
            conn.close()

class EnderecoService:
    """Serviço para gerenciar endereços"""
    
    @staticmethod
    def criar_endereco(rua, numero, bairro):
        """
        Cria um novo endereço
        """
        conn = get_connection()
        if conn is None:
            return None
        
        try:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO ENDERECO (RUA, NUMERO, BAIRRO) VALUES (%s, %s, %s) RETURNING ID_ENDERECO",
                (rua, numero, bairro)
            )
            endereco_id = cur.fetchone()[0]
            conn.commit()
            print(f"✅ Endereço criado com ID: {endereco_id}")
            return endereco_id
            
        except Exception as e:
            print(f"❌ Erro ao criar endereço: {e}")
            conn.rollback()
            return None
        finally:
            cur.close()
            conn.close()
    
    @staticmethod
    def deletar_endereco(id_endereco):
        """
        Deleta um endereço pelo ID
        """
        conn = get_connection()
        if conn is None:
            return False
        
        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM ENDERECO WHERE ID_ENDERECO = %s", (id_endereco,))
            conn.commit()
            
            if cur.rowcount > 0:
                print(f"✅ Endereço {id_endereco} deletado com sucesso!")
                return True
            else:
                print(f"⚠️ Endereço {id_endereco} não encontrado")
                return False
                
        except Exception as e:
            print(f"❌ Erro ao deletar endereço: {e}")
            conn.rollback()
            return False
        finally:
            cur.close()
            conn.close()
    
    @staticmethod
    def listar_enderecos():
        """
        Lista todos os endereços
        """
        conn = get_connection()
        if conn is None:
            return []
        
        try:
            cur = conn.cursor()
            cur.execute("SELECT ID_ENDERECO, RUA, NUMERO, BAIRRO FROM ENDERECO ORDER BY RUA")
            
            enderecos = []
            for id_endereco, rua, numero, bairro in cur.fetchall():
                enderecos.append(Endereco(id_endereco, rua, numero, bairro))
            
            return enderecos
            
        except Exception as e:
            print(f"❌ Erro ao listar endereços: {e}")
            return []
        finally:
            cur.close()
            conn.close()
        
        try:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO EMPRESA (CNPJ, RAZAO_SOCIAL) VALUES (%s, %s)",
                (cnpj, razao_social)
            )
            conn.commit()
            print(f"✅ Empresa {razao_social} criada com sucesso!")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao criar empresa: {e}")
            conn.rollback()
            return False
        finally:
            cur.close()
            conn.close()
    
    @staticmethod
    def deletar_empresa(cnpj):
        """
        NOVO: Deleta uma empresa pelo CNPJ
        """
        conn = get_connection()
        if conn is None:
            return False
        
        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM EMPRESA WHERE CNPJ = %s", (cnpj,))
            conn.commit()
            
            if cur.rowcount > 0:
                print(f"✅ Empresa {cnpj} deletada com sucesso!")
                return True
            else:
                print(f"⚠️ Empresa {cnpj} não encontrada")
                return False
                
        except Exception as e:
            print(f"❌ Erro ao deletar empresa: {e}")
            conn.rollback()
            return False
        finally:
            cur.close()
            conn.close()
    
    @staticmethod
    def listar_empresas():
        """
        Lista todas as empresas do sistema
        Retorna lista de objetos Empresa
        """
        conn = get_connection()
        if conn is None:
            return []
        
        try:
            cur = conn.cursor()
            cur.execute("SELECT CNPJ, RAZAO_SOCIAL FROM EMPRESA ORDER BY RAZAO_SOCIAL")
            
            empresas = []
            for cnpj, razao_social in cur.fetchall():
                empresas.append(Empresa(cnpj, razao_social))
            
            return empresas
            
        except Exception as e:
            print(f"❌ Erro ao listar empresas: {e}")
            return []
        finally:
            cur.close()
            conn.close()
    
    @staticmethod
    def criar_filial(cnpj_ind, nome):
        """
        Cria uma nova filial
        """
        conn = get_connection()
        if conn is None:
            return False
        
        try:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO FILIAIS (CNPJ_IND_, NOME) VALUES (%s, %s)",
                (cnpj_ind, nome)
            )
            conn.commit()
            print(f"✅ Filial {nome} criada com sucesso!")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao criar filial: {e}")
            conn.rollback()
            return False
        finally:
            cur.close()
            conn.close()
    
    @staticmethod
    def deletar_filial(cnpj_ind):
        """
        NOVO: Deleta uma filial pelo CNPJ
        """
        conn = get_connection()
        if conn is None:
            return False
        
        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM FILIAIS WHERE CNPJ_IND_ = %s", (cnpj_ind,))
            conn.commit()
            
            if cur.rowcount > 0:
                print(f"✅ Filial {cnpj_ind} deletada com sucesso!")
                return True
            else:
                print(f"⚠️ Filial {cnpj_ind} não encontrada")
                return False
                
        except Exception as e:
            print(f"❌ Erro ao deletar filial: {e}")
            conn.rollback()
            return False
        finally:
            cur.close()
            conn.close()
    
    @staticmethod
    def listar_filiais():
        """
        Lista todas as filiais
        """
        conn = get_connection()
        if conn is None:
            return []
        
        try:
            cur = conn.cursor()
            cur.execute("SELECT CNPJ_IND_, NOME FROM FILIAIS ORDER BY NOME")
            
            filiais = []
            for cnpj_ind, nome in cur.fetchall():
                filiais.append(Filial(cnpj_ind, nome))
            
            return filiais
            
        except Exception as e:
            print(f"❌ Erro ao listar filiais: {e}")
            return []
        finally:
            cur.close()
            conn.close()

class EnderecoService:
    """Serviço para gerenciar endereços"""
    
    @staticmethod
    def criar_endereco(rua, numero, bairro):
        """
        Cria um novo endereço
        Retorna o ID do endereço criado ou None se erro
        """
        conn = get_connection()
        if conn is None:
            return None
        
        try:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO ENDERECO (RUA, NUMERO, BAIRRO) VALUES (%s, %s, %s) RETURNING ID_ENDERECO",
                (rua, numero, bairro)
            )
            endereco_id = cur.fetchone()[0]
            conn.commit()
            print(f"✅ Endereço criado com ID: {endereco_id}")
            return endereco_id
            
        except Exception as e:
            print(f"❌ Erro ao criar endereço: {e}")
            conn.rollback()
            return None
        finally:
            cur.close()
            conn.close()
    
    @staticmethod
    def deletar_endereco(id_endereco):
        """
        NOVO: Deleta um endereço pelo ID
        """
        conn = get_connection()
        if conn is None:
            return False
        
        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM ENDERECO WHERE ID_ENDERECO = %s", (id_endereco,))
            conn.commit()
            
            if cur.rowcount > 0:
                print(f"✅ Endereço {id_endereco} deletado com sucesso!")
                return True
            else:
                print(f"⚠️ Endereço {id_endereco} não encontrado")
                return False
                
        except Exception as e:
            print(f"❌ Erro ao deletar endereço: {e}")
            conn.rollback()
            return False
        finally:
            cur.close()
            conn.close()
    
    @staticmethod
    def listar_enderecos():
        """
        Lista todos os endereços
        """
        conn = get_connection()
        if conn is None:
            return []
        
        try:
            cur = conn.cursor()
            cur.execute("SELECT ID_ENDERECO, RUA, NUMERO, BAIRRO FROM ENDERECO ORDER BY RUA")
            
            enderecos = []
            for id_endereco, rua, numero, bairro in cur.fetchall():
                enderecos.append(Endereco(id_endereco, rua, numero, bairro))
            
            return enderecos
            
        except Exception as e:
            print(f"❌ Erro ao listar endereços: {e}")
            return []
        finally:
            cur.close()
            conn.close()