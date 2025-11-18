# 📄 main.py
"""
PROGRAMA PRINCIPAL - Sistema de Gestão de Manutenção
Ponto de entrada do sistema completo
"""

import tkinter as tk
from tkinter import messagebox
from interface.main_app import SistemaManutencaoApp

def verificar_dependencias():
    """
    Verifica se todas as dependências estão instaladas
    """
    try:
        import psycopg2
        from dotenv import load_dotenv
        return True
    except ImportError as e:
        print(f"❌ Dependência não encontrada: {e}")
        return False

def main():
    """
    Função principal do sistema
    """
    print("🔧 Iniciando Sistema de Gestão de Manutenção...")
    print("📊 Desenvolvido por: O Arquiteto")
    print("=" * 50)
    
    # Verificar dependências
    if not verificar_dependencias():
        messagebox.showerror(
            "Erro de Dependências", 
            "Instale as dependências necessárias:\n\n"
            "pip install psycopg2-binary python-dotenv"
        )
        return
    
    # Verificar conexão com banco
    try:
        from database.database import get_connection
        conn = get_connection()
        if conn:
            print("✅ Conexão com PostgreSQL: OK")
            conn.close()
        else:
            messagebox.showerror(
                "Erro de Conexão", 
                "Não foi possível conectar ao PostgreSQL.\n"
                "Verifique:\n"
                "1. Servidor PostgreSQL está rodando\n"
                "2. Arquivo .env com credenciais corretas\n"
                "3. Banco de dados existe"
            )
            return
    except Exception as e:
        messagebox.showerror("Erro", f"Erro inesperado: {e}")
        return
    
    # Iniciar interface gráfica
    try:
        print("🎨 Iniciando interface gráfica...")
        root = tk.Tk()
        app = SistemaManutencaoApp(root)
        
        # Configurar fechamento seguro
        def on_closing():
            if messagebox.askokcancel("Sair", "Deseja realmente sair do sistema?"):
                print("👋 Encerrando sistema...")
                root.destroy()
        
        root.protocol("WM_DELETE_WINDOW", on_closing)
        root.mainloop()
        
    except Exception as e:
        print(f"❌ Erro na interface: {e}")
        messagebox.showerror("Erro", f"Erro na interface gráfica: {e}")

if __name__ == "__main__":
    main()