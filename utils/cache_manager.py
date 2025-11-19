# 📄 utils/cache_manager.py
"""
SISTEMA DE CACHE PARA MELHORAR PERFORMANCE
Cache de dados frequentes para reduzir queries ao banco
"""

import time
from typing import Any, Dict
import threading

class CacheManager:
    """
    Gerenciador de cache em memória para dados frequentes
    """
    
    _instance = None
    _cache: Dict[str, Dict[str, Any]] = {}
    _lock = threading.RLock()
    
    # Tempos de expiração em segundos
    TTL_COLABORADORES = 300  # 5 minutos
    TTL_EMPRESAS = 600       # 10 minutos  
    TTL_FILIAIS = 600        # 10 minutos
    TTL_SOLICITACOES = 120   # 2 minutos
    
    @classmethod
    def get_instance(cls):
        """Singleton pattern"""
        if cls._instance is None:
            cls._instance = CacheManager()
        return cls._instance
    
    def __init__(self):
        self._cache = {}
    
    def get(self, key: str) -> Any:
        """
        Recupera dados do cache se ainda forem válidos
        """
        with self._lock:
            if key in self._cache:
                cache_data = self._cache[key]
                # Verifica se o cache ainda é válido
                if time.time() - cache_data['timestamp'] < cache_data['ttl']:
                    return cache_data['data']
                else:
                    # Remove do cache se expirado
                    del self._cache[key]
                    print(f"🔄 Cache expirado: {key}")
            return None
    
    def set(self, key: str, data: Any, ttl: int = 300):
        """
        Armazena dados no cache com tempo de expiração
        """
        with self._lock:
            self._cache[key] = {
                'data': data,
                'timestamp': time.time(),
                'ttl': ttl
            }
            print(f"💾 Cache atualizado: {key} (TTL: {ttl}s)")
    
    def delete(self, key: str):
        """
        Remove dados específicos do cache
        """
        with self._lock:
            if key in self._cache:
                del self._cache[key]
                print(f"🗑️  Cache removido: {key}")
    
    def clear(self):
        """
        Limpa todo o cache
        """
        with self._lock:
            self._cache.clear()
            print("🧹 Cache limpo completamente")
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Retorna estatísticas do cache
        """
        with self._lock:
            total_items = len(self._cache)
            expired_items = 0
            now = time.time()
            
            for key, data in self._cache.items():
                if now - data['timestamp'] > data['ttl']:
                    expired_items += 1
            
            return {
                'total_items': total_items,
                'expired_items': expired_items,
                'valid_items': total_items - expired_items
            }

# Instância global do cache
cache_manager = CacheManager.get_instance()