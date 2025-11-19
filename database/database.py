# 📄 database/database.py (VERSÃO SIMPLIFICADA E CORRIGIDA)
"""
MÓDULO DE ACESSO AO POSTGRESQL - VERSÃO SIMPLIFICADA
Sistema de Gestão de Manutenção
"""

import psycopg2
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configurações do Banco de Dados
DB_CONFIG = {
    'dbname': os.getenv("DB_NAME", "gestao_manutencao"),
    'user': os.getenv("DB_USER", "postgres"),
    'password': os.getenv("DB_PASSWORD", "password"),
    'host': os.getenv("DB_HOST", "localhost"),
    'port': os.getenv("DB_PORT", "5432")
}

def get_connection():
    '''
    Cria e retorna uma conexão com o PostgreSQL.
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
# Função para criar todas as tabelas (VERSÃO CORRIGIDA)
#---------------------------------------------------------

def create_tables():
    '''
    Cria todas as tabelas necessárias no sistema de manutenção
    VERSÃO CORRIGIDA - Adiciona campo FILIAL na tabela SOLICITACAO
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
            DT_CONCLUSAO DATE,
            FILIAL VARCHAR(100)  -- NOVO CAMPO ADICIONADO
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
# Função para adicionar coluna FILIAL se não existir
#-------------------------------------------------------

def atualizar_estrutura_solicitacao():
    """
    NOVA FUNÇÃO: Adiciona a coluna FILIAL na tabela SOLICITACAO se não existir
    """
    conn = get_connection()
    if conn is None:
        return False
    
    cur = conn.cursor()
    
    try:
        # Verificar se a coluna FILIAL já existe
        cur.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='solicitacao' and column_name='filial'
        """)
        
        if not cur.fetchone():
            # Adicionar a coluna FILIAL
            cur.execute("ALTER TABLE SOLICITACAO ADD COLUMN FILIAL VARCHAR(100)")
            conn.commit()
            print("✅ Coluna FILIAL adicionada à tabela SOLICITACAO!")
        else:
            print("✅ Coluna FILIAL já existe na tabela SOLICITACAO")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao atualizar estrutura: {e}")
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
# Execução direta - ATUALIZA O BANCO COMPLETO
#-------------------------------------------------------

class DatabaseConnection:
    """
    Context manager para gerenciar conexões com o banco de dados
    VERSÃO CORRIGIDA: Melhor tratamento de exceções
    """
    
    def __enter__(self):
        """Abre a conexão quando entra no contexto"""
        self.conn = get_connection()
        return self.conn
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Fecha a conexão quando sai do contexto
        CORREÇÃO: Não tenta fazer rollback se conexão já fechada
        """
        if self.conn:
            try:
                # Se houve exceção, tenta rollback primeiro
                if exc_type is not None:
                    self.conn.rollback()
                    print("🔄 Rollback executado devido a exceção")
            except Exception as rollback_error:
                print(f"⚠️ Erro no rollback (pode ser normal): {rollback_error}")
            finally:
                # Sempre fecha a conexão
                self.conn.close()
                print("✅ Conexão fechada automaticamente")

def executar_query(query, params=None):
    """
    Função utilitária para executar queries com context manager
    """
    with DatabaseConnection() as conn:
        if conn is None:
            return None
        try:
            cur = conn.cursor()
            cur.execute(query, params or ())
            
            # Se for SELECT, retorna resultados
            if query.strip().upper().startswith('SELECT'):
                resultados = cur.fetchall()
                colunas = [desc[0] for desc in cur.description]
                return resultados, colunas
            else:
                # Para INSERT/UPDATE/DELETE, retorna rowcount
                conn.commit()
                return cur.rowcount
                
        except Exception as e:
            conn.rollback()
            print(f"❌ Erro na query: {e}")
            raise e

def criar_indices():
    """
    Cria índices para melhorar performance das queries
    """
    commands = [
        # Índices para tabela SOLICITACAO (mais usada)
        "CREATE INDEX IF NOT EXISTS idx_solicitacao_status ON SOLICITACAO(STATUS)",
        "CREATE INDEX IF NOT EXISTS idx_solicitacao_data_abertura ON SOLICITACAO(DT_ABERTURA)",
        "CREATE INDEX IF NOT EXISTS idx_solicitacao_area ON SOLICITACAO(AREA)",
        "CREATE INDEX IF NOT EXISTS idx_solicitacao_responsavel ON SOLICITACAO(RESPONSAVEL)",
        
        # Índices para tabela COLABORADORES
        "CREATE INDEX IF NOT EXISTS idx_colaboradores_nome ON COLABORADORES(NOME)",
        "CREATE INDEX IF NOT EXISTS idx_colaboradores_cargo ON COLABORADORES(CARGO)",
        
        # Índices para tabela FILIAIS
        "CREATE INDEX IF NOT EXISTS idx_filiais_nome ON FILIAIS(NOME)",
        
        # Índices para tabela EMPRESA
        "CREATE INDEX IF NOT EXISTS idx_empresa_razao_social ON EMPRESA(RAZAO_SOCIAL)",
        
        # Índices para relações frequentes
        "CREATE INDEX IF NOT EXISTS idx_possui_colab_apt_matricula ON POSSUI_COLABORADOR_APTIDAO(FK_COLABORADORES_MATRICULA)",
        "CREATE INDEX IF NOT EXISTS idx_faz_filial ON FAZ(FK_FILIAIS_CNPJ_IND_)"
    ]
    
    with DatabaseConnection() as conn:
        if conn is None:
            return False
        
        cur = conn.cursor()
        
        try:
            for command in commands:
                cur.execute(command)
            
            conn.commit()
            print("✅ Índices criados/atualizados com sucesso!")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao criar índices: {e}")
            conn.rollback()
            return False

if __name__ == "__main__":
    print("🏗️  Iniciando construção/atualização do banco de dados...")
    
    if create_tables():
        print("🔄 Atualizando estrutura da tabela SOLICITACAO...")
        atualizar_estrutura_solicitacao()
        print("📊 Populando com dados iniciais...")
        popular_dados_iniciais()
        print("🚀 Criando índices para performance...")
        criar_indices()  # ← LINHA NOVA
        print("🎉 Sistema de banco de dados pronto para uso!")
    else:
        print("❌ Falha na criação do banco de dados")