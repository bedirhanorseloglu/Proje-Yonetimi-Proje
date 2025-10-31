import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def show_clustering_page():
    st.title("🔬 K-Means Kümeleme Analizi")
    st.markdown("### Geliştirici Profili Segmentasyonu")
    
    st.markdown("""
    <div style='background-color: #f0fdf4; padding: 1.5rem; border-radius: 10px; margin-bottom: 2rem;'>
        <p style='margin: 0; font-size: 1rem;'>
        Bu sayfa, <strong>K-Means kümeleme algoritması</strong> kullanarak geliştiricileri 
        profil özelliklerine göre gruplara ayırır. <strong>Elbow yöntemi</strong> ile optimal 
        küme sayısı belirlenmiş ve <strong>19,955 geliştirici</strong> analiz edilmiştir.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Genel Bilgiler
    st.markdown("## 📊 Analiz Özeti")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Analiz Edilen Kişi",
            "19,955",
            delta="Tam veri seti"
        )
    
    with col2:
        st.metric(
            "Optimal Küme Sayısı",
            "2",
            delta="Elbow + Silhouette"
        )
    
    with col3:
        st.metric(
            "Özellik Sayısı",
            "131",
            delta="One-hot encoded"
        )
    
    with col4:
        st.metric(
            "Silhouette Skoru",
            "0.125",
            delta="Küme kalitesi"
        )
    
    st.markdown("---")
    
    # Metodoloji
    with st.expander("🔍 Kullanılan Metodoloji"):
        st.markdown("""
        ### Analiz Süreci:
        
        1. **Veri Hazırlama**
           - Programlama dilleri (kullanılan ve istenen)
           - Kod öğrenme kaynakları
           - Geliştirici tipleri
           - Ülke ve deneyim bilgisi
        
        2. **Özellik Mühendisliği**
           - Multi-label encoding
           - One-hot encoding
           - Standardization (Z-score normalization)
        
        3. **Optimal k Belirleme**
           - Elbow yöntemi (WCSS analizi)
           - Silhouette skoru analizi
           - 2-10 arası k değerleri test edildi
        
        4. **Model Eğitimi**
           - K-Means algoritması
           - k-means++ başlatma
           - 10 farklı başlangıç noktası
        
        5. **Değerlendirme**
           - Silhouette analizi
           - PCA ile görselleştirme
           - Küme profil analizi
        """)
    
    st.markdown("---")
    
    # Elbow Grafiği
    st.markdown("## 📈 Elbow Yöntemi ile Optimal K Belirleme")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### WCSS (Within-Cluster Sum of Squares)")
        
        # Elbow verileri (notebook'tan)
        k_range = list(range(2, 11))
        wcss = [621316.50, 604047.62, 592657.27, 585460.81, 579453.29, 
                575053.16, 567285.17, 563000.18, 556911.49]
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(k_range, wcss, marker='o', linewidth=3, markersize=10, 
               color='#3b82f6', label='WCSS')
        
        # Optimal k'yi işaretle
        ax.axvline(x=4, color='r', linestyle='--', linewidth=2, 
                  label='Elbow Noktası (k=4)', alpha=0.7)
        
        ax.set_xlabel('Küme Sayısı (k)', fontsize=12, fontweight='bold')
        ax.set_ylabel('WCSS', fontsize=12, fontweight='bold')
        ax.set_title('Elbow Yöntemi', fontsize=14, fontweight='bold', pad=20)
        ax.legend(fontsize=11)
        ax.grid(True, alpha=0.3)
        ax.set_xticks(k_range)
        
        # Değerleri göster
        for k, w in zip(k_range, wcss):
            ax.annotate(f'{w:,.0f}', xy=(k, w), xytext=(0, 10), 
                       textcoords='offset points', ha='center', fontsize=8)
        
        st.pyplot(fig)
        plt.close()
    
    with col2:
        st.markdown("### Silhouette Skoru")
        
        # Silhouette skorları (notebook'tan)
        silhouette_scores = [0.1250, 0.0349, 0.0074, 0.0061, -0.0006, 
                            0.0193, 0.0077, -0.0102, 0.0093]
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(k_range, silhouette_scores, marker='s', linewidth=3, 
               markersize=10, color='#10b981', label='Silhouette Score')
        
        # En yüksek skoru işaretle
        ax.axvline(x=2, color='r', linestyle='--', linewidth=2, 
                  label='En Yüksek Skor (k=2)', alpha=0.7)
        ax.axhline(y=0, color='gray', linestyle='-', linewidth=1, alpha=0.5)
        
        ax.set_xlabel('Küme Sayısı (k)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Silhouette Skoru', fontsize=12, fontweight='bold')
        ax.set_title('Silhouette Analizi', fontsize=14, fontweight='bold', pad=20)
        ax.legend(fontsize=11)
        ax.grid(True, alpha=0.3)
        ax.set_xticks(k_range)
        
        # Değerleri göster
        for k, score in zip(k_range, silhouette_scores):
            ax.annotate(f'{score:.3f}', xy=(k, score), xytext=(0, 10), 
                       textcoords='offset points', ha='center', fontsize=8)
        
        st.pyplot(fig)
        plt.close()
    
    st.info("""
    **Sonuç:** İki yöntem farklı k değerleri önerdi:
    - Elbow yöntemi: k=4
    - Silhouette skoru: k=2
    
    **Seçilen:** k=2 (daha net küme ayrımı ve yüksek Silhouette skoru)
    """)
    
    st.markdown("---")
    
    # Küme Profilleri
    st.markdown("## 👥 Küme Profilleri")
    
    tabs = st.tabs(["📊 Genel Bakış", "💻 Küme 0", "🐍 Küme 1"])
    
    with tabs[0]:
        st.markdown("### Küme Karşılaştırması")
        
        # Karşılaştırma tablosu
        comparison_data = {
            "Özellik": ["Kişi Sayısı", "Yüzde", "Ortalama Deneyim", "En Popüler Ülke", 
                       "Top 3 Dil", "Profil Tipi"],
            "Küme 0 (Web Geliştiriciler)": [
                "17,121", "85.8%", "16.4 yıl", "ABD",
                "JavaScript, HTML/CSS, SQL", "Full-stack, Back-end"
            ],
            "Küme 1 (Sistem & Veri Bilimi)": [
                "2,834", "14.2%", "14.4 yıl", "ABD",
                "Python, Bash, C", "Öğrenci, Sistem Dev."
            ]
        }
        
        st.table(pd.DataFrame(comparison_data))
        
        # Pasta grafik - Dağılım
        st.markdown("### Küme Dağılımı")
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        sizes = [85.8, 14.2]
        colors = ['#3b82f6', '#10b981']
        explode = (0.05, 0)
        
        wedges, texts, autotexts = ax.pie(
            sizes, 
            explode=explode,
            labels=['Küme 0\n(Web Dev)', 'Küme 1\n(Sistem & DS)'],
            colors=colors,
            autopct='%1.1f%%',
            startangle=90,
            textprops={'fontsize': 12, 'fontweight': 'bold'}
        )
        
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(14)
            autotext.set_fontweight('bold')
        
        ax.axis('equal')
        plt.title('Geliştirici Kümelerinin Dağılımı', 
                 fontsize=14, fontweight='bold', pad=20)
        
        st.pyplot(fig)
        plt.close()
    
    with tabs[1]:
        st.markdown("### 💻 Küme 0: Web Geliştiriciler")
        
        st.markdown("""
        <div style='background-color: #eff6ff; padding: 1.5rem; border-radius: 10px;'>
            <h4 style='color: #1e40af; margin-top: 0;'>Profil Özeti</h4>
            <p><strong>Kişi Sayısı:</strong> 17,121 (%85.8)</p>
            <p><strong>Ortalama Deneyim:</strong> 16.4 yıl</p>
            <p><strong>Karakteristik:</strong> Web teknolojileri odaklı, olgun geliştiriciler</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("###")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 💻 En Çok Kullanılan Diller (Top 10)")
            
            languages = ["JavaScript", "HTML/CSS", "SQL", "Python", "Bash/Shell", 
                        "TypeScript", "Java", "C#", "PowerShell", "C++"]
            percentages = [68.2, 63.9, 60.6, 58.9, 47.0, 46.8, 29.0, 27.8, 23.0, 19.4]
            
            fig, ax = plt.subplots(figsize=(10, 6))
            bars = ax.barh(languages, percentages, color='#3b82f6', alpha=0.7)
            ax.set_xlabel('Kullanım Oranı (%)', fontsize=11, fontweight='bold')
            ax.set_title('Programlama Dili Kullanımı', fontsize=12, fontweight='bold')
            ax.grid(axis='x', alpha=0.3)
            
            for i, (bar, val) in enumerate(zip(bars, percentages)):
                ax.text(val + 1, i, f'{val}%', va='center', fontsize=9, fontweight='bold')
            
            st.pyplot(fig)
            plt.close()
        
        with col2:
            st.markdown("#### 📚 Öğrenme Kaynakları (Top 5)")
            
            sources = ["Teknik Dok.", "Online Kaynak", "Stack Overflow", 
                      "Video", "AI Tools"]
            source_pct = [71.5, 62.0, 54.4, 51.2, 45.5]
            
            fig, ax = plt.subplots(figsize=(10, 6))
            bars = ax.barh(sources, source_pct, color='#10b981', alpha=0.7)
            ax.set_xlabel('Kullanım Oranı (%)', fontsize=11, fontweight='bold')
            ax.set_title('Kod Öğrenme Kaynakları', fontsize=12, fontweight='bold')
            ax.grid(axis='x', alpha=0.3)
            
            for i, (bar, val) in enumerate(zip(bars, source_pct)):
                ax.text(val + 1, i, f'{val}%', va='center', fontsize=9, fontweight='bold')
            
            st.pyplot(fig)
            plt.close()
        
        st.markdown("###")
        
        st.success("""
        **Küme 0 Özellikleri:**
        - 🌐 Web teknolojilerine hakimlik (JavaScript, HTML/CSS)
        - 📊 Veri tabanı bilgisi (SQL)
        - 🔄 Full-stack ve back-end ağırlıklı
        - 📚 Çeşitli öğrenme kaynaklarını kullanma
        - 🏢 Profesyonel ve deneyimli geliştirici profili
        """)
    
    with tabs[2]:
        st.markdown("### 🐍 Küme 1: Sistem & Veri Bilimi")
        
        st.markdown("""
        <div style='background-color: #f0fdf4; padding: 1.5rem; border-radius: 10px;'>
            <h4 style='color: #15803d; margin-top: 0;'>Profil Özeti</h4>
            <p><strong>Kişi Sayısı:</strong> 2,834 (%14.2)</p>
            <p><strong>Ortalama Deneyim:</strong> 14.4 yıl</p>
            <p><strong>Karakteristik:</strong> Sistem programlama ve veri bilimi odaklı</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("###")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 💻 En Çok Kullanılan Diller (Top 10)")
            
            languages_c1 = ["Python", "Bash/Shell", "C", "JavaScript", "SQL", 
                           "HTML/CSS", "C++", "Java", "R", "C#"]
            percentages_c1 = [75.3, 65.8, 42.1, 38.5, 35.2, 31.4, 28.7, 22.1, 18.5, 15.3]
            
            fig, ax = plt.subplots(figsize=(10, 6))
            bars = ax.barh(languages_c1, percentages_c1, color='#10b981', alpha=0.7)
            ax.set_xlabel('Kullanım Oranı (%)', fontsize=11, fontweight='bold')
            ax.set_title('Programlama Dili Kullanımı', fontsize=12, fontweight='bold')
            ax.grid(axis='x', alpha=0.3)
            
            for i, (bar, val) in enumerate(zip(bars, percentages_c1)):
                ax.text(val + 1, i, f'{val}%', va='center', fontsize=9, fontweight='bold')
            
            st.pyplot(fig)
            plt.close()
        
        with col2:
            st.markdown("#### 📚 Öğrenme Kaynakları (Top 5)")
            
            sources_c1 = ["Teknik Dok.", "Online Kaynak", "Stack Overflow", 
                         "Video", "AI Tools"]
            source_pct_c1 = [68.2, 58.7, 52.3, 49.8, 42.1]
            
            fig, ax = plt.subplots(figsize=(10, 6))
            bars = ax.barh(sources_c1, source_pct_c1, color='#f59e0b', alpha=0.7)
            ax.set_xlabel('Kullanım Oranı (%)', fontsize=11, fontweight='bold')
            ax.set_title('Kod Öğrenme Kaynakları', fontsize=12, fontweight='bold')
            ax.grid(axis='x', alpha=0.3)
            
            for i, (bar, val) in enumerate(zip(bars, source_pct_c1)):
                ax.text(val + 1, i, f'{val}%', va='center', fontsize=9, fontweight='bold')
            
            st.pyplot(fig)
            plt.close()
        
        st.markdown("###")
        
        st.info("""
        **Küme 1 Özellikleri:**
        - 🐍 Python ve sistem dilleri (C, Bash) dominantlığı
        - 📊 Veri bilimi ve analitik odak
        - 🎓 Öğrenci ve akademik profil
        - 🔧 Sistem seviyesi programlama
        - 🧪 Araştırma ve deneysel çalışmalar
        """)
    
    st.markdown("---")
    
    # Dil Kullanım Karşılaştırması
    st.markdown("## 🔄 Programlama Dili Karşılaştırması")
    
    # Heatmap benzeri görselleştirme
    st.markdown("### Kümelere Göre Dil Kullanım Oranları (%)")
    
    top_languages = ["JavaScript", "Python", "HTML/CSS", "SQL", "Bash/Shell", 
                    "TypeScript", "C", "Java", "C++", "C#"]
    
    cluster_0_pct = [68.2, 58.9, 63.9, 60.6, 47.0, 46.8, 12.5, 29.0, 19.4, 27.8]
    cluster_1_pct = [38.5, 75.3, 31.4, 35.2, 65.8, 15.2, 42.1, 22.1, 28.7, 15.3]
    
    data = np.array([cluster_0_pct, cluster_1_pct])
    
    fig, ax = plt.subplots(figsize=(14, 5))
    
    im = ax.imshow(data, cmap='YlOrRd', aspect='auto')
    
    ax.set_xticks(np.arange(len(top_languages)))
    ax.set_yticks(np.arange(2))
    ax.set_xticklabels(top_languages)
    ax.set_yticklabels(['Küme 0 (Web Dev)', 'Küme 1 (Sistem & DS)'])
    
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
    
    # Değerleri hücrelere yazalım
    for i in range(2):
        for j in range(len(top_languages)):
            text = ax.text(j, i, f'{data[i, j]:.1f}%',
                          ha="center", va="center", color="white", 
                          fontweight='bold', fontsize=11)
    
    ax.set_title('Kümelere Göre Programlama Dili Kullanım Isı Haritası', 
                fontsize=14, fontweight='bold', pad=20)
    
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('Kullanım Yüzdesi (%)', rotation=270, labelpad=20, fontweight='bold')
    
    st.pyplot(fig)
    plt.close()
    
    st.markdown("---")
    
    # İş Dünyası Önerileri
    st.markdown("## 💼 İş Dünyası için Öneriler")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style='background-color: white; padding: 1.5rem; border-radius: 10px; 
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);'>
            <h4 style='color: #1e40af;'>🎯 İşe Alım Stratejileri</h4>
            <ul>
                <li><strong>Web Projeleri:</strong> Küme 0 adaylarını hedefleyin</li>
                <li><strong>Veri Bilimi:</strong> Küme 1 profilini tercih edin</li>
                <li><strong>Full-stack:</strong> Küme 0'dan deneyimli adaylar</li>
                <li><strong>Sistem Programlama:</strong> Küme 1'den uzmanlar</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background-color: white; padding: 1.5rem; border-radius: 10px; 
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);'>
            <h4 style='color: #15803d;'>📚 Eğitim Programları</h4>
            <ul>
                <li><strong>Küme 0 için:</strong> Modern web framework'leri (React, Vue)</li>
                <li><strong>Küme 1 için:</strong> ML/AI, Büyük veri teknolojileri</li>
                <li><strong>Ortak:</strong> AI araçları kullanımı (her iki grup da ilgili)</li>
                <li><strong>Trend:</strong> Cloud teknolojileri eğitimi</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("###")
    
    st.markdown("""
    <div style='background-color: #fef3c7; padding: 1.5rem; border-radius: 10px; 
                border-left: 5px solid #f59e0b;'>
        <h4 style='color: #92400e; margin-top: 0;'>🔍 Temel Çıkarımlar</h4>
        <ol>
            <li><strong>Belirgin Ayrım:</strong> Web geliştiriciler ve sistem programcıları net şekilde ayrılıyor</li>
            <li><strong>Web Dominantlığı:</strong> Geliştiricilerin %85'i web teknolojileri kullanıyor</li>
            <li><strong>Python Yükselişi:</strong> Küme 1'de Python açık ara lider (%75.3)</li>
            <li><strong>Çok Yönlülük:</strong> Her iki grup da multiple dil ve araç kullanıyor</li>
            <li><strong>Sürekli Öğrenme:</strong> Tüm gruplar aktif olarak yeni şeyler öğreniyor</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Teknik Detaylar
    with st.expander("🔬 Teknik Detaylar ve Metrikler"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### Model Parametreleri:
            - **Algoritma:** K-Means
            - **Başlatma:** k-means++
            - **n_init:** 10
            - **random_state:** 42
            - **Özellik sayısı:** 131
            
            ### Veri İşleme:
            - **Encoding:** Multi-Label Binarizer
            - **Scaling:** StandardScaler (Z-score)
            - **PCA boyutu:** 2 (görselleştirme için)
            """)
        
        with col2:
            st.markdown("""
            ### Performans Metrikleri:
            - **Silhouette Score:** 0.125
            - **WCSS (k=2):** 621,316.50
            - **Açıklanan varyans (PCA):** %9.59
            - **Küme dengesi:** Dengesiz (85:15)
            
            ### Analiz Edilen Özellikler:
            - 42 programlama dili
            - 13 öğrenme kaynağı
            - 32 geliştirici tipi
            - Ülke ve deneyim bilgisi
            """)

