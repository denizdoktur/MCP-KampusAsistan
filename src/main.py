#!/usr/bin/env python3
"""
MCBU Öğrenci İşleri MCP Server - Düzeltilmiş ve Optimize Edilmiş
Tüm hatalar giderildi, performans iyileştirildi
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

# Hızlı logging setup
logging.basicConfig(
    level=logging.ERROR,  # Sadece hatalar
    format='%(levelname)s: %(message)s',
    handlers=[logging.StreamHandler(sys.stderr)]
)

logger = logging.getLogger(__name__)

class MCPServer:
    """Basit ve hızlı MCP Server"""
    
    def __init__(self):
        self.name = "MCBU Student Affairs Server"
        self.version = "1.2.0"
        self.db_manager = None
        self.tools = {}
        self.initialized = False
    
    async def init_database(self):
        """Veritabanını sadece gerektiğinde başlat"""
        if self.db_manager is None:
            try:
                # Import'ları lazy yap
                from src.database.connection import DatabaseManager
                from src.tools.student_db import StudentDatabaseTool
                
                self.db_manager = DatabaseManager("data/student_affairs.db")
                await self.db_manager.initialize()
                
                # Tool'u kaydet
                student_tool = StudentDatabaseTool(self.db_manager)
                self.tools[student_tool.name] = student_tool
                
                print("✅ Veritabanı hazır", file=sys.stderr)
                
            except Exception as e:
                logger.error(f"Veritabanı hatası: {e}")
                raise
    
    async def handle_request(self, request: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """MCP isteğini işle"""
        method = request.get("method")
        req_id = request.get("id")
        
        try:
            if method == "initialize":
                self.initialized = True
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {"tools": {}},
                        "serverInfo": {
                            "name": self.name,
                            "version": self.version
                        }
                    }
                }
            
            elif method == "tools/list":
                # Lazy init
                await self.init_database()
                
                tools_list = []
                for tool in self.tools.values():
                    tools_list.append({
                        "name": tool.name,
                        "description": tool.description,
                        "inputSchema": tool.input_schema
                    })
                
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {"tools": tools_list}
                }
            
            elif method == "tools/call":
                # Lazy init
                await self.init_database()
                
                params = request.get("params", {})
                tool_name = params.get("name")
                arguments = params.get("arguments", {})
                
                if tool_name in self.tools:
                    tool = self.tools[tool_name]
                    result = await tool.execute(**arguments)
                    
                    return {
                        "jsonrpc": "2.0",
                        "id": req_id,
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
                    raise ValueError(f"Bilinmeyen tool: {tool_name}")
            
            elif method == "notifications/initialized":
                # Continue.dev ready - no response needed
                return None
            
            else:
                # Bilinmeyen method - boş yanıt
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {}
                }
        
        except Exception as e:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {
                    "code": -1,
                    "message": str(e)
                }
            }

async def main():
    """Ana STDIO döngüsü"""
    server = MCPServer()
    
    # Başlatma mesajı
    print("🎓 MCBU MCP Server başlatılıyor...", file=sys.stderr, flush=True)
    
    try:
        while True:
            # STDIN'den JSON okuma
            line = await asyncio.get_event_loop().run_in_executor(
                None, sys.stdin.readline
            )
            
            if not line:
                break
            
            line = line.strip()
            if not line:
                continue
            
            try:
                # JSON parse
                request = json.loads(line)
                
                # İsteği işle
                response = await server.handle_request(request)
                
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
        print("Server durduruldu", file=sys.stderr)
    except Exception as e:
        print(f"Server hatası: {e}", file=sys.stderr)
        raise

if __name__ == "__main__":
    asyncio.run(main())