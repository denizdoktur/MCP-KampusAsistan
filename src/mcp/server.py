"""
MCP Server Ana Sınıfı
Model Context Protocol server implementasyonu
"""

import sys
import json
import asyncio
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

from ..tools.base_tool import BaseTool

logger = logging.getLogger(__name__)

class MCPServer:
    """MCP Protocol Server"""
    
    def __init__(self, name: str, version: str, description: str):
        self.name = name
        self.version = version
        self.description = description
        self.tools: Dict[str, BaseTool] = {}
        self.initialized = False
        
    def register_tool(self, tool: BaseTool):
        """Tool kaydet"""
        self.tools[tool.name] = tool
        logger.info(f"Tool kaydedildi: {tool.name}")
    
    def unregister_tool(self, tool_name: str):
        """Tool kaydını kaldır"""
        if tool_name in self.tools:
            del self.tools[tool_name]
            logger.info(f"Tool kaydı kaldırıldı: {tool_name}")
    
    async def handle_initialize(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Initialize isteğini işle"""
        self.initialized = True
        
        return {
            "jsonrpc": "2.0",
            "id": request.get("id"),
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {}
                },
                "serverInfo": {
                    "name": self.name,
                    "version": self.version
                }
            }
        }
    
    async def handle_tools_list(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Tool listesi isteğini işle"""
        tools_list = []
        
        for tool in self.tools.values():
            tools_list.append({
                "name": tool.name,
                "description": tool.description,
                "inputSchema": tool.input_schema
            })
        
        return {
            "jsonrpc": "2.0",
            "id": request.get("id"),
            "result": {"tools": tools_list}
        }
    
    async def handle_tools_call(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Tool çağrısı isteğini işle"""
        try:
            params = request.get("params", {})
            tool_name = params.get("name")
            arguments = params.get("arguments", {})
            
            if not tool_name:
                raise ValueError("Tool name gerekli")
            
            if tool_name not in self.tools:
                raise ValueError(f"Bilinmeyen tool: {tool_name}")
            
            # Tool'u çalıştır
            tool = self.tools[tool_name]
            result = await tool.safe_execute(**arguments)
            
            return {
                "jsonrpc": "2.0",
                "id": request.get("id"),
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps(result, ensure_ascii=False, indent=2)
                        }
                    ]
                }
            }
            
        except Exception as e:
            logger.error(f"Tool çağrısı hatası: {e}")
            return {
                "jsonrpc": "2.0",
                "id": request.get("id"),
                "error": {
                    "code": -1,
                    "message": str(e)
                }
            }
    
    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Gelen isteği işle"""
        try:
            method = request.get("method")
            
            if method == "initialize":
                return await self.handle_initialize(request)
            elif method == "tools/list":
                return await self.handle_tools_list(request)
            elif method == "tools/call":
                return await self.handle_tools_call(request)
            elif method == "ping":
                return await self.handle_ping(request)
            elif method == "notifications/initialized":
                # İstemci başlatma tamamlandığında gönderilen bildirim
                return None  # Yanıt gerekmez
            else:
                # Bilinmeyen method - boş yanıt dön
                return {
                    "jsonrpc": "2.0",
                    "id": request.get("id"),
                    "result": {}
                }
                
        except Exception as e:
            logger.error(f"İstek işleme hatası: {e}")
            return {
                "jsonrpc": "2.0",
                "id": request.get("id"),
                "error": {
                    "code": -32603,
                    "message": f"Internal error: {str(e)}"
                }
            }
    
    async def handle_ping(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Ping isteğini işle"""
        return {
            "jsonrpc": "2.0",
            "id": request.get("id"),
            "result": {
                "status": "alive",
                "timestamp": datetime.now().isoformat(),
                "server": self.name,
                "version": self.version,
                "tools_count": len(self.tools)
            }
        }
    
    async def run_stdio(self):
        """STDIO üzerinden MCP server çalıştır"""
        logger.info(f"🚀 {self.name} başlatılıyor...")
        logger.info(f"📊 Kayıtlı tool sayısı: {len(self.tools)}")
        logger.info(f"🔧 Tool'lar: {list(self.tools.keys())}")
        
        try:
            while True:
                # STDIN'den satır oku
                line = await asyncio.get_event_loop().run_in_executor(
                    None, sys.stdin.readline
                )
                
                if not line:
                    logger.info("STDIN kapatıldı, server sonlandırılıyor")
                    break
                
                line = line.strip()
                if not line:
                    continue
                
                try:
                    # JSON isteğini parse et
                    request = json.loads(line)
                    logger.debug(f"📥 Gelen istek: {request.get('method', 'unknown')}")
                    
                    # İsteği işle
                    response = await self.handle_request(request)
                    
                    # Yanıt varsa gönder
                    if response is not None:
                        response_json = json.dumps(response, ensure_ascii=False)
                        print(response_json, flush=True)
                        logger.debug(f"📤 Gönderilen yanıt: {response.get('result', {}).get('content', [{}])[0].get('type', 'unknown') if 'result' in response else 'error'}")
                    
                except json.JSONDecodeError as e:
                    logger.error(f"JSON parse hatası: {e}")
                    error_response = {
                        "jsonrpc": "2.0",
                        "id": None,
                        "error": {
                            "code": -32700,
                            "message": "Parse error"
                        }
                    }
                    print(json.dumps(error_response), flush=True)
                
                except Exception as e:
                    logger.error(f"İstek işleme hatası: {e}")
                    error_response = {
                        "jsonrpc": "2.0",
                        "id": None,
                        "error": {
                            "code": -32603,
                            "message": f"Internal error: {str(e)}"
                        }
                    }
                    print(json.dumps(error_response), flush=True)
        
        except KeyboardInterrupt:
            logger.info("🛑 Server manuel olarak durduruldu")
        except Exception as e:
            logger.error(f"❌ Server hatası: {e}")
            raise
        finally:
            logger.info("🔚 Server kapandı")
    
    def get_server_info(self) -> Dict[str, Any]:
        """Server bilgilerini getir"""
        return {
            "name": self.name,
            "version": self.version,
            "description": self.description,
            "initialized": self.initialized,
            "tools_count": len(self.tools),
            "tools": list(self.tools.keys()),
            "capabilities": {
                "tools": {}
            }
        }
    
    def get_tool_info(self, tool_name: str) -> Optional[Dict[str, Any]]:
        """Belirli bir tool'un bilgilerini getir"""
        if tool_name not in self.tools:
            return None
        
        tool = self.tools[tool_name]
        return {
            "name": tool.name,
            "description": tool.description,
            "input_schema": tool.input_schema,
            "class_name": tool.__class__.__name__
        }
    
    async def validate_tool_call(self, tool_name: str, arguments: Dict[str, Any]) -> bool:
        """Tool çağrısını doğrula"""
        if tool_name not in self.tools:
            return False
        
        try:
            tool = self.tools[tool_name]
            tool.validate_parameters(arguments)
            return True
        except Exception:
            return False
    
    def get_statistics(self) -> Dict[str, Any]:
        """Server istatistikleri"""
        return {
            "server_name": self.name,
            "uptime": "N/A",  # Gelecekte eklenebilir
            "total_tools": len(self.tools),
            "tools_by_category": self._categorize_tools(),
            "initialization_status": self.initialized
        }
    
    def _categorize_tools(self) -> Dict[str, List[str]]:
        """Tool'ları kategorilere ayır"""
        categories = {
            "database": [],
            "web_scraping": [], 
            "api_integration": [],
            "utility": []
        }
        
        for tool_name, tool in self.tools.items():
            if "database" in tool_name.lower() or "db" in tool_name.lower():
                categories["database"].append(tool_name)
            elif "scraper" in tool_name.lower() or "web" in tool_name.lower():
                categories["web_scraping"].append(tool_name)
            elif "api" in tool_name.lower():
                categories["api_integration"].append(tool_name)
            else:
                categories["utility"].append(tool_name)
        
        return categories