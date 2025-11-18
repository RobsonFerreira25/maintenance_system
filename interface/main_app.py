# 📄 interface/main_app.py (VERSÃO COM LISTAGEM DE FILIAIS)
"""
INTERFACE PRINCIPAL - Sistema de Gestão de Manutenção
VERSÃO COM LISTAGEM COMPLETA DE EMPRESAS E FILIAIS
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime

# Importando nossos serviços
from services.empresa_service import EmpresaService, EnderecoService
from services.colaborador_service import ColaboradorService
from services.solicitacao_service import SolicitacaoService

class SistemaManutencaoApp:
    """Classe principal da interface gráfica"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("🏭 Sistema de Gestão de Manutenção - O Arquiteto")
        self.root.geometry("1300x800")  # Aumentei um pouco a largura
        self.root.configure(bg='#2C3E50')
        
        # Configurar estilo moderno
        self.configurar_estilo()
        
        # Criar interface
        self.criar_menu_superior()
        self.criar_abas_principais()
        
        # Carregar dados iniciais
        self.carregar_dados_iniciais()
    
    def configurar_estilo(self):
        """Configura estilos modernos para a interface"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configurar cores e estilos
        style.configure('TNotebook', background='#34495E')
        style.configure('TNotebook.Tab', background='#7F8C8D', foreground='white')
        style.map('TNotebook.Tab', background=[('selected', '#3498DB')])
        
        style.configure('TFrame', background='#34495E')
        style.configure('TLabel', background='#34495E', foreground='#ECF0F1')
        style.configure('TButton', background='#3498DB', foreground='white')
        style.configure('Delete.TButton', background='#E74C3C', foreground='white')
        style.configure('Header.TLabel', font=('Arial', 12, 'bold'))
    
    def criar_menu_superior(self):
        """Cria o menu superior com informações do sistema"""
        menu_frame = tk.Frame(self.root, bg='#1C2833', height=60)
        menu_frame.pack(fill='x', padx=10, pady=5)
        menu_frame.pack_propagate(False)
        
        # Título do sistema
        titulo = tk.Label(
            menu_frame,
            text="🔧 SISTEMA DE GESTÃO DE MANUTENÇÃO",
            font=('Arial', 16, 'bold'),
            fg='#3498DB',
            bg='#1C2833'
        )
        titulo.pack(side='left', padx=20, pady=10)
        
        # Data e hora
        self.label_data = tk.Label(
            menu_frame,
            text=self.obter_data_atual(),
            font=('Arial', 10),
            fg='#ECF0F1',
            bg='#1C2833'
        )
        self.label_data.pack(side='right', padx=20, pady=10)
        
        # Atualizar data a cada minuto
        self.atualizar_data()
    
    def obter_data_atual(self):
        """Retorna data e hora atual formatada"""
        return datetime.now().strftime("%d/%m/%Y %H:%M")
    
    def atualizar_data(self):
        """Atualiza a data e hora a cada minuto"""
        self.label_data.config(text=self.obter_data_atual())
        self.root.after(60000, self.atualizar_data)
    
    def criar_abas_principais(self):
        """Cria as abas principais do sistema"""
        # Criar notebook (abas)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Criar abas
        self.criar_aba_empresas()
        self.criar_aba_colaboradores()
        self.criar_aba_solicitacoes()
        self.criar_aba_dashboard()
    
    def criar_aba_empresas(self):
        """Cria a aba de gestão de empresas e filiais COM LISTAGEM DE FILIAIS"""
        frame_empresas = ttk.Frame(self.notebook)
        self.notebook.add(frame_empresas, text="🏢 Empresas & Filiais")
        
        # Frame de cadastro (lado esquerdo)
        frame_cadastro = ttk.Frame(frame_empresas)
        frame_cadastro.pack(side='left', fill='y', padx=10, pady=5)
        
        # Sub-frame para empresas
        frame_empresa_cadastro = ttk.LabelFrame(frame_cadastro, text="Cadastrar Nova Empresa", padding=10)
        frame_empresa_cadastro.pack(fill='x', pady=5)
        
        # Campos para empresa
        ttk.Label(frame_empresa_cadastro, text="CNPJ:").grid(row=0, column=0, sticky='w', pady=2)
        self.entry_cnpj = ttk.Entry(frame_empresa_cadastro, width=20)
        self.entry_cnpj.grid(row=0, column=1, pady=2, padx=5)
        
        ttk.Label(frame_empresa_cadastro, text="Razão Social:").grid(row=1, column=0, sticky='w', pady=2)
        self.entry_razao_social = ttk.Entry(frame_empresa_cadastro, width=30)
        self.entry_razao_social.grid(row=1, column=1, pady=2, padx=5)
        
        # Botão cadastrar empresa
        btn_cadastrar_empresa = ttk.Button(
            frame_empresa_cadastro, 
            text="Cadastrar Empresa", 
            command=self.cadastrar_empresa
        )
        btn_cadastrar_empresa.grid(row=2, column=0, columnspan=2, pady=10)
        
        # Sub-frame para filiais
        frame_filial_cadastro = ttk.LabelFrame(frame_cadastro, text="Cadastrar Filial", padding=10)
        frame_filial_cadastro.pack(fill='x', pady=5)
        
        ttk.Label(frame_filial_cadastro, text="CNPJ Filial:").grid(row=0, column=0, sticky='w', pady=2)
        self.entry_cnpj_filial = ttk.Entry(frame_filial_cadastro, width=20)
        self.entry_cnpj_filial.grid(row=0, column=1, pady=2, padx=5)
        
        ttk.Label(frame_filial_cadastro, text="Nome Filial:").grid(row=1, column=0, sticky='w', pady=2)
        self.entry_nome_filial = ttk.Entry(frame_filial_cadastro, width=30)
        self.entry_nome_filial.grid(row=1, column=1, pady=2, padx=5)
        
        btn_cadastrar_filial = ttk.Button(
            frame_filial_cadastro, 
            text="Cadastrar Filial", 
            command=self.cadastrar_filial
        )
        btn_cadastrar_filial.grid(row=2, column=0, columnspan=2, pady=10)
        
        # Frame de listagem (lado direito)
        frame_listagem = ttk.Frame(frame_empresas)
        frame_listagem.pack(side='right', fill='both', expand=True, padx=10, pady=5)
        
        # NOTEBOOK para empresas e filiais
        notebook_listagem = ttk.Notebook(frame_listagem)
        notebook_listagem.pack(fill='both', expand=True)
        
        # Aba de Empresas
        frame_empresas_lista = ttk.Frame(notebook_listagem)
        notebook_listagem.add(frame_empresas_lista, text="📊 Empresas")
        
        # Treeview para listar empresas
        colunas_empresas = ('CNPJ', 'Razão Social')
        self.tree_empresas = ttk.Treeview(frame_empresas_lista, columns=colunas_empresas, show='headings', height=12)
        
        # Configurar colunas empresas
        for col in colunas_empresas:
            self.tree_empresas.heading(col, text=col)
            self.tree_empresas.column(col, width=200)
        
        self.tree_empresas.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Frame de botões para empresas
        frame_botoes_empresas = ttk.Frame(frame_empresas_lista)
        frame_botoes_empresas.pack(fill='x', pady=5)
        
        btn_atualizar_empresas = ttk.Button(
            frame_botoes_empresas,
            text="🔄 Atualizar Lista",
            command=self.carregar_empresas
        )
        btn_atualizar_empresas.pack(side='left', padx=5)
        
        btn_deletar_empresa = ttk.Button(
            frame_botoes_empresas,
            text="🗑️ Deletar Empresa",
            command=self.deletar_empresa,
            style='Delete.TButton'
        )
        btn_deletar_empresa.pack(side='left', padx=5)
        
        # Aba de Filiais
        frame_filiais_lista = ttk.Frame(notebook_listagem)
        notebook_listagem.add(frame_filiais_lista, text="🏪 Filiais")
        
        # Treeview para listar filiais
        colunas_filiais = ('CNPJ', 'Nome da Filial')
        self.tree_filiais = ttk.Treeview(frame_filiais_lista, columns=colunas_filiais, show='headings', height=12)
        
        # Configurar colunas filiais
        for col in colunas_filiais:
            self.tree_filiais.heading(col, text=col)
            self.tree_filiais.column(col, width=200)
        
        self.tree_filiais.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Frame de botões para filiais
        frame_botoes_filiais = ttk.Frame(frame_filiais_lista)
        frame_botoes_filiais.pack(fill='x', pady=5)
        
        btn_atualizar_filiais = ttk.Button(
            frame_botoes_filiais,
            text="🔄 Atualizar Lista",
            command=self.carregar_filiais
        )
        btn_atualizar_filiais.pack(side='left', padx=5)
        
        btn_deletar_filial = ttk.Button(
            frame_botoes_filiais,
            text="🗑️ Deletar Filial",
            command=self.deletar_filial,
            style='Delete.TButton'
        )
        btn_deletar_filial.pack(side='left', padx=5)
    
    def criar_aba_colaboradores(self):
        """Cria a aba de gestão de colaboradores"""
        frame_colaboradores = ttk.Frame(self.notebook)
        self.notebook.add(frame_colaboradores, text="👥 Colaboradores")
        
        # Frame de cadastro
        frame_cadastro = ttk.LabelFrame(frame_colaboradores, text="Cadastrar Colaborador", padding=10)
        frame_cadastro.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(frame_cadastro, text="Matrícula:").grid(row=0, column=0, sticky='w', pady=2)
        self.entry_matricula = ttk.Entry(frame_cadastro, width=15)
        self.entry_matricula.grid(row=0, column=1, pady=2, padx=5)
        
        ttk.Label(frame_cadastro, text="Nome:").grid(row=1, column=0, sticky='w', pady=2)
        self.entry_nome_colab = ttk.Entry(frame_cadastro, width=30)
        self.entry_nome_colab.grid(row=1, column=1, pady=2, padx=5)
        
        ttk.Label(frame_cadastro, text="Cargo:").grid(row=2, column=0, sticky='w', pady=2)
        self.entry_cargo = ttk.Entry(frame_cadastro, width=25)
        self.entry_cargo.grid(row=2, column=1, pady=2, padx=5)
        
        btn_cadastrar_colab = ttk.Button(
            frame_cadastro,
            text="Cadastrar Colaborador",
            command=self.cadastrar_colaborador
        )
        btn_cadastrar_colab.grid(row=3, column=0, columnspan=2, pady=10)
        
        # Frame de listagem
        frame_listagem = ttk.LabelFrame(frame_colaboradores, text="Colaboradores Cadastrados", padding=10)
        frame_listagem.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Treeview para colaboradores
        colunas = ('Matrícula', 'Nome', 'Cargo')
        self.tree_colaboradores = ttk.Treeview(frame_listagem, columns=colunas, show='headings', height=12)
        
        for col in colunas:
            self.tree_colaboradores.heading(col, text=col)
            self.tree_colaboradores.column(col, width=150)
        
        self.tree_colaboradores.pack(fill='both', expand=True)
        
        # Frame de botões para colaboradores
        frame_botoes_colab = ttk.Frame(frame_listagem)
        frame_botoes_colab.pack(fill='x', pady=5)
        
        btn_atualizar_colab = ttk.Button(
            frame_botoes_colab,
            text="🔄 Atualizar Lista",
            command=self.carregar_colaboradores
        )
        btn_atualizar_colab.pack(side='left', padx=5)
        
        btn_deletar_colab = ttk.Button(
            frame_botoes_colab,
            text="🗑️ Deletar Colaborador",
            command=self.deletar_colaborador,
            style='Delete.TButton'
        )
        btn_deletar_colab.pack(side='left', padx=5)
    
    def criar_aba_solicitacoes(self):
        """Cria a aba de gestão de solicitações de manutenção"""
        frame_solicitacoes = ttk.Frame(self.notebook)
        self.notebook.add(frame_solicitacoes, text="📋 Solicitações")
        
        # Frame de cadastro
        frame_cadastro = ttk.LabelFrame(frame_solicitacoes, text="Nova Solicitação", padding=10)
        frame_cadastro.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(frame_cadastro, text="Nº Solicitação:").grid(row=0, column=0, sticky='w', pady=2)
        self.entry_num_solic = ttk.Entry(frame_cadastro, width=15)
        self.entry_num_solic.grid(row=0, column=1, pady=2, padx=5)
        
        ttk.Label(frame_cadastro, text="Área:").grid(row=1, column=0, sticky='w', pady=2)
        self.combo_area = ttk.Combobox(frame_cadastro, width=20, values=['Elétrica', 'Hidráulica', 'Civil', 'Serviços Gerais'])
        self.combo_area.grid(row=1, column=1, pady=2, padx=5)
        
        # Combobox para responsáveis
        ttk.Label(frame_cadastro, text="Responsável:").grid(row=2, column=0, sticky='w', pady=2)
        self.combo_responsavel = ttk.Combobox(frame_cadastro, width=25)
        self.combo_responsavel.grid(row=2, column=1, pady=2, padx=5)
        
        # Botão para atualizar lista de responsáveis
        btn_atualizar_resp = ttk.Button(
            frame_cadastro,
            text="🔄 Atualizar Lista",
            command=self.carregar_responsaveis,
            width=15
        )
        btn_atualizar_resp.grid(row=2, column=2, padx=5)
        
        ttk.Label(frame_cadastro, text="Descrição:").grid(row=3, column=0, sticky='nw', pady=2)
        self.text_descricao = scrolledtext.ScrolledText(frame_cadastro, width=30, height=4)
        self.text_descricao.grid(row=3, column=1, pady=2, padx=5)
        
        btn_criar_solic = ttk.Button(
            frame_cadastro,
            text="Criar Solicitação",
            command=self.criar_solicitacao
        )
        btn_criar_solic.grid(row=4, column=0, columnspan=2, pady=10)
        
        # Frame de listagem e controle
        frame_controle = ttk.LabelFrame(frame_solicitacoes, text="Controle de Solicitações", padding=10)
        frame_controle.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Treeview para solicitações
        colunas = ('Nº', 'Data', 'Área', 'Status', 'Responsável', 'Descrição')
        self.tree_solicitacoes = ttk.Treeview(frame_controle, columns=colunas, show='headings', height=10)
        
        larguras = [80, 100, 100, 100, 120, 200]
        for i, col in enumerate(colunas):
            self.tree_solicitacoes.heading(col, text=col)
            self.tree_solicitacoes.column(col, width=larguras[i])
        
        self.tree_solicitacoes.pack(fill='both', expand=True)
        
        # Frame de botões para controle
        frame_botoes = ttk.Frame(frame_controle)
        frame_botoes.pack(fill='x', pady=5)
        
        btn_atualizar_solic = ttk.Button(
            frame_botoes,
            text="🔄 Atualizar Lista",
            command=self.carregar_solicitacoes
        )
        btn_atualizar_solic.pack(side='left', padx=5)
        
        btn_marcar_andamento = ttk.Button(
            frame_botoes,
            text="▶️ Em Andamento",
            command=lambda: self.atualizar_status_solicitacao("Em Andamento")
        )
        btn_marcar_andamento.pack(side='left', padx=5)
        
        btn_marcar_concluida = ttk.Button(
            frame_botoes,
            text="✅ Concluída",
            command=lambda: self.atualizar_status_solicitacao("Concluída")
        )
        btn_marcar_concluida.pack(side='left', padx=5)
        
        btn_deletar_solic = ttk.Button(
            frame_botoes,
            text="🗑️ Deletar Solicitação",
            command=self.deletar_solicitacao,
            style='Delete.TButton'
        )
        btn_deletar_solic.pack(side='left', padx=5)
    
    def criar_aba_dashboard(self):
        """Cria a aba de dashboard com resumo do sistema"""
        frame_dashboard = ttk.Frame(self.notebook)
        self.notebook.add(frame_dashboard, text="📊 Dashboard")
        
        # Frame de estatísticas
        frame_stats = ttk.LabelFrame(frame_dashboard, text="Resumo do Sistema", padding=15)
        frame_stats.pack(fill='x', padx=10, pady=5)
        
        # Criar labels para estatísticas
        self.label_total_empresas = ttk.Label(
            frame_stats, 
            text="Empresas: Carregando...",
            font=('Arial', 11, 'bold'),
            foreground='#3498DB'
        )
        self.label_total_empresas.pack(anchor='w', pady=2)
        
        self.label_total_colaboradores = ttk.Label(
            frame_stats,
            text="Colaboradores: Carregando...",
            font=('Arial', 11, 'bold'),
            foreground='#2ECC71'
        )
        self.label_total_colaboradores.pack(anchor='w', pady=2)
        
        self.label_total_solicitacoes = ttk.Label(
            frame_stats,
            text="Solicitações: Carregando...",
            font=('Arial', 11, 'bold'),
            foreground='#E74C3C'
        )
        self.label_total_solicitacoes.pack(anchor='w', pady=2)
        
        self.label_solicitacoes_abertas = ttk.Label(
            frame_stats,
            text="Solicitações Abertas: Carregando...",
            font=('Arial', 11, 'bold'),
            foreground='#F39C12'
        )
        self.label_solicitacoes_abertas.pack(anchor='w', pady=2)
        
        # NOVO: Estatística de filiais
        self.label_total_filiais = ttk.Label(
            frame_stats,
            text="Filiais: Carregando...",
            font=('Arial', 11, 'bold'),
            foreground='#9B59B6'
        )
        self.label_total_filiais.pack(anchor='w', pady=2)
        
        # Botão atualizar dashboard
        btn_atualizar_dash = ttk.Button(
            frame_stats,
            text="🔄 Atualizar Dashboard",
            command=self.atualizar_dashboard
        )
        btn_atualizar_dash.pack(pady=10)
        
        # Frame de últimas solicitações
        frame_ultimas = ttk.LabelFrame(frame_dashboard, text="Últimas Solicitações", padding=10)
        frame_ultimas.pack(fill='both', expand=True, padx=10, pady=5)
        
        colunas = ('Nº', 'Data', 'Área', 'Status')
        self.tree_ultimas_solic = ttk.Treeview(frame_ultimas, columns=colunas, show='headings', height=8)
        
        for col in colunas:
            self.tree_ultimas_solic.heading(col, text=col)
            self.tree_ultimas_solic.column(col, width=120)
        
        self.tree_ultimas_solic.pack(fill='both', expand=True)
    
    # ========== MÉTODOS DE CONTROLE ==========
    
    def carregar_dados_iniciais(self):
        """Carrega dados iniciais na interface"""
        self.carregar_empresas()
        self.carregar_filiais()  # NOVO: Carrega filiais também
        self.carregar_colaboradores()
        self.carregar_solicitacoes()
        self.carregar_responsaveis()
        self.atualizar_dashboard()
    
    def carregar_responsaveis(self):
        """Carrega a lista de colaboradores no combobox de responsáveis"""
        try:
            responsaveis = ColaboradorService.listar_nomes_colaboradores()
            self.combo_responsavel['values'] = responsaveis
            
            if responsaveis:
                self.combo_responsavel.set(responsaveis[0])
                print(f"✅ {len(responsaveis)} responsáveis carregados no combobox")
            else:
                self.combo_responsavel.set('')
                print("ℹ️ Nenhum colaborador cadastrado ainda")
                
        except Exception as e:
            print(f"❌ Erro ao carregar responsáveis: {e}")
            messagebox.showwarning("Atenção", "Erro ao carregar lista de responsáveis")
    
    # ========== MÉTODOS DE CADASTRO ==========
    
    def cadastrar_empresa(self):
        """Cadastra uma nova empresa"""
        cnpj = self.entry_cnpj.get().strip()
        razao_social = self.entry_razao_social.get().strip()
        
        if not cnpj or not razao_social:
            messagebox.showwarning("Atenção", "Por favor, preencha todos os campos!")
            return
        
        if EmpresaService.criar_empresa(cnpj, razao_social):
            self.entry_cnpj.delete(0, tk.END)
            self.entry_razao_social.delete(0, tk.END)
            self.carregar_empresas()
            self.atualizar_dashboard()
    
    def cadastrar_filial(self):
        """Cadastra uma nova filial"""
        cnpj_ind = self.entry_cnpj_filial.get().strip()
        nome = self.entry_nome_filial.get().strip()
        
        if not cnpj_ind or not nome:
            messagebox.showwarning("Atenção", "Por favor, preencha todos os campos!")
            return
        
        if EmpresaService.criar_filial(cnpj_ind, nome):
            self.entry_cnpj_filial.delete(0, tk.END)
            self.entry_nome_filial.delete(0, tk.END)
            self.carregar_filiais()  # NOVO: Atualiza lista de filiais
            self.atualizar_dashboard()
    
    def cadastrar_colaborador(self):
        """Cadastra um novo colaborador"""
        try:
            matricula = int(self.entry_matricula.get().strip())
            nome = self.entry_nome_colab.get().strip()
            cargo = self.entry_cargo.get().strip()
            
            if not nome or not cargo:
                messagebox.showwarning("Atenção", "Por favor, preencha todos os campos!")
                return
            
            if ColaboradorService.criar_colaborador(matricula, nome, cargo):
                self.entry_matricula.delete(0, tk.END)
                self.entry_nome_colab.delete(0, tk.END)
                self.entry_cargo.delete(0, tk.END)
                self.carregar_colaboradores()
                self.carregar_responsaveis()
                self.atualizar_dashboard()
                
        except ValueError:
            messagebox.showerror("Erro", "Matrícula deve ser um número!")
    
    def criar_solicitacao(self):
        """Cria uma nova solicitação"""
        try:
            n_solicitacao = int(self.entry_num_solic.get().strip())
            area = self.combo_area.get().strip()
            responsavel = self.combo_responsavel.get().strip()
            descricao = self.text_descricao.get('1.0', tk.END).strip()
            
            if not all([n_solicitacao, area, responsavel, descricao]):
                messagebox.showwarning("Atenção", "Por favor, preencha todos os campos!")
                return
            
            # Verifica se o responsável existe na lista
            responsaveis_validos = ColaboradorService.listar_nomes_colaboradores()
            if responsavel not in responsaveis_validos:
                messagebox.showerror("Erro", "Por favor, selecione um responsável válido da lista!")
                return
            
            if SolicitacaoService.criar_solicitacao(n_solicitacao, area, responsavel, descricao):
                self.entry_num_solic.delete(0, tk.END)
                self.combo_area.set('')
                self.combo_responsavel.set('')
                self.text_descricao.delete('1.0', tk.END)
                self.carregar_solicitacoes()
                self.atualizar_dashboard()
                
        except ValueError:
            messagebox.showerror("Erro", "Número da solicitação deve ser um número!")
    
    # ========== MÉTODOS DE CARREGAMENTO ==========
    
    def carregar_empresas(self):
        """Carrega a lista de empresas no treeview"""
        for item in self.tree_empresas.get_children():
            self.tree_empresas.delete(item)
        
        empresas = EmpresaService.listar_empresas()
        for empresa in empresas:
            self.tree_empresas.insert('', 'end', values=(empresa.cnpj, empresa.razao_social))
    
    def carregar_filiais(self):
        """NOVO: Carrega a lista de filiais no treeview"""
        for item in self.tree_filiais.get_children():
            self.tree_filiais.delete(item)
        
        filiais = EmpresaService.listar_filiais()
        for filial in filiais:
            self.tree_filiais.insert('', 'end', values=(filial.cnpj_ind, filial.nome))
    
    def carregar_colaboradores(self):
        """Carrega a lista de colaboradores"""
        for item in self.tree_colaboradores.get_children():
            self.tree_colaboradores.delete(item)
        
        colaboradores = ColaboradorService.listar_colaboradores()
        for colab in colaboradores:
            self.tree_colaboradores.insert('', 'end', values=(colab.matricula, colab.nome, colab.cargo))
    
    def carregar_solicitacoes(self):
        """Carrega a lista de solicitações"""
        for item in self.tree_solicitacoes.get_children():
            self.tree_solicitacoes.delete(item)
        
        solicitacoes = SolicitacaoService.listar_solicitacoes()
        for sol in solicitacoes:
            # Data formatada com verificação segura
            data_formatada = ""
            if sol.dt_abertura:
                if hasattr(sol.dt_abertura, 'strftime'):
                    data_formatada = sol.dt_abertura.strftime('%d/%m/%Y')
                else:
                    data_formatada = str(sol.dt_abertura)
            
            # Descrição com verificação segura para None
            descricao_exibicao = ""
            if sol.descricao:
                if len(sol.descricao) > 50:
                    descricao_exibicao = sol.descricao[:50] + '...'
                else:
                    descricao_exibicao = sol.descricao
            else:
                descricao_exibicao = "Sem descrição"
            
            self.tree_solicitacoes.insert('', 'end', values=(
                str(sol.n_solicitacao) if sol.n_solicitacao else "",
                data_formatada,
                str(sol.area) if sol.area else "",
                str(sol.status) if sol.status else "",
                str(sol.responsavel) if sol.responsavel else "",
                descricao_exibicao
            ))
    
    # ========== MÉTODOS DE DELETE ==========
    
    def deletar_empresa(self):
        """Deleta a empresa selecionada"""
        selecionado = self.tree_empresas.selection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Por favor, selecione uma empresa para deletar!")
            return
        
        item = selecionado[0]
        cnpj = self.tree_empresas.item(item)['values'][0]
        razao_social = self.tree_empresas.item(item)['values'][1]
        
        # Confirmação antes de deletar
        confirmacao = messagebox.askyesno(
            "Confirmar Deleção", 
            f"Tem certeza que deseja deletar a empresa:\n\n{razao_social}\nCNPJ: {cnpj}\n\nEsta ação não pode ser desfeita!"
        )
        
        if confirmacao:
            if EmpresaService.deletar_empresa(cnpj):
                messagebox.showinfo("Sucesso", "Empresa deletada com sucesso!")
                self.carregar_empresas()
                self.atualizar_dashboard()
            else:
                messagebox.showerror("Erro", "Erro ao deletar empresa. Verifique se não há registros vinculados.")
    
    def deletar_filial(self):
        """NOVO: Deleta a filial selecionada"""
        selecionado = self.tree_filiais.selection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Por favor, selecione uma filial para deletar!")
            return
        
        item = selecionado[0]
        cnpj_ind = self.tree_filiais.item(item)['values'][0]
        nome_filial = self.tree_filiais.item(item)['values'][1]
        
        # Confirmação antes de deletar
        confirmacao = messagebox.askyesno(
            "Confirmar Deleção", 
            f"Tem certeza que deseja deletar a filial:\n\n{nome_filial}\nCNPJ: {cnpj_ind}\n\nEsta ação não pode ser desfeita!"
        )
        
        if confirmacao:
            if EmpresaService.deletar_filial(cnpj_ind):
                messagebox.showinfo("Sucesso", "Filial deletada com sucesso!")
                self.carregar_filiais()
                self.atualizar_dashboard()
            else:
                messagebox.showerror("Erro", "Erro ao deletar filial. Verifique se não há registros vinculados.")
    
    def deletar_colaborador(self):
        """Deleta o colaborador selecionado"""
        selecionado = self.tree_colaboradores.selection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Por favor, selecione um colaborador para deletar!")
            return
        
        item = selecionado[0]
        matricula = self.tree_colaboradores.item(item)['values'][0]
        nome = self.tree_colaboradores.item(item)['values'][1]
        
        # Confirmação antes de deletar
        confirmacao = messagebox.askyesno(
            "Confirmar Deleção", 
            f"Tem certeza que deseja deletar o colaborador:\n\n{nome}\nMatrícula: {matricula}\n\nEsta ação não pode ser desfeita!"
        )
        
        if confirmacao:
            if ColaboradorService.deletar_colaborador(matricula):
                messagebox.showinfo("Sucesso", "Colaborador deletado com sucesso!")
                self.carregar_colaboradores()
                self.carregar_responsaveis()
                self.atualizar_dashboard()
            else:
                messagebox.showerror("Erro", "Erro ao deletar colaborador. Verifique se não há registros vinculados.")
    
    def deletar_solicitacao(self):
        """Deleta a solicitação selecionada"""
        selecionado = self.tree_solicitacoes.selection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Por favor, selecione uma solicitação para deletar!")
            return
        
        item = selecionado[0]
        n_solicitacao = self.tree_solicitacoes.item(item)['values'][0]
        descricao = self.tree_solicitacoes.item(item)['values'][5]
        
        # Confirmação antes de deletar
        confirmacao = messagebox.askyesno(
            "Confirmar Deleção", 
            f"Tem certeza que deseja deletar a solicitação:\n\n#{n_solicitacao}\nDescrição: {descricao}\n\nEsta ação não pode ser desfeita!"
        )
        
        if confirmacao:
            if SolicitacaoService.deletar_solicitacao(n_solicitacao):
                messagebox.showinfo("Sucesso", "Solicitação deletada com sucesso!")
                self.carregar_solicitacoes()
                self.atualizar_dashboard()
            else:
                messagebox.showerror("Erro", "Erro ao deletar solicitação.")
    
    # ========== MÉTODOS DE ATUALIZAÇÃO ==========
    
    def atualizar_status_solicitacao(self, novo_status):
        """Atualiza o status da solicitação selecionada"""
        selecionado = self.tree_solicitacoes.selection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Por favor, selecione uma solicitação!")
            return
        
        item = selecionado[0]
        n_solicitacao = self.tree_solicitacoes.item(item)['values'][0]
        
        if SolicitacaoService.atualizar_status_solicitacao(n_solicitacao, novo_status):
            self.carregar_solicitacoes()
            self.atualizar_dashboard()
    
    def atualizar_dashboard(self):
        """Atualiza as informações do dashboard - VERSÃO ATUALIZADA"""
        try:
            # Estatísticas básicas
            empresas = EmpresaService.listar_empresas() or []
            filiais = EmpresaService.listar_filiais() or []  # NOVO: Estatística de filiais
            colaboradores = ColaboradorService.listar_colaboradores() or []
            solicitacoes = SolicitacaoService.listar_solicitacoes() or []
            
            # Contar solicitações abertas com verificação segura
            abertas = 0
            for sol in solicitacoes:
                if sol.status and sol.status.lower() in ['aberta', 'em andamento']:
                    abertas += 1
            
            # Atualizar labels
            self.label_total_empresas.config(text=f"🏢 Empresas: {len(empresas)}")
            self.label_total_filiais.config(text=f"🏪 Filiais: {len(filiais)}")  # NOVO: Label de filiais
            self.label_total_colaboradores.config(text=f"👥 Colaboradores: {len(colaboradores)}")
            self.label_total_solicitacoes.config(text=f"📋 Total Solicitações: {len(solicitacoes)}")
            self.label_solicitacoes_abertas.config(text=f"⚠️ Solicitações Abertas: {abertas}")
            
            # Atualizar últimas solicitações
            for item in self.tree_ultimas_solic.get_children():
                self.tree_ultimas_solic.delete(item)
            
            ultimas = solicitacoes[:5]
            for sol in ultimas:
                # Data formatada com verificação segura
                data_formatada = ""
                if sol.dt_abertura:
                    if hasattr(sol.dt_abertura, 'strftime'):
                        data_formatada = sol.dt_abertura.strftime('%d/%m/%Y')
                    else:
                        data_formatada = str(sol.dt_abertura)
                
                self.tree_ultimas_solic.insert('', 'end', values=(
                    str(sol.n_solicitacao) if sol.n_solicitacao else "",
                    data_formatada,
                    str(sol.area) if sol.area else "",
                    str(sol.status) if sol.status else ""
                ))
                
        except Exception as e:
            print(f"⚠️ Erro ao atualizar dashboard: {e}")

# Função para iniciar a aplicação
def main():
    """Função principal para iniciar a interface gráfica"""
    try:
        root = tk.Tk()
        app = SistemaManutencaoApp(root)
        root.mainloop()
    except Exception as e:
        print(f"❌ Erro fatal na aplicação: {e}")
        messagebox.showerror("Erro Fatal", f"O sistema encontrou um erro:\n{e}")

if __name__ == "__main__":
    main()