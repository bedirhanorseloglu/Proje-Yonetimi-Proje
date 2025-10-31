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
- **Tahmin Sayfası:** Kullanıcı bilgilerine göre maaş tahmini
- **Keşif Sayfası:** Veri görselleştirme ve istatistikler

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
├── predict_page.py             # Tahmin sayfası
├── explore_page.py             # Keşif sayfası
├── saved_steps.pkl             # Eğitilmiş maaş tahmin modeli
├── clustering_model.pkl        # Kümeleme modeli
└── README.md                   # Proje dökümantasyonu
```

## 🚀 Kurulum ve Çalıştırma

### Gereksinimler
```bash
pip install pandas numpy scikit-learn matplotlib seaborn streamlit
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

## 📊 Görselleştirmeler

Proje şunları içerir:
- Elbow grafiği (optimal k belirleme)
- Silhouette skoru grafikleri
- PCA ile 2D küme görselleştirmesi
- Programlama dili kullanım ısı haritası
- Detaylı küme analiz raporları

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

