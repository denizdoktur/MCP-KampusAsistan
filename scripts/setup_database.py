#!/usr/bin/env python3
"""
MCBU MCP Projesi - Hızlı Kurulum
1 dakikada kurulum ve test
"""

import sys
import asyncio
import logging
from pathlib import Path

# Proje kök dizini
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Minimal logging
logging.basicConfig(level=logging.ERROR)

async def quick_setup():
    """Hızlı kurulum"""
    
    print("🚀 MCBU MCP Hızlı Kurulum")
    print("-" * 40)
    
    try:
        # 1. Database kurulumu
        print("📊 Veritabanı kuruluyor...")
        from src.database.connection import DatabaseManager
        
        db_manager = DatabaseManager("data/student_affairs.db")
        await db_manager.initialize()
        
        # 2. İstatistikleri göster
        stats = await db_manager.get_database_stats()
        print(f"   ✅ {stats.get('ogrenciler_count', 0)} öğrenci")
        print(f"   ✅ {stats.get('fakulteler_count', 0)} fakülte")
        print(f"   ✅ {stats.get('dersler_count', 0)} ders")
        
        # 3. Tool test
        print("🔧 Tool test ediliyor...")
        from src.tools.student_db import StudentDatabaseTool
        
        tool = StudentDatabaseTool(db_manager)
        
        # Basit test
        test_result = await tool.execute(operation="istatistik")
        
        if test_result.get("success"):
            print("   ✅ Tool çalışıyor")
            data = test_result.get("data", {})
            print(f"   📈 Toplam öğrenci: {data.get('toplam_ogrenci', 0)}")
        else:
            print(f"   ❌ Tool hatası: {test_result.get('error')}")
            return False
        
        # 4. Örnek sorgular
        print("📝 Örnek sorgular test ediliyor...")
        
        # Öğrenci arama
        search_result = await tool.execute(
            operation="ogrenci_ara",
            arama_metni="Ahmet",
            limit=5
        )
        
        if search_result.get("success"):
            found = search_result.get("data", {}).get("bulunan_sayi", 0)
            print(f"   ✅ Öğrenci arama: {found} sonuç")
        
        # Detay bilgi
        detail_result = await tool.execute(
            operation="ogrenci_detay",
            ogrenci_no="202012345"
        )
        
        if detail_result.get("success"):
            print("   ✅ Öğrenci detay sorgusu çalışıyor")
        
        print("\n🎉 Kurulum Tamamlandı!")
        print("\n📋 Sonraki Adımlar:")
        print("1. Continue.dev config dosyasına ekleyin:")
        print('   "mcbu-student": {')
        print(f'     "command": "python",')
        print(f'     "args": ["{project_root}/src/main.py"]')
        print('   }')
        print("\n2. Continue.dev chat'te test edin:")
        print('   "202012345 numaralı öğrencinin bilgilerini getir"')
        print('   "Bilgisayar Mühendisliği öğrencilerini listele"')
        
        return True
        
    except Exception as e:
        print(f"❌ Kurulum hatası: {e}")
        return False

async def test_mcp_server():
    """MCP server'ı test et"""
    print("\n🧪 MCP Server test ediliyor...")
    
    try:
        # Server'ı import et
        from src.main import MCPServer
        
        server = MCPServer()
        
        # Basit initialize test
        init_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {}
        }
        
        response = await server.handle_request(init_request)
        
        if response and response.get("result"):
            print("   ✅ MCP Server başlatma OK")
            
            # Tools list test
            tools_request = {
                "jsonrpc": "2.0", 
                "id": 2,
                "method": "tools/list"
            }
            
            tools_response = await server.handle_request(tools_request)
            
            if tools_response and tools_response.get("result"):
                tools = tools_response["result"].get("tools", [])
                print(f"   ✅ {len(tools)} tool kayıtlı")
                
                # Tool çağrısı test
                call_request = {
                    "jsonrpc": "2.0",
                    "id": 3,
                    "method": "tools/call",
                    "params": {
                        "name": "student_database",
                        "arguments": {
                            "operation": "istatistik"
                        }
                    }
                }
                
                call_response = await server.handle_request(call_request)
                
                if call_response and call_response.get("result"):
                    print("   ✅ Tool çağrısı çalışıyor")
                    return True
        
        print("   ❌ MCP Server test başarısız")
        return False
        
    except Exception as e:
        print(f"   ❌ MCP test hatası: {e}")
        return False

async def main():
    """Ana kurulum fonksiyonu"""
    
    # Hızlı kurulum
    setup_ok = await quick_setup()
    
    if not setup_ok:
        print("\n❌ Kurulum başarısız!")
        return 1
    
    # MCP test
    mcp_ok = await test_mcp_server()
    
    if not mcp_ok:
        print("\n⚠️  MCP server test başarısız, ancak veritabanı kuruldu")
    
    print(f"\n✨ Kurulum dosyası: {project_root}/src/main.py")
    print("🔗 Continue.dev ile kullanmaya hazır!")
    
    return 0

if __name__ == "__main__":
    exit_code = asyncio.run(main())