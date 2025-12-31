# Kutuphane Kitap Arama Sistemi

Programlama Lab I (BLM/YZM 217) - Proje 2
Kocaeli Saglik ve Teknoloji Universitesi - 2025-2026 Guz Donemi

## Proje Hakkinda

Python ve Flask ile gelistirilmis kapsamli bir kutuphane yonetim sistemi. Kitap ve uye yonetimi, arama algoritmalari, siralama algoritmalari ve web arayuzu icermektedir.

## Ozellikler

### Temel Ozellikler
- **Kitap Yonetimi**: Kitap ekleme, silme, guncelleme ve listeleme
- **Uye Yonetimi**: Uye kaydi, guncelleme ve takibi
- **Odunc Sistemi**: Kitap odunc verme ve iade islemleri
- **JSON Veri Saklama**: Tum veriler JSON formatinda saklanir

### Arama Fonksiyonlari
- Baslika gore arama
- Yazara gore arama
- Kategoriye gore arama
- ISBN numarasina gore arama

### Siralama Algoritmalari
- **Quick Sort**: Hizli siralama algoritmasi
- **Bubble Sort**: Kabarcik siralama algoritmasi
- Siralama kriterleri: Baslik, Yazar, Yil, Sayfa Sayisi

### Web Arayuzu (Flask)
- Modern ve kullanici dostu arayuz
- Kitap listesi ve ekleme sayfasi
- Uye listesi ve ekleme sayfasi
- Odunc islemleri sayfasi
- Gelismis arama sayfasi

## Kurulum

### Gereksinimler
- Python 3.8+
- Flask (web arayuzu icin)

### Bagimliliklari Yukleme
```bash
pip install flask
```

### Calistirma
```bash
python kutuphane.py
```

Web arayuzune `http://localhost:5000` adresinden erisebilirsiniz.

## Dosya Yapisi

```
Programlama_Lab_II/
├── kutuphane.py           # Ana Python dosyasi (tum kod)
├── kutuphane_verileri.json # Veri dosyasi
├── test_kutuphane.py      # Unit testler
├── templates/             # Flask HTML sablonlari
│   ├── index.html         # Ana sayfa
│   ├── kitaplar.html      # Kitap listesi
│   ├── kitap_ekle.html    # Kitap ekleme formu
│   ├── uyeler.html        # Uye listesi
│   ├── uye_ekle.html      # Uye ekleme formu
│   ├── odunc.html         # Odunc islemleri
│   └── arama.html         # Arama sayfasi
└── README.md              # Bu dosya
```

## Sinif Yapisi

### Book Sinifi
Kutuphane kitaplarini temsil eder:
- `book_id`: Kitap ID numarasi
- `title`: Kitap basligi
- `author`: Yazar adi
- `isbn`: ISBN numarasi
- `publisher`: Yayinevi
- `year`: Yayin yili
- `page_count`: Sayfa sayisi
- `category`: Kategori
- `available`: Musaitlik durumu

### Member Sinifi
Kutuphane uyelerini temsil eder:
- `member_id`: Uye ID numarasi
- `name`: Uye adi soyadi
- `phone`: Telefon numarasi
- `email`: E-posta adresi
- `address`: Adres
- `membership_date`: Uyelik tarihi
- `borrowed_books`: Odunc alinan kitaplar

### Library Sinifi
Tum CRUD islemlerini ve odunc verme/iade islemlerini yonetir.

## Testler

Testleri calistirmak icin:
```bash
python -m pytest test_kutuphane.py -v
```

## Lisans

Bu proje egitim amaciyla gelistirilmistir.

## Gelistirici

Kocaeli Saglik ve Teknoloji Universitesi - Programlama Lab I
# library-management-system
