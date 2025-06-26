# 🎓 MCBU Öğrenci İşleri MCP Projesi

> **Manisa Celal Bayar Üniversitesi Öğrenci İşleri Otomasyonu için Model Context Protocol (MCP) tabanlı chatbot sistemi**

## 📋 Proje Hakkında

Bu proje, öğrenci işlerine yönelik süreçleri hızlandırmak ve otomatikleştirmek amacıyla geliştirilmiş bir MCP (Model Context Protocol) tabanlı chatbot sistemidir. Öğrencilere çeşitli işlemler ve bilgilendirmeler sunarak, öğrenci işleriyle doğrudan iletişim kurma gereksinimini azaltmayı hedefler.

### 🎯 Ana Hedefler
- Öğrenci işleri süreçlerinin otomasyonu
- 7/24 öğrenci hizmetleri
- Hızlı ve doğru bilgi erişimi
- İş yükü azaltımı

## 🚀 Özellikler

### 🔧 Üç Ana Tool
1. **MCBU Web Scraper** (`mcbu_web_scraper`)
   - Üniversite web sitesini scrape eder
   - Vizyon, misyon, fakülte bilgileri
   - Akademik takvim ve duyurular
   - İletişim bilgileri

2. **Öğrenci Veritabanı** (`student_database`) 
   - Kapsamlı öğrenci bilgi sistemi
   - Not sorguları ve akademik geçmiş
   - Ders kayıtları ve programlar
   - Staj, burs ve kulüp bilgileri
   - Belge talepleri ve başvurular

3. **Web API Entegrasyonu** (`web_api_integration`)
   - Gelecekteki API entegrasyonu için placeholder
   - Gerçek zamanlı sistem bağlantısı (geliştirme aşamasında)
   - Mock veriler ile test imkanı

### 📊 Kapsamlı Veritabanı
- **23 farklı tablo** ile ilişkisel veri yapısı
- Öğrenci demografik ve akademik bilgileri
- Fakülte, bölüm ve öğretim üyesi kayıtları
- Not sistemi ve başarı takibi
- Sosyal aktiviteler ve kulüp üyelikleri
- Staj ve mesajlaşma sistemleri

## 🏗️ Proje Yapısı

```
student_affairs_mcp/
├── src/
│   ├── main.py                    # MCP server entry point
│   ├── config/
│   │   ├── settings.py            # Proje ayarları
│   │   └── database.py            # DB yapılandırması
│   ├── tools/
│   │   ├── base_tool.py           # Temel tool sınıfı
│   │   ├── mcbu_scraper.py        # Web scraper tool
│   │   ├── student_db.py          # Veritabanı tool
│   │   └── web_api_placeholder.py # API placeholder
│   ├── database/
│   │   ├── connection.py          # DB bağlantı yöneticisi
│   │   └── schema.sql             # Veritabanı şeması
│   └── mcp/
│       └── server.py              # MCP server sınıfı
├── data/
│   ├── student_affairs.db         # SQLite veritabanı
│   └── logs/                      # Log dosyaları
└── scripts/
    └── setup_database.py          # Kurulum scripti
```

## 🛠️ Kurulum

### 1. Gereksinimleri Yükleyin
```bash
git clone <repository-url>
cd student_affairs_mcp
pip install -r requirements.txt
```

### 2. Çevre Değişkenlerini Ayarlayın
```bash
# .env dosyası oluşturun (opsiyonel - web scraper için)
touch .env
```

### 3. Veritabanını Başlatın
```bash
python src/main.py
# İlk çalıştırmada otomatik olarak veritabanı ve örnek veriler oluşturulur
```

### 4. Continue.dev ile Entegrasyon
Continue.dev konfigürasyonuna ekleyin:

```json
{
  "mcpServers": {
    "mcbu-student-affairs": {
      "command": "python",
      "args": ["/tam/yol/student_affairs_mcp/src/main.py"],
      "env": {}
    }
  }
}
```

## 💡 Kullanım Örnekleri

### 🔍 Öğrenci Bilgi Sorgulama
```
Continue.dev chatinde:
"202012345 numaralı öğrencinin bilgilerini getir"
"Ahmet Yılmaz isimli öğrencileri ara"
```

### 📚 Akademik Sorgular
```
"202012345 numaralı öğrencinin notlarını göster"
"2024-2025 Bahar dönemindeki derslerini listele"
"GANO hesapla ve dönem ortalamaları"
```

### 🏢 Üniversite Bilgileri
```
"MCBU'nun vizyon ve misyonunu anlat"
"Mühendislik fakültesindeki bölümleri listele"
"Akademik takvimi getir"
```

### 📋 İdari İşlemler
```
"Mezuniyet belgesi talep durumunu kontrol et"
"Aktif burs ve kredi bilgilerini göster"
"Kulüp üyeliklerimi listele"
```

