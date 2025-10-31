import streamlit as st
from predict_page import show_predict_page
from explore_page import show_explore_page
from clustering_page import show_clustering_page

# Sayfa yapılandırması
st.set_page_config(
    page_title="Stack Overflow Developer Survey - Analiz Platformu",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        background-color: #f5f7fa;
    }
    .stApp {
        max-width: 100%;
    }
    h1 {
        color: #1e3a8a;
        font-weight: 700;
    }
    h2 {
        color: #2563eb;
        font-weight: 600;
    }
    h3 {
        color: #3b82f6;
        font-weight: 500;
    }
    .stButton>button {
        background-color: #2563eb;
        color: white;
        font-weight: 600;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        border: none;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #1e40af;
        box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
        transform: translateY(-2px);
    }
    .css-1d391kg {
        padding: 2rem 1rem;
    }
    div[data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        color: #1e3a8a;
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=100)
    st.title("📊 Analiz Platformu")
    st.markdown("---")
    
    page = st.radio(
        "Navigasyon",
        ["🏠 Ana Sayfa", "📈 Veri Keşfi", "🎯 Maaş Tahmini", "🔬 Kümeleme Analizi"],
        index=0
    )
    
    st.markdown("---")
    st.markdown("### 📌 Proje Hakkında")
    st.info("""
    Stack Overflow Developer Survey 2024 verilerini kullanarak:
    - Maaş tahmini
    - Veri analizi
    - K-Means kümeleme
    """)
    
    st.markdown("---")
    st.markdown("**Geliştirici:** Bedirhan Örseoğlu")
    st.markdown("**GitHub:** [Proje Linki](https://github.com/bedirhanorseloglu/Proje-Yonetimi-Proje)")

# Ana sayfa
if page == "🏠 Ana Sayfa":
    st.title("🎓 Stack Overflow Developer Survey - Maaş Analizi ve Kümeleme Projesi")
    
    st.markdown("""
    <div style='background-color: white; padding: 2rem; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);'>
        <h2 style='color: #1e3a8a;'>📚 Hoş Geldiniz!</h2>
        <p style='font-size: 1.1rem; line-height: 1.6;'>
        Bu platform, <strong>Stack Overflow Developer Survey 2024</strong> verilerini kullanarak geliştiricilerin 
        maaşlarını tahmin eden ve geliştirici profillerini kümeleme analizi ile gruplandıran bir makine öğrenmesi projesidir.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("##")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div style='background-color: #dbeafe; padding: 1.5rem; border-radius: 10px; text-align: center;'>
            <h1 style='color: #1e40af; margin: 0;'>23,928</h1>
            <p style='color: #1e40af; margin: 0.5rem 0 0 0;'>Analiz Edilen Kişi</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background-color: #dcfce7; padding: 1.5rem; border-radius: 10px; text-align: center;'>
            <h1 style='color: #15803d; margin: 0;'>4</h1>
            <p style='color: #15803d; margin: 0.5rem 0 0 0;'>ML Modeli</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style='background-color: #fef3c7; padding: 1.5rem; border-radius: 10px; text-align: center;'>
            <h1 style='color: #92400e; margin: 0;'>2</h1>
            <p style='color: #92400e; margin: 0.5rem 0 0 0;'>Optimal Küme</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div style='background-color: #fce7f3; padding: 1.5rem; border-radius: 10px; text-align: center;'>
            <h1 style='color: #9f1239; margin: 0;'>131</h1>
            <p style='color: #9f1239; margin: 0.5rem 0 0 0;'>Özellik Sayısı</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("##")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style='background-color: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);'>
            <h3>📈 Veri Keşfi</h3>
            <p>Stack Overflow anket verilerini keşfedin. Ülkelere göre maaş dağılımları, deneyim seviyeleri ve 
            eğitim düzeylerine göre detaylı analizler yapın.</p>
            <ul>
                <li>Interaktif görselleştirmeler</li>
                <li>İstatistiksel analizler</li>
                <li>Karşılaştırmalı grafikler</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background-color: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);'>
            <h3>🎯 Maaş Tahmini</h3>
            <p>Ülke, eğitim düzeyi ve deneyim bilgilerinize göre maaş tahmini alın. 
            Decision Tree Regressor modeli kullanılarak yüksek doğrulukta tahminler yapılır.</p>
            <ul>
                <li>Gerçek zamanlı tahmin</li>
                <li>Karşılaştırmalı analiz</li>
                <li>Güven aralıkları</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("##")
    
    st.markdown("""
    <div style='background-color: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);'>
        <h3>🔬 Kümeleme Analizi</h3>
        <p>K-Means algoritması ile geliştiriciler 2 ana gruba ayrılmıştır:</p>
        <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-top: 1rem;'>
            <div style='background-color: #eff6ff; padding: 1rem; border-radius: 8px;'>
                <h4 style='color: #1e40af; margin-top: 0;'>Küme 0 (85.8%)</h4>
                <p><strong>Profil:</strong> Web Geliştiriciler</p>
                <p><strong>Diller:</strong> JavaScript, HTML/CSS, SQL</p>
                <p><strong>Deneyim:</strong> 16.4 yıl</p>
            </div>
            <div style='background-color: #f0fdf4; padding: 1rem; border-radius: 8px;'>
                <h4 style='color: #15803d; margin-top: 0;'>Küme 1 (14.2%)</h4>
                <p><strong>Profil:</strong> Sistem & Veri Bilimi</p>
                <p><strong>Diller:</strong> Python, Bash, C</p>
                <p><strong>Deneyim:</strong> 14.4 yıl</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("##")
    
    with st.expander("📊 Kullanılan Metodoloji ve Modeller"):
        st.markdown("""
        ### Maaş Tahmin Modelleri
        - **Linear Regression**: Temel regresyon modeli
        - **Decision Tree Regressor**: En yüksek performans (Seçilen model)
        - **Random Forest Regressor**: Ensemble öğrenme
        - **Gradient Boosting Machine**: Boosting yöntemi
        
        ### Kümeleme Analizi
        - **Algoritma**: K-Means Clustering
        - **Optimal k Belirleme**: Elbow Yöntemi + Silhouette Skoru
        - **Özellik Boyutu İndirgeme**: PCA (2D görselleştirme)
        - **Değerlendirme**: Silhouette Score, WCSS
        
        ### Değerlendirme Metrikleri
        - **R² Score**: Model açıklama gücü
        - **MAPE**: Ortalama mutlak yüzde hata
        - **MAE**: Ortalama mutlak hata
        - **MSE**: Ortalama kare hata
        """)

elif page == "📈 Veri Keşfi":
    show_explore_page()
elif page == "🎯 Maaş Tahmini":
    show_predict_page()
else:
    show_clustering_page()


# Çalıştırma komutları:
# conda activate ml
# streamlit run app.py
# conda run -n ml streamlit run app.py