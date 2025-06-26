"""
Öğrenci Veritabanı Tool
SQLite veritabanı ile öğrenci işleri operasyonları
"""

import sqlite3
import json
from typing import Dict, Any, List, Optional, Union
from datetime import datetime, date
from .base_tool import BaseTool

class StudentDatabaseTool(BaseTool):
    """Öğrenci veritabanı işlemleri tool'u"""
    
    def __init__(self, db_manager):
        super().__init__(
            name="student_database",
            description="Öğrenci veritabanı ile işlem yapar - sorgu, ekleme, güncelleme",
            input_schema={
                "type": "object",
                "properties": {
                    "operation": {
                        "type": "string",
                        "enum": [
                            "ogrenci_ara",
                            "ogrenci_bilgileri",
                            "ogrenci_notlari",
                            "ogrenci_dersleri", 
                            "devamsizlik_sorgula",
                            "burs_bilgileri",
                            "staj_bilgileri",
                            "mesaj_gonder",
                            "mesajlari_listele",
                            "belge_talep_et",
                            "mazeret_sinav_basvuru",
                            "ek_sinav_basvuru",
                            "kulup_uyelikleri",
                            "akademik_takvim",
                            "danisman_bilgileri",
                            "fakulte_bolum_listesi",
                            "ogretim_uyesi_ara",
                            "ders_programi",
                            "custom_query"
                        ],
                        "description": "Yapılacak veritabanı işlemi"
                    },
                    "ogrenci_no": {
                        "type": "string",
                        "description": "Öğrenci numarası"
                    },
                    "ogrenci_id": {
                        "type": "integer",
                        "description": "Öğrenci ID'si"
                    },
                    "akademik_donem": {
                        "type": "string",
                        "description": "Akademik dönem (örn: 2024-2025 Bahar)"
                    },
                    "ders_kodu": {
                        "type": "string",
                        "description": "Ders kodu"
                    },
                    "fakulte_id": {
                        "type": "integer",
                        "description": "Fakülte ID'si"
                    },
                    "bolum_id": {
                        "type": "integer", 
                        "description": "Bölüm ID'si"
                    },
                    "ogretim_uyesi_id": {
                        "type": "integer",
                        "description": "Öğretim üyesi ID'si"
                    },
                    "arama_metni": {
                        "type": "string",
                        "description": "Arama için metin"
                    },
                    "custom_sql": {
                        "type": "string",
                        "description": "Özel SQL sorgusu (sadece SELECT)"
                    },
                    "limit": {
                        "type": "integer",
                        "default": 50,
                        "description": "Sonuç limiti"
                    }
                },
                "required": ["operation"]
            }
        )
        self.db_manager = db_manager
    
    async def execute(self, **kwargs) -> Dict[str, Any]:
        """Veritabanı işlemini gerçekleştir"""
        operation = kwargs.get("operation")
        
        try:
            if operation == "ogrenci_ara":
                result = await self._ogrenci_ara(kwargs)
            elif operation == "ogrenci_bilgileri":
                result = await self._ogrenci_bilgileri(kwargs)
            elif operation == "ogrenci_notlari":
                result = await self._ogrenci_notlari(kwargs)
            elif operation == "ogrenci_dersleri":
                result = await self._ogrenci_dersleri(kwargs)
            elif operation == "devamsizlik_sorgula":
                result = await self._devamsizlik_sorgula(kwargs)
            elif operation == "burs_bilgileri":
                result = await self._burs_bilgileri(kwargs)
            elif operation == "staj_bilgileri":
                result = await self._staj_bilgileri(kwargs)
            elif operation == "mesaj_gonder":
                result = await self._mesaj_gonder(kwargs)
            elif operation == "mesajlari_listele":
                result = await self._mesajlari_listele(kwargs)
            elif operation == "belge_talep_et":
                result = await self._belge_talep_et(kwargs)
            elif operation == "mazeret_sinav_basvuru":
                result = await self._mazeret_sinav_basvuru(kwargs)
            elif operation == "ek_sinav_basvuru":
                result = await self._ek_sinav_basvuru(kwargs)
            elif operation == "kulup_uyelikleri":
                result = await self._kulup_uyelikleri(kwargs)
            elif operation == "akademik_takvim":
                result = await self._akademik_takvim(kwargs)
            elif operation == "danisman_bilgileri":
                result = await self._danisman_bilgileri(kwargs)
            elif operation == "fakulte_bolum_listesi":
                result = await self._fakulte_bolum_listesi(kwargs)
            elif operation == "ogretim_uyesi_ara":
                result = await self._ogretim_uyesi_ara(kwargs)
            elif operation == "ders_programi":
                result = await self._ders_programi(kwargs)
            elif operation == "custom_query":
                result = await self._custom_query(kwargs)
            else:
                return self.create_error_response(f"Bilinmeyen işlem: {operation}")
            
            return self.create_success_response(result, f"{operation} işlemi başarıyla tamamlandı")
            
        except Exception as e:
            return self.create_error_response(f"Veritabanı hatası: {str(e)}")
    
    async def _ogrenci_ara(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Öğrenci arama"""
        arama_metni = params.get("arama_metni", "")
        ogrenci_no = params.get("ogrenci_no", "")
        limit = params.get("limit", 50)
        
        query = """
        SELECT o.id, o.ogrenci_no, o.ad, o.soyad, o.sinif, o.durum,
               f.fakulte_adi, b.bolum_adi, o.gano
        FROM ogrenciler o
        LEFT JOIN fakulteler f ON o.fakulte_id = f.id
        LEFT JOIN bolumler b ON o.bolum_id = b.id
        WHERE 1=1
        """
        params_list = []
        
        if ogrenci_no:
            query += " AND o.ogrenci_no LIKE ?"
            params_list.append(f"%{ogrenci_no}%")
        
        if arama_metni:
            query += " AND (o.ad LIKE ? OR o.soyad LIKE ? OR o.ogrenci_no LIKE ?)"
            params_list.extend([f"%{arama_metni}%"] * 3)
        
        query += f" ORDER BY o.ogrenci_no LIMIT {limit}"
        
        results = await self.db_manager.fetch_all(query, params_list)
        
        return {
            "ogrenciler": [dict(row) for row in results],
            "toplam_sonuc": len(results),
            "arama_kriteri": {
                "ogrenci_no": ogrenci_no,
                "arama_metni": arama_metni
            }
        }
    
    async def _ogrenci_bilgileri(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Öğrenci detay bilgileri"""
        ogrenci_no = params.get("ogrenci_no")
        ogrenci_id = params.get("ogrenci_id")
        
        if not ogrenci_no and not ogrenci_id:
            raise ValueError("ogrenci_no veya ogrenci_id gerekli")
        
        # Ana öğrenci bilgileri
        query = """
        SELECT o.*, f.fakulte_adi, b.bolum_adi,
               d1.ad_soyad as birinci_danisman, d1.unvan as birinci_danisman_unvan,
               d2.ad_soyad as ikinci_danisman, d2.unvan as ikinci_danisman_unvan
        FROM ogrenciler o
        LEFT JOIN fakulteler f ON o.fakulte_id = f.id
        LEFT JOIN bolumler b ON o.bolum_id = b.id
        LEFT JOIN ogretim_uyeleri d1 ON o.birinci_danisman_id = d1.id
        LEFT JOIN ogretim_uyeleri d2 ON o.ikinci_danisman_id = d2.id
        WHERE """
        
        if ogrenci_no:
            query += "o.ogrenci_no = ?"
            param = ogrenci_no
        else:
            query += "o.id = ?"
            param = ogrenci_id
        
        ogrenci = await self.db_manager.fetch_one(query, [param])
        
        if not ogrenci:
            return {"error": "Öğrenci bulunamadı"}
        
        ogrenci_dict = dict(ogrenci)
        
        # Son dönem not ortalaması
        donem_query = """
        SELECT * FROM donem_notlari 
        WHERE ogrenci_id = ? 
        ORDER BY akademik_donem DESC LIMIT 1
        """
        son_donem = await self.db_manager.fetch_one(donem_query, [ogrenci_dict["id"]])
        
        # Aktif ders sayısı
        aktif_ders_query = """
        SELECT COUNT(*) as aktif_ders_sayisi
        FROM ogrenci_ders_kayitlari 
        WHERE ogrenci_id = ? AND durum = 'aktif'
        """
        aktif_ders = await self.db_manager.fetch_one(aktif_ders_query, [ogrenci_dict["id"]])
        
        return {
            "ogrenci_bilgileri": ogrenci_dict,
            "son_donem_notu": dict(son_donem) if son_donem else None,
            "aktif_ders_sayisi": dict(aktif_ders)["aktif_ders_sayisi"] if aktif_ders else 0
        }
    
    async def _ogrenci_notlari(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Öğrenci notları ve başarı durumu"""
        ogrenci_no = params.get("ogrenci_no")
        ogrenci_id = params.get("ogrenci_id")
        akademik_donem = params.get("akademik_donem")
        
        if not ogrenci_no and not ogrenci_id:
            raise ValueError("ogrenci_no veya ogrenci_id gerekli")
        
        # Öğrenci ID'sini bul
        if ogrenci_no:
            ogrenci_query = "SELECT id FROM ogrenciler WHERE ogrenci_no = ?"
            ogrenci_result = await self.db_manager.fetch_one(ogrenci_query, [ogrenci_no])
            if not ogrenci_result:
                return {"error": "Öğrenci bulunamadı"}
            ogrenci_id = ogrenci_result["id"]
        
        # Notlar sorgusu
        query = """
        SELECT sn.*, d.ders_kodu, d.ders_adi, d.kredi
        FROM sinav_notlari sn
        JOIN dersler d ON sn.ders_id = d.id
        WHERE sn.ogrenci_id = ?
        """
        params_list = [ogrenci_id]
        
        if akademik_donem:
            query += " AND sn.akademik_donem = ?"
            params_list.append(akademik_donem)
        
        query += " ORDER BY sn.akademik_donem DESC, d.ders_kodu"
        
        notlar = await self.db_manager.fetch_all(query, params_list)
        
        # Dönem not ortalamaları
        donem_query = """
        SELECT * FROM donem_notlari 
        WHERE ogrenci_id = ? 
        ORDER BY akademik_donem DESC
        """
        donem_notlari = await self.db_manager.fetch_all(donem_query, [ogrenci_id])
        
        return {
            "ders_notlari": [dict(row) for row in notlar],
            "donem_not_ortalamalari": [dict(row) for row in donem_notlari],
            "toplam_ders_sayisi": len(notlar)
        }
    
    async def _ogrenci_dersleri(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Öğrencinin aldığı dersler"""
        ogrenci_no = params.get("ogrenci_no")
        limit = params.get("limit", 50)
        
        if not ogrenci_no:
            raise ValueError("ogrenci_no gerekli")
        
        # Öğrenci ID'sini bul
        ogrenci_query = "SELECT id FROM ogrenciler WHERE ogrenci_no = ?"
        ogrenci_result = await self.db_manager.fetch_one(ogrenci_query, [ogrenci_no])
        if not ogrenci_result:
            return {"error": "Öğrenci bulunamadı"}
        ogrenci_id = ogrenci_result["id"]
        
        # Dersler sorgusu
        query = """
        SELECT odk.*, d.ders_kodu, d.ders_adi, d.kredi
        FROM ogrenci_ders_kayitlari odk
        JOIN dersler d ON odk.ders_id = d.id
        WHERE odk.ogrenci_id = ?
        ORDER BY odk.akademik_donem DESC, d.ders_kodu
        LIMIT ?
        """
        
        dersler = await self.db_manager.fetch_all(query, [ogrenci_id, limit])
        
        return {
            "dersler": [dict(row) for row in dersler],
            "toplam_ders": len(dersler)
        }
    
    async def _fakulte_bolum_listesi(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Fakülte ve bölüm listesi"""
        fakulte_id = params.get("fakulte_id")
        
        # Fakülteler
        fakulte_query = "SELECT * FROM fakulteler ORDER BY fakulte_adi"
        fakulteler = await self.db_manager.fetch_all(fakulte_query)
        
        # Bölümler
        if fakulte_id:
            bolum_query = "SELECT * FROM bolumler WHERE fakulte_id = ? ORDER BY bolum_adi"
            bolumler = await self.db_manager.fetch_all(bolum_query, [fakulte_id])
        else:
            bolum_query = """
            SELECT b.*, f.fakulte_adi 
            FROM bolumler b
            JOIN fakulteler f ON b.fakulte_id = f.id
            ORDER BY f.fakulte_adi, b.bolum_adi
            """
            bolumler = await self.db_manager.fetch_all(bolum_query)
        
        return {
            "fakulteler": [dict(row) for row in fakulteler],
            "bolumler": [dict(row) for row in bolumler],
            "toplam_fakulte": len(fakulteler),
            "toplam_bolum": len(bolumler)
        }
    
    async def _devamsizlik_sorgula(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Devamsızlık durumu sorgulama"""
        return {"info": "Devamsızlık sorgusu henüz aktif değil"}
    
    async def _burs_bilgileri(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Burs ve kredi bilgileri"""
        return {"info": "Burs bilgileri sorgusu henüz aktif değil"}
    
    async def _staj_bilgileri(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Staj bilgileri"""
        return {"info": "Staj bilgileri sorgusu henüz aktif değil"}
    
    async def _mesaj_gonder(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Öğretim üyesine mesaj gönder"""
        return {"info": "Mesaj gönderme işlevi henüz aktif değil"}
    
    async def _mesajlari_listele(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Öğrenci mesajlarını listele"""
        return {"info": "Mesaj listeleme işlevi henüz aktif değil"}
    
    async def _belge_talep_et(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Belge talep durumu"""
        return {"info": "Belge talep işlevi henüz aktif değil"}
    
    async def _mazeret_sinav_basvuru(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Mazeret sınav başvuruları"""
        return {"info": "Mazeret sınav başvuru işlevi henüz aktif değil"}
    
    async def _ek_sinav_basvuru(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Ek sınav başvuruları"""
        return {"info": "Ek sınav başvuru işlevi henüz aktif değil"}
    
    async def _kulup_uyelikleri(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Kulüp üyelikleri"""
        return {"info": "Kulüp üyelikleri sorgusu henüz aktif değil"}
    
    async def _akademik_takvim(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Akademik takvim bilgileri"""
        return {
            "info": "Akademik takvim bilgileri için MCBU web scraper tool'unu kullanın",
            "alternatif": "mcbu_web_scraper tool'u ile akademik_takvim seçeneğini kullanabilirsiniz"
        }
    
    async def _danisman_bilgileri(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Danışman bilgileri"""
        ogrenci_no = params.get("ogrenci_no")
        
        if not ogrenci_no:
            raise ValueError("ogrenci_no gerekli")
        
        query = """
        SELECT o.ogrenci_no, o.ad as ogrenci_ad, o.soyad as ogrenci_soyad,
               d1.ad_soyad as birinci_danisman, d1.unvan as birinci_danisman_unvan,
               d1.telefon as birinci_danisman_telefon, d1.email as birinci_danisman_email,
               d1.ofis_no as birinci_danisman_ofis
        FROM ogrenciler o
        LEFT JOIN ogretim_uyeleri d1 ON o.birinci_danisman_id = d1.id
        WHERE o.ogrenci_no = ?
        """
        
        result = await self.db_manager.fetch_one(query, [ogrenci_no])
        
        if not result:
            return {"error": "Öğrenci bulunamadı"}
        
        return dict(result)
    
    async def _ogretim_uyesi_ara(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Öğretim üyesi arama"""
        arama_metni = params.get("arama_metni", "")
        limit = params.get("limit", 50)
        
        query = """
        SELECT ou.*, f.fakulte_adi, b.bolum_adi
        FROM ogretim_uyeleri ou
        LEFT JOIN fakulteler f ON ou.fakulte_id = f.id
        LEFT JOIN bolumler b ON ou.bolum_id = b.id
        WHERE 1=1
        """
        params_list = []
        
        if arama_metni:
            query += " AND (ou.ad_soyad LIKE ? OR ou.unvan LIKE ? OR ou.uzmanlik_alani LIKE ?)"
            params_list.extend([f"%{arama_metni}%"] * 3)
        
        query += f" ORDER BY ou.ad_soyad LIMIT {limit}"
        
        results = await self.db_manager.fetch_all(query, params_list)
        
        return {
            "ogretim_uyeleri": [dict(row) for row in results],
            "toplam_sonuc": len(results)
        }
    
    async def _ders_programi(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Ders programı"""
        return {"info": "Ders programı sorgusu henüz aktif değil"}
    
    async def _custom_query(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Özel SQL sorgusu"""
        return {"info": "Özel SQL sorgusu henüz aktif değil"}