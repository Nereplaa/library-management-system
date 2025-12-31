"""
Kütüphane Kitap Arama Sistemi
Programlama Lab I - Proje 2
Kocaeli Sağlık ve Teknoloji Üniversitesi
2025-2026 Güz Dönemi
"""

from datetime import datetime
import json
import os

# Flask'ı opsiyonel olarak yükle
try:
    from flask import Flask, render_template, request, redirect, url_for, flash
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False


# ==================== FAZ 1: TEMEL SINIFLAR ====================

class Book:
    """
    Kitap sınıfı - Kütüphanedeki kitapları temsil eder.
    
    Özellikler:
        book_id: Kitap ID numarası
        title: Kitap başlığı
        author: Yazar adı
        isbn: ISBN numarası
        publisher: Yayınevi
        year: Yayın yılı
        page_count: Sayfa sayısı
        category: Kategori
        available: Müsait mi (True/False)
    """
    
    def __init__(self, book_id: int, title: str, author: str, isbn: str,
                 publisher: str, year: int, page_count: int, category: str,
                 available: bool = True):
        """Kitap nesnesini oluşturur."""
        self.book_id = book_id
        self.title = title
        self.author = author
        self.isbn = isbn
        self.publisher = publisher
        self.year = year
        self.page_count = page_count
        self.category = category
        self.available = available
    
    def __str__(self) -> str:
        """Kitap bilgilerini okunabilir formatta döndürür."""
        durum = "Müsait" if self.available else "Ödünç Verildi"
        return (f"[{self.book_id}] {self.title} - {self.author} "
                f"({self.year}) | {self.category} | {durum}")
    
    def __repr__(self) -> str:
        """Kitap nesnesinin teknik gösterimi."""
        return f"Book(id={self.book_id}, title='{self.title}')"
    
    def to_dict(self) -> dict:
        """Kitap nesnesini sözlük formatına çevirir (JSON için)."""
        return {
            "book_id": self.book_id,
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "publisher": self.publisher,
            "year": self.year,
            "page_count": self.page_count,
            "category": self.category,
            "available": self.available
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Book':
        """Sözlükten kitap nesnesi oluşturur (JSON'dan yükleme için)."""
        return cls(
            book_id=data["book_id"],
            title=data["title"],
            author=data["author"],
            isbn=data["isbn"],
            publisher=data["publisher"],
            year=data["year"],
            page_count=data["page_count"],
            category=data["category"],
            available=data.get("available", True)
        )


class Member:
    """
    Üye sınıfı - Kütüphane üyelerini temsil eder.
    
    Özellikler:
        member_id: Üye ID numarası
        name: Üye adı soyadı
        phone: Telefon numarası
        email: E-posta adresi
        address: Adres
        membership_date: Üyelik tarihi
        borrowed_books: Ödünç alınan kitapların ID listesi
    """
    
    def __init__(self, member_id: int, name: str, phone: str, email: str,
                 address: str, membership_date: str = None,
                 borrowed_books: list = None):
        """Üye nesnesini oluşturur."""
        self.member_id = member_id
        self.name = name
        self.phone = phone
        self.email = email
        self.address = address
        # Üyelik tarihi verilmezse bugünün tarihini kullan
        self.membership_date = membership_date or datetime.now().strftime("%Y-%m-%d")
        # Ödünç kitap listesi verilmezse boş liste oluştur
        self.borrowed_books = borrowed_books if borrowed_books is not None else []
    
    def __str__(self) -> str:
        """Üye bilgilerini okunabilir formatta döndürür."""
        kitap_sayisi = len(self.borrowed_books)
        return (f"[{self.member_id}] {self.name} | {self.phone} | "
                f"Ödünç: {kitap_sayisi} kitap")
    
    def __repr__(self) -> str:
        """Üye nesnesinin teknik gösterimi."""
        return f"Member(id={self.member_id}, name='{self.name}')"
    
    def to_dict(self) -> dict:
        """Üye nesnesini sözlük formatına çevirir (JSON için)."""
        return {
            "member_id": self.member_id,
            "name": self.name,
            "phone": self.phone,
            "email": self.email,
            "address": self.address,
            "membership_date": self.membership_date,
            "borrowed_books": self.borrowed_books
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Member':
        """Sözlükten üye nesnesi oluşturur (JSON'dan yükleme için)."""
        return cls(
            member_id=data["member_id"],
            name=data["name"],
            phone=data["phone"],
            email=data["email"],
            address=data["address"],
            membership_date=data.get("membership_date"),
            borrowed_books=data.get("borrowed_books", [])
        )


# ==================== FAZ 2: LIBRARY SINIFI ====================

class Library:
    """
    Kütüphane sınıfı - Kitap ve üye yönetimini sağlar.
    
    Bu sınıf tüm CRUD (Create, Read, Update, Delete) işlemlerini
    ve ödünç verme/iade işlemlerini yönetir.
    """
    
    def __init__(self):
        """Kütüphane nesnesini oluşturur."""
        self.books = []      # Kitap listesi
        self.members = []    # Üye listesi
        self._next_book_id = 1    # Sonraki kitap ID
        self._next_member_id = 1  # Sonraki üye ID
    
    # ========== KİTAP İŞLEMLERİ ==========
    
    def add_book(self, title: str, author: str, isbn: str, publisher: str,
                 year: int, page_count: int, category: str) -> Book:
        """
        Kütüphaneye yeni kitap ekler.
        
        Returns:
            Book: Eklenen kitap nesnesi
        """
        book = Book(
            book_id=self._next_book_id,
            title=title,
            author=author,
            isbn=isbn,
            publisher=publisher,
            year=year,
            page_count=page_count,
            category=category
        )
        self.books.append(book)
        self._next_book_id += 1
        return book
    
    def remove_book(self, book_id: int) -> bool:
        """
        Kitabı kütüphaneden siler.
        
        Args:
            book_id: Silinecek kitabın ID'si
            
        Returns:
            bool: Silme başarılı ise True, değilse False
        """
        for i, book in enumerate(self.books):
            if book.book_id == book_id:
                # Kitap ödünç verilmişse silme
                if not book.available:
                    print(f"Hata: Kitap ödünç verilmiş, silinemez!")
                    return False
                self.books.pop(i)
                return True
        return False
    
    def update_book(self, book_id: int, **kwargs) -> bool:
        """
        Kitap bilgilerini günceller.
        
        Args:
            book_id: Güncellenecek kitabın ID'si
            **kwargs: Güncellenecek alanlar (title, author, vb.)
            
        Returns:
            bool: Güncelleme başarılı ise True
        """
        book = self.get_book(book_id)
        if book:
            for key, value in kwargs.items():
                if hasattr(book, key) and key != 'book_id':
                    setattr(book, key, value)
            return True
        return False
    
    def get_book(self, book_id: int) -> Book:
        """
        ID'ye göre kitap getirir.
        
        Returns:
            Book: Bulunan kitap veya None
        """
        for book in self.books:
            if book.book_id == book_id:
                return book
        return None
    
    def list_books(self) -> list:
        """Tüm kitapları listeler."""
        return self.books.copy()
    
    # ========== ÜYE İŞLEMLERİ ==========
    
    def add_member(self, name: str, phone: str, email: str, address: str) -> Member:
        """
        Kütüphaneye yeni üye ekler.
        
        Returns:
            Member: Eklenen üye nesnesi
        """
        member = Member(
            member_id=self._next_member_id,
            name=name,
            phone=phone,
            email=email,
            address=address
        )
        self.members.append(member)
        self._next_member_id += 1
        return member
    
    def remove_member(self, member_id: int) -> bool:
        """
        Üyeyi kütüphaneden siler.
        
        Args:
            member_id: Silinecek üyenin ID'si
            
        Returns:
            bool: Silme başarılı ise True
        """
        for i, member in enumerate(self.members):
            if member.member_id == member_id:
                # Üyede ödünç kitap varsa silme
                if member.borrowed_books:
                    print(f"Hata: Üyede ödünç kitap var, silinemez!")
                    return False
                self.members.pop(i)
                return True
        return False
    
    def update_member(self, member_id: int, **kwargs) -> bool:
        """
        Üye bilgilerini günceller.
        
        Args:
            member_id: Güncellenecek üyenin ID'si
            **kwargs: Güncellenecek alanlar (name, phone, vb.)
            
        Returns:
            bool: Güncelleme başarılı ise True
        """
        member = self.get_member(member_id)
        if member:
            for key, value in kwargs.items():
                if hasattr(member, key) and key != 'member_id':
                    setattr(member, key, value)
            return True
        return False
    
    def get_member(self, member_id: int) -> Member:
        """
        ID'ye göre üye getirir.
        
        Returns:
            Member: Bulunan üye veya None
        """
        for member in self.members:
            if member.member_id == member_id:
                return member
        return None
    
    def list_members(self) -> list:
        """Tüm üyeleri listeler."""
        return self.members.copy()
    
    # ========== ÖDÜNÇ İŞLEMLERİ ==========
    
    def borrow_book(self, member_id: int, book_id: int) -> bool:
        """
        Üyeye kitap ödünç verir.
        
        Args:
            member_id: Ödünç alan üyenin ID'si
            book_id: Ödünç verilecek kitabın ID'si
            
        Returns:
            bool: İşlem başarılı ise True
        """
        member = self.get_member(member_id)
        book = self.get_book(book_id)
        
        if not member:
            print("Hata: Üye bulunamadı!")
            return False
        
        if not book:
            print("Hata: Kitap bulunamadı!")
            return False
        
        if not book.available:
            print("Hata: Kitap zaten ödünç verilmiş!")
            return False
        
        # Kitabı ödünç ver
        book.available = False
        member.borrowed_books.append(book_id)
        return True
    
    def return_book(self, member_id: int, book_id: int) -> bool:
        """
        Ödünç alınan kitabı iade alır.
        
        Args:
            member_id: İade eden üyenin ID'si
            book_id: İade edilecek kitabın ID'si
            
        Returns:
            bool: İşlem başarılı ise True
        """
        member = self.get_member(member_id)
        book = self.get_book(book_id)
        
        if not member:
            print("Hata: Üye bulunamadı!")
            return False
        
        if not book:
            print("Hata: Kitap bulunamadı!")
            return False
        
        if book_id not in member.borrowed_books:
            print("Hata: Bu kitap bu üyede kayıtlı değil!")
            return False
        
        # Kitabı iade al
        book.available = True
        member.borrowed_books.remove(book_id)
        return True
    
    # ========== FAZ 3: ARAMA FONKSİYONLARI ==========
    
    def search_by_title(self, title: str) -> list:
        """
        Başlığa göre kitap arar.
        
        Args:
            title: Aranacak başlık (kısmi eşleşme)
            
        Returns:
            list: Eşleşen kitapların listesi
        """
        title_lower = title.lower()
        results = []
        for book in self.books:
            if title_lower in book.title.lower():
                results.append(book)
        return results
    
    def search_by_author(self, author: str) -> list:
        """
        Yazara göre kitap arar.
        
        Args:
            author: Aranacak yazar adı (kısmi eşleşme)
            
        Returns:
            list: Eşleşen kitapların listesi
        """
        author_lower = author.lower()
        results = []
        for book in self.books:
            if author_lower in book.author.lower():
                results.append(book)
        return results
    
    def search_by_category(self, category: str) -> list:
        """
        Kategoriye göre kitap arar.
        
        Args:
            category: Aranacak kategori (kısmi eşleşme)
            
        Returns:
            list: Eşleşen kitapların listesi
        """
        category_lower = category.lower()
        results = []
        for book in self.books:
            if category_lower in book.category.lower():
                results.append(book)
        return results
    
    def search_by_isbn(self, isbn: str) -> Book:
        """
        ISBN'e göre kitap arar.
        
        Args:
            isbn: Aranacak ISBN numarası (tam eşleşme)
            
        Returns:
            Book: Bulunan kitap veya None
        """
        for book in self.books:
            if book.isbn == isbn:
                return book
        return None


# ==================== FAZ 4: SIRALAMA ALGORİTMALARI ====================

def quick_sort(books: list, key: str = "title", reverse: bool = False) -> list:
    """
    Quick Sort algoritması ile kitapları sıralar.
    
    Args:
        books: Sıralanacak kitap listesi
        key: Sıralama kriteri ("title", "author", "year", "page_count")
        reverse: True ise azalan sıralama
        
    Returns:
        list: Sıralanmış kitap listesi
    """
    # Boş veya tek elemanlı liste zaten sıralı
    if len(books) <= 1:
        return books.copy()
    
    # Listeyi kopyala (orijinali değiştirme)
    arr = books.copy()
    
    def get_key_value(book):
        """Kitaptan sıralama anahtarını al."""
        value = getattr(book, key)
        # String ise küçük harfe çevir
        if isinstance(value, str):
            return value.lower()
        return value
    
    def partition(low, high):
        """Partition fonksiyonu - pivot etrafında böl."""
        pivot = get_key_value(arr[high])
        i = low - 1
        
        for j in range(low, high):
            current = get_key_value(arr[j])
            # Karşılaştırma yönünü belirle
            if reverse:
                condition = current > pivot
            else:
                condition = current < pivot
            
            if condition:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1
    
    def quick_sort_recursive(low, high):
        """Recursive Quick Sort."""
        if low < high:
            pi = partition(low, high)
            quick_sort_recursive(low, pi - 1)
            quick_sort_recursive(pi + 1, high)
    
    quick_sort_recursive(0, len(arr) - 1)
    return arr


def bubble_sort(books: list, key: str = "title", reverse: bool = False) -> list:
    """
    Bubble Sort algoritması ile kitapları sıralar.
    
    Args:
        books: Sıralanacak kitap listesi
        key: Sıralama kriteri ("title", "author", "year", "page_count")
        reverse: True ise azalan sıralama
        
    Returns:
        list: Sıralanmış kitap listesi
    """
    # Listeyi kopyala (orijinali değiştirme)
    arr = books.copy()
    n = len(arr)
    
    def get_key_value(book):
        """Kitaptan sıralama anahtarını al."""
        value = getattr(book, key)
        # String ise küçük harfe çevir
        if isinstance(value, str):
            return value.lower()
        return value
    
    # Bubble Sort algoritması
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            current = get_key_value(arr[j])
            next_val = get_key_value(arr[j + 1])
            
            # Karşılaştırma yönünü belirle
            if reverse:
                condition = current < next_val
            else:
                condition = current > next_val
            
            if condition:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        
        # Eğer bu geçişte swap yapılmadıysa liste sıralı
        if not swapped:
            break
    
    return arr


# ==================== FAZ 5: DOSYA İŞLEMLERİ ====================

def save_to_json(library: 'Library', filename: str = "kutuphane_verileri.json") -> bool:
    """
    Kütüphane verilerini JSON dosyasına kaydeder.
    
    Args:
        library: Kaydedilecek Library nesnesi
        filename: Dosya adı
        
    Returns:
        bool: Kaydetme başarılı ise True
    """
    try:
        data = {
            "books": [book.to_dict() for book in library.books],
            "members": [member.to_dict() for member in library.members],
            "next_book_id": library._next_book_id,
            "next_member_id": library._next_member_id
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        return True
    except Exception as e:
        print(f"Hata: Dosya kaydedilemedi - {e}")
        return False


def load_from_json(filename: str = "kutuphane_verileri.json") -> 'Library':
    """
    JSON dosyasından kütüphane verilerini yükler.
    
    Args:
        filename: Dosya adı
        
    Returns:
        Library: Yüklenen kütüphane nesnesi veya yeni boş kütüphane
    """
    library = Library()
    
    # Dosya yoksa boş kütüphane döndür
    if not os.path.exists(filename):
        print(f"Bilgi: '{filename}' dosyası bulunamadı, yeni kütüphane oluşturuldu.")
        return library
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Kitapları yükle
        for book_data in data.get("books", []):
            book = Book.from_dict(book_data)
            library.books.append(book)
        
        # Üyeleri yükle
        for member_data in data.get("members", []):
            member = Member.from_dict(member_data)
            library.members.append(member)
        
        # ID sayaçlarını ayarla
        library._next_book_id = data.get("next_book_id", 1)
        library._next_member_id = data.get("next_member_id", 1)
        
        return library
    except Exception as e:
        print(f"Hata: Dosya yüklenemedi - {e}")
        return library


# ==================== FAZ 6: FLASK WEB ARAYÜZÜ ====================

# Global kütüphane nesnesi
web_kutuphane = None

def get_kutuphane():
    """Kütüphane nesnesini döndürür."""
    global web_kutuphane
    if web_kutuphane is None:
        web_kutuphane = load_from_json("kutuphane_verileri.json")
    return web_kutuphane

def kaydet():
    """Değişiklikleri JSON'a kaydeder."""
    save_to_json(get_kutuphane(), "kutuphane_verileri.json")


def validate_isbn(isbn: str) -> tuple:
    """
    ISBN formatini dogrular.
    
    Gecerli formatlar:
    - ISBN-10: 10 karakter (son karakter X olabilir)
    - ISBN-13: 13 karakter (978 veya 979 ile baslar)
    - Tireli veya tiresiz kabul edilir
    
    Args:
        isbn: Dogrulanacak ISBN
        
    Returns:
        tuple: (gecerli_mi, temizlenmis_isbn, hata_mesaji)
    """
    # Tireleri ve bosluklari kaldir
    temiz = isbn.replace("-", "").replace(" ", "").upper()
    
    # Bos kontrol
    if not temiz:
        return (False, "", "ISBN bos olamaz!")
    
    # ISBN-10 kontrolu
    if len(temiz) == 10:
        # Ilk 9 karakter rakam olmali
        if not temiz[:9].isdigit():
            return (False, "", "ISBN-10 formati hatali! Ilk 9 karakter rakam olmali.")
        # Son karakter rakam veya X olmali
        if not (temiz[9].isdigit() or temiz[9] == 'X'):
            return (False, "", "ISBN-10 formati hatali! Son karakter rakam veya X olmali.")
        return (True, temiz, "")
    
    # ISBN-13 kontrolu
    elif len(temiz) == 13:
        # Tum karakterler rakam olmali
        if not temiz.isdigit():
            return (False, "", "ISBN-13 formati hatali! Tum karakterler rakam olmali.")
        # 978 veya 979 ile baslamali
        if not (temiz.startswith("978") or temiz.startswith("979")):
            return (False, "", "ISBN-13 formati hatali! 978 veya 979 ile baslamali.")
        return (True, temiz, "")
    
    else:
        return (False, "", f"ISBN 10 veya 13 karakter olmali! (Girilen: {len(temiz)} karakter)")


# Flask route'ları (sadece Flask yüklüyse)
if FLASK_AVAILABLE:
    app = Flask(__name__)
    app.secret_key = 'kutuphane_gizli_anahtar_2025'

    @app.route('/')
    def index():
        """Ana sayfa."""
        ktp = get_kutuphane()
        return render_template('index.html', 
                             kitap_sayisi=len(ktp.books),
                             uye_sayisi=len(ktp.members),
                             odunc_sayisi=sum(1 for b in ktp.books if not b.available))

    @app.route('/kitaplar')
    def kitaplar():
        """Kitap listesi sayfası."""
        ktp = get_kutuphane()
        siralama = request.args.get('siralama', 'title')
        yon = request.args.get('yon', 'asc')
        kitaplar_list = ktp.list_books()
        if siralama in ['title', 'author', 'year', 'page_count']:
            kitaplar_list = quick_sort(kitaplar_list, key=siralama, reverse=(yon == 'desc'))
        return render_template('kitaplar.html', kitaplar=kitaplar_list, siralama=siralama, yon=yon)

    @app.route('/kitap-ekle', methods=['GET', 'POST'])
    def kitap_ekle():
        """Kitap ekleme sayfası."""
        if request.method == 'POST':
            try:
                # Form verilerini al ve dogrula
                title = request.form.get('title', '').strip()
                author = request.form.get('author', '').strip()
                isbn_raw = request.form.get('isbn', '').strip()
                publisher = request.form.get('publisher', '').strip()
                category = request.form.get('category', '').strip()
                
                # Bos alan kontrolu
                if not all([title, author, isbn_raw, publisher, category]):
                    flash('Tum alanlar doldurulmalidir!', 'error')
                    return render_template('kitap_ekle.html')
                
                # ISBN format kontrolu
                gecerli, isbn, hata = validate_isbn(isbn_raw)
                if not gecerli:
                    flash(f'ISBN Hatasi: {hata}', 'error')
                    return render_template('kitap_ekle.html')
                
                # Sayi alanlari kontrolu
                try:
                    year = int(request.form.get('year', '0'))
                    if year < 1900 or year > 2100:
                        flash('Yil 1900-2100 arasi olmalidir!', 'error')
                        return render_template('kitap_ekle.html')
                except ValueError:
                    flash('Yil sayisal bir deger olmalidir!', 'error')
                    return render_template('kitap_ekle.html')
                
                try:
                    page_count = int(request.form.get('page_count', '0'))
                    if page_count < 1:
                        flash('Sayfa sayisi en az 1 olmalidir!', 'error')
                        return render_template('kitap_ekle.html')
                except ValueError:
                    flash('Sayfa sayisi sayisal bir deger olmalidir!', 'error')
                    return render_template('kitap_ekle.html')
                
                # Kitabi ekle
                ktp = get_kutuphane()
                ktp.add_book(
                    title=title,
                    author=author,
                    isbn=isbn,
                    publisher=publisher,
                    year=year,
                    page_count=page_count,
                    category=category
                )
                kaydet()
                flash('Kitap basariyla eklendi!', 'success')
                return redirect(url_for('kitaplar'))
            except Exception as e:
                flash(f'Hata olustu: {str(e)}', 'error')
                return render_template('kitap_ekle.html')
        return render_template('kitap_ekle.html')

    @app.route('/kitap-sil/<int:book_id>')
    def kitap_sil(book_id):
        """Kitap silme."""
        ktp = get_kutuphane()
        if ktp.remove_book(book_id):
            kaydet()
            flash('Kitap başarıyla silindi!', 'success')
        else:
            flash('Kitap silinemedi! (Ödünç verilmiş olabilir)', 'error')
        return redirect(url_for('kitaplar'))

    @app.route('/uyeler')
    def uyeler():
        """Üye listesi sayfası."""
        ktp = get_kutuphane()
        return render_template('uyeler.html', uyeler=ktp.list_members())

    @app.route('/uye-ekle', methods=['GET', 'POST'])
    def uye_ekle():
        """Üye ekleme sayfası."""
        if request.method == 'POST':
            try:
                # Form verilerini al ve dogrula
                name = request.form.get('name', '').strip()
                phone = request.form.get('phone', '').strip()
                email = request.form.get('email', '').strip()
                address = request.form.get('address', '').strip()
                
                # Bos alan kontrolu
                if not all([name, phone, email, address]):
                    flash('Tum alanlar doldurulmalidir!', 'error')
                    return render_template('uye_ekle.html')
                
                # Minimum uzunluk kontrolu
                if len(name) < 2:
                    flash('Ad soyad en az 2 karakter olmalidir!', 'error')
                    return render_template('uye_ekle.html')
                
                if len(phone) < 7:
                    flash('Telefon numarasi en az 7 karakter olmalidir!', 'error')
                    return render_template('uye_ekle.html')
                
                # Basit e-posta kontrolu
                if '@' not in email or '.' not in email:
                    flash('Gecerli bir e-posta adresi girin!', 'error')
                    return render_template('uye_ekle.html')
                
                # Uye ekle
                ktp = get_kutuphane()
                ktp.add_member(
                    name=name,
                    phone=phone,
                    email=email,
                    address=address
                )
                kaydet()
                flash('Uye basariyla eklendi!', 'success')
                return redirect(url_for('uyeler'))
            except Exception as e:
                flash(f'Hata olustu: {str(e)}', 'error')
                return render_template('uye_ekle.html')
        return render_template('uye_ekle.html')

    @app.route('/uye-sil/<int:member_id>')
    def uye_sil(member_id):
        """Üye silme."""
        ktp = get_kutuphane()
        if ktp.remove_member(member_id):
            kaydet()
            flash('Üye başarıyla silindi!', 'success')
        else:
            flash('Üye silinemedi! (Ödünç kitabı olabilir)', 'error')
        return redirect(url_for('uyeler'))

    @app.route('/odunc', methods=['GET', 'POST'])
    def odunc():
        """Ödünç verme/iade sayfası."""
        ktp = get_kutuphane()
        if request.method == 'POST':
            try:
                islem = request.form.get('islem', '')
                
                # ID'leri dogrula
                try:
                    member_id = int(request.form.get('member_id', '0'))
                    book_id = int(request.form.get('book_id', '0'))
                except ValueError:
                    flash('Gecersiz uye veya kitap secimi!', 'error')
                    return render_template('odunc.html', kitaplar=ktp.list_books(), uyeler=ktp.list_members())
                
                if member_id <= 0 or book_id <= 0:
                    flash('Lutfen uye ve kitap secin!', 'error')
                    return render_template('odunc.html', kitaplar=ktp.list_books(), uyeler=ktp.list_members())
                
                if islem == 'odunc':
                    if ktp.borrow_book(member_id, book_id):
                        kaydet()
                        flash('Kitap odunc verildi!', 'success')
                    else:
                        flash('Odunc verilemedi! (Kitap musait olmayabilir)', 'error')
                elif islem == 'iade':
                    if ktp.return_book(member_id, book_id):
                        kaydet()
                        flash('Kitap iade alindi!', 'success')
                    else:
                        flash('Iade alinamadi! (Kitap bu uyede olmayabilir)', 'error')
                else:
                    flash('Gecersiz islem!', 'error')
            except Exception as e:
                flash(f'Hata olustu: {str(e)}', 'error')
        return render_template('odunc.html', kitaplar=ktp.list_books(), uyeler=ktp.list_members())

    @app.route('/arama', methods=['GET', 'POST'])
    def arama():
        """Arama sayfası."""
        ktp = get_kutuphane()
        sonuclar = []
        arama_yapildi = False
        secili_kriter = 'title'  # Varsayilan
        secili_kelime = ''
        
        if request.method == 'POST':
            secili_kriter = request.form.get('kriter', 'title')
            secili_kelime = request.form.get('kelime', '')
            arama_yapildi = True
            
            if secili_kriter == 'title':
                sonuclar = ktp.search_by_title(secili_kelime)
            elif secili_kriter == 'author':
                sonuclar = ktp.search_by_author(secili_kelime)
            elif secili_kriter == 'category':
                sonuclar = ktp.search_by_category(secili_kelime)
            elif secili_kriter == 'isbn':
                kitap = ktp.search_by_isbn(secili_kelime)
                if kitap:
                    sonuclar = [kitap]
        
        return render_template('arama.html', 
                             sonuclar=sonuclar, 
                             arama_yapildi=arama_yapildi,
                             secili_kriter=secili_kriter,
                             secili_kelime=secili_kelime)

    def run_flask():
        """Flask uygulamasını başlatır."""
        print("\n" + "=" * 50)
        print("Flask Web Sunucusu Baslatiliyor...")
        print("=" * 50)
        print("\nTarayicinizda acin: http://127.0.0.1:5000")
        print("\nDurdurmak icin: CTRL+C")
        print("=" * 50 + "\n")
        app.run(debug=True, use_reloader=False)


# ==================== TERMİNAL MENÜSÜ ====================

def get_int_input(prompt, min_val=None, max_val=None):
    """
    Kullanicidan integer deger alir. Hatali giriste tekrar sorar.
    
    Args:
        prompt: Kullaniciya gosterilecek mesaj
        min_val: Minimum deger (opsiyonel)
        max_val: Maximum deger (opsiyonel)
    
    Returns:
        int: Gecerli integer deger
    """
    while True:
        try:
            deger = int(input(prompt).strip())
            if min_val is not None and deger < min_val:
                print(f"  [HATA] Deger en az {min_val} olmali!")
                continue
            if max_val is not None and deger > max_val:
                print(f"  [HATA] Deger en fazla {max_val} olmali!")
                continue
            return deger
        except ValueError:
            print("  [HATA] Lutfen gecerli bir sayi girin!")


def get_str_input(prompt, allow_empty=False):
    """
    Kullanicidan string deger alir. Bos giriste tekrar sorar.
    
    Args:
        prompt: Kullaniciya gosterilecek mesaj
        allow_empty: Bos deger kabul edilsin mi
    
    Returns:
        str: Gecerli string deger
    """
    while True:
        deger = input(prompt).strip()
        if not allow_empty and not deger:
            print("  [HATA] Bu alan bos birakilamaz!")
            continue
        return deger


def get_isbn_input(prompt):
    """
    Kullanicidan gecerli ISBN alir. Hatali formatta tekrar sorar.
    
    Args:
        prompt: Kullaniciya gosterilecek mesaj
        
    Returns:
        str: Gecerli ISBN
    """
    print("  [BILGI] ISBN formati: 10 veya 13 karakter (orn: 978-605-1234-56-7)")
    while True:
        deger = input(prompt).strip()
        if not deger:
            print("  [HATA] ISBN bos birakilamaz!")
            continue
        
        gecerli, temiz_isbn, hata = validate_isbn(deger)
        if gecerli:
            return temiz_isbn
        else:
            print(f"  [HATA] {hata}")


def terminal_menu():
    """Terminal tabanlı menü sistemi."""
    ktp = get_kutuphane()
    
    while True:
        print("\n" + "=" * 50)
        print("     KUTUPHANE YONETIM SISTEMI")
        print("=" * 50)
        print("\n  1. Kitaplari Listele")
        print("  2. Kitap Ekle")
        print("  3. Kitap Sil")
        print("  4. Uyeleri Listele")
        print("  5. Uye Ekle")
        print("  6. Uye Sil")
        print("  7. Kitap Odunc Ver")
        print("  8. Kitap Iade Al")
        print("  9. Kitap Ara")
        print(" 10. Kitaplari Sirala")
        print("  0. Cikis")
        print("\n" + "=" * 50)
        
        secim = input("\nSeciminiz (0-10): ").strip()
        
        if secim == "1":
            # Kitapları listele
            print("\n--- KITAPLAR ---")
            kitaplar = ktp.list_books()
            if kitaplar:
                for k in kitaplar:
                    durum = "Musait" if k.available else "Odunc"
                    print(f"[{k.book_id}] {k.title} - {k.author} ({k.year}) | {k.category} | {durum}")
            else:
                print("Hic kitap yok.")
                
        elif secim == "2":
            # Kitap ekle
            print("\n--- KITAP EKLE ---")
            title = get_str_input("Baslik: ")
            author = get_str_input("Yazar: ")
            isbn = get_isbn_input("ISBN: ")
            publisher = get_str_input("Yayinevi: ")
            year = get_int_input("Yil (1900-2100): ", min_val=1900, max_val=2100)
            page_count = get_int_input("Sayfa Sayisi (1+): ", min_val=1)
            category = get_str_input("Kategori: ")
            kitap = ktp.add_book(title, author, isbn, publisher, year, page_count, category)
            kaydet()
            print(f"\nKitap eklendi: {kitap}")
            
        elif secim == "3":
            # Kitap sil
            print("\n--- KITAP SIL ---")
            book_id = get_int_input("Silinecek Kitap ID: ", min_val=1)
            if ktp.remove_book(book_id):
                kaydet()
                print("Kitap silindi!")
            else:
                print("Kitap silinemedi!")
                
        elif secim == "4":
            # Üyeleri listele
            print("\n--- UYELER ---")
            uyeler = ktp.list_members()
            if uyeler:
                for u in uyeler:
                    print(f"[{u.member_id}] {u.name} | {u.phone} | Odunc: {len(u.borrowed_books)} kitap")
            else:
                print("Hic uye yok.")
                
        elif secim == "5":
            # Üye ekle
            print("\n--- UYE EKLE ---")
            name = get_str_input("Ad Soyad: ")
            phone = get_str_input("Telefon: ")
            email = get_str_input("E-posta: ")
            address = get_str_input("Adres: ")
            uye = ktp.add_member(name, phone, email, address)
            kaydet()
            print(f"\nUye eklendi: {uye}")
            
        elif secim == "6":
            # Üye sil
            print("\n--- UYE SIL ---")
            member_id = get_int_input("Silinecek Uye ID: ", min_val=1)
            if ktp.remove_member(member_id):
                kaydet()
                print("Uye silindi!")
            else:
                print("Uye silinemedi!")
                
        elif secim == "7":
            # Ödünç ver
            print("\n--- ODUNC VER ---")
            member_id = get_int_input("Uye ID: ", min_val=1)
            book_id = get_int_input("Kitap ID: ", min_val=1)
            if ktp.borrow_book(member_id, book_id):
                kaydet()
                print("Kitap odunc verildi!")
            else:
                print("Odunc verilemedi!")
                
        elif secim == "8":
            # İade al
            print("\n--- IADE AL ---")
            member_id = get_int_input("Uye ID: ", min_val=1)
            book_id = get_int_input("Kitap ID: ", min_val=1)
            if ktp.return_book(member_id, book_id):
                kaydet()
                print("Kitap iade alindi!")
            else:
                print("Iade alinamadi!")
                
        elif secim == "9":
            # Arama
            print("\n--- KITAP ARA ---")
            print("1. Basliga gore")
            print("2. Yazara gore")
            print("3. Kategoriye gore")
            print("4. ISBN'e gore")
            kriter = input("Kriter (1-4): ").strip()
            kelime = input("Arama kelimesi: ").strip()
            
            sonuclar = []
            if kriter == "1":
                sonuclar = ktp.search_by_title(kelime)
            elif kriter == "2":
                sonuclar = ktp.search_by_author(kelime)
            elif kriter == "3":
                sonuclar = ktp.search_by_category(kelime)
            elif kriter == "4":
                kitap = ktp.search_by_isbn(kelime)
                if kitap:
                    sonuclar = [kitap]
            
            print(f"\n{len(sonuclar)} sonuc bulundu:")
            for k in sonuclar:
                print(f"  {k}")
                
        elif secim == "10":
            # Sıralama
            print("\n--- SIRALA ---")
            print("1. Basliga gore")
            print("2. Yazara gore")
            print("3. Yila gore")
            print("4. Sayfa sayisina gore")
            kriter = input("Kriter (1-4): ").strip()
            yon = input("Yon (a=artan, z=azalan): ").strip().lower()
            
            keys = {"1": "title", "2": "author", "3": "year", "4": "page_count"}
            if kriter in keys:
                sirali = quick_sort(ktp.list_books(), key=keys[kriter], reverse=(yon == "z"))
                print("\nSirali Liste:")
                for k in sirali:
                    print(f"  {k}")
                    
        elif secim == "0":
            print("\nCikis yapiliyor. Gule gule!")
            break
        else:
            print("\nGecersiz secim!")


# ==================== ANA PROGRAM ====================
if __name__ == "__main__":
    
    # Templates klasörünün varlığını kontrol et
    templates_exists = os.path.exists("templates") and os.path.isdir("templates")
    
    print("\n" + "=" * 60)
    print("     KUTUPHANE YONETIM SISTEMI")
    print("     Programlama Lab I - Proje 2")
    print("=" * 60)
    
    # Flask ve templates kontrolü
    if FLASK_AVAILABLE and templates_exists:
        print("\n[INFO] Flask yuklü ve templates klasoru mevcut.")
        print("[INFO] Web arayuzu baslatilabiir.")
        print("\nNasil calistirmak istersiniz?")
        print("  1. Web Arayuzu (Flask)")
        print("  2. Terminal Menusu")
        secim = input("\nSeciminiz (1/2): ").strip()
        
        if secim == "1":
            run_flask()
        else:
            terminal_menu()
    else:
        if not FLASK_AVAILABLE:
            print("\n[UYARI] Flask yuklü degil!")
            print("        Flask yuklemek icin: pip install flask")
        if not templates_exists:
            print("\n[UYARI] templates klasoru bulunamadi!")
        print("\n[INFO] Terminal menusu baslatiliyor...")
        terminal_menu()
