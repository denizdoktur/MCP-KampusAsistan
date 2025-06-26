async def _insert_sample_data(self):
        """Örnek veri ekle"""
        # Fakülteler
        fakulteler = [
            ("Muhendislik Fakultesi", "Prof. Dr. Ali KORKMAZ", "0236-201-2000", "muhendislik@mcbu.edu.tr", "Sehit Prof. Dr. Ilhan Varank Yerleskesi"),
            ("Tip Fakultesi", "Prof. Dr. Mehmet SAGLAM", "0236-233-2000", "tip@mcbu.edu.tr", "Uncubozkoyu Yerleskesi"),
            ("Iktisadi ve Idari Bilimler Fakultesi", "Prof. Dr. Ayse YILMAZ", "0236-201-3000", "iibf@mcbu.edu.tr", "Merkez Yerleske"),
            ("Fen-Edebiyat Fakultesi", "Prof. Dr. Fatma OZKAN", "0236-201-4000", "fenedebiyat@mcbu.edu.tr", "Merkez Yerleske")
        ]
        
        for fakulte in fakulteler:
            await self.execute(
                "INSERT OR IGNORE INTO fakulteler (fakulte_adi, dekan, telefon, email, adres) VALUES (?, ?, ?, ?, ?)",
                fakulte
            )
        
        # Bölümler
        bolumler = [
            (1, "Bilgisayar Muhendisligi", "BM", "Dr. Ogr. Uyesi Zeynep CIPILOGLUYILDIZ", "0236-201-2100", "bilgisayar@mcbu.edu.tr"),
            (1, "Elektrik-Elektronik Muhendisligi", "EEM", "Prof. Dr. Ahmet OZTURK", "0236-201-2200", "elektrik@mcbu.edu.tr"),
            (1, "Makine Muhendisligi", "MM", "Prof. Dr. Mehmet KAYA", "0236-201-2300", "makine@mcbu.edu.tr"),
            (2, "Genel Tip", "TIP", "Prof. Dr. Selma DOKTOR", "0236-233-2100", "tip@mcbu.edu.tr"),
            (3, "Isletme", "ISL", "Prof. Dr. Can TICARET", "0236-201-3100", "isletme@mcbu.edu.tr"),
            (3, "Ekonomi", "EKO", "Prof. Dr. Para BIRIKIM", "0236-201-3200", "ekonomi@mcbu.edu.tr"),
            (4, "Matematik", "MAT", "Prof. Dr. Sayi TOPLAM", "0236-201-4100", "matematik@mcbu.edu.tr"),
            (4, "Edebiyat", "EDB", "Dr. Ogr. Uyesi Siir YAZICI", "0236-201-4200", "edebiyat@mcbu.edu.tr")
        ]
        
        for bolum in bolumler:
            await self.execute(
                "INSERT OR IGNORE INTO bolumler (fakulte_id, bolum_adi, bolum_kodu, bolum_baskani, telefon, email) VALUES (?, ?, ?, ?, ?, ?)",
                bolum
            )
        
        # Öğretim üyeleri
        ogretim_uyeleri = [
            ("Dr. Ogr. Uyesi Zeynep CIPILOGLUYILDIZ", "Dr. Ogr. Uyesi", 1, 1, "0236-201-2101", "zeynepc@mcbu.edu.tr", "MF-201", "0000-0002-1234-5678", "https://avesis.mcbu.edu.tr/zeynepc", "Yazilim Muhendisligi, Veri Bilimi"),
            ("Prof. Dr. Ahmet OZTURK", "Profesor", 1, 2, "0236-201-2201", "ahmetozturk@mcbu.edu.tr", "MF-301", "0000-0002-2345-6789", "https://avesis.mcbu.edu.tr/ahmetozturk", "Guc Elektronigi, Kontrol Sistemleri"),
            ("Prof. Dr. Mehmet KAYA", "Profesor", 1, 3, "0236-201-2301", "mehmetkaya@mcbu.edu.tr", "MF-401", "0000-0002-3456-7890", "https://avesis.mcbu.edu.tr/mehmetkaya", "Termodinamik, Makine Tasarimi"),
            ("Prof. Dr. Selma DOKTOR", "Profesor", 2, 4, "0236-233-2101", "selmadoktor@mcbu.edu.tr", "TF-101", "0000-0002-4567-8901", "https://avesis.mcbu.edu.tr/selmadoktor", "Kardiyoloji, Ic Hastaliklari"),
            ("Prof. Dr. Can TICARET", "Profesor", 3, 5, "0236-201-3101", "canticaret@mcbu.edu.tr", "IF-201", "0000-0002-5678-9012", "https://avesis.mcbu.edu.tr/canticaret", "Pazarlama, Strateji"),
            ("Prof. Dr. Para BIRIKIM", "Profesor", 3, 6, "0236-201-3201", "parabirikim@mcbu.edu.tr", "IF-301", "0000-0002-6789-0123", "https://avesis.mcbu.edu.tr/parabirikim", "Makroekonomi, Para Politikasi")
        ]
        
        for ogretim_uyesi in ogretim_uyeleri:
            await self.execute(
                "INSERT OR IGNORE INTO ogretim_uyeleri (ad_soyad, unvan, fakulte_id, bolum_id, telefon, email, ofis_no, orcid, web_sayfasi, uzmanlik_alani) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                ogretim_uyesi
            )
        
        # Dersler
        dersler = [
            ("BM101", "Programlamaya Giris", 3, 2, 1, 1, "guz", "zorunlu", None, "C programlama dili temellerinin ogretilmesi", 1, 1),
            ("BM201", "Veri Yapilari", 4, 3, 1, 2, "bahar", "zorunlu", "BM101", "Temel veri yapilari ve algoritmalarin ogretilmesi", 1, 1),
            ("BM301", "Veritabani Sistemleri", 3, 2, 1, 3, "guz", "zorunlu", "BM201", "Iliskisel veritabani tasarimi ve SQL", 1, 1),
            ("BM401", "Bitirme Projesi I", 4, 1, 3, 4, "guz", "zorunlu", "Tum zorunlu dersler", "Mezuniyet projesi hazirlama", 1, 1),
            ("BM402", "Bitirme Projesi II", 4, 1, 3, 4, "bahar", "zorunlu", "BM401", "Mezuniyet projesi tamamlama", 1, 1),
            ("BM411", "Yazilim Muhendisligi", 3, 2, 1, 4, "guz", "secmeli", "BM301", "Yazilim gelistirme surecleri", 1, 1),
            ("EEM101", "Devre Analizi", 4, 3, 1, 1, "guz", "zorunlu", None, "Temel elektrik devreleri", 1, 2),
            ("MM101", "Muhendislik Mekanigi", 3, 2, 1, 1, "guz", "zorunlu", None, "Statik ve dinamik", 1, 3)
        ]
        
        for ders in dersler:
            await self.execute(
                "INSERT OR IGNORE INTO dersler (ders_kodu, ders_adi, kredi, teorik_saat, uygulama_saat, sinif, donem, zorunlu_secmeli, on_kosul, ders_icerigi, fakulte_id, bolum_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                ders
            )
        
        # Örnek öğrenci
        ogrenci_data = (
            "202012345", "12345678901", "Ahmet", "YILMAZ", "2000-05-15", "Erkek", "TC",
            1, 1, 4, "2024-2025 Bahar", "2020-09-15", None, "I.O.", 8, 12, 4, "aktif",
            1, None, 3.42,
            "05551234567", "ahmet.yilmaz@ogr.mcbu.edu.tr", 
            "Yunusemre Mah. Ataturk Cad. No:123", "Manisa", "Yunusemre", "45000",
            None, None,
            "Garanti Bankasi", "TR330006200119000006672315", "6672315",
            "muaf", "Ingilizce", None,
            False, False, None
        )
        
        await self.execute(
            """INSERT OR IGNORE INTO ogrenciler (
                ogrenci_no, tc_kimlik_no, ad, soyad, dogum_tarihi, cinsiyet, uyruk,
                fakulte_id, bolum_id, sinif, aktif_akademik_donem, kayit_tarihi, mezuniyet_tarihi, ogrenim_turu,
                normal_sure, azami_sure, okudugu_yil, durum,
                birinci_danisman_id, ikinci_danisman_id, gano,
                telefon, email, adres, il, ilce, posta_kodu,
                web_sayfasi, orcid,
                banka_adi, iban, hesap_no,
                hazirlik_durumu, hazirlik_dili, hazirlik_donemi,
                cift_anadal_kaydi, yan_dal_kaydi, ceza_durumu
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            ogrenci_data
        )
        
        # Daha fazla örnek öğrenci ekle
        additional_students = [
            ("202012346", "12345678902", "Ayse", "KAYA", "2001-03-20", "Kadin", "TC", 1, 1, 3, "2024-2025 Bahar", "2020-09-15", None, "I.O.", 8, 12, 3, "aktif", 1, None, 3.15, "05551234568", "ayse.kaya@ogr.mcbu.edu.tr", "Merkez Mah. Istiklal Cad. No:45", "Manisa", "Sehzadeler", "45010", None, None, "Ziraat Bankasi", "TR640001000119000006672316", "6672316", "muaf", "Ingilizce", None, False, False, None),
            ("202112347", "12345678903", "Mehmet", "OZKAN", "2001-11-10", "Erkek", "TC", 1, 2, 2, "2024-2025 Bahar", "2021-09-15", None, "I.O.", 8, 12, 2, "aktif", 2, None, 2.89, "05551234569", "mehmet.ozkan@ogr.mcbu.edu.tr", "Cumhuriyet Mah. Gazi Cad. No:67", "Manisa", "Yunusemre", "45020", None, None, "Is Bankasi", "TR340006400119000006672317", "6672317", "muaf", "Ingilizce", None, False, False, None),
            ("202012348", "12345678904", "Fatma", "SAHIN", "2000-08-25", "Kadin", "TC", 3, 5, 4, "2024-2025 Bahar", "2020-09-15", None, "I.O.", 8, 12, 4, "aktif", 5, None, 3.67, "05551234570", "fatma.sahin@ogr.mcbu.edu.tr", "Yeni Mah. Ataturk Bulvari No:89", "Manisa", "Sehzadeler", "45030", None, None, "Akbank", "TR460004600119000006672318", "6672318", "muaf", "Ingilizce", None, False, False, None)
        ]
        
        for student in additional_students:
            await self.execute(
                """INSERT OR IGNORE INTO ogrenciler (
                    ogrenci_no, tc_kimlik_no, ad, soyad, dogum_tarihi, cinsiyet, uyruk,
                    fakulte_id, bolum_id, sinif, aktif_akademik_donem, kayit_tarihi, mezuniyet_tarihi, ogrenim_turu,
                    normal_sure, azami_sure, okudugu_yil, durum,
                    birinci_danisman_id, ikinci_danisman_id, gano,
                    telefon, email, adres, il, ilce, posta_kodu,
                    web_sayfasi, orcid,
                    banka_adi, iban, hesap_no,
                    hazirlik_durumu, hazirlik_dili, hazirlik_donemi,
                    cift_anadal_kaydi, yan_dal_kaydi, ceza_durumu
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                student
            )
        
        # Örnek ders kayıtları
        ders_kayitlari = [
            (1, 1, "2024-2025 Guz", "2024-09-15", "tamamlanan"),
            (1, 2, "2024-2025 Bahar", "2025-02-01", "aktif"),
            (1, 3, "2024-2025 Guz", "2024-09-15", "tamamlanan"),
            (1, 4, "2024-2025 Guz", "2024-09-15", "aktif"),
            (1, 6, "2024-2025 Guz", "2024-09-15", "aktif"),
            (2, 1, "2023-2024 Guz", "2023-09-15", "tamamlanan"),
            (2, 2, "2024-2025 Bahar", "2025-02-01", "aktif")
        ]
        
        for kayit in ders_kayitlari:
            await self.execute(
                "INSERT OR IGNORE INTO ogrenci_ders_kayitlari (ogrenci_id, ders_id, akademik_donem, kayit_tarihi, durum) VALUES (?, ?, ?, ?, ?)",
                kayit
            )
        
        # Örnek notlar
        notlar = [
            (1, 1, "2024-2025 Guz", 85, 78, None, None, 90, 88, 83.2, "BA", "gecti"),
            (1, 3, "2024-2025 Guz", 92, 89, None, None, 95, 90, 90.8, "AA", "gecti"),
            (2, 1, "2023-2024 Guz", 75, 72, None, None, 80, 75, 74.6, "BB", "gecti")
        ]
        
        for not_kaydi in notlar:
            await self.execute(
                "INSERT OR IGNORE INTO sinav_notlari (ogrenci_id, ders_id, akademik_donem, vize_notu, final_notu, butunleme_notu, mazeret_sinavi_notu, odev_notu, laboratuvar_notu, toplam_puan, harf_notu, basari_durumu) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                not_kaydi
            )
        
        # Örnek dönem notları
        donem_notlari = [
            (1, "2024-2025 Guz", 7, 7, 3.45, 3.45, 3.42),
            (1, "2024-2025 Bahar", 4, 4, 0.0, 3.45, 3.42),
            (2, "2023-2024 Guz", 3, 3, 2.85, 2.85, 2.85),
            (2, "2024-2025 Bahar", 3, 3, 0.0, 2.85, 2.85)
        ]
        
        for donem in donem_notlari:
            await self.execute(
                "INSERT OR IGNORE INTO donem_notlari (ogrenci_id, akademik_donem, alinan_kredi, basarili_kredi, yariyil_not_ortalamasi, yil_not_ortalamasi, genel_not_ortalamasi) VALUES (?, ?, ?, ?, ?, ?, ?)",
                donem
            )
        
        # Örnek kulüpler
        kulupler = [
            ("Bilgisayar Muhendisligi Kulubu", 1, 1, "2020-10-01", "Bilgisayar muhendisligi ogrencilerinin sosyal ve akademik gelisimini destekler"),
            ("IEEE Ogrenci Kolu", 1, 2, "2019-05-15", "Elektrik-elektronik muhendisligi alaninda etkinlikler duzenler"),
            ("Genc Isadamlari Kulubu", 3, 5, "2018-03-10", "Girisimcilik ve is dunyasi ile ilgili etkinlikler")
        ]
        
        for kulup in kulupler:
            await self.execute(
                "INSERT OR IGNORE INTO kulup_topluluklar (kulup_adi, kurucu_fakulte_id, danisman_id, kurulus_tarihi, aciklama) VALUES (?, ?, ?, ?, ?)",
                kulup
            )
        
        # Örnek kulüp üyelikleri
        uyelikler = [
            (1, 1, "2021-10-01", None, "uye", "aktif"),
            (2, 2, "2022-09-15", None, "sekreter", "aktif"),
            (4, 3, "2021-03-01", None, "baskan", "aktif")
        ]
        
        for uyelik in uyelikler:
            await self.execute(
                "INSERT OR IGNORE INTO ogrenci_kulup_uyelikleri (ogrenci_id, kulup_id, katilim_tarihi, ayrilma_tarihi, gorev, durum) VALUES (?, ?, ?, ?, ?, ?)",
                uyelik
            )
        
        # Commit all changes
        await self.commit()

import sqlite3
import aiosqlite
import logging
from typing import List, Dict, Any, Optional, Union
from pathlib import Path
import asyncio

logger = logging.getLogger(__name__)

class DatabaseManager:
    """SQLite veritabanı bağlantı yöneticisi"""
    
    def __init__(self, db_path: str = "data/student_affairs.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._connection = None
        
    async def initialize(self):
        """Veritabanını başlat ve tabloları oluştur"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                # Önce temel tabloları oluştur
                await self._create_tables(db)
                await db.commit()
                logger.info("Veritabanı şeması başarıyla oluşturuldu")
            
            # Örnek veri ekle (eğer tablo boşsa)
            await self._populate_sample_data_if_empty()
            
        except Exception as e:
            logger.error(f"Veritabanı başlatma hatası: {e}")
            raise
    
    async def _create_tables(self, db):
        """Tabloları oluştur"""
        # Fakülteler tablosu
        await db.execute("""
            CREATE TABLE IF NOT EXISTS fakulteler (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fakulte_adi TEXT NOT NULL,
                dekan TEXT,
                telefon TEXT,
                email TEXT,
                adres TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Bölümler tablosu
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
        
        # Öğretim üyeleri tablosu
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
                orcid TEXT,
                web_sayfasi TEXT,
                uzmanlik_alani TEXT,
                FOREIGN KEY (fakulte_id) REFERENCES fakulteler(id),
                FOREIGN KEY (bolum_id) REFERENCES bolumler(id)
            )
        """)
        
        # Dersler tablosu
        await db.execute("""
            CREATE TABLE IF NOT EXISTS dersler (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ders_kodu TEXT NOT NULL UNIQUE,
                ders_adi TEXT NOT NULL,
                kredi INTEGER,
                teorik_saat INTEGER,
                uygulama_saat INTEGER,
                sinif INTEGER,
                donem TEXT,
                zorunlu_secmeli TEXT,
                on_kosul TEXT,
                ders_icerigi TEXT,
                fakulte_id INTEGER,
                bolum_id INTEGER,
                FOREIGN KEY (fakulte_id) REFERENCES fakulteler(id),
                FOREIGN KEY (bolum_id) REFERENCES bolumler(id)
            )
        """)
        
        # Öğrenciler tablosu (Ana tablo)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS ogrenciler (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ogrenci_no TEXT NOT NULL UNIQUE,
                tc_kimlik_no TEXT UNIQUE,
                ad TEXT NOT NULL,
                soyad TEXT NOT NULL,
                dogum_tarihi DATE,
                cinsiyet TEXT,
                uyruk TEXT DEFAULT 'TC',
                fakulte_id INTEGER,
                bolum_id INTEGER,
                sinif INTEGER,
                aktif_akademik_donem TEXT,
                kayit_tarihi DATE,
                mezuniyet_tarihi DATE,
                ogrenim_turu TEXT,
                normal_sure INTEGER DEFAULT 8,
                azami_sure INTEGER DEFAULT 12,
                okudugu_yil INTEGER,
                durum TEXT DEFAULT 'aktif',
                birinci_danisman_id INTEGER,
                ikinci_danisman_id INTEGER,
                gano REAL,
                telefon TEXT,
                email TEXT,
                adres TEXT,
                il TEXT,
                ilce TEXT,
                posta_kodu TEXT,
                web_sayfasi TEXT,
                orcid TEXT,
                banka_adi TEXT,
                iban TEXT,
                hesap_no TEXT,
                hazirlik_durumu TEXT,
                hazirlik_dili TEXT,
                hazirlik_donemi TEXT,
                cift_anadal_kaydi BOOLEAN DEFAULT FALSE,
                yan_dal_kaydi BOOLEAN DEFAULT FALSE,
                ceza_durumu TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (fakulte_id) REFERENCES fakulteler(id),
                FOREIGN KEY (bolum_id) REFERENCES bolumler(id),
                FOREIGN KEY (birinci_danisman_id) REFERENCES ogretim_uyeleri(id),
                FOREIGN KEY (ikinci_danisman_id) REFERENCES ogretim_uyeleri(id)
            )
        """)
        
        # Ders programı
        await db.execute("""
            CREATE TABLE IF NOT EXISTS ders_programi (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ders_id INTEGER,
                ogretim_uyesi_id INTEGER,
                akademik_donem TEXT,
                gun TEXT,
                saat TEXT,
                derslik TEXT,
                FOREIGN KEY (ders_id) REFERENCES dersler(id),
                FOREIGN KEY (ogretim_uyesi_id) REFERENCES ogretim_uyeleri(id)
            )
        """)
        
        # Öğrenci ders kayıtları
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
                butunleme_notu REAL,
                mazeret_sinavi_notu REAL,
                odev_notu REAL,
                laboratuvar_notu REAL,
                toplam_puan REAL,
                harf_notu TEXT,
                basari_durumu TEXT,
                FOREIGN KEY (ogrenci_id) REFERENCES ogrenciler(id),
                FOREIGN KEY (ders_id) REFERENCES dersler(id)
            )
        """)
        
        # Dönem not ortalamaları
        await db.execute("""
            CREATE TABLE IF NOT EXISTS donem_notlari (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ogrenci_id INTEGER,
                akademik_donem TEXT,
                alinan_kredi INTEGER,
                basarili_kredi INTEGER,
                yariyil_not_ortalamasi REAL,
                yil_not_ortalamasi REAL,
                genel_not_ortalamasi REAL,
                FOREIGN KEY (ogrenci_id) REFERENCES ogrenciler(id)
            )
        """)
        
        # Devamsızlık kayıtları
        await db.execute("""
            CREATE TABLE IF NOT EXISTS devamsizlik (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ogrenci_id INTEGER,
                ders_id INTEGER,
                akademik_donem TEXT,
                toplam_devamsizlik_saati INTEGER,
                devamsizlik_yuzdesi REAL,
                uyari_durumu TEXT,
                FOREIGN KEY (ogrenci_id) REFERENCES ogrenciler(id),
                FOREIGN KEY (ders_id) REFERENCES dersler(id)
            )
        """)
        
        # Burs ve krediler
        await db.execute("""
            CREATE TABLE IF NOT EXISTS burs_krediler (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ogrenci_id INTEGER,
                burs_tipi TEXT,
                kurum TEXT,
                baslangic_tarihi DATE,
                bitis_tarihi DATE,
                tutar REAL,
                durum TEXT,
                FOREIGN KEY (ogrenci_id) REFERENCES ogrenciler(id)
            )
        """)
        
        # Kulüp ve topluluklar
        await db.execute("""
            CREATE TABLE IF NOT EXISTS kulup_topluluklar (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                kulup_adi TEXT NOT NULL,
                kurucu_fakulte_id INTEGER,
                danisman_id INTEGER,
                kurulus_tarihi DATE,
                aciklama TEXT,
                FOREIGN KEY (kurucu_fakulte_id) REFERENCES fakulteler(id),
                FOREIGN KEY (danisman_id) REFERENCES ogretim_uyeleri(id)
            )
        """)
        
        # Öğrenci kulüp üyelikleri
        await db.execute("""
            CREATE TABLE IF NOT EXISTS ogrenci_kulup_uyelikleri (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ogrenci_id INTEGER,
                kulup_id INTEGER,
                katilim_tarihi DATE,
                ayrilma_tarihi DATE,
                gorev TEXT,
                durum TEXT DEFAULT 'aktif',
                FOREIGN KEY (ogrenci_id) REFERENCES ogrenciler(id),
                FOREIGN KEY (kulup_id) REFERENCES kulup_topluluklar(id)
            )
        """)
        
        # Kayıt dondurma bilgileri
        await db.execute("""
            CREATE TABLE IF NOT EXISTS kayit_dondurma (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ogrenci_id INTEGER,
                baslangic_tarihi DATE,
                bitis_tarihi DATE,
                donem_sayisi INTEGER,
                sebep TEXT,
                belge_yolu TEXT,
                onay_durumu TEXT,
                FOREIGN KEY (ogrenci_id) REFERENCES ogrenciler(id)
            )
        """)
        
        # Onur ve yüksek onur belgeleri
        await db.execute("""
            CREATE TABLE IF NOT EXISTS onur_belgeleri (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ogrenci_id INTEGER,
                akademik_donem TEXT,
                belge_tipi TEXT,
                not_ortalamasi REAL,
                verilis_tarihi DATE,
                FOREIGN KEY (ogrenci_id) REFERENCES ogrenciler(id)
            )
        """)
        
        # Mazeret sınav başvuruları
        await db.execute("""
            CREATE TABLE IF NOT EXISTS mazeret_sinav_basvurulari (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ogrenci_id INTEGER,
                ders_id INTEGER,
                basvuru_tarihi DATE,
                mazeret_sebep TEXT,
                belge_yolu TEXT,
                onay_durumu TEXT,
                sinav_tarihi DATE,
                FOREIGN KEY (ogrenci_id) REFERENCES ogrenciler(id),
                FOREIGN KEY (ders_id) REFERENCES dersler(id)
            )
        """)
        
        # Ek sınav başvuruları
        await db.execute("""
            CREATE TABLE IF NOT EXISTS ek_sinav_basvurulari (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ogrenci_id INTEGER,
                ders_id INTEGER,
                basvuru_tarihi DATE,
                onay_durumu TEXT,
                sinav_tarihi DATE,
                ucret REAL,
                odeme_durumu TEXT,
                FOREIGN KEY (ogrenci_id) REFERENCES ogrenciler(id),
                FOREIGN KEY (ders_id) REFERENCES dersler(id)
            )
        """)
        
        # Belge talepleri
        await db.execute("""
            CREATE TABLE IF NOT EXISTS belge_talepleri (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ogrenci_id INTEGER,
                belge_tipi TEXT,
                talep_tarihi DATE,
                teslim_tarihi DATE,
                durum TEXT,
                ucret REAL,
                odeme_durumu TEXT,
                FOREIGN KEY (ogrenci_id) REFERENCES ogrenciler(id)
            )
        """)
        
        # Mesajlaşma sistemi
        await db.execute("""
            CREATE TABLE IF NOT EXISTS mesajlar (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                gonderici_ogrenci_id INTEGER,
                alici_ogretim_uyesi_id INTEGER,
                konu TEXT,
                mesaj_icerigi TEXT,
                gonderim_tarihi DATETIME DEFAULT CURRENT_TIMESTAMP,
                okunma_tarihi DATETIME,
                cevap_durumu TEXT DEFAULT 'beklemede',
                ek_dosya_yolu TEXT,
                FOREIGN KEY (gonderici_ogrenci_id) REFERENCES ogrenciler(id),
                FOREIGN KEY (alici_ogretim_uyesi_id) REFERENCES ogretim_uyeleri(id)
            )
        """)
        
        # Mesaj cevapları
        await db.execute("""
            CREATE TABLE IF NOT EXISTS mesaj_cevaplari (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ana_mesaj_id INTEGER,
                gonderici_ogretim_uyesi_id INTEGER,
                cevap_icerigi TEXT,
                gonderim_tarihi DATETIME DEFAULT CURRENT_TIMESTAMP,
                ek_dosya_yolu TEXT,
                FOREIGN KEY (ana_mesaj_id) REFERENCES mesajlar(id),
                FOREIGN KEY (gonderici_ogretim_uyesi_id) REFERENCES ogretim_uyeleri(id)
            )
        """)
        
        # Staj bilgileri
        await db.execute("""
            CREATE TABLE IF NOT EXISTS stajlar (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ogrenci_id INTEGER,
                staj_tipi TEXT,
                firma_adi TEXT,
                firma_adresi TEXT,
                staj_baslangic_tarihi DATE,
                staj_bitis_tarihi DATE,
                staj_suresi INTEGER,
                staj_puani REAL,
                danisman_onay TEXT,
                firma_degerlendirme_formu TEXT,
                ogrenci_raporu TEXT,
                FOREIGN KEY (ogrenci_id) REFERENCES ogrenciler(id)
            )
        """)
        
        # Ceza bilgileri
        await db.execute("""
            CREATE TABLE IF NOT EXISTS ceza_bilgileri (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ogrenci_id INTEGER,
                ceza_tipi TEXT,
                ceza_sebebi TEXT,
                ceza_tarihi DATE,
                ceza_suresi INTEGER,
                aktif_durum BOOLEAN DEFAULT TRUE,
                aciklama TEXT,
                FOREIGN KEY (ogrenci_id) REFERENCES ogrenciler(id)
            )
        """)
        
        # Öğrenim ücreti bilgileri
        await db.execute("""
            CREATE TABLE IF NOT EXISTS ogrenim_ucreti (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ogrenci_id INTEGER,
                akademik_donem TEXT,
                ucret_tipi TEXT,
                tutar REAL,
                son_odeme_tarihi DATE,
                odeme_durumu TEXT,
                odeme_tarihi DATE,
                FOREIGN KEY (ogrenci_id) REFERENCES ogrenciler(id)
            )
        """)
        
        # Trigger oluştur
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
            # Öğrenci tablosunun boş olup olmadığını kontrol et
            count = await self.fetch_scalar("SELECT COUNT(*) FROM ogrenciler")
            
            if count == 0:
                logger.info("Veritabanı boş, örnek veriler ekleniyor...")
                await self._insert_sample_data()
                logger.info("Örnek veriler başarıyla eklendi")
            
        except Exception as e:
            logger.warning(f"Örnek veri ekleme hatası: {e}")
    
    async def _insert_sample_data(self):
        """Örnek veri ekle"""
        # Fakülteler
        fakulteler = [
            ("Mühendislik Fakültesi", "Prof. Dr. Ali KORKMAZ", "0236-201-2000", "muhendislik@mcbu.edu.tr", "Şehit Prof. Dr. İlhan Varank Yerleşkesi"),
            ("Tıp Fakültesi", "Prof. Dr. Mehmet SAĞLAM", "0236-233-2000", "tip@mcbu.edu.tr", "Uncubozköy Yerleşkesi"),
            ("İktisadi ve İdari Bilimler Fakültesi", "Prof. Dr. Ayşe YILMAZ", "0236-201-3000", "iibf@mcbu.edu.tr", "Merkez Yerleşke"),
            ("Fen-Edebiyat Fakültesi", "Prof. Dr. Fatma ÖZKAN", "0236-201-4000", "fenedebiyat@mcbu.edu.tr", "Merkez Yerleşke")
        ]
        
        for fakulte in fakulteler:
            await self.execute(
                "INSERT OR IGNORE INTO fakulteler (fakülte_adi, dekan, telefon, email, adres) VALUES (?, ?, ?, ?, ?)",
                fakulte
            )
        
        # Bölümler
        bolumler = [
            (1, "Bilgisayar Mühendisliği", "BM", "Dr. Öğr. Üyesi Zeynep ÇİPİLOĞLU YILDIZ", "0236-201-2100", "bilgisayar@mcbu.edu.tr"),
            (1, "Elektrik-Elektronik Mühendisliği", "EEM", "Prof. Dr. Ahmet ÖZTÜRK", "0236-201-2200", "elektrik@mcbu.edu.tr"),
            (1, "Makine Mühendisliği", "MM", "Prof. Dr. Mehmet KAYA", "0236-201-2300", "makine@mcbu.edu.tr"),
            (2, "Genel Tıp", "TIP", "Prof. Dr. Selma DOKTOR", "0236-233-2100", "tip@mcbu.edu.tr"),
            (3, "İşletme", "ISL", "Prof. Dr. Can TICARET", "0236-201-3100", "isletme@mcbu.edu.tr"),
            (3, "Ekonomi", "EKO", "Prof. Dr. Para BIRIKIM", "0236-201-3200", "ekonomi@mcbu.edu.tr"),
            (4, "Matematik", "MAT", "Prof. Dr. Sayı TOPLAM", "0236-201-4100", "matematik@mcbu.edu.tr"),
            (4, "Edebiyat", "EDB", "Dr. Öğr. Üyesi Şiir YAZICI", "0236-201-4200", "edebiyat@mcbu.edu.tr")
        ]
        
        for bolum in bolumler:
            await self.execute(
                "INSERT OR IGNORE INTO bolumler (fakulte_id, bolum_adi, bolum_kodu, bolum_baskani, telefon, email) VALUES (?, ?, ?, ?, ?, ?)",
                bolum
            )
        
        # Öğretim üyeleri
        ogretim_uyeleri = [
            ("Dr. Öğr. Üyesi Zeynep ÇİPİLOĞLU YILDIZ", "Dr. Öğr. Üyesi", 1, 1, "0236-201-2101", "zeynepc@mcbu.edu.tr", "MF-201", "0000-0002-1234-5678", "https://avesis.mcbu.edu.tr/zeynepc", "Yazılım Mühendisliği, Veri Bilimi"),
            ("Prof. Dr. Ahmet ÖZTÜRK", "Profesör", 1, 2, "0236-201-2201", "ahmetozturk@mcbu.edu.tr", "MF-301", "0000-0002-2345-6789", "https://avesis.mcbu.edu.tr/ahmetozturk", "Güç Elektroniği, Kontrol Sistemleri"),
            ("Prof. Dr. Mehmet KAYA", "Profesör", 1, 3, "0236-201-2301", "mehmetkaya@mcbu.edu.tr", "MF-401", "0000-0002-3456-7890", "https://avesis.mcbu.edu.tr/mehmetkaya", "Termodinamik, Makine Tasarımı"),
            ("Prof. Dr. Selma DOKTOR", "Profesör", 2, 4, "0236-233-2101", "selmadoktor@mcbu.edu.tr", "TF-101", "0000-0002-4567-8901", "https://avesis.mcbu.edu.tr/selmadoktor", "Kardiyoloji, İç Hastalıkları"),
            ("Prof. Dr. Can TICARET", "Profesör", 3, 5, "0236-201-3101", "canticaret@mcbu.edu.tr", "IF-201", "0000-0002-5678-9012", "https://avesis.mcbu.edu.tr/canticaret", "Pazarlama, Strateji"),
            ("Prof. Dr. Para BIRIKIM", "Profesör", 3, 6, "0236-201-3201", "parabirikim@mcbu.edu.tr", "IF-301", "0000-0002-6789-0123", "https://avesis.mcbu.edu.tr/parabirikim", "Makroekonomi, Para Politikası")
        ]
        
        for ogretim_uyesi in ogretim_uyeleri:
            await self.execute(
                "INSERT OR IGNORE INTO ogretim_uyeleri (ad_soyad, unvan, fakulte_id, bolum_id, telefon, email, ofis_no, orcid, web_sayfasi, uzmanlik_alani) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                ogretim_uyesi
            )
        
        # Dersler
        dersler = [
            ("BM101", "Programlamaya Giriş", 3, 2, 1, 1, "güz", "zorunlu", None, "C programlama dili temellerinin öğretilmesi", 1, 1),
            ("BM201", "Veri Yapıları", 4, 3, 1, 2, "bahar", "zorunlu", "BM101", "Temel veri yapıları ve algoritmaların öğretilmesi", 1, 1),
            ("BM301", "Veritabanı Sistemleri", 3, 2, 1, 3, "güz", "zorunlu", "BM201", "İlişkisel veritabanı tasarımı ve SQL", 1, 1),
            ("BM401", "Bitirme Projesi I", 4, 1, 3, 4, "güz", "zorunlu", "Tüm zorunlu dersler", "Mezuniyet projesi hazırlama", 1, 1),
            ("BM402", "Bitirme Projesi II", 4, 1, 3, 4, "bahar", "zorunlu", "BM401", "Mezuniyet projesi tamamlama", 1, 1),
            ("BM411", "Yazılım Mühendisliği", 3, 2, 1, 4, "güz", "seçmeli", "BM301", "Yazılım geliştirme süreçleri", 1, 1),
            ("EEM101", "Devre Analizi", 4, 3, 1, 1, "güz", "zorunlu", None, "Temel elektrik devreleri", 1, 2),
            ("MM101", "Mühendislik Mekaniği", 3, 2, 1, 1, "güz", "zorunlu", None, "Statik ve dinamik", 1, 3)
        ]
        
        for ders in dersler:
            await self.execute(
                "INSERT OR IGNORE INTO dersler (ders_kodu, ders_adi, kredi, teorik_saat, uygulama_saat, sinif, donem, zorunlu_secmeli, on_kosul, ders_icerigi, fakulte_id, bolum_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                ders
            )
        
        # Örnek öğrenci
        ogrenci_data = (
            "202012345", "12345678901", "Ahmet", "YILMAZ", "2000-05-15", "Erkek", "TC",
            1, 1, 4, "2024-2025 Bahar", "2020-09-15", None, "İ.Ö.", 8, 12, 4, "aktif",
            1, None, 3.42,
            "05551234567", "ahmet.yilmaz@ogr.mcbu.edu.tr", 
            "Yunusemre Mah. Atatürk Cad. No:123", "Manisa", "Yunusemre", "45000",
            None, None,
            "Garanti Bankası", "TR330006200119000006672315", "6672315",
            "muaf", "İngilizce", None,
            False, False, None
        )
        
        await self.execute(
            """INSERT OR IGNORE INTO ogrenciler (
                ogrenci_no, tc_kimlik_no, ad, soyad, dogum_tarihi, cinsiyet, uyruk,
                fakulte_id, bolum_id, sinif, aktif_akademik_donem, kayit_tarihi, mezuniyet_tarihi, ogrenim_turu,
                normal_sure, azami_sure, okuduğu_yil, durum,
                birinci_danisman_id, ikinci_danisman_id, gano,
                telefon, email, adres, il, ilce, posta_kodu,
                web_sayfasi, orcid,
                banka_adi, iban, hesap_no,
                hazirlik_durumu, hazirlik_dili, hazirlik_donemi,
                cift_anadal_kaydi, yan_dal_kaydi, ceza_durumu
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            ogrenci_data
        )
        
        # Daha fazla örnek öğrenci ekle
        additional_students = [
            ("202012346", "12345678902", "Ayşe", "KAYA", "2001-03-20", "Kadın", "TC", 1, 1, 3, "2024-2025 Bahar", "2020-09-15", None, "İ.Ö.", 8, 12, 3, "aktif", 1, None, 3.15, "05551234568", "ayse.kaya@ogr.mcbu.edu.tr", "Merkez Mah. İstiklal Cad. No:45", "Manisa", "Şehzadeler", "45010", None, None, "Ziraat Bankası", "TR640001000119000006672316", "6672316", "muaf", "İngilizce", None, False, False, None),
            ("202112347", "12345678903", "Mehmet", "ÖZKAN", "2001-11-10", "Erkek", "TC", 1, 2, 2, "2024-2025 Bahar", "2021-09-15", None, "İ.Ö.", 8, 12, 2, "aktif", 2, None, 2.89, "05551234569", "mehmet.ozkan@ogr.mcbu.edu.tr", "Cumhuriyet Mah. Gazi Cad. No:67", "Manisa", "Yunusemre", "45020", None, None, "İş Bankası", "TR340006400119000006672317", "6672317", "muaf", "İngilizce", None, False, False, None),
            ("202012348", "12345678904", "Fatma", "ŞAHIN", "2000-08-25", "Kadın", "TC", 3, 5, 4, "2024-2025 Bahar", "2020-09-15", None, "İ.Ö.", 8, 12, 4, "aktif", 5, None, 3.67, "05551234570", "fatma.sahin@ogr.mcbu.edu.tr", "Yeni Mah. Atatürk Bulvarı No:89", "Manisa", "Şehzadeler", "45030", None, None, "Akbank", "TR460004600119000006672318", "6672318", "muaf", "İngilizce", None, False, False, None)
        ]
        
        for student in additional_students:
            await self.execute(
                """INSERT OR IGNORE INTO ogrenciler (
                    ogrenci_no, tc_kimlik_no, ad, soyad, dogum_tarihi, cinsiyet, uyruk,
                    fakulte_id, bolum_id, sinif, aktif_akademik_donem, kayit_tarihi, mezuniyet_tarihi, ogrenim_turu,
                    normal_sure, azami_sure, okuduğu_yil, durum,
                    birinci_danisman_id, ikinci_danisman_id, gano,
                    telefon, email, adres, il, ilce, posta_kodu,
                    web_sayfasi, orcid,
                    banka_adi, iban, hesap_no,
                    hazirlik_durumu, hazirlik_dili, hazirlik_donemi,
                    cift_anadal_kaydi, yan_dal_kaydi, ceza_durumu
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                student
            )
        
        # Örnek ders kayıtları
        ders_kayitlari = [
            (1, 1, "2024-2025 Güz", "2024-09-15", "tamamlanan"),
            (1, 2, "2024-2025 Bahar", "2025-02-01", "aktif"),
            (1, 3, "2024-2025 Güz", "2024-09-15", "tamamlanan"),
            (1, 4, "2024-2025 Güz", "2024-09-15", "aktif"),
            (1, 6, "2024-2025 Güz", "2024-09-15", "aktif"),
            (2, 1, "2023-2024 Güz", "2023-09-15", "tamamlanan"),
            (2, 2, "2024-2025 Bahar", "2025-02-01", "aktif")
        ]
        
        for kayit in ders_kayitlari:
            await self.execute(
                "INSERT OR IGNORE INTO ogrenci_ders_kayitlari (ogrenci_id, ders_id, akademik_donem, kayit_tarihi, durum) VALUES (?, ?, ?, ?, ?)",
                kayit
            )
        
        # Örnek notlar
        notlar = [
            (1, 1, "2024-2025 Güz", 85, 78, None, None, 90, 88, 83.2, "BA", "geçti"),
            (1, 3, "2024-2025 Güz", 92, 89, None, None, 95, 90, 90.8, "AA", "geçti"),
            (2, 1, "2023-2024 Güz", 75, 72, None, None, 80, 75, 74.6, "BB", "geçti")
        ]
        
        for not_kaydi in notlar:
            await self.execute(
                "INSERT OR IGNORE INTO sinav_notlari (ogrenci_id, ders_id, akademik_donem, vize_notu, final_notu, butunleme_notu, mazeret_sinavi_notu, odev_notu, laboratuvar_notu, toplam_puan, harf_notu, basari_durumu) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                not_kaydi
            )
        
        # Örnek dönem notları
        donem_notlari = [
            (1, "2024-2025 Güz", 7, 7, 3.45, 3.45, 3.42),
            (1, "2024-2025 Bahar", 4, 4, 0.0, 3.45, 3.42),
            (2, "2023-2024 Güz", 3, 3, 2.85, 2.85, 2.85),
            (2, "2024-2025 Bahar", 3, 3, 0.0, 2.85, 2.85)
        ]
        
        for donem in donem_notlari:
            await self.execute(
                "INSERT OR IGNORE INTO donem_notlari (ogrenci_id, akademik_donem, alinan_kredi, basarili_kredi, yariyil_not_ortalamasi, yil_not_ortalamasi, genel_not_ortalamasi) VALUES (?, ?, ?, ?, ?, ?, ?)",
                donem
            )
        
        # Örnek kulüpler
        kulupler = [
            ("Bilgisayar Mühendisliği Kulübü", 1, 1, "2020-10-01", "Bilgisayar mühendisliği öğrencilerinin sosyal ve akademik gelişimini destekler"),
            ("IEEE Öğrenci Kolu", 1, 2, "2019-05-15", "Elektrik-elektronik mühendisliği alanında etkinlikler düzenler"),
            ("Genç İşadamları Kulübü", 3, 5, "2018-03-10", "Girişimcilik ve iş dünyası ile ilgili etkinlikler")
        ]
        
        for kulup in kulupler:
            await self.execute(
                "INSERT OR IGNORE INTO kulup_topluluklar (kulup_adi, kurucu_fakulte_id, danisman_id, kuruluş_tarihi, aciklama) VALUES (?, ?, ?, ?, ?)",
                kulup
            )
        
        # Örnek kulüp üyelikleri
        uyelikler = [
            (1, 1, "2021-10-01", None, "üye", "aktif"),
            (2, 2, "2022-09-15", None, "sekreter", "aktif"),
            (4, 3, "2021-03-01", None, "başkan", "aktif")
        ]
        
        for uyelik in uyelikler:
            await self.execute(
                "INSERT OR IGNORE INTO ogrenci_kulup_uyelikleri (ogrenci_id, kulup_id, katilim_tarihi, ayrilma_tarihi, gorev, durum) VALUES (?, ?, ?, ?, ?, ?)",
                uyelik
            )
        
        # Commit all changes
        await self.commit()
    
    async def connect(self):
        """Veritabanına bağlan"""
        if not self._connection:
            self._connection = await aiosqlite.connect(self.db_path)
            self._connection.row_factory = aiosqlite.Row
        return self._connection
    
    async def disconnect(self):
        """Veritabanı bağlantısını kapat"""
        if self._connection:
            await self._connection.close()
            self._connection = None
    
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
        """Tek satır getir - optimized connection"""
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
        """Tüm satırları getir - optimized connection"""
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
    
    async def commit(self):
        """Değişiklikleri kaydet"""
        if self._connection:
            await self._connection.commit()
    
    async def rollback(self):
        """Değişiklikleri geri al"""
        if self._connection:
            await self._connection.rollback()
    
    async def get_table_info(self, table_name: str) -> List[Dict[str, Any]]:
        """Tablo bilgilerini getir"""
        query = f"PRAGMA table_info({table_name})"
        rows = await self.fetch_all(query)
        return [dict(row) for row in rows]
    
    async def get_all_tables(self) -> List[str]:
        """Tüm tablo isimlerini getir"""
        query = "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        rows = await self.fetch_all(query)
        return [row['name'] for row in rows]
    
    async def vacuum_database(self):
        """Veritabanını optimize et"""
        await self.execute("VACUUM")
        logger.info("Veritabanı optimize edildi")
    
    async def backup_database(self, backup_path: str):
        """Veritabanını yedekle"""
        try:
            async with aiosqlite.connect(self.db_path) as source:
                async with aiosqlite.connect(backup_path) as backup:
                    await source.backup(backup)
            logger.info(f"Veritabanı yedeği oluşturuldu: {backup_path}")
        except Exception as e:
            logger.error(f"Yedekleme hatası: {e}")
            raise
    
    async def get_database_stats(self) -> Dict[str, Any]:
        """Veritabanı istatistikleri"""
        stats = {}
        
        # Tablo sayıları
        tables = await self.get_all_tables()
        for table in tables:
            if not table.startswith('sqlite_'):
                count = await self.fetch_scalar(f"SELECT COUNT(*) FROM {table}")
                stats[f"{table}_count"] = count
        
        # Veritabanı boyutu
        db_size = self.db_path.stat().st_size if self.db_path.exists() else 0
        stats['database_size_mb'] = round(db_size / (1024 * 1024), 2)
        
        return stats
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._connection:
            asyncio.create_task(self.disconnect())