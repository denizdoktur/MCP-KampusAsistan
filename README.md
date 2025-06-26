# 🎓 MCBU Öğrenci İşleri MCP Server

> **Manisa Celal Bayar Üniversitesi için Model Context Protocol (MCP) tabanlı öğrenci işleri chatbot sistemi**

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://python.org)
[![Continue.dev](https://img.shields.io/badge/Continue.dev-Compatible-green.svg)](https://continue.dev)

## 🌟 Özellikler

- 🔍 **Öğrenci Bilgi Sorgulama**: Detaylı öğrenci kayıtları ve akademik geçmiş
- 📊 **Not Sistemi**: Sınav notları, GANO hesaplama, dönem ortalamaları  
- 🏢 **Organizasyon Yapısı**: Fakülte, bölüm ve öğretim üyesi bilgileri
- 🎯 **Continue.dev Entegrasyonu**: Doğal dil ile veritabanı sorguları
- ⚡ **Yüksek Performans**: Optimize edilmiş SQLite veritabanı
- 🛡️ **Güvenli**: SQL injection koruması ve parameterized queries

## 🚀 Hızlı Başlangıç

### Gereksinimler
- Python 3.8+
- Continue.dev (VS Code veya JetBrains)

### Kurulum

```bash
# Repository'yi klonlayın
git clone https://github.com/KULLANICI_ADI/mcbu-student-affairs-mcp.git
cd mcbu-student-affairs-mcp

# Bağımlılıkları yükleyin
pip install -r requirements.txt

# Hızlı kurulum ve test
python scripts/setup_database.py

# Server'ı başlatın
python src/main.py
```

### Continue.dev Konfigürasyonu

```json
{
  "mcpServers": {
    "mcbu-student-affairs": {
      "command": "python",
      "args": ["/tam/yol/mcbu-student-affairs-mcp/src/main.py"],
      "env": {}
    }
  }
}
```

## 💡 Kullanım Örnekleri

```
"202012345 numaralı öğrencinin bilgilerini getir"
"Ahmet isimli öğrencileri ara"
"Bilgisayar Mühendisliği öğrencilerini listele"
"Veritabanı istatistiklerini göster"
"En yüksek GANO'ya sahip öğrencileri bul"
```

## 🏗️ Proje Yapısı

```
mcbu-student-affairs-mcp/
├── src/
│   ├── main.py                 # MCP server entry point
│   ├── database/
│   │   └── connection.py       # SQLite veritabanı yöneticisi
│   └── tools/
│       ├── base_tool.py        # Temel tool sınıfı
│       └── student_db.py       # Öğrenci veritabanı tool'u
├── scripts/
│   └── quick_setup.py          # Hızlı kurulum scripti
├── data/                       # Veritabanı dosyaları (otomatik)
├── requirements.txt            # Python bağımlılıkları
└── README.md
```

## 🗃️ Veritabanı Şeması

### Ana Tablolar
- **ogrenciler**: Öğrenci bilgileri ve akademik durum
- **fakulteler**: Fakülte organizasyonu
- **bolumler**: Bölüm yapısı
- **ogretim_uyeleri**: Öğretim kadrosu
- **dersler**: Ders kataloğu
- **sinav_notlari**: Akademik başarı kayıtları

## 🔧 API Referansı

### Student Database Tool İşlemleri

| İşlem | Açıklama |
|-------|----------|
| `ogrenci_ara` | Öğrenci arama (ad, soyad, numara) |
| `ogrenci_detay` | Detaylı öğrenci bilgileri |
| `notlari_getir` | Sınav notları ve ortalamaları |
| `dersleri_listele` | Ders kayıt geçmişi |
| `fakulte_bolum_listesi` | Organizasyon yapısı |
| `danisman_bilgisi` | Danışman iletişim bilgileri |
| `istatistik` | Genel veritabanı istatistikleri |

### Örnek Kullanım

```python
# Tool çağrısı
{
  "operation": "ogrenci_ara",
  "arama_metni": "Ahmet",
  "limit": 10
}
```

## 🧪 Test Etme

```bash
# Kurulum testi
python scripts/setup_database.py

# Manuel test
python -c "
import asyncio
from src.tools.student_db import StudentDatabaseTool
from src.database.connection import DatabaseManager

async def test():
    db = DatabaseManager()
    await db.initialize()
    tool = StudentDatabaseTool(db)
    result = await tool.execute(operation='istatistik')
    print(result)

asyncio.run(test())
"
```


## 📋 Yapılacaklar

- [ ] Web scraping tool entegrasyonu
- [ ] Gerçek API bağlantısı
- [ ] Çok dilli destek
- [ ] Advanced analytics
- [ ] Mobile uyumlu web interface