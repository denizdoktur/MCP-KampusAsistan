#!/usr/bin/env python3
"""
Optimize Edilmiş MCP Server
Performans iyileştirmeleri ile hızlı çalışma
"""

import sys
import json
import asyncio
import logging
from typing import Dict, Any, Optional
from pathlib import Path

# Proje kök dizinini path'e ekle
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Basit settings
class SimpleSettings:
    database_path = "data/student_affairs.db"

settings = SimpleSettings()

try:
    from src.tools.student_db import StudentDatabaseTool
    from src.database.connection import DatabaseManager
except ImportError as e:
    print(f"Import hatası: {e}", file=sys.stderr)
    sys.exit(1)

# Logging setup (daha az verbose)
logging.basicConfig(
    level=logging.WARNING,  # Sadece önemli mesajlar
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stderr)]
)

logger = logging.getLogger(__name__)

class OptimizedMCPServer:
    """Optimize edilmiş MCP Server - Singleton pattern"""
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self.db_manager = DatabaseManager(settings.database_path)
            self.tools = {}
            self._db_ready = False
            self._register_tools()
            self._initialized = True
    
    def _register_tools(self):
        """Tool'ları kaydet"""
        student_db_tool = StudentDatabaseTool(self.db_manager)
        self.tools[student_db_tool.name] = student_db_tool
    
    async def ensure_database_ready(self):
        """Veritabanının hazır olduğundan emin ol (tek seferlik)"""
        if not self._db_ready:
            try:
                await self.db_manager.initialize()
                self._db_ready = True
            except Exception as e:
                logger.error(f"Veritabanı hatası: {e}")
                raise

# Global server instance
_server_instance: Optional[OptimizedMCPServer] = None

async def get_server() -> OptimizedMCPServer:
    """Server instance'ını al veya oluştur"""
    global _server_instance
    if _server_instance is None:
        _server_instance = OptimizedMCPServer()
        await _server_instance.ensure_database_ready()
    return _server_instance

async def handle_request(request: Dict[str, Any]) -> Dict[str, Any]:
    """MCP isteğini işle - optimize edilmiş"""
    try:
        method = request.get("method")
        request_id = request.get("id")
        
        if method == "initialize":
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {"tools": {}},
                    "serverInfo": {
                        "name": "MCBU Student Database Server (Optimized)",
                        "version": "1.1.0"
                    }
                }
            }
        
        elif method == "tools/list":
            server = await get_server()
            tools_list = []
            
            for tool in server.tools.values():
                tools_list.append({
                    "name": tool.name,
                    "description": tool.description,
                    "inputSchema": tool.input_schema
                })
            
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {"tools": tools_list}
            }
        
        elif method == "tools/call":
            server = await get_server()
            
            tool_name = request["params"]["name"]
            arguments = request["params"].get("arguments", {})
            
            if tool_name in server.tools:
                tool = server.tools[tool_name]
                
                # Tool'u hızlı çalıştır
                result = await tool.execute(**arguments)
                
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": json.dumps(result, ensure_ascii=False, indent=2)
                            }
                        ]
                    }
                }
            else:
                raise Exception(f"Bilinmeyen tool: {tool_name}")
        
        elif method == "notifications/initialized":
            # Continue.dev ready notification - no response needed
            return None
        
        else:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {}
            }
    
    except Exception as e:
        return {
            "jsonrpc": "2.0",
            "id": request.get("id"),
            "error": {
                "code": -1,
                "message": str(e)
            }
        }

async def main():
    """Ana STDIO döngüsü - optimize edilmiş"""
    print("MCBU Fast Server baslatiliyor...", file=sys.stderr, flush=True)
    
    # Server'ı önceden hazırla
    await get_server()
    print("Server hazir!", file=sys.stderr, flush=True)
    
    try:
        while True:
            # STDIN'den satır oku
            line = await asyncio.get_event_loop().run_in_executor(
                None, sys.stdin.readline
            )
            
            if not line:
                break
            
            line = line.strip()
            if not line:
                continue
            
            try:
                # JSON isteğini parse et
                request = json.loads(line)
                
                # İsteği hızlı işle
                response = await handle_request(request)
                
                # Yanıt varsa gönder
                if response is not None:
                    print(json.dumps(response, ensure_ascii=False), flush=True)
                
            except json.JSONDecodeError:
                error_response = {
                    "jsonrpc": "2.0",
                    "id": None,
                    "error": {"code": -32700, "message": "Parse error"}
                }
                print(json.dumps(error_response), flush=True)
            
            except Exception as e:
                error_response = {
                    "jsonrpc": "2.0",
                    "id": None,
                    "error": {"code": -1, "message": str(e)}
                }
                print(json.dumps(error_response), flush=True)
    
    except KeyboardInterrupt:
        pass
    except Exception as e:
        logger.error(f"Server hatasi: {e}")
        raise

if __name__ == "__main__":
    # Hızlı başlatma
    asyncio.run(main())