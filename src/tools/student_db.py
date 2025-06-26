"""
Basitleştirilmiş Öğrenci Veritabanı Tool
Sadece temel işlevler, yüksek performans
"""

from typing import Dict, Any, List
from .base_tool import BaseTool

class StudentDatabaseTool(BaseTool):
    """Öğrenci veritabanı işlemleri - basitleştirilmiş"""
    
    def __init__(self, db_manager):
        super().__init__(
            name="student_database",
            description="Öğrenci bilgileri ve akademik kayıtlar",
            input_schema={
                "type": "object",
                "properties": {
                    "operation": {
                        "type": "string",
                        "enum": [
                            "ogrenci_ara",
                            "ogrenci_detay",
                            "notlari_getir",
                            "dersleri_listele",
                            "fakulte_bolum_listesi",
                            "danisman_bilgisi",
                            "istatistik"
                        ],
                        "description": "Yapılacak işlem"
                    },
                    "ogrenci_no": {
                        "type": "string",
                        "description": "Öğrenci numarası"
                    },
                    "arama_metni": {
                        "type": "string",
                        "description": "Ad, soyad veya numara ile arama"
                    },
                    "limit": {
                        "type": "integer",
                        "default": 20,
                        "description": "Maksimum sonuç sayısı"
                    }
                },
                "required": ["operation"]
            }
        )
        self.db = db_manager
    
    async def execute(self, **kwargs) -> Dict[str, Any]:
        """Ana işlem yöneticisi"""
        operation = kwargs.get("operation")
        
        try:
            if operation == "ogrenci_ara":
                result = await self._ogrenci_ara(kwargs)
            elif operation == "ogrenci_detay":
                result = await self._ogrenci_detay(kwargs)
            elif operation == "notlari_getir":
                result = await self._notlari_getir(kwargs)
            elif operation == "dersleri_listele":
                result = await self._dersleri_listele(kwargs)
            elif operation == "fakulte_bolum_listesi":
                result = await self._fakulte_bolum_listesi()
            elif operation == "danisman_bilgisi":
                result = await self._danisman_bilgisi(kwargs)
            elif operation == "istatistik":
                result = await self._istatistik()
            else:
                return self.create_error_response(f"Bilinmeyen işlem: {operation}")
            
            return self.create_success_response(result)
            
        except Exception as e:
            return self.create_error_response(f"Veritabanı hatası: {str(e)}")
    
    async def _ogrenci_ara(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Öğrenci arama - optimize edilmiş"""
        arama_metni = params.get("arama_metni", "")
        ogrenci_no = params.get("ogrenci_no", "")
        limit = min(params.get("limit", 20), 100)  # Max 100
        
        if not arama_metni and not ogrenci_no:
            # Eğer arama kriteri yoksa, son kayıtları getir
            query = """
            SELECT o.ogrenci_no, o.ad, o.soyad, o.sinif, o.gano,
                   f.fakulte_adi, b.bolum_adi
            FROM ogrenciler o
            LEFT JOIN fakulteler f ON o.fakulte_id = f.id
            LEFT JOIN bolumler b ON o.bolum_id = b.id
            WHERE o.durum = 'aktif'
            ORDER BY o.kayit_tarihi DESC
            LIMIT ?
            """
            results = await self.db.fetch_all(query, [limit])
        else:
            # Arama ile
            query = """
            SELECT o.ogrenci_no, o.ad, o.soyad, o.sinif, o.gano,
                   f.fakulte_adi, b.bolum_adi
            FROM ogrenciler o
            LEFT JOIN fakulteler f ON o.fakulte_id = f.id
            LEFT JOIN bolumler b ON o.bolum_id = b.id
            WHERE o.durum = 'aktif'
            """
            params_list = []
            
            if ogrenci_no:
                query += " AND o.ogrenci_no LIKE ?"
                params_list.append(f"%{ogrenci_no}%")
            
            if arama_metni:
                query += " AND (o.ad LIKE ? OR o.soyad LIKE ?)"
                params_list.extend([f"%{arama_metni}%", f"%{arama_metni}%"])
            
            query += f" ORDER BY o.ad, o.soyad LIMIT ?"
            params_list.append(limit)
            
            results = await self.db.fetch_all(query, params_list)
        
        return {
            "ogrenciler": [dict(row) for row in results],
            "bulunan_sayi": len(results),
            "arama_kriterleri": {
                "ogrenci_no": ogrenci_no,
                "arama_metni": arama_metni
            }
        }
    
    async def _ogrenci_detay(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Öğrenci detay bilgileri"""
        ogrenci_no = params.get("ogrenci_no")
        if not ogrenci_no:
            raise ValueError("ogrenci_no gerekli")
        
        # Ana bilgiler
        query = """
        SELECT o.*, f.fakulte_adi, b.bolum_adi,
               d.ad_soyad as danisman_adi, d.unvan as danisman_unvan,
               d.telefon as danisman_telefon, d.email as danisman_email
        FROM ogrenciler o
        LEFT JOIN fakulteler f ON o.fakulte_id = f.id
        LEFT JOIN bolumler b ON o.bolum_id = b.id
        LEFT JOIN ogretim_uyeleri d ON o.birinci_danisman_id = d.id
        WHERE o.ogrenci_no = ?
        """
        
        ogrenci = await self.db.fetch_one(query, [ogrenci_no])
        
        if not ogrenci:
            return {"hata": "Öğrenci bulunamadı"}
        
        return {"ogrenci": dict(ogrenci)}
    
    async def _notlari_getir(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Öğrenci notları"""
        ogrenci_no = params.get("ogrenci_no")
        if not ogrenci_no:
            raise ValueError("ogrenci_no gerekli")
        
        # Önce öğrenci ID'sini bul
        ogrenci_query = "SELECT id FROM ogrenciler WHERE ogrenci_no = ?"
        ogrenci_result = await self.db.fetch_one(ogrenci_query, [ogrenci_no])
        
        if not ogrenci_result:
            return {"hata": "Öğrenci bulunamadı"}
        
        ogrenci_id = ogrenci_result["id"]
        
        # Notları getir
        notlar_query = """
        SELECT sn.akademik_donem, d.ders_kodu, d.ders_adi, d.kredi,
               sn.vize_notu, sn.final_notu, sn.toplam_puan, 
               sn.harf_notu, sn.basari_durumu
        FROM sinav_notlari sn
        JOIN dersler d ON sn.ders_id = d.id
        WHERE sn.ogrenci_id = ?
        ORDER BY sn.akademik_donem DESC, d.ders_kodu
        """
        
        notlar = await self.db.fetch_all(notlar_query, [ogrenci_id])
        
        # Dönem ortalamaları
        donem_query = """
        SELECT akademik_donem, alinan_kredi, basarili_kredi,
               donem_not_ortalamasi, genel_not_ortalamasi
        FROM donem_notlari
        WHERE ogrenci_id = ?
        ORDER BY akademik_donem DESC
        """
        
        donemler = await self.db.fetch_all(donem_query, [ogrenci_id])
        
        return {
            "notlar": [dict(row) for row in notlar],
            "donem_ortalamalari": [dict(row) for row in donemler],
            "toplam_ders": len(notlar)
        }
    
    async def _dersleri_listele(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Öğrencinin ders kayıtları"""
        ogrenci_no = params.get("ogrenci_no")
        if not ogrenci_no:
            raise ValueError("ogrenci_no gerekli")
        
        # Öğrenci ID
        ogrenci_query = "SELECT id FROM ogrenciler WHERE ogrenci_no = ?"
        ogrenci_result = await self.db.fetch_one(ogrenci_query, [ogrenci_no])
        
        if not ogrenci_result:
            return {"hata": "Öğrenci bulunamadı"}
        
        ogrenci_id = ogrenci_result["id"]
        
        # Dersler
        query = """
        SELECT odk.akademik_donem, d.ders_kodu, d.ders_adi, 
               d.kredi, odk.durum, odk.kayit_tarihi
        FROM ogrenci_ders_kayitlari odk
        JOIN dersler d ON odk.ders_id = d.id
        WHERE odk.ogrenci_id = ?
        ORDER BY odk.akademik_donem DESC, d.ders_kodu
        LIMIT 50
        """
        
        dersler = await self.db.fetch_all(query, [ogrenci_id])
        
        return {
            "ders_kayitlari": [dict(row) for row in dersler],
            "toplam": len(dersler)
        }
    
    async def _fakulte_bolum_listesi(self) -> Dict[str, Any]:
        """Fakülte ve bölümleri listele"""
        
        # Fakülteler
        fakulte_query = "SELECT * FROM fakulteler ORDER BY fakulte_adi"
        fakulteler = await self.db.fetch_all(fakulte_query)
        
        # Bölümler
        bolum_query = """
        SELECT b.*, f.fakulte_adi 
        FROM bolumler b
        JOIN fakulteler f ON b.fakulte_id = f.id
        ORDER BY f.fakulte_adi, b.bolum_adi
        """
        bolumler = await self.db.fetch_all(bolum_query)
        
        return {
            "fakulteler": [dict(row) for row in fakulteler],
            "bolumler": [dict(row) for row in bolumler]
        }
    
    async def _danisman_bilgisi(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Öğrencinin danışman bilgileri"""
        ogrenci_no = params.get("ogrenci_no")
        if not ogrenci_no:
            raise ValueError("ogrenci_no gerekli")
        
        query = """
        SELECT o.ogrenci_no, o.ad || ' ' || o.soyad as ogrenci_adi,
               d.ad_soyad as danisman, d.unvan, d.telefon, d.email, d.ofis_no
        FROM ogrenciler o
        LEFT JOIN ogretim_uyeleri d ON o.birinci_danisman_id = d.id
        WHERE o.ogrenci_no = ?
        """
        
        result = await self.db.fetch_one(query, [ogrenci_no])
        
        if not result:
            return {"hata": "Öğrenci bulunamadı"}
        
        return dict(result)
    
    async def _istatistik(self) -> Dict[str, Any]:
        """Genel istatistikler"""
        
        stats = {}
        
        # Temel sayılar
        stats["toplam_ogrenci"] = await self.db.fetch_scalar("SELECT COUNT(*) FROM ogrenciler WHERE durum = 'aktif'")
        stats["toplam_fakulte"] = await self.db.fetch_scalar("SELECT COUNT(*) FROM fakulteler")
        stats["toplam_bolum"] = await self.db.fetch_scalar("SELECT COUNT(*) FROM bolumler")
        stats["toplam_ders"] = await self.db.fetch_scalar("SELECT COUNT(*) FROM dersler")
        
        # En yüksek GANO
        stats["en_yuksek_gano"] = await self.db.fetch_scalar("SELECT MAX(gano) FROM ogrenciler WHERE gano IS NOT NULL")
        
        # Fakülte bazında öğrenci sayıları
        fakulte_stats_query = """
        SELECT f.fakulte_adi, COUNT(o.id) as ogrenci_sayisi
        FROM fakulteler f
        LEFT JOIN ogrenciler o ON f.id = o.fakulte_id AND o.durum = 'aktif'
        GROUP BY f.id, f.fakulte_adi
        ORDER BY ogrenci_sayisi DESC
        """
        fakulte_stats = await self.db.fetch_all(fakulte_stats_query)
        stats["fakulte_dagilimi"] = [dict(row) for row in fakulte_stats]
        
        return stats