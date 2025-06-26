"""
Temel Tool Sınıfı
Tüm MCP tool'ları bu sınıftan türetilir
"""

import json
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class BaseTool(ABC):
    """Tüm MCP tool'ları için temel sınıf"""
    
    def __init__(self, name: str, description: str, input_schema: Dict[str, Any]):
        self.name = name
        self.description = description
        self.input_schema = input_schema
        self.logger = logging.getLogger(f"tools.{name}")
    
    @abstractmethod
    async def execute(self, **kwargs) -> Dict[str, Any]:
        """
        Tool'un ana işlevini gerçekleştir
        
        Args:
            **kwargs: Tool'a gelen parametreler
            
        Returns:
            Dict[str, Any]: Tool sonucu
        """
        pass
    
    def validate_parameters(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parametreleri doğrula
        
        Args:
            parameters: Gelen parametreler
            
        Returns:
            Dict[str, Any]: Doğrulanmış parametreler
            
        Raises:
            ValueError: Parametre doğrulama hatası
        """
        required_fields = self.input_schema.get("required", [])
        properties = self.input_schema.get("properties", {})
        
        # Zorunlu alanları kontrol et
        for field in required_fields:
            if field not in parameters:
                raise ValueError(f"Zorunlu parametre eksik: {field}")
        
        # Tip kontrolü 
        validated = {}
        for field, value in parameters.items():
            if field in properties:
                field_type = properties[field].get("type")
                if field_type == "string" and not isinstance(value, str):
                    raise ValueError(f"{field} string olmalı")
                elif field_type == "integer" and not isinstance(value, int):
                    raise ValueError(f"{field} integer olmalı")
                elif field_type == "boolean" and not isinstance(value, bool):
                    raise ValueError(f"{field} boolean olmalı")
            
            validated[field] = value
        
        return validated
    
    def create_success_response(self, data: Any, message: str = "İşlem başarılı") -> Dict[str, Any]:
        """
        Başarılı yanıt oluştur
        
        Args:
            data: Yanıt verisi
            message: Başarı mesajı
            
        Returns:
            Dict[str, Any]: Formatlanmış yanıt
        """
        return {
            "success": True,
            "message": message,
            "data": data,
            "timestamp": datetime.now().isoformat(),
            "tool": self.name
        }
    
    def create_error_response(self, error: str, error_code: Optional[str] = None) -> Dict[str, Any]:
        """
        Hata yanıtı oluştur
        
        Args:
            error: Hata mesajı
            error_code: Hata kodu (opsiyonel)
            
        Returns:
            Dict[str, Any]: Formatlanmış hata yanıtı
        """
        response = {
            "success": False,
            "error": error,
            "timestamp": datetime.now().isoformat(),
            "tool": self.name
        }
        
        if error_code:
            response["error_code"] = error_code
        
        return response
    
    async def safe_execute(self, **kwargs) -> Dict[str, Any]:
        """
        Güvenli tool çalıştırma (hata yakalama ile)
        
        Args:
            **kwargs: Tool parametreleri
            
        Returns:
            Dict[str, Any]: Tool sonucu veya hata
        """
        try:
            # Parametreleri doğrula
            validated_params = self.validate_parameters(kwargs)
            
            # Tool'u çalıştır
            self.logger.info(f"Tool çalıştırılıyor: {self.name}")
            result = await self.execute(**validated_params)
            
            self.logger.info(f"Tool başarıyla tamamlandı: {self.name}")
            return result
            
        except ValueError as e:
            error_msg = f"Parametre hatası: {e}"
            self.logger.error(error_msg)
            return self.create_error_response(error_msg, "VALIDATION_ERROR")
        
        except Exception as e:
            error_msg = f"Tool çalıştırma hatası: {e}"
            self.logger.error(error_msg)
            return self.create_error_response(error_msg, "EXECUTION_ERROR")
    
    def to_mcp_tool_definition(self) -> Dict[str, Any]:
        """
        MCP tool tanımına dönüştür
        
        Returns:
            Dict[str, Any]: MCP tool tanımı
        """
        return {
            "name": self.name,
            "description": self.description,
            "inputSchema": self.input_schema
        }