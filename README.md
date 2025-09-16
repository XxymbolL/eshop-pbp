# Tugas PBP : Football Shop - Alpha shoes
[link to PWS](https://rifqy-pradipta-alphashoes.pbp.cs.ui.ac.id/)

---
<details>
<Summary><b>Tugas 2</b></Summary>

## checklist:
- [x] Membuat sebuah proyek Django baru.
	- Buat folder baru dan python venv dengan install seluruh requirement untuk setup Django.
	- Buat project baru: `django-admin startproject alpha_shoes`.
- [x] Membuat aplikasi dengan nama main pada proyek tersebut.
	- Buat aplikasi main dengan: `python manage.py startapp main`.
	- Tambahkan `main` pada **settings.py**, spesifiknya pada ==INSTALLED_APPS== agar main dikenali oleh Django.
- [x] Melakukan routing pada proyek agar dapat menjalankan aplikasi main.
	- Buat folder template serta file **main.html** di dalamnya, yang akan menjadi tampilan utama, untuk sekarang hanya display nama toko dan identitas, dalam bentuk placeholder.
	- Data yang akan ditampilkan pada main dibuat pada **views.py**, yang akan me-render **main.html** placeholder dengan value yang dimiliki views.
	- Routing program melalui **urls.py** dengan import **main.views** dan hook **main.urls**(file urls.py pada `main/`) ke **urls.py** pada direktori proyek `alpha_shoes/`.
- [x] Membuat model pada aplikasi main dengan nama Product dan memiliki atribut wajib sebagai berikut.

``` 
- name sebagai nama item dengan tipe CharField.
- price sebagai harga item dengan tipe IntegerField.
- description sebagai deskripsi item dengan tipe TextField.
- thumbnail sebagai gambar item dengan tipe URLField.
- category sebagai kategori item dengan tipe CharField.
- is_featured sebagai status unggulan item dengan tipe BooleanField
```

- pada models, saya menggunakan:
    - id(sebagai primary key database), 
    - name sebagai CharField, 
    - price sebagai PositiveIntegerField, 
    - description sebagai TextField, 
    - thumbnail sebagai URLField, 
    - size sebagai CharField, dan 
    - stock sebagai PositiveIntegerField.

- karena Shoe dapat memiliki berbagai size, saya menggunakan class tambahan bernama ShoeSize yang menjadi database kedua untuk melakukan store terhadap masing-masing dari size dan stok tiap sepatu. Berikut adalah model yang saya buat:


```python
class Shoes(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    price = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True)
    thumbnail = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

    @property
    def total_stock(self):
        return sum(s.stock for s in self.sizes.all())

    @property
    def is_available(self):
        return self.total_stock > 0

    def decrease_stock(self, size, amount=1):
        size_row = self.sizes.get(size=size)
        if amount < 0:
            raise ValueError("tidak dapa negatif")
        if size_row.stock < amount:
            raise ValueError("stock tidak cukup")
        size_row.stock -= amount
        size_row.save()


class ShoeSize(models.Model):
    shoes = models.ForeignKey(Shoes, on_delete=models.CASCADE, related_name='sizes')
    size = models.CharField(max_length=2, choices=SIZE_CHOICES)
    stock = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('shoes', 'size')
```

- [x] Membuat sebuah fungsi pada views.py untuk dikembalikan ke dalam sebuah template HTML yang menampilkan nama aplikasi serta nama dan kelas kamu.
	- hal ini sudah saya lakukan bersamaan dengan routing diatas untuk mempersingkat waktu.
- [x] Membuat sebuah routing pada urls.py aplikasi main untuk memetakan fungsi yang telah dibuat pada views.py.
	-  hal ini juga sudah saya lakukan bersamaan dengan routing diatas untuk mempersingkat waktu.
- [x] Melakukan deployment ke PWS terhadap aplikasi yang sudah dibuat sehingga nantinya dapat diakses oleh teman-temanmu melalui Internet.
	- push project ke git PWS.
	- karena segala credential tidak dimasukkan dalam push, maka harus dilakukan setup environs pada PWS dengan credential-credential yang diperlukan.
	- PWS akan runserver dengan sendirinya.
- [x] Membuat sebuah README.md yang berisi tautan menuju aplikasi PWS yang sudah di-deploy, serta jawaban dari beberapa pertanyaan berikut.
---
##  Bagan  penjelasan mengenai kaitan antara urls.py, views.py, models.py, dan berkas html.
![](https://miro.medium.com/v2/resize:fit:1100/format:webp/1*K-o5Vn65A7PJZTSrlsm2rQ.jpeg)

*gambar diambil dari. [^1]*
keempat file tersebut sangat berkaitan karena:
- `urls.py` (proyek & app): Mencocokkan URL → menentukan view mana dipanggil.
- `views.py`: Menerima request, (opsional) ambil data di `models.py`, lalu panggil **template** dengan context → print `HttpResponse`.
- `models.py`: Sumber data, desain tabel dan isinya(variabel) yang akan dipakai **view**.
- `templates/*.html`: Presentasi, menampilkan data yang dikirim **view** ke user dalam bentuk HTML.
Keempatnya terhubung menjadi: **URL → View → Model → Template → Response**.

---
## Peran settings.py dalam proyek Django
`settings.py` adalah **pusat konfigurasi proyek Django**. Semua pengaturan, dimulai dari database, lokasi aplikasi, lokasi template, hingga security disatukan dalam satu tempat, sehingga proyek bisa berjalan konsisten dan mudah diatur.
## Cara Kerja Migrasi Database di Django

Migrasi digunakan untuk menjaga sinkronisasi antara **models.py** dan **database**.
1. Buat/Ubah model di `models.py`.
2. Jalankan:
    ```bash
    python manage.py makemigrations
    ```
    Django membuat **file migrasi**.
3. Jalankan:
    ```bash
    python manage.py migrate
    ```
    Django mengeksekusi file migrasi, membuat atau mengubah tabel sesuai model.

Dengan migrasi, perubahan struktur database bisa **dilacak, dikelola, dan dijalankan otomatis** tanpa harus menulis kembali database secara manual.

---
## Kenapa Django?
Karena Django mencakup *FullStack* development sehingga dapat mengatur *FrontEnd* dan *BackEnd* secara mudah untuk pemula. Dengan menggunakan ==python==, Django menjadi alternatif yang banyak digunakan untuk pemula yang baru mempelajari dapat mengikuti dengan mudah disertai dengan dokumentasi yang lengkap.

#### Apakah ada feedback untuk asisten dosen tutorial 1 yang telah kamu kerjakan sebelumnya?
Keren :0, terimakasih sudah memberikan tutorial lengkap.
![](yeah.gif)


</details>

---
[^1]:https://medium.com/@developerstacks/django-request-response-cycle-7165167f54c5