## 🗃️ Veritabanı Şeması

### Ana Tablolar
- **ogrenciler**: Temel öğrenci bilgileri
- **fakulteler/bolumler**: Akademik organizasyon
- **ogretim_uyeleri**: Öğretim kadrosu
- **dersler**: Ders kataloğu
- **sinav_notlari**: Akademik başarı
- **ogrenci_ders_kayitlari**: Ders alım geçmişi

### Destekleyici Tablolar
- **burs_krediler**: Mali destek bilgileri
- **stajlar**: Staj kayıtları
- **kulup_topluluklar**: Sosyal aktiviteler
- **mesajlar**: İletişim sistemi
- **belge_talepleri**: Belge işlemleri

## 🔧 Tool API Referansı

### MCBU Web Scraper
```json
{
  "page_type": "vizyon_misyon|fakulteler|bolumler|akademik_takvim",
  "custom_url": "https://www.mcbu.edu.tr/custom-page",
  "max_content_length": 5000
}
```

### Öğrenci Veritabanı
```json
{
  "operation": "ogrenci_ara|ogrenci_bilgileri|ogrenci_notlari",
  "ogrenci_no": "202012345",
  "akademik_donem": "2024-2025 Bahar",
  "limit": 50
}
```

#### Desteklenen İşlemler
- `ogrenci_ara`: Öğrenci arama
- `ogrenci_bilgileri`: Detaylı bilgiler  
- `ogrenci_notlari`: Not ve başarı durumu
- `ogrenci_dersleri`: Ders kayıtları
- `devamsizlik_sorgula`: Devamsızlık kontrol
- `burs_bilgileri`: Burs ve krediler
- `staj_bilgileri`: Staj kayıtları
- `kulup_uyelikleri`: Kulüp aktiviteleri
- `danisman_bilgileri`: Danışman iletişim
- `custom_query`: Özel SQL sorguları

## 🔒 Güvenlik

### SQL Güvenliği
- Sadece SELECT sorguları desteklenir
- Parametreli sorgular kullanılır
- Tehlikeli anahtar kelimeler engellenir
- Sonuç sayısı sınırlandırılır

### Veri Gizliliği
- Kişisel verilerin korunması
- KVKK uyumlu veri işleme
- Log kayıtlarında hassas bilgi maskeleme

## 📈 Gelecek Geliştirmeler

### Faz 1: API Entegrasyonu
- [ ] Üniversite IT departmanı ile koordinasyon
- [ ] Gerçek API endpoint'leri entegrasyonu
- [ ] OAuth2/JWT kimlik doğrulama

### Faz 2: İleri Özellikler  
- [ ] Gerçek zamanlı bildirimler
- [ ] Belge otomatik oluşturma
- [ ] E-imza entegrasyonu
- [ ] Mobile uygulaması

### Faz 3: AI Geliştirmeleri
- [ ] Doğal dil işleme geliştirilmesi
- [ ] Otomatik form doldurma
- [ ] Akıllı öneri sistemi
- [ ] Çok dilli destek

## 📞 İletişim ve Destek

### Geliştirme Ekibi
- **Proje Sahibi**: [İsim]
- **Geliştirici**: [İsim]

### Teknik Destek
- **E-posta**: [email]
- **GitHub**: [repository-url]

### Üniversite İletişim
- **Bilgi İşlem Daire Başkanlığı**: Gelecekteki API entegrasyonu için
- **Öğrenci İşleri Daire Başkanlığı**: İş süreçleri koordinasyonu

## 📄 Lisans

Bu proje [Lisans Türü] altında lisanslanmıştır. Detaylar için `LICENSE` dosyasına bakınız.

## 🤝 Katkıda Bulunma

1. Repository'yi fork edin
2. Feature branch oluşturun (`git checkout -b feature/YeniOzellik`)
3. Değişikliklerinizi commit edin (`git commit -m 'Yeni özellik eklendi'`)
4. Branch'inizi push edin (`git push origin feature/YeniOzellik`)
5. Pull Request oluşturun

## 📊 Proje İstatistikleri

- **Toplam kod satırı**: ~2000+ 
- **Tool sayısı**: 3
- **Veritabanı tablosu**: 23
- **Desteklenen işlem**: 15+
- **Örnek veri**: 100+ kayıt

## 🏆 Başarımlar

- ✅ Modüler ve ölçeklenebilir mimari
- ✅ Kapsamlı veritabanı tasarımı  
- ✅ Type-safe kod yapısı
- ✅ Async/await performans optimizasyonu
- ✅ Comprehensive logging sistemi
- ✅ Continue.dev entegrasyonu

---

**Not**: Bu proje eğitim amaçlı geliştirilmiştir ve gerçek üniversite verilerini içermez. Tüm veriler örnek/dummy verilerdir.