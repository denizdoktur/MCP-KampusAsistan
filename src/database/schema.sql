-- Öğrenci İşleri Kapsamlı Veritabanı Şeması
-- Manisa Celal Bayar Üniversitesi için tasarlanmıştır

-- Fakülteler tablosu
CREATE TABLE IF NOT EXISTS fakulteler (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fakülte_adi TEXT NOT NULL,
    dekan TEXT,
    telefon TEXT,
    email TEXT,
    adres TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Bölümler tablosu
CREATE TABLE IF NOT EXISTS bolumler (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fakulte_id INTEGER,
    bolum_adi TEXT NOT NULL,
    bolum_kodu TEXT,
    bolum_baskani TEXT,
    telefon TEXT,
    email TEXT,
    FOREIGN KEY (fakulte_id) REFERENCES fakulteler(id)
);

-- Öğretim üyeleri tablosu
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
);

-- Dersler tablosu
CREATE TABLE IF NOT EXISTS dersler (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ders_kodu TEXT NOT NULL UNIQUE,
    ders_adi TEXT NOT NULL,
    kredi INTEGER,
    teorik_saat INTEGER,
    uygulama_saat INTEGER,
    sinif INTEGER,
    donem TEXT, -- güz/bahar
    zorunlu_secmeli TEXT, -- zorunlu/seçmeli
    on_kosul TEXT,
    ders_icerigi TEXT,
    fakulte_id INTEGER,
    bolum_id INTEGER,
    FOREIGN KEY (fakulte_id) REFERENCES fakulteler(id),
    FOREIGN KEY (bolum_id) REFERENCES bolumler(id)
);

-- Öğrenciler tablosu (Ana tablo)
CREATE TABLE IF NOT EXISTS ogrenciler (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ogrenci_no TEXT NOT NULL UNIQUE,
    tc_kimlik_no TEXT UNIQUE,
    ad TEXT NOT NULL,
    soyad TEXT NOT NULL,
    dogum_tarihi DATE,
    cinsiyet TEXT,
    uyruk TEXT DEFAULT 'TC',
    
    -- Akademik bilgiler
    fakulte_id INTEGER,
    bolum_id INTEGER,
    sinif INTEGER,
    aktif_akademik_donem TEXT, -- 2024-2025 Bahar
    kayit_tarihi DATE,
    mezuniyet_tarihi DATE,
    ogrenim_turu TEXT, -- İ.Ö./II.Ö./Doktora
    normal_sure INTEGER DEFAULT 8, -- dönem cinsinden
    azami_sure INTEGER DEFAULT 12, -- dönem cinsinden
    okuduğu_yil INTEGER,
    durum TEXT DEFAULT 'aktif', -- aktif/mezun/kayıt_dondurulmuş/çıkarılmış
    
    -- Danışman bilgileri
    birinci_danisman_id INTEGER,
    ikinci_danisman_id INTEGER,
    
    -- Akademik başarı
    gano REAL,
    
    -- İletişim bilgileri
    telefon TEXT,
    email TEXT,
    adres TEXT,
    il TEXT,
    ilce TEXT,
    posta_kodu TEXT,
    web_sayfasi TEXT,
    orcid TEXT,
    
    -- Banka bilgileri
    banka_adi TEXT,
    iban TEXT,
    hesap_no TEXT,
    
    -- Hazırlık durumu
    hazirlik_durumu TEXT, -- muaf/başarılı/devam_ediyor
    hazirlik_dili TEXT, -- İngilizce/Almanca vs
    hazirlik_donemi TEXT,
    
    -- Özel program durumları
    cift_anadal_kaydi BOOLEAN DEFAULT FALSE,
    yan_dal_kaydi BOOLEAN DEFAULT FALSE,
    ceza_durumu TEXT,
    
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (fakulte_id) REFERENCES fakulteler(id),
    FOREIGN KEY (bolum_id) REFERENCES bolumler(id),
    FOREIGN KEY (birinci_danisman_id) REFERENCES ogretim_uyeleri(id),
    FOREIGN KEY (ikinci_danisman_id) REFERENCES ogretim_uyeleri(id)
);

-- Ders programı (hangi öğretim üyesi hangi dersi veriyor)
CREATE TABLE IF NOT EXISTS ders_programi (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ders_id INTEGER,
    ogretim_uyesi_id INTEGER,
    akademik_donem TEXT, -- 2024-2025 Bahar
    gun TEXT,
    saat TEXT,
    derslik TEXT,
    FOREIGN KEY (ders_id) REFERENCES dersler(id),
    FOREIGN KEY (ogretim_uyesi_id) REFERENCES ogretim_uyeleri(id)
);

