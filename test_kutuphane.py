"""
Kutuphane Yonetim Sistemi - Test Dosyasi
Tum fonksiyonlari test eder.
"""

import os
import sys

# Ana modulu import et
from kutuphane import (
    Book, Member, Library,
    quick_sort, bubble_sort,
    save_to_json, load_from_json,
    FLASK_AVAILABLE
)

# Test sayaclari
passed = 0
failed = 0

def test(condition, test_name):
    """Test fonksiyonu - basarili/basarisiz sayar."""
    global passed, failed
    if condition:
        print(f"  [OK] {test_name}")
        passed += 1
    else:
        print(f"  [FAIL] {test_name}")
        failed += 1

def run_all_tests():
    """Tum testleri calistirir."""
    global passed, failed
    
    print("\n" + "=" * 70)
    print("     KUTUPHANE YONETIM SISTEMI - KAPSAMLI TEST")
    print("=" * 70)
    
    # ==================== FAZ 1 TESTLERI ====================
    print("\n" + "-" * 70)
    print("FAZ 1: Book ve Member Siniflari")
    print("-" * 70)
    
    # Book sinifi testleri
    print("\n[BOOK SINIFI TESTLERI]")
    
    kitap = Book(
        book_id=1,
        title="Test Kitabi",
        author="Test Yazar",
        isbn="978-123-456",
        publisher="Test Yayinevi",
        year=2024,
        page_count=300,
        category="Test"
    )
    
    test(kitap.book_id == 1, "book_id dogru atandi")
    test(kitap.title == "Test Kitabi", "title dogru atandi")
    test(kitap.author == "Test Yazar", "author dogru atandi")
    test(kitap.isbn == "978-123-456", "isbn dogru atandi")
    test(kitap.publisher == "Test Yayinevi", "publisher dogru atandi")
    test(kitap.year == 2024, "year dogru atandi")
    test(kitap.page_count == 300, "page_count dogru atandi")
    test(kitap.category == "Test", "category dogru atandi")
    test(kitap.available == True, "available varsayilan True")
    
    # __str__ testi
    test("Test Kitabi" in str(kitap), "__str__ metodu calisiyor")
    
    # to_dict testi
    kitap_dict = kitap.to_dict()
    test(isinstance(kitap_dict, dict), "to_dict() sozluk donduruyor")
    test(kitap_dict["title"] == "Test Kitabi", "to_dict() dogru veri iceriyor")
    
    # from_dict testi
    kitap2 = Book.from_dict(kitap_dict)
    test(kitap2.title == kitap.title, "from_dict() dogru calisiyor")
    
    # Member sinifi testleri
    print("\n[MEMBER SINIFI TESTLERI]")
    
    uye = Member(
        member_id=1,
        name="Test Uye",
        phone="0532-111-2222",
        email="test@email.com",
        address="Test Adres"
    )
    
    test(uye.member_id == 1, "member_id dogru atandi")
    test(uye.name == "Test Uye", "name dogru atandi")
    test(uye.phone == "0532-111-2222", "phone dogru atandi")
    test(uye.email == "test@email.com", "email dogru atandi")
    test(uye.address == "Test Adres", "address dogru atandi")
    test(uye.membership_date is not None, "membership_date otomatik atandi")
    test(isinstance(uye.borrowed_books, list), "borrowed_books liste olarak olusturuldu")
    test(len(uye.borrowed_books) == 0, "borrowed_books baslangicta bos")
    
    # __str__ testi
    test("Test Uye" in str(uye), "__str__ metodu calisiyor")
    
    # to_dict ve from_dict testleri
    uye_dict = uye.to_dict()
    test(isinstance(uye_dict, dict), "to_dict() sozluk donduruyor")
    uye2 = Member.from_dict(uye_dict)
    test(uye2.name == uye.name, "from_dict() dogru calisiyor")
    
    # ==================== FAZ 2 TESTLERI ====================
    print("\n" + "-" * 70)
    print("FAZ 2: Library Sinifi (CRUD Islemleri)")
    print("-" * 70)
    
    ktp = Library()
    
    # Kitap ekleme testleri
    print("\n[KITAP CRUD TESTLERI]")
    
    k1 = ktp.add_book("Python", "Ahmet", "111", "Yay1", 2020, 100, "Prog")
    test(k1 is not None, "add_book() kitap donduruyor")
    test(k1.book_id == 1, "Ilk kitap ID'si 1")
    test(len(ktp.books) == 1, "Kitap listeye eklendi")
    
    k2 = ktp.add_book("Java", "Mehmet", "222", "Yay2", 2021, 200, "Prog")
    test(k2.book_id == 2, "Ikinci kitap ID'si 2")
    test(len(ktp.books) == 2, "Ikinci kitap eklendi")
    
    k3 = ktp.add_book("C++", "Ayse", "333", "Yay3", 2019, 150, "Prog")
    k4 = ktp.add_book("Roman", "Can", "444", "Yay4", 2022, 250, "Edebiyat")
    test(len(ktp.books) == 4, "Toplam 4 kitap eklendi")
    
    # get_book testi
    bulunan = ktp.get_book(1)
    test(bulunan is not None, "get_book() kitap buluyor")
    test(bulunan.title == "Python", "get_book() dogru kitabi getiriyor")
    
    bulunamayan = ktp.get_book(999)
    test(bulunamayan is None, "get_book() olmayan icin None donduruyor")
    
    # update_book testi
    guncellendi = ktp.update_book(1, title="Python 3", year=2024)
    test(guncellendi == True, "update_book() True donduruyor")
    test(ktp.get_book(1).title == "Python 3", "Kitap basligi guncellendi")
    test(ktp.get_book(1).year == 2024, "Kitap yili guncellendi")
    
    # list_books testi
    tum_kitaplar = ktp.list_books()
    test(len(tum_kitaplar) == 4, "list_books() tum kitaplari donduruyor")
    
    # Uye ekleme testleri
    print("\n[UYE CRUD TESTLERI]")
    
    u1 = ktp.add_member("Ali", "111", "ali@test.com", "Ankara")
    test(u1 is not None, "add_member() uye donduruyor")
    test(u1.member_id == 1, "Ilk uye ID'si 1")
    test(len(ktp.members) == 1, "Uye listeye eklendi")
    
    u2 = ktp.add_member("Veli", "222", "veli@test.com", "Istanbul")
    test(u2.member_id == 2, "Ikinci uye ID'si 2")
    
    # get_member testi
    bulunan_uye = ktp.get_member(1)
    test(bulunan_uye is not None, "get_member() uye buluyor")
    test(bulunan_uye.name == "Ali", "get_member() dogru uyeyi getiriyor")
    
    # update_member testi
    ktp.update_member(1, phone="999")
    test(ktp.get_member(1).phone == "999", "Uye telefonu guncellendi")
    
    # Odunc islemleri
    print("\n[ODUNC ISLEMLERI TESTLERI]")
    
    odunc_sonuc = ktp.borrow_book(1, 1)  # Ali, Python kitabini
    test(odunc_sonuc == True, "borrow_book() basarili")
    test(ktp.get_book(1).available == False, "Kitap artik musait degil")
    test(1 in ktp.get_member(1).borrowed_books, "Kitap uyenin listesinde")
    
    # Ayni kitabi tekrar odunc verme denemesi
    tekrar = ktp.borrow_book(2, 1)
    test(tekrar == False, "Odunc verilmis kitap tekrar verilemez")
    
    # Iade islemi
    iade_sonuc = ktp.return_book(1, 1)
    test(iade_sonuc == True, "return_book() basarili")
    test(ktp.get_book(1).available == True, "Kitap tekrar musait")
    test(1 not in ktp.get_member(1).borrowed_books, "Kitap uye listesinden cikti")
    
    # Silme islemleri
    print("\n[SILME ISLEMLERI TESTLERI]")
    
    # Once odunc ver, sonra silmeyi dene
    ktp.borrow_book(1, 2)  # Ali, Java kitabini odunc aldi
    silme_basarisiz = ktp.remove_book(2)
    test(silme_basarisiz == False, "Odunc verilmis kitap silinemez")
    
    # Musait kitabi sil
    silme_basarili = ktp.remove_book(3)  # C++ kitabini sil
    test(silme_basarili == True, "Musait kitap silindi")
    test(len(ktp.books) == 3, "Kitap sayisi azaldi")
    
    # Odunclu uyeyi silmeyi dene
    uye_silinemez = ktp.remove_member(1)
    test(uye_silinemez == False, "Odunclu uye silinemez")
    
    # Oduncsuz uyeyi sil
    uye_silindi = ktp.remove_member(2)
    test(uye_silindi == True, "Oduncsuz uye silindi")
    
    # ==================== FAZ 3 TESTLERI ====================
    print("\n" + "-" * 70)
    print("FAZ 3: Arama Fonksiyonlari")
    print("-" * 70)
    
    # Yeni kutuphane olustur
    ktp2 = Library()
    ktp2.add_book("Python Programlama", "Ahmet Yilmaz", "111", "Yay", 2020, 100, "Programlama")
    ktp2.add_book("Java Temelleri", "Ahmet Kaya", "222", "Yay", 2021, 200, "Programlama")
    ktp2.add_book("Roman Kitabi", "Mehmet Can", "333", "Yay", 2022, 300, "Roman")
    
    print("\n[ARAMA TESTLERI]")
    
    # Basliga gore arama
    sonuc = ktp2.search_by_title("Python")
    test(len(sonuc) == 1, "search_by_title() dogru sonuc sayisi")
    test(sonuc[0].title == "Python Programlama", "search_by_title() dogru kitap")
    
    # Kismi eslesme
    sonuc2 = ktp2.search_by_title("ama")  # Programlama icinde
    test(len(sonuc2) == 1, "search_by_title() kismi eslesme calisiyor")
    
    # Yazara gore arama
    sonuc3 = ktp2.search_by_author("Ahmet")
    test(len(sonuc3) == 2, "search_by_author() dogru sonuc sayisi")
    
    # Kategoriye gore arama
    sonuc4 = ktp2.search_by_category("Programlama")
    test(len(sonuc4) == 2, "search_by_category() dogru sonuc sayisi")
    
    sonuc5 = ktp2.search_by_category("Roman")
    test(len(sonuc5) == 1, "search_by_category() tek sonuc")
    
    # ISBN'e gore arama
    sonuc6 = ktp2.search_by_isbn("222")
    test(sonuc6 is not None, "search_by_isbn() kitap buluyor")
    test(sonuc6.title == "Java Temelleri", "search_by_isbn() dogru kitap")
    
    sonuc7 = ktp2.search_by_isbn("999")
    test(sonuc7 is None, "search_by_isbn() olmayan icin None")
    
    # ==================== FAZ 4 TESTLERI ====================
    print("\n" + "-" * 70)
    print("FAZ 4: Siralama Algoritmalari")
    print("-" * 70)
    
    # Test verileri
    ktp3 = Library()
    ktp3.add_book("Zebra", "Yazar3", "111", "Yay", 2022, 300, "A")
    ktp3.add_book("Alfa", "Yazar1", "222", "Yay", 2020, 100, "B")
    ktp3.add_book("Beta", "Yazar2", "333", "Yay", 2021, 200, "C")
    
    print("\n[QUICK SORT TESTLERI]")
    
    # Basliga gore artan
    sirali = quick_sort(ktp3.books, key="title")
    test(sirali[0].title == "Alfa", "Quick Sort baslik artan - ilk eleman")
    test(sirali[2].title == "Zebra", "Quick Sort baslik artan - son eleman")
    
    # Basliga gore azalan
    sirali_azalan = quick_sort(ktp3.books, key="title", reverse=True)
    test(sirali_azalan[0].title == "Zebra", "Quick Sort baslik azalan - ilk")
    test(sirali_azalan[2].title == "Alfa", "Quick Sort baslik azalan - son")
    
    # Yila gore
    sirali_yil = quick_sort(ktp3.books, key="year")
    test(sirali_yil[0].year == 2020, "Quick Sort yil artan")
    
    # Sayfa sayisina gore
    sirali_sayfa = quick_sort(ktp3.books, key="page_count", reverse=True)
    test(sirali_sayfa[0].page_count == 300, "Quick Sort sayfa azalan")
    
    print("\n[BUBBLE SORT TESTLERI]")
    
    # Basliga gore artan
    sirali_b = bubble_sort(ktp3.books, key="title")
    test(sirali_b[0].title == "Alfa", "Bubble Sort baslik artan - ilk")
    test(sirali_b[2].title == "Zebra", "Bubble Sort baslik artan - son")
    
    # Yazara gore
    sirali_yazar = bubble_sort(ktp3.books, key="author")
    test(sirali_yazar[0].author == "Yazar1", "Bubble Sort yazar artan")
    
    # Orijinal liste degismedi mi?
    test(ktp3.books[0].title == "Zebra", "Orijinal liste degismedi")
    
    # ==================== FAZ 5 TESTLERI ====================
    print("\n" + "-" * 70)
    print("FAZ 5: Dosya Islemleri")
    print("-" * 70)
    
    print("\n[JSON ISLEMLERI TESTLERI]")
    
    # Kaydetme
    test_dosya = "test_veriler_gecici.json"
    
    ktp4 = Library()
    ktp4.add_book("Test Kitap", "Test Yazar", "123", "Yay", 2024, 100, "Test")
    ktp4.add_member("Test Uye", "555", "test@test.com", "Test Adres")
    ktp4.borrow_book(1, 1)
    
    kayit_sonuc = save_to_json(ktp4, test_dosya)
    test(kayit_sonuc == True, "save_to_json() basarili")
    test(os.path.exists(test_dosya), "JSON dosyasi olusturuldu")
    
    # Yukleme
    yuklenen = load_from_json(test_dosya)
    test(yuklenen is not None, "load_from_json() kutuphane donduruyor")
    test(len(yuklenen.books) == 1, "Kitaplar yuklendi")
    test(len(yuklenen.members) == 1, "Uyeler yuklendi")
    test(yuklenen.books[0].title == "Test Kitap", "Kitap verisi dogru")
    test(yuklenen.members[0].name == "Test Uye", "Uye verisi dogru")
    test(yuklenen.books[0].available == False, "Odunc durumu korundu")
    test(1 in yuklenen.members[0].borrowed_books, "Odunc listesi korundu")
    
    # Olmayan dosya yukleme
    bos_ktp = load_from_json("olmayan_dosya_12345.json")
    test(bos_ktp is not None, "Olmayan dosya icin bos kutuphane")
    test(len(bos_ktp.books) == 0, "Bos kutuphane 0 kitap")
    
    # Test dosyasini sil
    if os.path.exists(test_dosya):
        os.remove(test_dosya)
        test(not os.path.exists(test_dosya), "Test dosyasi temizlendi")
    
    # ==================== FAZ 6 TESTLERI ====================
    print("\n" + "-" * 70)
    print("FAZ 6: Flask Web Arayuzu")
    print("-" * 70)
    
    print("\n[FLASK KONTROLLERI]")
    
    if FLASK_AVAILABLE:
        test(True, "Flask modulu yuklu")
        
        # Flask uygulamasini import et
        try:
            from kutuphane import app
            test(app is not None, "Flask app objesi mevcut")
            
            # Route'lari kontrol et
            rules = [rule.rule for rule in app.url_map.iter_rules()]
            test('/' in rules, "Ana sayfa route'u (/) mevcut")
            test('/kitaplar' in rules, "/kitaplar route'u mevcut")
            test('/uyeler' in rules, "/uyeler route'u mevcut")
            test('/odunc' in rules, "/odunc route'u mevcut")
            test('/arama' in rules, "/arama route'u mevcut")
            test('/kitap-ekle' in rules, "/kitap-ekle route'u mevcut")
            test('/uye-ekle' in rules, "/uye-ekle route'u mevcut")
            
        except Exception as e:
            test(False, f"Flask app kontrolu: {e}")
    else:
        print("  [INFO] Flask yuklu degil (opsiyonel ozellik)")
        test(True, "Flask olmadan da calisiyor (terminal modu)")
    
    # Templates kontrolu
    templates_var = os.path.exists("templates") and os.path.isdir("templates")
    if templates_var:
        test(True, "templates klasoru mevcut")
        
        template_dosyalari = ["index.html", "kitaplar.html", "uyeler.html", 
                             "odunc.html", "arama.html", "kitap_ekle.html", "uye_ekle.html"]
        for dosya in template_dosyalari:
            dosya_yolu = os.path.join("templates", dosya)
            test(os.path.exists(dosya_yolu), f"{dosya} mevcut")
    else:
        print("  [INFO] templates klasoru bulunamadi")
    
    # ==================== SONUC ====================
    print("\n" + "=" * 70)
    print("TEST SONUCLARI")
    print("=" * 70)
    
    toplam = passed + failed
    basari_orani = (passed / toplam * 100) if toplam > 0 else 0
    
    print(f"\n  Basarili: {passed}")
    print(f"  Basarisiz: {failed}")
    print(f"  Toplam: {toplam}")
    print(f"  Basari Orani: %{basari_orani:.1f}")
    
    if failed == 0:
        print("\n  TUM TESTLER BASARILI!")
    else:
        print(f"\n  {failed} test basarisiz!")
    
    print("\n" + "=" * 70)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
