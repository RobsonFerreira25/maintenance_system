# 📄 services/relatorio_service.py
"""
SERVIÇO DE RELATÓRIOS AVANÇADOS
Gera relatórios analíticos do sistema
"""

from database.database import DatabaseConnection
from datetime import datetime, timedelta
from typing import Dict, List, Any

class RelatorioService:
    """Serviço para geração de relatórios analíticos"""
    
    @staticmethod
    def relatorio_estatisticas_gerais() -> Dict[str, Any]:
        """
        Gera relatório com estatísticas gerais do sistema
        """
        try:
            with DatabaseConnection() as conn:
                if conn is None:
                    return {}
                
                cur = conn.cursor()
                
                # Estatísticas básicas
                cur.execute("SELECT COUNT(*) FROM EMPRESA")
                total_empresas = cur.fetchone()[0]
                
                cur.execute("SELECT COUNT(*) FROM FILIAIS")
                total_filiais = cur.fetchone()[0]
                
                cur.execute("SELECT COUNT(*) FROM COLABORADORES")
                total_colaboradores = cur.fetchone()[0]
                
                cur.execute("SELECT COUNT(*) FROM SOLICITACAO")
                total_solicitacoes = cur.fetchone()[0]
                
                # Solicitações por status
                cur.execute("""
                    SELECT STATUS, COUNT(*) as quantidade 
                    FROM SOLICITACAO 
                    GROUP BY STATUS
                """)
                solicitacoes_por_status = {row[0]: row[1] for row in cur.fetchall()}
                
                # Solicitações por área
                cur.execute("""
                    SELECT AREA, COUNT(*) as quantidade 
                    FROM SOLICITACAO 
                    GROUP BY AREA
                    ORDER BY quantidade DESC
                """)
                solicitacoes_por_area = {row[0]: row[1] for row in cur.fetchall()}
                
                # Solicitações dos últimos 30 dias
                data_30_dias_atras = (datetime.now() - timedelta(days=30)).date()
                cur.execute("""
                    SELECT COUNT(*) 
                    FROM SOLICITACAO 
                    WHERE DT_ABERTURA >= %s
                """, (data_30_dias_atras,))
                solicitacoes_30_dias = cur.fetchone()[0]
                
                # Tempo médio de conclusão
                cur.execute("""
                    SELECT AVG(DT_CONCLUSAO - DT_ABERTURA) 
                    FROM SOLICITACAO 
                    WHERE STATUS = 'Concluída' AND DT_CONCLUSAO IS NOT NULL
                """)
                tempo_medio_conclusao = cur.fetchone()[0]
                
                return {
                    'total_empresas': total_empresas,
                    'total_filiais': total_filiais,
                    'total_colaboradores': total_colaboradores,
                    'total_solicitacoes': total_solicitacoes,
                    'solicitacoes_por_status': solicitacoes_por_status,
                    'solicitacoes_por_area': solicitacoes_por_area,
                    'solicitacoes_30_dias': solicitacoes_30_dias,
                    'tempo_medio_conclusao': tempo_medio_conclusao,
                    'data_geracao': datetime.now().strftime('%d/%m/%Y %H:%M')
                }
                
        except Exception as e:
            print(f"❌ Erro ao gerar relatório estatístico: {e}")
            return {}
    
    @staticmethod
    def relatorio_desempenho_colaboradores() -> List[Dict[str, Any]]:
        """
        Relatório de desempenho por colaborador
        """
        try:
            with DatabaseConnection() as conn:
                if conn is None:
                    return []
                
                cur = conn.cursor()
                
                cur.execute("""
                    SELECT 
                        RESPONSAVEL,
                        COUNT(*) as total_solicitacoes,
                        COUNT(CASE WHEN STATUS = 'Concluída' THEN 1 END) as concluidas,
                        COUNT(CASE WHEN STATUS = 'Em Andamento' THEN 1 END) as em_andamento,
                        COUNT(CASE WHEN STATUS = 'Aberta' THEN 1 END) as abertas,
                        AVG(CASE WHEN STATUS = 'Concluída' AND DT_CONCLUSAO IS NOT NULL 
                            THEN (DT_CONCLUSAO - DT_ABERTURA) END) as tempo_medio_conclusao
                    FROM SOLICITACAO
                    WHERE RESPONSAVEL IS NOT NULL
                    GROUP BY RESPONSAVEL
                    ORDER BY total_solicitacoes DESC
                """)
                
                resultados = []
                for row in cur.fetchall():
                    resultados.append({
                        'responsavel': row[0],
                        'total_solicitacoes': row[1],
                        'concluidas': row[2],
                        'em_andamento': row[3],
                        'abertas': row[4],
                        'tempo_medio_conclusao': row[5] or 0,
                        'taxa_conclusao': (row[2] / row[1] * 100) if row[1] > 0 else 0
                    })
                
                return resultados
                
        except Exception as e:
            print(f"❌ Erro ao gerar relatório de desempenho: {e}")
            return []
    
    @staticmethod
    def relatorio_solicitacoes_periodo(data_inicio: str, data_fim: str) -> Dict[str, Any]:
        """
        Relatório de solicitações por período
        """
        try:
            with DatabaseConnection() as conn:
                if conn is None:
                    return {}
                
                cur = conn.cursor()
                
                cur.execute("""
                    SELECT 
                        COUNT(*) as total,
                        COUNT(CASE WHEN STATUS = 'Concluída' THEN 1 END) as concluidas,
                        COUNT(CASE WHEN STATUS = 'Em Andamento' THEN 1 END) as em_andamento,
                        COUNT(CASE WHEN STATUS = 'Aberta' THEN 1 END) as abertas,
                        COUNT(CASE WHEN STATUS = 'Cancelada' THEN 1 END) as canceladas,
                        AREA,
                        COUNT(*) as quantidade
                    FROM SOLICITACAO
                    WHERE DT_ABERTURA BETWEEN %s AND %s
                    GROUP BY AREA
                    ORDER BY quantidade DESC
                """, (data_inicio, data_fim))
                
                por_area = []
                for row in cur.fetchall():
                    por_area.append({
                        'area': row[5],
                        'quantidade': row[6],
                        'percentual': (row[6] / row[0] * 100) if row[0] > 0 else 0
                    })
                
                # Estatísticas gerais do período
                cur.execute("""
                    SELECT 
                        COUNT(*) as total,
                        COUNT(CASE WHEN STATUS = 'Concluída' THEN 1 END) as concluidas,
                        AVG(CASE WHEN STATUS = 'Concluída' AND DT_CONCLUSAO IS NOT NULL 
                            THEN (DT_CONCLUSAO - DT_ABERTURA) END) as tempo_medio
                    FROM SOLICITACAO
                    WHERE DT_ABERTURA BETWEEN %s AND %s
                """, (data_inicio, data_fim))
                
                stats_row = cur.fetchone()
                
                return {
                    'periodo': f"{data_inicio} a {data_fim}",
                    'total_solicitacoes': stats_row[0],
                    'concluidas': stats_row[1],
                    'taxa_conclusao': (stats_row[1] / stats_row[0] * 100) if stats_row[0] > 0 else 0,
                    'tempo_medio_conclusao': stats_row[2] or 0,
                    'solicitacoes_por_area': por_area,
                    'data_geracao': datetime.now().strftime('%d/%m/%Y %H:%M')
                }
                
        except Exception as e:
            print(f"❌ Erro ao gerar relatório por período: {e}")
            return {}