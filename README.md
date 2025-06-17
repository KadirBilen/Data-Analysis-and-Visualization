# Veri Analizi Platformu

Flask tabanlı kapsamlı veri analizi ve görselleştirme web uygulaması.

## 🚀 Özellikler

- **Dosya Yükleme**: CSV, Excel ve JSON dosyalarını yükleme
- **Manuel Veri Girişi**: Verilerinizi doğrudan platforma girme
- **Kapsamlı Analiz**: İstatistiksel özetler, eksik değer analizi, korelasyon matrisi
- **İnteraktif Görselleştirme**: Plotly ile dinamik grafikler
- **Responsive Tasarım**: Mobil ve masaüstü uyumlu arayüz
- **Örnek Veri Setleri**: Test için hazır veri setleri

## 📋 Gereksinimler

- Python 3.8+
- Flask 3.0+
- pandas, numpy, matplotlib, seaborn, plotly
- Bootstrap 5 (CDN üzerinden)

## 🛠️ Kurulum

1. **Projeyi klonlayın:**
   \`\`\`bash
   git clone <repository-url>
   cd flask-data-analysis
   \`\`\`

2. **Sanal ortam oluşturun:**
   \`\`\`bash
   python -m venv venv
   source venv/bin/activate # Linux/Mac

# veya

venv\Scripts\activate # Windows
\`\`\`

3. **Gerekli paketleri yükleyin:**
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

4. **Uygulamayı başlatın:**
   \`\`\`bash
   python run.py
   \`\`\`

5. **Tarayıcınızda açın:**
   \`\`\`
   http://localhost:5000
   \`\`\`

## 📁 Proje Yapısı

\`\`\`
flask-data-analysis/
├── app.py # Ana Flask uygulaması
├── run.py # Uygulama başlatıcı
├── requirements.txt # Python bağımlılıkları
├── README.md # Proje dokümantasyonu
├── utils/ # Yardımcı modüller
│ ├── data_processor.py # Veri işleme fonksiyonları
│ └── visualizer.py # Görselleştirme fonksiyonları
├── templates/ # HTML şablonları
│ ├── base.html
│ ├── index.html
│ ├── upload.html
│ ├── manual_input.html
│ └── results.html
├── static/ # Statik dosyalar
│ ├── css/
│ │ └── style.css
│ └── js/
│ └── main.js
├── scripts/ # Yardımcı scriptler
│ ├── setup_database.py
│ └── sample_data_generator.py
├── uploads/ # Yüklenen dosyalar
└── sample_data/ # Örnek veri setleri
\`\`\`

## 🎯 Kullanım

### 1. Dosya Yükleme

- Ana sayfadan "Dosya Yükle" seçeneğini tıklayın
- CSV, Excel (.xlsx, .xls) veya JSON dosyanızı seçin
- "Analiz Et" butonuna tıklayın

### 2. Manuel Veri Girişi

- Ana sayfadan "Manuel Giriş" seçeneğini tıklayın
- Veri formatını seçin (CSV veya JSON)
- Verilerinizi metin alanına yapıştırın
- "Analiz Et" butonuna tıklayın

### 3. Analiz Sonuçları

Analiz tamamlandıktan sonra şunları görebilirsiniz:

- **Temel Bilgiler**: Satır/sütun sayısı, bellek kullanımı
- **Veri Önizleme**: İlk birkaç satır
- **Sütun Bilgileri**: Veri tipleri ve eksik değerler
- **İstatistiksel Özet**: Sayısal sütunlar için istatistikler
- **Görselleştirme**: İnteraktif grafikler

### 4. Görselleştirme Seçenekleri

- Histogram
- Scatter Plot
- Line Plot
- Bar Chart
- Pie Chart
- Box Plot
- Heatmap/Korelasyon Matrisi

## 📊 Desteklenen Dosya Formatları

### CSV Örneği:

\`\`\`csv
isim,yaş,şehir,maaş
Ali,25,İstanbul,5000
Ayşe,30,Ankara,6000
Mehmet,35,İzmir,7000
\`\`\`

### JSON Örneği:

\`\`\`json
[
{"isim": "Ali", "yaş": 25, "şehir": "İstanbul", "maaş": 5000},
{"isim": "Ayşe", "yaş": 30, "şehir": "Ankara", "maaş": 6000}
]
\`\`\`

## 🔧 Geliştirme

### Yeni Analiz Fonksiyonu Ekleme

`utils/data_processor.py` dosyasında `DataProcessor` sınıfına yeni metodlar ekleyebilirsiniz.

### Yeni Görselleştirme Türü Ekleme

`utils/visualizer.py` dosyasında `Visualizer` sınıfına yeni grafik metodları ekleyebilirsiniz.

### Veritabanı İşlemleri

SQLite veritabanı kullanılmaktadır. `scripts/setup_database.py` ile veritabanını yeniden oluşturabilirsiniz.

## 🐛 Sorun Giderme

### Yaygın Hatalar:

1. **ModuleNotFoundError**: `pip install -r requirements.txt` komutunu çalıştırın
2. **Port zaten kullanımda**: `run.py` dosyasında port numarasını değiştirin
3. **Dosya yükleme hatası**: Dosya boyutunun 16MB'dan küçük olduğundan emin olun
4. **Grafik görünmüyor**: İnternet bağlantınızı kontrol edin (Plotly CDN gerekli)

## 📈 Performans İpuçları

- Büyük dosyalar için (>1GB) chunk okuma kullanın
- Çok sütunlu veriler için sadece gerekli sütunları analiz edin
- Görselleştirme için veri örneklemesi yapın

## 🤝 Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/yeni-ozellik`)
3. Değişikliklerinizi commit edin (`git commit -am 'Yeni özellik eklendi'`)
4. Branch'inizi push edin (`git push origin feature/yeni-ozellik`)
5. Pull Request oluşturun

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## 📞 İletişim

Sorularınız için issue açabilir veya e-posta gönderebilirsiniz.

---

**Not**: Bu platform eğitim ve demo amaçlı geliştirilmiştir. Üretim ortamında kullanmadan önce güvenlik önlemlerini gözden geçirin.