-- Öğrenci ders kayıtları
CREATE TABLE IF NOT EXISTS ogrenci_ders_kayitlari (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ogrenci_id INTEGER,
    ders_id INTEGER,
    akademik_donem TEXT,
    kayit_tarihi DATE,
    durum TEXT DEFAULT 'aktif', -- aktif/bırakılan/tamamlanan
    FOREIGN KEY (ogrenci_id) REFERENCES ogrenciler(id),
    FOREIGN KEY (ders_id) REFERENCES dersler(id)
);

-- Sınav notları
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
    basari_durumu TEXT, -- geçti/kaldı/devam
    FOREIGN KEY (ogrenci_id) REFERENCES ogrenciler(id),
    FOREIGN KEY (ders_id) REFERENCES dersler(id)
);

-- Dönem not ortalamaları
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
);

-- Devamsızlık kayıtları
CREATE TABLE IF NOT EXISTS devamsizlik (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ogrenci_id INTEGER,
    ders_id INTEGER,
    akademik_donem TEXT,
    toplam_devamsizlik_saati INTEGER,
    devamsizlik_yüzdesi REAL,
    uyari_durumu TEXT, -- uyarı_yok/1.uyarı/2.uyarı/sınav_hakkı_kaybı
    FOREIGN KEY (ogrenci_id) REFERENCES ogrenciler(id),
    FOREIGN KEY (ders_id) REFERENCES dersler(id)
);

-- Burs ve krediler
CREATE TABLE IF NOT EXISTS burs_krediler (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ogrenci_id INTEGER,
    burs_tipi TEXT, -- kredi/burs/öğrenim_bursu
    kurum TEXT,
    baslangic_tarihi DATE,
    bitis_tarihi DATE,
    tutar REAL,
    durum TEXT, -- aktif/tamamlanan/iptal
    FOREIGN KEY (ogrenci_id) REFERENCES ogrenciler(id)
);

-- Kulüp ve topluluklar
CREATE TABLE IF NOT EXISTS kulup_topluluklar (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    kulup_adi TEXT NOT NULL,
    kurucu_fakulte_id INTEGER,
    danisman_id INTEGER,
    kuruluş_tarihi DATE,
    aciklama TEXT,
    FOREIGN KEY (kurucu_fakulte_id) REFERENCES fakulteler(id),
    FOREIGN KEY (danisman_id) REFERENCES ogretim_uyeleri(id)
);

-- Öğrenci kulüp üyelikleri
CREATE TABLE IF NOT EXISTS ogrenci_kulup_uyelikleri (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ogrenci_id INTEGER,
    kulup_id INTEGER,
    katilim_tarihi DATE,
    ayrilma_tarihi DATE,
    gorev TEXT, -- üye/başkan/sekreter vs
    durum TEXT DEFAULT 'aktif',
    FOREIGN KEY (ogrenci_id) REFERENCES ogrenciler(id),
    FOREIGN KEY (kulup_id) REFERENCES kulup_topluluklar(id)
);

-- Kayıt dondurma bilgileri
CREATE TABLE IF NOT EXISTS kayit_dondurma (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ogrenci_id INTEGER,
    baslangic_tarihi DATE,
    bitis_tarihi DATE,
    donem_sayisi INTEGER,
    sebep TEXT,
    belge_yolu TEXT,
    onay_durumu TEXT, -- onaylandı/beklemede/reddedildi
    FOREIGN KEY (ogrenci_id) REFERENCES ogrenciler(id)
);

-- Onur ve yüksek onur belgeleri
CREATE TABLE IF NOT EXISTS onur_belgeleri (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ogrenci_id INTEGER,
    akademik_donem TEXT,
    belge_tipi TEXT, -- onur/yüksek_onur
    not_ortalamasi REAL,
    veriliş_tarihi DATE,
    FOREIGN KEY (ogrenci_id) REFERENCES ogrenciler(id)
);

-- Mazeret sınav başvuruları
CREATE TABLE IF NOT EXISTS mazeret_sinav_basvurulari (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ogrenci_id INTEGER,
    ders_id INTEGER,
    basvuru_tarihi DATE,
    mazeret_sebep TEXT,
    belge_yolu TEXT,
    onay_durumu TEXT, -- onaylandı/beklemede/reddedildi
    sinav_tarihi DATE,
    FOREIGN KEY (ogrenci_id) REFERENCES ogrenciler(id),
    FOREIGN KEY (ders_id) REFERENCES dersler(id)
);

