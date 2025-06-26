#!/usr/bin/env python3
"""
Öğrenci İşleri MCP Projesi - Veritabanı Kurulum Scripti
Bu script veritabanını kurar ve örnek verileri ekler
"""

import sys
import asyncio
import logging
from pathlib import Path

# Proje kök dizinini path'e ekle
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.database.connection import DatabaseManager
from src.config.settings import Settings

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def setup_database():
    """Veritabanını kur ve test et"""
    
    print("🎓 MCBU Öğrenci İşleri MCP Projesi - Veritabanı Kurulumu")
    print("=" * 60)
    
    try:
        # Settings yükle
        settings = Settings()
        logger.info(f"📁 Veritabanı yolu: {settings.database_path}")
        
        # DatabaseManager oluştur
        db_manager = DatabaseManager(settings.database_path)
        
        # Veritabanını başlat
        print("📊 Veritabanı şeması oluşturuluyor...")
        await db_manager.initialize()
        
        # İstatistikleri göster
        print("\n📈 Veritabanı İstatistikleri:")
        stats = await db_manager.get_database_stats()
        for key, value in stats.items():
            if '_count' in key:
                table_name = key.replace('_count', '')
                print(f"   {table_name}: {value} kayıt")
            elif key == 'database_size_mb':
                print(f"   Veritabanı boyutu: {value} MB")
        
        # Tabloları listele
        print("\n📋 Oluşturulan Tablolar:")
        tables = await db_manager.get_all_tables()
        for table in tables:
            if not table.startswith('sqlite_'):
                print(f"   ✅ {table}")
        
        # Örnek sorgular
        print("\n🔍 Örnek Sorgular Test Ediliyor:")
        
        # Öğrenci sayısı
        student_count = await db_manager.fetch_scalar("SELECT COUNT(*) FROM ogrenciler")
        print(f"   👥 Toplam öğrenci: {student_count}")
        
        # Fakülte sayısı
        faculty_count = await db_manager.fetch_scalar("SELECT COUNT(*) FROM fakulteler")
        print(f"   🏢 Toplam fakülte: {faculty_count}")
        
        # En yüksek GANO
        max_gpa = await db_manager.fetch_scalar("SELECT MAX(gano) FROM ogrenciler WHERE gano IS NOT NULL")
        print(f"   🏆 En yüksek GANO: {max_gpa}")
        
        # Örnek öğrenci bilgisi
        sample_student = await db_manager.fetch_one("""
            SELECT o.ogrenci_no, o.ad, o.soyad, f.fakülte_adi, b.bolum_adi
            FROM ogrenciler o
            JOIN fakulteler f ON o.fakulte_id = f.id
            JOIN bolumler b ON o.bolum_id = b.id
            LIMIT 1
        """)
        
        if sample_student:
            print(f"   📚 Örnek öğrenci: {sample_student['ogrenci_no']} - {sample_student['ad']} {sample_student['soyad']}")
            print(f"     Fakülte: {sample_student['fakülte_adi']}")
            print(f"     Bölüm: {sample_student['bolum_adi']}")
        
        print("\n✅ Veritabanı kurulumu başarıyla tamamlandı!")
        print("\n📖 Kullanım Örnekleri:")
        print("   python src/main.py  # MCP server'ı başlat")
        print("   # Continue.dev ile test et:")
        print("   # '202012345 numaralı öğrencinin bilgilerini getir'")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Kurulum hatası: {e}")
        return False

async def test_tools():
    """Tool'ları test et"""
    print("\n🔧 Tool'lar Test Ediliyor:")
    
    try:
        from src.tools.mcbu_scraper import MCBUScraperTool
        from src.tools.student_db import StudentDatabaseTool
        from src.tools.web_api_placeholder import WebAPIPlaceholderTool
        from src.database.connection import DatabaseManager
        from src.config.settings import Settings
        
        # DatabaseManager
        settings = Settings()
        db_manager = DatabaseManager(settings.database_path)
        
        # Tool'ları oluştur
        mcbu_scraper = MCBUScraperTool()
        student_db = StudentDatabaseTool(db_manager)
        web_api = WebAPIPlaceholderTool()
        
        print(f"   ✅ {mcbu_scraper.name}: {mcbu_scraper.description}")
        print(f"   ✅ {student_db.name}: {student_db.description}")
        print(f"   ✅ {web_api.name}: {web_api.description}")
        
        # Basit test
        print("\n🧪 Basit Tool Testleri:")
        
        # Student DB test
        test_result = await student_db.execute(
            operation="fakulte_bolum_listesi"
        )
        if test_result.get("success"):
            data = test_result.get("data", {})
            print(f"   ✅ Veritabanı tool'u: {len(data.get('fakulteler', []))} fakülte bulundu")
        else:
            print(f"   ❌ Veritabanı tool'u hatası: {test_result.get('error')}")
        
        # Web API test (mock)
        api_result = await web_api.execute(
            api_endpoint="student_info",
            student_id="202012345"
        )
        if api_result.get("success"):
            print("   ✅ Web API tool'u: Mock response başarılı")
        else:
            print(f"   ❌ Web API tool'u hatası: {api_result.get('error')}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Tool test hatası: {e}")
        return False

