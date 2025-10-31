# Stack Overflow Developer Survey - Maaş Tahmini ve Kümeleme Analizi

Bu proje, Stack Overflow Developer Survey 2024 verileri kullanılarak geliştiricilerin maaş tahminleri ve kümeleme analizi yapan bir makine öğrenmesi uygulamasıdır.

## 🎯 Proje Özellikleri

### 1. Maaş Tahmin Modeli
- **Kullanılan Algoritmalar:**
  - Linear Regression
  - Decision Tree Regressor
  - Random Forest Regressor
  - Gradient Boosting Machine (GBM)
- **En İyi Model:** Decision Tree Regressor
- **Değerlendirme Metrikleri:** R², MAPE, MAE, MSE

### 2. K-Means Kümeleme Analizi
- **Elbow Yöntemi** ile optimal küme sayısı belirleme
- **Silhouette Skoru** ile küme kalitesi değerlendirmesi
- **Analiz Edilen Faktörler:**
  - Kullanılan ve istenen programlama dilleri
  - Kod öğrenme kaynakları
  - Geliştirici tipleri
  - Ülke ve deneyim seviyesi

### 3. Web Uygulaması (Streamlit)
- **Ana Sayfa:** Proje özeti ve genel bakış
- **Veri Keşfi:** İstatistiksel analizler ve interaktif görselleştirmeler
  - ANOVA testleri
  - Korelasyon analizleri
  - Dağılım analizleri (Q-Q plot, histogram)
  - Violin ve box plot görselleştirmeleri
- **Maaş Tahmini:** Gerçek zamanlı tahmin ve karşılaştırmalar
  - Deneyim projeksiyonu
  - Ülke karşılaştırmaları
  - Model performans metrikleri
- **Kümeleme Analizi:** K-Means sonuçları ve küme profilleri
  - Elbow ve Silhouette grafikleri
  - Küme karakteristikleri
  - Dil kullanım ısı haritaları

## 📊 Kümeleme Bulguları

Analiz sonucunda **2 ana geliştirici grubu** tespit edildi:

**Küme 0 (85.8%):**
- Web geliştirme odaklı (JavaScript, HTML/CSS, SQL)
- Full-stack ve back-end geliştiriciler
- Ortalama deneyim: 16.4 yıl

**Küme 1 (14.2%):**
- Sistem programlama ve veri bilimi odaklı (Python, Bash, C)
- Öğrenciler ve sistem geliştiricileri
- Ortalama deneyim: 14.4 yıl

## 🛠️ Kullanılan Teknolojiler

- **Python 3.x**
- **Pandas** - Veri analizi
- **NumPy** - Sayısal hesaplamalar
- **Scikit-learn** - Makine öğrenmesi modelleri
- **Matplotlib & Seaborn** - Veri görselleştirme
- **Streamlit** - Web uygulaması

## 📁 Dosya Yapısı

```
MLAPP_3/
├── SalaryPrediction.ipynb    # Ana analiz notebook'u
├── app.py                      # Streamlit ana uygulaması
├── predict_page.py             # Maaş tahmin sayfası
├── explore_page.py             # Veri keşif sayfası
├── clustering_page.py          # Kümeleme analizi sayfası
├── requirements.txt            # Gerekli Python paketleri
├── saved_steps.pkl             # Eğitilmiş maaş tahmin modeli
├── clustering_model.pkl        # Kümeleme modeli (opsiyonel)
└── README.md                   # Proje dökümantasyonu
```

## 🚀 Kurulum ve Çalıştırma

### Gereksinimler
```bash
pip install -r requirements.txt
```

veya manuel olarak:
```bash
pip install streamlit pandas numpy scikit-learn matplotlib seaborn scipy
```

### Notebook'u Çalıştırma
```bash
jupyter notebook SalaryPrediction.ipynb
```

### Web Uygulamasını Çalıştırma
```bash
streamlit run app.py
```

## 📈 Model Performansı

### Maaş Tahmin Modeli
- Decision Tree Regressor en yüksek performansı gösterdi
- Modeller karşılaştırmalı olarak R², MAPE, MAE ve MSE metrikleriyle değerlendirildi

### Kümeleme Modeli
- Elbow yöntemi: k = 4 önerdi
- Silhouette skoru: k = 2 önerdi
- Final karar: k = 2 (daha net küme ayrımı)

## 📊 Görselleştirmeler ve Özellikler

### Analiz ve Görselleştirmeler:
- **Elbow grafiği** - Optimal k belirleme için WCSS analizi
- **Silhouette skoru grafikleri** - Küme kalitesi değerlendirmesi
- **PCA 2D görselleştirme** - Kümelerin düşük boyutlu temsili
- **Isı haritaları** - Programlama dili kullanım oranları
- **Violin/Box plotlar** - Maaş dağılım analizleri
- **Scatter plotlar** - Deneyim vs maaş ilişkisi
- **ANOVA testleri** - İstatistiksel anlamlılık testleri
- **Q-Q plotlar** - Normallik testleri

### Streamlit Arayüzü:
- 🎨 Modern ve profesyonel tasarım
- 📱 Responsive layout
- 🎯 İnteraktif görselleştirmeler
- 📊 Gerçek zamanlı metrikler
- 💾 CSV export özelliği
- 🔬 İleri düzey istatistiksel analizler

## 💡 Kullanım Senaryoları

1. **İşe Alım:** Her kümenin özelliklerine göre özelleştirilmiş iş ilanları
2. **Eğitim:** Kümelere özel eğitim programları
3. **Teknoloji Seçimi:** Hangi teknolojilerin hangi gruplarda popüler olduğunu anlama
4. **Pazarlama:** Hedef kitleye özel pazarlama stratejileri

## 📝 Veri Seti

Stack Overflow Developer Survey 2024 verileri kullanılmıştır.
- **Not:** `survey_results_public.csv` dosyası boyutu nedeniyle GitHub'a yüklenmemiştir.

## 👨‍💻 Geliştirici

Bedirhan Örseoğlu

## 📄 Lisans

Bu proje eğitim amaçlı geliştirilmiştir.

---

⭐ Projeyi beğendiyseniz yıldız vermeyi unutmayın!

