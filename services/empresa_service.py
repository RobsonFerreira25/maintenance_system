'''
SERVIÇOS DE EMPRESA - Gerencia tudo relacionado a empresas e filiais
Aqui fica a LÓGICA DE NEGÓCIO para empresas
'''


from database.database import get_connection
from database.models import Empresa, Filial, Endereco

class EmpresaService:
    '''Serviço para Gerenciar empresas e filiais'''
    
    @staticmethod
    def criar_empresa(cnpj, razao_social):
        '''
        Cria uma nova empresa no siatema
        Retorna True se sucesso, False se erro
        '''
        conn = get_connection()
        if conn is None:
            return False
        
        try:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO EMPRESA (CNPJ, RAZAO_SOCIAL) VALUES (%s, %s)",
                (cnpj, razao_social)
            )
            conn.commit()
            print(f"Empresa {razao_social} criada com sucesso!")
            return True
        
        except Exception as e:
            print(f"Erro ao criar empresa {e}")
            conn.rollback()
            return False
        finally:
            cur.close()
            conn.close()
            
            
            
    @staticmethod
    def listar_empresas():
        '''Lista todas as empresas do sistema
           Retorna a lista de objetos Empresas
        '''
        conn = get_connection()
        if conn is None:
          return[]
        
        try:
            cur = conn.cursor()
            cur.execute(
                "SELECT CNPJ, RAZAO_SOCIAL FROM EMPRESA ORDER BY RAZAO_SOCIAL")
            
            empresas = []
            for cnpj, razao_social in cur.fetchall():
                empresas.append(Empresa(cnpj, razao_social))
            
            return empresas
        
        except Exception as e:
            print(f"Erro ao listar empresas {e}")
            return []
        finally:
            cur.close()
            conn.close()
            
            
            
    @staticmethod
    def criar_filial(cnpj_id, nome):
        '''
        Cria uma nova filial
        '''
        conn = get_connection()
        if conn is None:
            return False
        
        try:
            cur = conn.cursor()
            cur.execute(
                "INSERT FILIAIS INTO (CNPJ_ID, NOME) VALUES (%s, %s)",
                (cnpj_id, nome)
            )
            
            conn.commit()
            print(f"Filial {nome} criada com sucesso!")
            return True
        
        except Exception as e:
            print(f" Erro ao criar filial: {e}")
            conn.rollback()
            return False
        finally:
            cur.close()
            conn.close()
            
            
    @staticmethod
    def listar_filiais():
        '''
        Lista todas as filiais do sistema
        '''
        conn = get_connection()
        if conn is None:
            return []
        
        
        try:
            cur = conn.cursor()
            cur.execute(
                "SELECT CNPJ_ID, NOME FROM FILIAIS ORDER BY NOME")
            
            filiais = []
            for cnpj_id, nome in cur.fetchall():
                filiais.append(Filial(cnpj_id, nome))
            
            return filiais
        
        except Exception as e:
            print(f"Erro ao listar filiais {e}")
            return []
        
        finally:
            cur.close()
            conn.close()
            
            
            
class EnderecoService:
    '''Serviço para gerenciar endereços'''
    
    @staticmethod
    def criar_endereco(rua, numero, bairro):
        '''
        Cria um novo endereço
        Retorna o ID do endereço ou None se erro
        '''
        conn = get_connection()
        if conn is None:
            return None
        
        try:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO ENDERECO (RUA< NUMERO, BAIRRO) VALUES (%s, %s, %s) RETURNING ID ENDERECO",
                (rua, numero, bairro)
            )
            
            endereco_id = cur.fetchone()[0]
            conn.commit()
            print(f"Endereço criado com ID: {endereco_id}")
            return endereco_id
        
        except Exception as e:
            print(f"Erro ao criar endereço: {e}")
            conn.rollback()
            return None
        finally:
            cur.close()
            conn.close()
            
            
            
    @staticmethod
    def listar_endereco():
        '''Lista todos os endereços'''
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
            print(f"Erro ao listar enderecos: {e}")
            return []
        finally:
            cur.close()
            conn.close()
            
            
            
# Teste rápido do serviço
if __name__ == "__main__":
    print("🧪 Testando Serviço de Empresas...")
    
# Teste de criação de empresa
EmpresaService.criar_empresa("12.345.678/0001-90", "Empresa Teste Ltda")

# Teste de Listagem
empresas  = EmpresaService.listar_empresas()
print(f"📊 Empresas cadastradas: {len(empresas)}")
for emp in empresas:
    print(f"  - {emp.razao_social} ({emp.cnpj})")