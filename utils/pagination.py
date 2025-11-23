# 📄 utils/pagination.py
"""
SISTEMA DE PAGINAÇÃO PARA LISTAS GRANDES
Melhora performance em listas com muitos registros
"""

from typing import List, Tuple, Any
import math

class Paginator:
    """
    Classe para paginação de listas grandes
    """
    
    def __init__(self, items: List[Any], items_per_page: int = 10):
        self.items = items
        self.items_per_page = items_per_page
        self.total_items = len(items)
        self.total_pages = math.ceil(self.total_items / items_per_page)
        self.current_page = 1
    
    def get_page(self, page_number: int = 1) -> Tuple[List[Any], dict]:
        """
        Retorna os itens da página específica
        """
        if page_number < 1:
            page_number = 1
        elif page_number > self.total_pages:
            page_number = self.total_pages
        
        self.current_page = page_number
        
        start_index = (page_number - 1) * self.items_per_page
        end_index = start_index + self.items_per_page
        
        page_items = self.items[start_index:end_index]
        
        pagination_info = {
            'current_page': page_number,
            'total_pages': self.total_pages,
            'total_items': self.total_items,
            'items_per_page': self.items_per_page,
            'start_index': start_index + 1,
            'end_index': min(end_index, self.total_items),
            'has_previous': page_number > 1,
            'has_next': page_number < self.total_pages
        }
        
        return page_items, pagination_info
    
    def get_pagination_range(self, max_pages: int = 5) -> List[int]:
        """
        Retorna range de páginas para exibição
        """
        if self.total_pages <= max_pages:
            return list(range(1, self.total_pages + 1))
        
        start = max(1, self.current_page - max_pages // 2)
        end = min(self.total_pages, start + max_pages - 1)
        
        if end - start + 1 < max_pages:
            start = max(1, end - max_pages + 1)
        
        return list(range(start, end + 1))

class DatabasePaginator:
    """
    Paginação direto no banco de dados para otimização
    """
    
    @staticmethod
    def paginate_query(query: str, page: int = 1, per_page: int = 10, params: tuple = None) -> Tuple[List[Any], dict]:
        """
        Executa query com LIMIT e OFFSET para paginação eficiente
        """
        from database.database import DatabaseConnection
        
        offset = (page - 1) * per_page
        
        # Query para contar total de registros (sem LIMIT)
        count_query = f"SELECT COUNT(*) FROM ({query}) as subquery"
        
        # Query principal com paginação
        paginated_query = f"{query} LIMIT {per_page} OFFSET {offset}"
        
        try:
            with DatabaseConnection() as conn:
                if conn is None:
                    return [], {}
                
                cur = conn.cursor()
                
                # Contar total de registros
                cur.execute(count_query, params or ())
                total_items = cur.fetchone()[0]
                total_pages = math.ceil(total_items / per_page)
                
                # Buscar dados paginados
                cur.execute(paginated_query, params or ())
                page_items = cur.fetchall()
                
                pagination_info = {
                    'current_page': page,
                    'total_pages': total_pages,
                    'total_items': total_items,
                    'items_per_page': per_page,
                    'start_index': offset + 1,
                    'end_index': min(offset + per_page, total_items),
                    'has_previous': page > 1,
                    'has_next': page < total_pages
                }
                
                return page_items, pagination_info
                
        except Exception as e:
            print(f"❌ Erro na paginação de query: {e}")
            return [], {}