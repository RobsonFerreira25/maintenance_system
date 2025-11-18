# 📄 database/database.py (VERSÃO FINAL)
"""
MÓDULO DE ACESSO AO POSTGRESQL - VERSÃO FINAL
Sistema de Gestão de Manutenção
"""

import psycopg2
from config.settings import DB_CONFIG

def get_connection():
    '''
    Cria e retorna uma conexão com o PostgreSQL.
    Versão final com tratamento robusto de erros.
    '''
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        print("✅ Conexão com PostgreSQL estabelecida com sucesso!")
        return conn
    
    except psycopg2.OperationalError as e:
        print(f"❌ Erro de conexão com o banco: {e}")
        print("🔧 Verifique:")
        print("   - Servidor PostgreSQL está rodando")
        print("   - Credenciais no arquivo .env")
        print("   - Banco de dados existe")
        return None
    
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return None

#---------------------------------------------------------
# Função para criar todas as tabelas (VERSÃO MELHORADA)
#---------------------------------------------------------

def create_tables():
    '''
    Cria todas as tabelas necessárias no sistema de manutenção
    VERSÃO MELHORADA com as sugestões de robustez
    '''
    
    commands = [
        # --- TABELAS PRINCIPAIS ORIGINAIS ---
        """
        CREATE TABLE IF NOT EXISTS EMPRESA (
            CNPJ VARCHAR(20) PRIMARY KEY,
            RAZAO_SOCIAL VARCHAR(150) NOT NULL
        );
        """,

        """
        CREATE TABLE IF NOT EXISTS FILIAIS (
            CNPJ_IND_ VARCHAR(20) PRIMARY KEY,
            NOME VARCHAR(100) NOT NULL
        );
        """,

        """
        CREATE TABLE IF NOT EXISTS ENDERECO (
            ID_ENDERECO SERIAL PRIMARY KEY,
            RUA VARCHAR(150) NOT NULL,
            NUMERO INT,
            BAIRRO VARCHAR(100),
            UNIQUE(RUA, NUMERO, BAIRRO)
        );
        """,

        """
        CREATE TABLE IF NOT EXISTS SETOR_MANUT_ (
            NOME VARCHAR(100) PRIMARY KEY
        );
        """,

        """
        CREATE TABLE IF NOT EXISTS COLABORADORES (
            MATRICULA INT PRIMARY KEY,
            NOME VARCHAR(150),
            CARGO VARCHAR(100)
        );
        """,

        """
        CREATE TABLE IF NOT EXISTS APTIDOES (
            ID_APTIDAO VARCHAR(20) PRIMARY KEY,
            ELETRICA VARCHAR(5),
            HIDRAULICA VARCHAR(5),
            CIVIL VARCHAR(5),
            SERVICOS_GERAIS VARCHAR(5)
        );
        """,

        """
        CREATE TABLE IF NOT EXISTS SOLICITACAO (
            N_SOLICITACAO INT PRIMARY KEY,
            DT_ABERTURA DATE,
            AREA VARCHAR(100),
            STATUS VARCHAR(50),
            RESPONSAVEL VARCHAR(100),
            DESCRICAO TEXT,
            DT_CONCLUSAO DATE
        );
        """,

        # --- NOVAS TABELAS MELHORADAS ---
        """
        CREATE TABLE IF NOT EXISTS TIPO_APTIDAO (
            ID_TIPO_APTIDAO SERIAL PRIMARY KEY,
            NOME_APTIDAO VARCHAR(50) UNIQUE NOT NULL
        );
        """,

        """
        CREATE TABLE IF NOT EXISTS COLABORADOR_APTIDAO (
            ID_COLAB_APTIDAO SERIAL PRIMARY KEY,
            FK_COLABORADORES_MATRICULA INT,
            FK_TIPO_APTIDAO_ID INT,
            NIVEL VARCHAR(20),
            
            CONSTRAINT FK_COL_APT_COLAB 
                FOREIGN KEY (FK_COLABORADORES_MATRICULA)
                REFERENCES COLABORADORES(MATRICULA)
                ON DELETE CASCADE,
                
            CONSTRAINT FK_COL_APT_TIPO
                FOREIGN KEY (FK_TIPO_APTIDAO_ID) 
                REFERENCES TIPO_APTIDAO(ID_TIPO_APTIDAO)
                ON DELETE CASCADE,
                
            UNIQUE(FK_COLABORADORES_MATRICULA, FK_TIPO_APTIDAO_ID)
        );
        """,

        # --- RELACIONAMENTOS ORIGINAIS ---
        """
        CREATE TABLE IF NOT EXISTS POSSUI_FILIAIS_ENDERECO_EMPRESA (
            FK_FILIAIS_CNPJ_IND_ VARCHAR(20),
            FK_ENDERECO_ID_ENDERECO INT,
            FK_EMPRESA_CNPJ VARCHAR(20),
            
            CONSTRAINT FK_PFEE_FILIAIS 
                FOREIGN KEY (FK_FILIAIS_CNPJ_IND_)
                REFERENCES FILIAIS (CNPJ_IND_)
                ON DELETE RESTRICT,

            CONSTRAINT FK_PFEE_ENDERECO 
                FOREIGN KEY (FK_ENDERECO_ID_ENDERECO)
                REFERENCES ENDERECO (ID_ENDERECO)
                ON DELETE RESTRICT,

            CONSTRAINT FK_PFEE_EMPRESA 
                FOREIGN KEY (FK_EMPRESA_CNPJ)
                REFERENCES EMPRESA (CNPJ)
                ON DELETE CASCADE
        );
        """,

        """
        CREATE TABLE IF NOT EXISTS ATENDE_SETOR_MANUT_EMPRESA_FILIAIS (
            FK_SETOR_MANUT__NOME VARCHAR(100),
            FK_EMPRESA_CNPJ VARCHAR(20),
            FK_FILIAIS_CNPJ_IND_ VARCHAR(20),

            CONSTRAINT FK_ASMEF_SETOR 
                FOREIGN KEY (FK_SETOR_MANUT__NOME)
                REFERENCES SETOR_MANUT_ (NOME),

            CONSTRAINT FK_ASMEF_EMPRESA
                FOREIGN KEY (FK_EMPRESA_CNPJ)
                REFERENCES EMPRESA (CNPJ),

            CONSTRAINT FK_ASMEF_FILIAL
                FOREIGN KEY (FK_FILIAIS_CNPJ_IND_)
                REFERENCES FILIAIS (CNPJ_IND_)
        );
        """,

        """
        CREATE TABLE IF NOT EXISTS POSSUI_SETOR_COLABORADOR (
            FK_SETOR_MANUT__NOME VARCHAR(100),
            FK_COLABORADORES_MATRICULA INT,

            CONSTRAINT FK_PSC_SETOR 
                FOREIGN KEY (FK_SETOR_MANUT__NOME)
                REFERENCES SETOR_MANUT_ (NOME),

            CONSTRAINT FK_PSC_COLAB 
                FOREIGN KEY (FK_COLABORADORES_MATRICULA)
                REFERENCES COLABORADORES (MATRICULA)
        );
        """,

        """
        CREATE TABLE IF NOT EXISTS POSSUI_COLABORADOR_APTIDAO (
            FK_COLABORADORES_MATRICULA INT,
            FK_APTIDOES_ID_APTIDAO VARCHAR(20),

            CONSTRAINT FK_PCA_COLAB 
                FOREIGN KEY (FK_COLABORADORES_MATRICULA)
                REFERENCES COLABORADORES (MATRICULA),

            CONSTRAINT FK_PCA_APTIDAO
                FOREIGN KEY (FK_APTIDOES_ID_APTIDAO)
                REFERENCES APTIDOES (ID_APTIDAO)
        );
        """,

        """
        CREATE TABLE IF NOT EXISTS FAZ (
            FK_SOLICITACAO_N_SOLICITACAO INT,
            FK_FILIAIS_CNPJ_IND_ VARCHAR(20),

            CONSTRAINT FK_FAZ_SOLIC 
                FOREIGN KEY (FK_SOLICITACAO_N_SOLICITACAO)
                REFERENCES SOLICITACAO (N_SOLICITACAO),

            CONSTRAINT FK_FAZ_FILIAL
                FOREIGN KEY (FK_FILIAIS_CNPJ_IND_)
                REFERENCES FILIAIS (CNPJ_IND_)
                ON DELETE SET NULL
        );
        """
    ]
    
    conn = get_connection()
    if conn is None:
        print("❌ Não foi possível conectar ao banco para criar tabelas")
        return False
    
    cur = conn.cursor()
    
    try:
        for command in commands:
            cur.execute(command)
        
        conn.commit()
        print("✅ Todas as tabelas criadas/atualizadas com sucesso!")
        return True
    
    except Exception as e:
        print(f"❌ Erro ao criar as Tabelas: {e}")
        conn.rollback()
        return False
    
    finally:
        cur.close()
        conn.close()