async def create_sample_queries():
    """Örnek sorguları dosyaya yaz"""
    print("\n📝 Örnek Sorguları Oluşturuluyor...")
    
    sample_queries = """
# MCBU Öğrenci İşleri MCP - Örnek Sorgular

## Continue.dev Chat Örnekleri

### Öğrenci Bilgi Sorguları
- "202012345 numaralı öğrencinin bilgilerini getir"
- "Ahmet Yılmaz isimli öğrencileri ara"
- "Bilgisayar Mühendisliği bölümündeki öğrencileri listele"

### Akademik Sorguları
- "202012345 numaralı öğrencinin notlarını göster"
- "2024-2025 Bahar dönemindeki derslerini listele"
- "GANO hesapla ve dönem ortalamaları"
- "Devamsızlık durumunu kontrol et"

### Üniversite Bilgileri
- "MCBU'nun vizyon ve misyonunu anlat"
- "Mühendislik fakültesindeki bölümleri listele"
- "Akademik takvimi getir"
- "İletişim bilgilerini göster"

### İdari İşlemler
- "Burs ve kredi bilgilerini göster"
- "Staj kayıtlarını listele"
- "Kulüp üyeliklerimi göster"
- "Danışman bilgilerini getir"

### Özel Sorgular
- "En yüksek GANO'ya sahip öğrencileri listele"
- "2024-2025 Güz döneminde verilen dersleri göster"
- "Aktif kulüpleri ve üye sayılarını listele"

## Tool Parametreleri

### Student Database Tool
```json
{
  "operation": "ogrenci_ara",
  "arama_metni": "Ahmet",
  "limit": 10
}
```

### MCBU Web Scraper Tool
```json
{
  "page_type": "vizyon_misyon"
}
```

### Web API Tool (Mock)
```json
{
  "api_endpoint": "student_info",
  "student_id": "202012345"
}
```
"""
    
    try:
        # Örnek sorguları dosyaya yaz
        queries_path = project_root / "data" / "sample_queries.md"
        queries_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(queries_path, 'w', encoding='utf-8') as f:
            f.write(sample_queries)
        
        print(f"   ✅ Örnek sorgular kaydedildi: {queries_path}")
        return True
        
    except Exception as e:
        logger.error(f"❌ Örnek sorgu oluşturma hatası: {e}")
        return False

async def main():
    """Ana kurulum fonksiyonu"""
    print("🚀 Kurulum başlatılıyor...\n")
    
    # Veritabanı kurulumu
    db_success = await setup_database()
    if not db_success:
        print("❌ Veritabanı kurulumu başarısız!")
        return 1
    
    # Tool testleri
    tool_success = await test_tools()
    if not tool_success:
        print("⚠️  Tool testleri başarısız, ancak kurulum devam ediyor...")
    
    # Örnek sorgular
    queries_success = await create_sample_queries()
    if not queries_success:
        print("⚠️  Örnek sorgu oluşturma başarısız...")
    
    print("\n" + "=" * 60)
    print("🎉 Kurulum tamamlandı!")
    print("\n📋 Sonraki Adımlar:")
    print("1. Continue.dev yapılandırması yapın")
    print("2. 'python src/main.py' ile server'ı başlatın")
    print("3. Continue.dev chat'inde örnek sorguları deneyin")
    print("\n📚 Daha fazla bilgi için README.md dosyasına bakın")
    
    return 0

if __name__ == "__main__":
    exit_code = asyncio.run(main())