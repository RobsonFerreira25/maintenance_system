# 📄 utils/pdf_generator.py
"""
GERADOR DE PDF PARA ORDENS DE SERVIÇO - MODELO PROFISSIONAL
Baseado no layout fornecido: modelo de os pdf.pdf
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime
import tkinter as tk
from tkinter import messagebox

class PDFGenerator:
    """Classe para geração de PDFs no modelo profissional"""
    
    @staticmethod
    def gerar_os_pdf(solicitacao, caminho_arquivo=None):
        """
        Gera um PDF profissional da Ordem de Serviço no modelo especificado
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
                rightMargin=20*mm,
                leftMargin=20*mm,
                topMargin=15*mm,
                bottomMargin=15*mm
            )
            
            # Elementos do documento
            elements = []
            
            # Estilos personalizados
            styles = getSampleStyleSheet()
            
            # ========== CABEÇALHO COM Nº DA O.S ==========
            estilo_numero_os = ParagraphStyle(
                'NumeroOS',
                parent=styles['Normal'],
                fontSize=16,
                textColor=colors.black,
                alignment=1,  # Centralizado
                spaceAfter=20,
                fontName='Helvetica-Bold'
            )
            
            numero_os = Paragraph(f"Nº O.S<br/>{solicitacao.n_solicitacao}", estilo_numero_os)
            elements.append(numero_os)
            
            # ========== TÍTULO PRINCIPAL ==========
            estilo_titulo = ParagraphStyle(
                'TituloPrincipal',
                parent=styles['Normal'],
                fontSize=14,
                textColor=colors.black,
                alignment=1,  # Centralizado
                spaceAfter=25,
                fontName='Helvetica-Bold'
            )
            
            titulo = Paragraph("ORDEM DE SERVIÇO DE MANUTENÇÃO", estilo_titulo)
            elements.append(titulo)
            
            # ========== CLASSIFICAÇÃO DA O.S ==========
            dados_classificacao = [
                ["Classificação da O.S", "Nível", "Grupo Economico", "Filial"],
                ["", "II - Urgente", "ADM", solicitacao.nome_filial if solicitacao.nome_filial else "Não informada"]
            ]
            
            tabela_classificacao = Table(dados_classificacao, colWidths=[80*mm, 40*mm, 40*mm, 40*mm])
            tabela_classificacao.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#D9D9D9')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('FONTSIZE', (0, 1), (-1, 1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('TOPPADDING', (0, 1), (-1, 1), 8),
                ('BOTTOMPADDING', (0, 1), (-1, 1), 8),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            elements.append(tabela_classificacao)
            elements.append(Spacer(1, 20))
            
            # ========== SOLICITAÇÃO ==========
            dados_solicitacao = [
                ["Solicitação", "Solicitante", "Departamento", "Categoria", "Data da solicitação"],
                [
                    "Manutenção " + (solicitacao.area if solicitacao.area else ""), 
                    solicitacao.responsavel if solicitacao.responsavel else "Não informado",
                    "Manutenção", 
                    solicitacao.area if solicitacao.area else "Outros",
                    solicitacao.dt_abertura.strftime('%d/%m/%Y') if solicitacao.dt_abertura else "N/A"
                ]
            ]
            
            tabela_solicitacao = Table(dados_solicitacao, colWidths=[60*mm, 40*mm, 40*mm, 30*mm, 40*mm])
            tabela_solicitacao.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#D9D9D9')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 9),
                ('FONTSIZE', (0, 1), (-1, 1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
                ('TOPPADDING', (0, 1), (-1, 1), 6),
                ('BOTTOMPADDING', (0, 1), (-1, 1), 6),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            elements.append(tabela_solicitacao)
            elements.append(Spacer(1, 15))
            
            # ========== OCORRÊNCIA ==========
            estilo_ocorrencia_titulo = ParagraphStyle(
                'OcorrenciaTitulo',
                parent=styles['Normal'],
                fontSize=10,
                textColor=colors.black,
                alignment=0,  # Esquerda
                spaceAfter=5,
                fontName='Helvetica-Bold'
            )
            
            ocorrencia_titulo = Paragraph("Ocorrencia", estilo_ocorrencia_titulo)
            elements.append(ocorrencia_titulo)
            
            # Descrição da ocorrência
            estilo_ocorrencia_desc = ParagraphStyle(
                'OcorrenciaDesc',
                parent=styles['Normal'],
                fontSize=10,
                textColor=colors.black,
                alignment=0,  # Esquerda
                leftIndent=10,
                spaceAfter=15,
                fontName='Helvetica'
            )
            
            descricao_formatada = solicitacao.descricao if solicitacao.descricao else "Sem descrição fornecida"
            ocorrencia_desc = Paragraph(descricao_formatada, estilo_ocorrencia_desc)
            elements.append(ocorrencia_desc)
            
            # ========== TEMPO TRABALHADO ==========
            dados_tempo = [
                ["Tempo trabalhado", "Nome", "Data da Execução", "Início", "Termino"],
                ["", solicitacao.responsavel if solicitacao.responsavel else "", 
                 solicitacao.dt_conclusao.strftime('%d/%m/%Y') if solicitacao.dt_conclusao else "Pendente", 
                 "", ""]
            ]
            
            tabela_tempo = Table(dados_tempo, colWidths=[40*mm, 50*mm, 40*mm, 30*mm, 30*mm])
            tabela_tempo.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#D9D9D9')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 9),
                ('FONTSIZE', (0, 1), (-1, 1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
                ('TOPPADDING', (0, 1), (-1, 1), 6),
                ('BOTTOMPADDING', (0, 1), (-1, 1), 6),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            elements.append(tabela_tempo)
            elements.append(Spacer(1, 15))
            
            # ========== FORNECEDOR E NOTA FISCAL ==========
            dados_fornecedor = [
                ["Fornecedor", "Nº Nota Fiscal", "Valor total", "Data da compra"],
                ["", "", "", ""]
            ]
            
            tabela_fornecedor = Table(dados_fornecedor, colWidths=[70*mm, 40*mm, 40*mm, 40*mm])
            tabela_fornecedor.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#D9D9D9')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 9),
                ('FONTSIZE', (0, 1), (-1, 1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
                ('TOPPADDING', (0, 1), (-1, 1), 6),
                ('BOTTOMPADDING', (0, 1), (-1, 1), 6),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            elements.append(tabela_fornecedor)
            elements.append(Spacer(1, 15))
            
            # ========== OBSERVAÇÕES ==========
            estilo_obs_titulo = ParagraphStyle(
                'ObservacoesTitulo',
                parent=styles['Normal'],
                fontSize=10,
                textColor=colors.black,
                alignment=0,  # Esquerda
                spaceAfter=5,
                fontName='Helvetica-Bold'
            )
            
            obs_titulo = Paragraph("Observações", estilo_obs_titulo)
            elements.append(obs_titulo)
            
            estilo_obs_texto = ParagraphStyle(
                'ObservacoesTexto',
                parent=styles['Normal'],
                fontSize=9,
                textColor=colors.black,
                alignment=0,  # Esquerda
                leftIndent=10,
                spaceAfter=20,
                fontName='Helvetica'
            )
            
            observacoes_texto = "Serviço de manutenção registrado no sistema. Ordem de serviço gerada automaticamente."
            if solicitacao.status == "Concluída" and solicitacao.dt_conclusao:
                observacoes_texto += f" Serviço concluído em {solicitacao.dt_conclusao.strftime('%d/%m/%Y')}."
            
            obs_texto = Paragraph(observacoes_texto, estilo_obs_texto)
            elements.append(obs_texto)
            
            # ========== ASSINATURAS ==========
            estilo_assinatura = ParagraphStyle(
                'Assinatura',
                parent=styles['Normal'],
                fontSize=9,
                textColor=colors.black,
                alignment=1,  # Centralizado
                spaceBefore=30,
                spaceAfter=5,
                fontName='Helvetica'
            )
            
            texto_assinatura = "Estou ciente que o serviço solicitado foi executado conforme as observações."
            assinatura_texto = Paragraph(texto_assinatura, estilo_assinatura)
            elements.append(assinatura_texto)
            
            # Linhas para assinatura
            dados_assinatura = [
                ["", ""],
                ["Solicitante / Responsável", "Técnico"]
            ]
            
            tabela_assinatura = Table(dados_assinatura, colWidths=[90*mm, 90*mm])
            tabela_assinatura.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('LINEABOVE', (0, 0), (0, 0), 1, colors.black),
                ('LINEABOVE', (1, 0), (1, 0), 1, colors.black),
                ('TOPPADDING', (0, 0), (-1, 0), 20),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 5),
            ]))
            
            elements.append(tabela_assinatura)
            
            # ========== RODAPÉ ==========
            estilo_rodape = ParagraphStyle(
                'Rodape',
                parent=styles['Normal'],
                fontSize=8,
                textColor=colors.gray,
                alignment=1,  # Centralizado
                spaceBefore=20,
                fontName='Helvetica'
            )
            
            rodape_texto = f"Documento gerado automaticamente pelo Sistema de Gestão de Manutenção em {datetime.now().strftime('%d/%m/%Y às %H:%M')}"
            rodape = Paragraph(rodape_texto, estilo_rodape)
            elements.append(rodape)
            
            # ========== GERAR PDF ==========
            doc.build(elements)
            print(f"✅ PDF profissional gerado com sucesso: {caminho_arquivo}")
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