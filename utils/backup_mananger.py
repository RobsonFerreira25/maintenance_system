"""
GERENCIADOR DE BACKUPS DO SISTEMA
Faz backup automático do banco de dados
"""

import os
import subprocess
from datetime import datetime
from config.settings import DB_CONFIG

class BackupManager:
    """Gerencia backups do banco de dados"""
    
    @staticmethod
    def criar_backup():
        """
        Cria um backup do banco de dados
        """
        try:
            # Nome do arquivo de backup com timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = f"backups/backup_{timestamp}.sql"
            
            # Comando pg_dump
            cmd = [
                'pg_dump',
                '-h', DB_CONFIG['host'],
                '-p', DB_CONFIG['port'],
                '-U', DB_CONFIG['user'],
                '-d', DB_CONFIG['dbname'],
                '-f', backup_file,
                '-w'  # Não pedir password (usa .pgpass)
            ]
            
            # Executar backup
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ Backup criado com sucesso: {backup_file}")
                return True
            else:
                print(f"❌ Erro no backup: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Erro ao criar backup: {e}")
            return False
    
    @staticmethod
    def listar_backups():
        """
        Lista todos os backups disponíveis
        """
        if not os.path.exists('backups'):
            return []
        
        backups = []
        for file in os.listdir('backups'):
            if file.startswith('backup_') and file.endswith('.sql'):
                file_path = os.path.join('backups', file)
                file_time = os.path.getctime(file_path)
                backups.append({
                    'nome': file,
                    'caminho': file_path,
                    'data': datetime.fromtimestamp(file_time).strftime('%d/%m/%Y %H:%M'),
                    'tamanho': f"{os.path.getsize(file_path) / 1024 / 1024:.2f} MB"
                })
        
        return sorted(backups, key=lambda x: x['nome'], reverse=True)

# Função para integrar com a interface
def fazer_backup_automatico():
    """
    Função para ser chamada pela interface
    """
    from utils.logger import log_activity
    
    if BackupManager.criar_backup():
        log_activity("Sistema", "Backup criado com sucesso")
        return True
    else:
        log_activity("Sistema", "Falha ao criar backup", "Erro no processo")
        return False