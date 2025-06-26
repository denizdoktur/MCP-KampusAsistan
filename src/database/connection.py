"""
Düzeltilmiş Database Connection Manager
Önemli hatalar giderildi ve performans iyileştirildi
"""

import aiosqlite
import logging
from typing import List, Dict, Any, Optional
from pathlib import Path

logger = logging.getLogger(__name__)

class DatabaseManager:
    """SQLite veritabanı bağlantı yöneticisi"""
    
    def __init__(self, db_path: str = "data/student_affairs.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
    async def initialize(self):
        """Veritabanını başlat ve tabloları oluştur"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await self._create_tables(db)
                await db.commit()
                logger.info("Veritabanı şeması başarıyla oluşturuldu")
            
            # Örnek veri ekle (eğer tablo boşsa)
            await self._populate_sample_data_if_empty()
            
        except Exception as e:
            logger.error(f"Veritabanı başlatma hatası: {e}")
            raise
    
    async def _create_tables(self, db):
        """Kompakt tablo yapısı oluştur"""
        
        # Fakülteler - DÜZELTME: fakulte_adi (Türkçe karakter sorunu)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS fakulteler (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fakulte_adi TEXT NOT NULL,
                dekan TEXT,
                telefon TEXT,
                email TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Bölümler
        await db.execute("""
            CREATE TABLE IF NOT EXISTS bolumler (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fakulte_id INTEGER,
                bolum_adi TEXT NOT NULL,
                bolum_kodu TEXT,
                bolum_baskani TEXT,
                telefon TEXT,
                email TEXT,
                FOREIGN KEY (fakulte_id) REFERENCES fakulteler(id)
            )
        """)
        
        # Öğretim üyeleri (sadeleştirilmiş)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS ogretim_uyeleri (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ad_soyad TEXT NOT NULL,
                unvan TEXT,
                fakulte_id INTEGER,
                bolum_id INTEGER,
                telefon TEXT,
                email TEXT,
                ofis_no TEXT,
                FOREIGN KEY (fakulte_id) REFERENCES fakulteler(id),
                FOREIGN KEY (bolum_id) REFERENCES bolumler(id)
            )
        """)
        
        # Dersler (sadeleştirilmiş)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS dersler (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ders_kodu TEXT NOT NULL UNIQUE,
                ders_adi TEXT NOT NULL,
                kredi INTEGER,
                sinif INTEGER,
                donem TEXT,
                zorunlu_secmeli TEXT,
                fakulte_id INTEGER,
                bolum_id INTEGER,
                FOREIGN KEY (fakulte_id) REFERENCES fakulteler(id),
                FOREIGN KEY (bolum_id) REFERENCES bolumler(id)
            )
        """)
        
        # Öğrenciler (temel alanlar)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS ogrenciler (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ogrenci_no TEXT NOT NULL UNIQUE,
                tc_kimlik_no TEXT UNIQUE,
                ad TEXT NOT NULL,
                soyad TEXT NOT NULL,
                dogum_tarihi DATE,
                cinsiyet TEXT,
                fakulte_id INTEGER,
                bolum_id INTEGER,
                sinif INTEGER,
                aktif_akademik_donem TEXT,
                kayit_tarihi DATE,
                durum TEXT DEFAULT 'aktif',
                birinci_danisman_id INTEGER,
                gano REAL,
                telefon TEXT,
                email TEXT,
                adres TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (fakulte_id) REFERENCES fakulteler(id),
                FOREIGN KEY (bolum_id) REFERENCES bolumler(id),
                FOREIGN KEY (birinci_danisman_id) REFERENCES ogretim_uyeleri(id)
            )
        """)
        
        # Ders kayıtları
        await db.execute("""
            CREATE TABLE IF NOT EXISTS ogrenci_ders_kayitlari (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ogrenci_id INTEGER,
                ders_id INTEGER,
                akademik_donem TEXT,
                kayit_tarihi DATE,
                durum TEXT DEFAULT 'aktif',
                FOREIGN KEY (ogrenci_id) REFERENCES ogrenciler(id),
                FOREIGN KEY (ders_id) REFERENCES dersler(id)
            )
        """)
        
        # Sınav notları
        await db.execute("""
            CREATE TABLE IF NOT EXISTS sinav_notlari (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ogrenci_id INTEGER,
                ders_id INTEGER,
                akademik_donem TEXT,
                vize_notu REAL,
                final_notu REAL,
                toplam_puan REAL,
                harf_notu TEXT,
                basari_durumu TEXT,
                FOREIGN KEY (ogrenci_id) REFERENCES ogrenciler(id),
                FOREIGN KEY (ders_id) REFERENCES dersler(id)
            )
        """)
        
        # Dönem notları
        await db.execute("""
            CREATE TABLE IF NOT EXISTS donem_notlari (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ogrenci_id INTEGER,
                akademik_donem TEXT,
                alinan_kredi INTEGER,
                basarili_kredi INTEGER,
                donem_not_ortalamasi REAL,
                genel_not_ortalamasi REAL,
                FOREIGN KEY (ogrenci_id) REFERENCES ogrenciler(id)
            )
        """)
        
        # Trigger
        await db.execute("""
            CREATE TRIGGER IF NOT EXISTS update_ogrenci_timestamp 
                AFTER UPDATE ON ogrenciler
                FOR EACH ROW
            BEGIN
                UPDATE ogrenciler SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
            END
        """)
    
    async def _populate_sample_data_if_empty(self):
        """Eğer veritabanı boşsa örnek veri ekle"""
        try:
            count = await self.fetch_scalar("SELECT COUNT(*) FROM ogrenciler")
            
            if count == 0:
                logger.info("Veritabanı boş, örnek veriler ekleniyor...")
                await self._insert_sample_data()
                logger.info("Örnek veriler başarıyla eklendi")
            
        except Exception as e:
            logger.warning(f"Örnek veri ekleme hatası: {e}")
    
    async def _insert_sample_data(self):
        """Kompakt örnek veri ekle"""
        
        # Fakülteler - DÜZELTME: doğru kolon adı
        fakulteler = [
            ("Mühendislik Fakültesi", "Prof. Dr. Ali KORKMAZ", "0236-201-2000", "muhendislik@mcbu.edu.tr"),
            ("Tıp Fakültesi", "Prof. Dr. Mehmet SAĞLAM", "0236-233-2000", "tip@mcbu.edu.tr"),
            ("İktisadi ve İdari Bilimler Fakültesi", "Prof. Dr. Ayşe YILMAZ", "0236-201-3000", "iibf@mcbu.edu.tr")
        ]
        
        for fakulte in fakulteler:
            await self.execute(
                "INSERT OR IGNORE INTO fakulteler (fakulte_adi, dekan, telefon, email) VALUES (?, ?, ?, ?)",
                fakulte
            )
        
        # Bölümler
        bolumler = [
            (1, "Bilgisayar Mühendisliği", "BM", "Dr. Öğr. Üyesi Zeynep YILDIZ", "0236-201-2100", "bilgisayar@mcbu.edu.tr"),
            (1, "Elektrik-Elektronik Mühendisliği", "EEM", "Prof. Dr. Ahmet ÖZTÜRK", "0236-201-2200", "elektrik@mcbu.edu.tr"),
            (2, "Genel Tıp", "TIP", "Prof. Dr. Selma DOKTOR", "0236-233-2100", "tip@mcbu.edu.tr"),
            (3, "İşletme", "ISL", "Prof. Dr. Can TICARET", "0236-201-3100", "isletme@mcbu.edu.tr")
        ]
        
        for bolum in bolumler:
            await self.execute(
                "INSERT OR IGNORE INTO bolumler (fakulte_id, bolum_adi, bolum_kodu, bolum_baskani, telefon, email) VALUES (?, ?, ?, ?, ?, ?)",
                bolum
            )
        
        # Öğretim üyeleri
        ogretim_uyeleri = [
            ("Dr. Öğr. Üyesi Zeynep YILDIZ", "Dr. Öğr. Üyesi", 1, 1, "0236-201-2101", "zeynep@mcbu.edu.tr", "MF-201"),
            ("Prof. Dr. Ahmet ÖZTÜRK", "Profesör", 1, 2, "0236-201-2201", "ahmet@mcbu.edu.tr", "MF-301"),
            ("Prof. Dr. Selma DOKTOR", "Profesör", 2, 3, "0236-233-2101", "selma@mcbu.edu.tr", "TF-101"),
            ("Prof. Dr. Can TICARET", "Profesör", 3, 4, "0236-201-3101", "can@mcbu.edu.tr", "IF-201")
        ]
        
        for ogretim_uyesi in ogretim_uyeleri:
            await self.execute(
                "INSERT OR IGNORE INTO ogretim_uyeleri (ad_soyad, unvan, fakulte_id, bolum_id, telefon, email, ofis_no) VALUES (?, ?, ?, ?, ?, ?, ?)",
                ogretim_uyesi
            )
        
        # Dersler
        dersler = [
            ("BM101", "Programlamaya Giriş", 3, 1, "guz", "zorunlu", 1, 1),
            ("BM201", "Veri Yapıları", 4, 2, "bahar", "zorunlu", 1, 1),
            ("BM301", "Veritabanı Sistemleri", 3, 3, "guz", "zorunlu", 1, 1),
            ("EEM101", "Devre Analizi", 4, 1, "guz", "zorunlu", 1, 2)
        ]
        
        for ders in dersler:
            await self.execute(
                "INSERT OR IGNORE INTO dersler (ders_kodu, ders_adi, kredi, sinif, donem, zorunlu_secmeli, fakulte_id, bolum_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                ders
            )
        
        # Örnek öğrenciler
        ogrenciler = [
            ("202012345", "12345678901", "Ahmet", "YILMAZ", "2000-05-15", "Erkek", 1, 1, 4, "2024-2025 Bahar", "2020-09-15", "aktif", 1, 3.42, "05551234567", "ahmet.yilmaz@ogr.mcbu.edu.tr", "Manisa"),
            ("202012346", "12345678902", "Ayşe", "KAYA", "2001-03-20", "Kadın", 1, 1, 3, "2024-2025 Bahar", "2020-09-15", "aktif", 1, 3.15, "05551234568", "ayse.kaya@ogr.mcbu.edu.tr", "Manisa"),
            ("202112347", "12345678903", "Mehmet", "ÖZKAN", "2001-11-10", "Erkek", 1, 2, 2, "2024-2025 Bahar", "2021-09-15", "aktif", 2, 2.89, "05551234569", "mehmet.ozkan@ogr.mcbu.edu.tr", "Manisa")
        ]
        
        for ogrenci in ogrenciler:
            await self.execute(
                """INSERT OR IGNORE INTO ogrenciler (
                    ogrenci_no, tc_kimlik_no, ad, soyad, dogum_tarihi, cinsiyet,
                    fakulte_id, bolum_id, sinif, aktif_akademik_donem, kayit_tarihi, durum,
                    birinci_danisman_id, gano, telefon, email, adres
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                ogrenci
            )
        
        # Örnek notlar
        notlar = [
            (1, 1, "2024-2025 Güz", 85, 78, 83.2, "BA", "geçti"),
            (1, 3, "2024-2025 Güz", 92, 89, 90.8, "AA", "geçti"),
            (2, 1, "2023-2024 Güz", 75, 72, 74.6, "BB", "geçti")
        ]
        
        for not_kaydi in notlar:
            await self.execute(
                "INSERT OR IGNORE INTO sinav_notlari (ogrenci_id, ders_id, akademik_donem, vize_notu, final_notu, toplam_puan, harf_notu, basari_durumu) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                not_kaydi
            )
    
    # Database operations metodları
    async def execute(self, query: str, parameters: tuple = None) -> int:
        """SQL sorgusu çalıştır"""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            if parameters:
                cursor = await db.execute(query, parameters)
            else:
                cursor = await db.execute(query)
            await db.commit()
            return cursor.lastrowid
    
    async def fetch_one(self, query: str, parameters: tuple = None) -> Optional[aiosqlite.Row]:
        """Tek satır getir"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                db.row_factory = aiosqlite.Row
                if parameters:
                    cursor = await db.execute(query, parameters)
                else:
                    cursor = await db.execute(query)
                return await cursor.fetchone()
        except Exception as e:
            logger.error(f"Database fetch_one error: {e}")
            return None
    
    async def fetch_all(self, query: str, parameters: tuple = None) -> List[aiosqlite.Row]:
        """Tüm satırları getir"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                db.row_factory = aiosqlite.Row
                if parameters:
                    cursor = await db.execute(query, parameters)
                else:
                    cursor = await db.execute(query)
                return await cursor.fetchall()
        except Exception as e:
            logger.error(f"Database fetch_all error: {e}")
            return []
    
    async def fetch_scalar(self, query: str, parameters: tuple = None) -> Any:
        """Tek değer getir"""
        result = await self.fetch_one(query, parameters)
        return result[0] if result else None
    
    async def get_all_tables(self) -> List[str]:
        """Tüm tablo isimlerini getir"""
        query = "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        rows = await self.fetch_all(query)
        return [row['name'] for row in rows]
    
    async def get_database_stats(self) -> Dict[str, Any]:
        """Veritabanı istatistikleri"""
        stats = {}
        
        tables = await self.get_all_tables()
        for table in tables:
            if not table.startswith('sqlite_'):
                count = await self.fetch_scalar(f"SELECT COUNT(*) FROM {table}")
                stats[f"{table}_count"] = count
        
        db_size = self.db_path.stat().st_size if self.db_path.exists() else 0
        stats['database_size_mb'] = round(db_size / (1024 * 1024), 2)
        
        return stats