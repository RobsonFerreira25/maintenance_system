# 📄 utils/pdf_generator.py
"""
GERADOR DE PDF PARA ORDENS DE SERVIÇO
Sistema profissional de impressão de OS
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime
import tkinter as tk
from tkinter import messagebox

class PDFGenerator:
    """Classe para geração de PDFs profissionais"""
    
    @staticmethod
    def gerar_os_pdf(solicitacao, caminho_arquivo=None):
        """
        Gera um PDF profissional da Ordem de Serviço
        """
        try:
            # Criar pasta de relatórios se não existir
            if not os.path.exists('relatorios'):
                os.makedirs('relatorios')
            
            # Definir nome do arquivo se não fornecido
            if not caminho_arquivo:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                caminho_arquivo = f'relatorios/OS_{solicitacao.n_solicitacao}_{timestamp}.pdf'
            
            # Criar documento PDF
            doc = SimpleDocTemplate(
                caminho_arquivo,
                pagesize=A4,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=18
            )
            
            # Elementos do documento
            elements = []
            
            # Estilos
            styles = getSampleStyleSheet()
            estilo_titulo = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=16,
                spaceAfter=30,
                alignment=1,  # Centralizado
                textColor=colors.HexColor('#2C3E50')
            )
            
            estilo_subtitulo = ParagraphStyle(
                'CustomSubtitle',
                parent=styles['Heading2'],
                fontSize=12,
                spaceAfter=12,
                textColor=colors.HexColor('#34495E')
            )
            
            estilo_normal = ParagraphStyle(
                'CustomNormal',
                parent=styles['Normal'],
                fontSize=10,
                spaceAfter=6
            )
            
            # Título
            titulo = Paragraph("ORDEM DE SERVIÇO - MANUTENÇÃO", estilo_titulo)
            elements.append(titulo)
            elements.append(Spacer(1, 20))
            
            # Informações da OS
            dados_os = [
                ["Nº DA OS:", str(solicitacao.n_solicitacao)],
                ["DATA ABERTURA:", solicitacao.dt_abertura.strftime('%d/%m/%Y') if solicitacao.dt_abertura else "N/A"],
                ["STATUS:", solicitacao.status if solicitacao.status else "N/A"],
                ["ÁREA:", solicitacao.area if solicitacao.area else "N/A"],
                ["RESPONSÁVEL:", solicitacao.responsavel if solicitacao.responsavel else "N/A"],
                ["FILIAL:", solicitacao.nome_filial if solicitacao.nome_filial else "Não informada"]
            ]
            
            if solicitacao.dt_conclusao:
                dados_os.append(["DATA CONCLUSÃO:", solicitacao.dt_conclusao.strftime('%d/%m/%Y')])
            
            tabela_os = Table(dados_os, colWidths=[150, 300])
            tabela_os.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498DB')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#ECF0F1')),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#BDC3C7'))
            ]))
            
            elements.append(tabela_os)
            elements.append(Spacer(1, 20))
            
            # Descrição do Serviço
            descricao_titulo = Paragraph("DESCRIÇÃO DO SERVIÇO", estilo_subtitulo)
            elements.append(descricao_titulo)
            
            descricao_texto = Paragraph(solicitacao.descricao if solicitacao.descricao else "Sem descrição", estilo_normal)
            elements.append(descricao_texto)
            elements.append(Spacer(1, 20))
            
            # Histórico (se aplicável)
            if solicitacao.dt_conclusao:
                historico_titulo = Paragraph("HISTÓRICO", estilo_subtitulo)
                elements.append(historico_titulo)
                
                historico_texto = f"Serviço concluído em {solicitacao.dt_conclusao.strftime('%d/%m/%Y')}"
                historico_para = Paragraph(historico_texto, estilo_normal)
                elements.append(historico_para)
                elements.append(Spacer(1, 20))
            
            # Rodapé
            rodape_titulo = Paragraph("INFORMAÇÕES ADICIONAIS", estilo_subtitulo)
            elements.append(rodape_titulo)
            
            rodape_texto = Paragraph(
                "Este documento foi gerado automaticamente pelo Sistema de Gestão de Manutenção. "
                "Qualquer dúvida, entre em contato com o setor responsável.",
                estilo_normal
            )
            elements.append(rodape_texto)
            
            # Data de geração
            data_geracao = Paragraph(
                f"Documento gerado em: {datetime.now().strftime('%d/%m/%Y às %H:%M')}",
                ParagraphStyle(
                    'CustomSmall',
                    parent=styles['Normal'],
                    fontSize=8,
                    textColor=colors.gray,
                    alignment=2  # Direita
                )
            )
            elements.append(Spacer(1, 30))
            elements.append(data_geracao)
            
            # Gerar PDF
            doc.build(elements)
            print(f"✅ PDF gerado com sucesso: {caminho_arquivo}")
            return caminho_arquivo
            
        except Exception as e:
            print(f"❌ Erro ao gerar PDF: {e}")
            return None
    
    @staticmethod
    def abrir_pdf(caminho_arquivo):
        """
        Abre o PDF no visualizador padrão do sistema
        """
        try:
            if os.name == 'nt':  # Windows
                os.startfile(caminho_arquivo)
            elif os.name == 'posix':  # Linux/Mac
                os.system(f'xdg-open "{caminho_arquivo}"')
            else:
                messagebox.showinfo("PDF Gerado", f"PDF salvo em: {caminho_arquivo}")
        except Exception as e:
            print(f"❌ Erro ao abrir PDF: {e}")
            messagebox.showinfo("PDF Gerado", f"PDF salvo em: {caminho_arquivo}")

# Função auxiliar para integração com a interface
def gerar_e_abrir_os_pdf(solicitacao):
    """
    Função para ser chamada pela interface
    Gera o PDF e abre automaticamente
    """
    try:
        caminho_pdf = PDFGenerator.gerar_os_pdf(solicitacao)
        if caminho_pdf:
            PDFGenerator.abrir_pdf(caminho_pdf)
            return True
        else:
            messagebox.showerror("Erro", "Não foi possível gerar o PDF da OS")
            return False
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao gerar PDF: {e}")
        return False