-- Ek sınav başvuruları
CREATE TABLE IF NOT EXISTS ek_sinav_basvurulari (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ogrenci_id INTEGER,
    ders_id INTEGER,
    basvuru_tarihi DATE,
    onay_durumu TEXT, -- onaylandı/beklemede/reddedildi
    sinav_tarihi DATE,
    ucret REAL,
    odeme_durumu TEXT, -- ödendi/ödenmedi
    FOREIGN KEY (ogrenci_id) REFERENCES ogrenciler(id),
    FOREIGN KEY (ders_id) REFERENCES dersler(id)
);

-- Belge talepleri
CREATE TABLE IF NOT EXISTS belge_talepleri (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ogrenci_id INTEGER,
    belge_tipi TEXT, -- transkript/mezuniyet_belgesi/öğrencilik_belgesi vs
    talep_tarihi DATE,
    teslim_tarihi DATE,
    durum TEXT, -- hazırlanıyor/hazır/teslim_edildi
    ucret REAL,
    odeme_durumu TEXT,
    FOREIGN KEY (ogrenci_id) REFERENCES ogrenciler(id)
);

-- Mesajlaşma sistemi
CREATE TABLE IF NOT EXISTS mesajlar (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    gonderici_ogrenci_id INTEGER,
    alici_ogretim_uyesi_id INTEGER,
    konu TEXT,
    mesaj_icerigi TEXT,
    gonderim_tarihi DATETIME DEFAULT CURRENT_TIMESTAMP,
    okunma_tarihi DATETIME,
    cevap_durumu TEXT DEFAULT 'beklemede', -- beklemede/cevaplanıyor/cevaplanmış
    ek_dosya_yolu TEXT,
    FOREIGN KEY (gonderici_ogrenci_id) REFERENCES ogrenciler(id),
    FOREIGN KEY (alici_ogretim_uyesi_id) REFERENCES ogretim_uyeleri(id)
);

-- Mesaj cevapları
CREATE TABLE IF NOT EXISTS mesaj_cevaplari (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ana_mesaj_id INTEGER,
    gonderici_ogretim_uyesi_id INTEGER,
    cevap_icerigi TEXT,
    gonderim_tarihi DATETIME DEFAULT CURRENT_TIMESTAMP,
    ek_dosya_yolu TEXT,
    FOREIGN KEY (ana_mesaj_id) REFERENCES mesajlar(id),
    FOREIGN KEY (gonderici_ogretim_uyesi_id) REFERENCES ogretim_uyeleri(id)
);

-- Staj bilgileri
CREATE TABLE IF NOT EXISTS stajlar (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ogrenci_id INTEGER,
    staj_tipi TEXT, -- zorunlu/gönüllü/yaz_stajı
    firma_adi TEXT,
    firma_adresi TEXT,
    staj_baslangic_tarihi DATE,
    staj_bitis_tarihi DATE,
    staj_suresi INTEGER, -- gün cinsinden
    staj_puani REAL,
    danisman_onay TEXT, -- onaylandı/beklemede/reddedildi
    firma_degerlendirme_formu TEXT,
    ogrenci_raporu TEXT,
    FOREIGN KEY (ogrenci_id) REFERENCES ogrenciler(id)
);

-- Ceza bilgileri
CREATE TABLE IF NOT EXISTS ceza_bilgileri (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ogrenci_id INTEGER,
    ceza_tipi TEXT, -- uyarı/kınama/uzaklaştırma vs
    ceza_sebebi TEXT,
    ceza_tarihi DATE,
    ceza_suresi INTEGER, -- gün cinsinden, sürekli cezalar için NULL
    aktif_durum BOOLEAN DEFAULT TRUE,
    aciklama TEXT,
    FOREIGN KEY (ogrenci_id) REFERENCES ogrenciler(id)
);

-- Öğrenim ücreti bilgileri
CREATE TABLE IF NOT EXISTS ogrenim_ucreti (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ogrenci_id INTEGER,
    akademik_donem TEXT,
    ucret_tipi TEXT, -- katkı_ücreti/öğrenim_ücreti
    tutar REAL,
    son_odeme_tarihi DATE,
    odeme_durumu TEXT, -- ödendi/ödenmedi/taksitli
    odeme_tarihi DATE,
    FOREIGN KEY (ogrenci_id) REFERENCES ogrenciler(id)
);

-- Trigger: Öğrenci güncellendiğinde updated_at alanını güncelle
CREATE TRIGGER IF NOT EXISTS update_ogrenci_timestamp 
    AFTER UPDATE ON ogrenciler
    FOR EACH ROW
BEGIN
    UPDATE ogrenciler SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;