#-------------------------------------------------------
# Função para popular dados iniciais
#-------------------------------------------------------

def popular_dados_iniciais():
    """
    Insere alguns dados de exemplo para teste
    """
    conn = get_connection()
    if conn is None:
        return False
    
    cur = conn.cursor()
    
    try:
        # Inserindo tipos de aptidão
        aptidoes_iniciais = [
            ('ELETRICA', 'Sim', 'Não', 'Não', 'Não'),
            ('HIDRAULICA', 'Não', 'Sim', 'Não', 'Não'),
            ('CIVIL', 'Não', 'Não', 'Sim', 'Não'),
            ('SERV_GERAIS', 'Não', 'Não', 'Não', 'Sim')
        ]
        
        for aptidao in aptidoes_iniciais:
            cur.execute("""
                INSERT INTO APTIDOES (ID_APTIDAO, ELETRICA, HIDRAULICA, CIVIL, SERVICOS_GERAIS)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (ID_APTIDAO) DO NOTHING
            """, aptidao)
        
        # Inserindo tipos de aptidão dinâmicos
        tipos_aptidao = ['Elétrica', 'Hidráulica', 'Civil', 'Pintura', 'Ar Condicionado']
        
        for tipo in tipos_aptidao:
            cur.execute("""
                INSERT INTO TIPO_APTIDAO (NOME_APTIDAO)
                VALUES (%s)
                ON CONFLICT (NOME_APTIDAO) DO NOTHING
            """, (tipo,))
        
        conn.commit()
        print("✅ Dados iniciais inseridos com sucesso!")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao inserir dados iniciais: {e}")
        conn.rollback()
        return False
    
    finally:
        cur.close()
        conn.close()

#-------------------------------------------------------
# Execução direta - CRIA O BANCO COMPLETO
#-------------------------------------------------------
if __name__ == "__main__":
    print("🏗️  Iniciando construção do banco de dados...")
    
    if create_tables():
        print("📊 Populando com dados iniciais...")
        popular_dados_iniciais()
        print("🎉 Sistema de banco de dados pronto para uso!")
    else:
        print("❌ Falha na criação do banco de dados")