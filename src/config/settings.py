"""
Basitleştirilmiş Proje Ayarları
pydantic_settings'e bağımlılık olmadan
"""

import os
from pathlib import Path
from typing import Optional

class Settings:
    """Basit uygulama ayarları"""
    
    def __init__(self):
        # Temel ayarlar
        self.app_name = "MCBU Öğrenci İşleri MCP Server"
        self.app_version = "1.0.0"
        self.debug = True
        self.log_level = "INFO"
        
        # Veritabanı ayarları
        self.database_path = "data/student_affairs.db"
        self.database_backup_enabled = True
        
        # MCP Server ayarları
        self.mcp_server_name = "Öğrenci İşleri MCP Server"
        self.mcp_server_description = "MCBU Öğrenci İşleri otomasyonu için MCP server"
        self.mcp_protocol_version = "2024-11-05"
        
        # Web Scraping ayarları
        self.scraper_timeout = 10
        self.scraper_max_retries = 3
        self.scraper_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        self.mcbu_base_url = "https://www.mcbu.edu.tr"
        
        # API ayarları (gelecek için)
        self.api_timeout = 30
        self.api_max_retries = 3
        
        # Güvenlik ayarları
        self.max_query_results = 1000
        self.allowed_sql_keywords = ["SELECT", "FROM", "WHERE", "JOIN", "ORDER BY", "GROUP BY", "HAVING", "LIMIT"]
        self.forbidden_sql_keywords = ["DROP", "DELETE", "UPDATE", "INSERT", "ALTER", "CREATE", "TRUNCATE", "GRANT", "REVOKE"]
        
        # Dosya yolları
        self.log_directory = "data/logs"
        self.backup_directory = "data/backups"
        self.temp_directory = "data/temp"
        
        # Dizinleri oluştur
        self._create_directories()
    
    def _create_directories(self):
        """Gerekli dizinleri oluştur"""
        directories = [
            self.log_directory,
            self.backup_directory,
            self.temp_directory,
            os.path.dirname(self.database_path)
        ]
        
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)
    
    @property
    def database_url(self) -> str:
        """SQLite veritabanı URL'si"""
        return f"sqlite:///{self.database_path}"
    
    def get_log_file_path(self, log_name: str = "mcp_server") -> str:
        """Log dosya yolu"""
        return os.path.join(self.log_directory, f"{log_name}.log")
    
    def is_sql_query_safe(self, query: str) -> bool:
        """SQL sorgusu güvenli mi kontrol et"""
        query_upper = query.upper().strip()
        
        # Yasak anahtar kelimeler kontrolü
        for keyword in self.forbidden_sql_keywords:
            if keyword in query_upper:
                return False
        
        # SELECT ile başlamalı
        if not query_upper.startswith("SELECT"):
            return False
        
        return True
    
    def get_scraper_headers(self) -> dict:
        """Web scraper için HTTP headers"""
        return {
            "User-Agent": self.scraper_user_agent,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "tr-TR,tr;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding": "gzip, deflate",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
        }
    
    def get_database_config(self) -> dict:
        """Veritabanı yapılandırması"""
        return {
            "path": self.database_path,
            "backup_enabled": self.database_backup_enabled,
            "max_query_results": self.max_query_results
        }
    
    def get_mcp_config(self) -> dict:
        """MCP server yapılandırması"""
        return {
            "name": self.mcp_server_name,
            "description": self.mcp_server_description,
            "version": self.app_version,
            "protocol_version": self.mcp_protocol_version
        }

# Global settings instance
settings = Settings()