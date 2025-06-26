
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
