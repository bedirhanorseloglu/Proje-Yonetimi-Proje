import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy import stats
from collections import Counter

# Grafik stili
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 10

def shorten_categories(categories, cutoff):
    categorical_map = {}
    for i in range(len(categories)):
        if categories.values[i] >= cutoff:
            categorical_map[categories.index[i]] = categories.index[i]
        else:
            categorical_map[categories.index[i]] = 'Other'
    return categorical_map

def clean_experience(x):
    if x == 'More than 50 years':
        return 50
    if x == 'Less than 1 year':
        return 0.5
    return float(x)

def clean_education(x):
    if "Bachelor" in x:
        return "Bachelor's degree (Lisans)"
    if "Master" in x:
        return "Master's degree (Yüksek Lisans)"
    if "Professional degree" in x or "doctoral" in x:
        return "Post grad (Doktora)"
    return "Less than a Bachelors (Lisans Altı)"

@st.cache_data
def load_survey_insights():
    """Tüm anket verilerini yükle (diller, öğrenme kanalları vb.)"""
    df_full = pd.read_csv("survey_results_public.csv")
    return df_full

@st.cache_data   
def load_data():
    df = pd.read_csv("survey_results_public.csv")
    
    # YearsCodePro veya YearsCode sütununu kontrol et (Notebook mantığı)
    years_col = 'YearsCodePro' if 'YearsCodePro' in df.columns else ('YearsCode' if 'YearsCode' in df.columns else None)
    if years_col is None:
        raise KeyError("Neither 'YearsCodePro' nor 'YearsCode' found in dataset.")
    
    # Gerekli sütunları seç
    keep_cols = ["Country", "EdLevel", years_col, "Employment", "ConvertedCompYearly"]
    df = df[keep_cols].copy()
    df = df.rename({"ConvertedCompYearly": "Salary", years_col: "YearsCodePro"}, axis=1)
    
    # Salary boş olanları çıkar
    df = df[df["Salary"].notnull()]
    
    # Tüm boş değerleri çıkar (Notebook'taki gibi)
    df = df.dropna()

    # Ülke kategorileme - 400'den az verisi olanları "Other"a at (Notebook mantığı)
    country_map = shorten_categories(df.Country.value_counts(), 400)
    df["Country"] = df["Country"].map(country_map)
    
    # Maaş filtreleme (Notebook'taki gibi)
    df = df[df["Salary"] <= 250000]
    df = df[df["Salary"] >= 10000]
    
    # "Other" ülkeleri ÇIKAR (Notebook'taki gibi)
    df = df[df['Country'] != 'Other']

    # YearsCodePro temizleme (Notebook'taki fonksiyon)
    df['YearsCodePro'] = df['YearsCodePro'].apply(clean_experience)
    
    # EdLevel temizleme
    df['EdLevel'] = df['EdLevel'].apply(clean_education)
    
    # Employment sütununu çıkar (artık gerekli değil)
    if 'Employment' in df.columns:
        df = df.drop("Employment", axis=1)
    
    return df

df = load_data()

def show_explore_page():
    st.title("📊 Veri Keşfi ve İstatistiksel Analiz")
    st.markdown("### Stack Overflow Geliştirici Anketi 2025 - Detaylı Analiz")
    
    # Tüm anket verilerini yükle (diller, öğrenme kanalları için)
    df_full = load_survey_insights()
    
    # Veri filtreleme bilgisi
    with st.expander("🔍 Veri Filtreleme Süreci Hakkında", expanded=False):
        st.markdown(f"""
        ### Neden {len(df_full):,} değil de {len(df):,} veri analiz ediliyor?
        
        Veri kalitesini artırmak ve güvenilir sonuçlar elde etmek için şu filtreler uygulandı:
        
        #### 1️⃣ **Maaş Bilgisi Olmayanlar** → ~30,000 kayıp
        - Birçok katılımcı maaş bilgisini paylaşmamış
        - Maaş analizi için bu alan zorunlu
        
        #### 2️⃣ **Herhangi Bir Boş Değer** → ~5,000-10,000 kayıp
        - EdLevel (Eğitim), YearsCodePro (Deneyim), Employment (İstihdam) eksik olanlar
        - Eksik veri modelin doğruluğunu düşürür
        
        #### 3️⃣ **Küçük Ülkeler (Other)** → Birkaç bin kayıp
        - 400'den az verisi olan ülkeler (Solomon Islands, Niger, Guinea gibi)
        - Az verili ülkeler modeli yanıltabilir
        
        #### 4️⃣ **Aşırı Uç Maaşlar (Outliers)** → Birkaç bin kayıp
        - Çok yüksek (>$250k) veya çok düşük (<$10k) maaşlar
        - Outlier'lar istatistiksel analizleri bozabilir
        
        ---
        
        ### ✅ Sonuç:
        **53,896** ham veri → **{len(df):,}** kaliteli, analiz edilebilir veri
        
        Bu filtreleme süreci:
        - ✅ Model doğruluğunu artırır
        - ✅ Güvenilir istatistikler sağlar
        - ✅ Yanıltıcı sonuçları önler
        """)
    
    # Genel istatistikler
    st.markdown("---")
    st.markdown("## 📈 Genel İstatistikler")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Toplam Veri",
            value=f"{len(df):,}",
            delta="Filtrelenmiş"
        )
    
    with col2:
        st.metric(
            label="Ortalama Maaş",
            value=f"${df['Salary'].mean():,.0f}",
            delta=f"±{df['Salary'].std():,.0f}"
        )
    
    with col3:
        st.metric(
            label="Medyan Maaş",
            value=f"${df['Salary'].median():,.0f}",
            delta="50. persentil"
        )
    
    with col4:
        st.metric(
            label="Ülke Sayısı",
            value=df['Country'].nunique(),
            delta="Analiz edildi"
        )
    
    st.markdown("---")
    
    # Veri dağılımı - Sekmeli düzenleme
    st.markdown("## 📊 Demografik Dağılımlar")
    
    demo_tabs = st.tabs(["📍 Ülkelere Göre", "🎓 Eğitim Düzeyine Göre"])
    
    with demo_tabs[0]:
        st.markdown("### Ülkelere Göre Veri Dağılımı")
        
        data = df["Country"].value_counts()
        
        # Pasta grafiği - daha büyük
        col1, col2 = st.columns([2, 1])
        
        with col1:
            fig, ax = plt.subplots(figsize=(12, 10))
            colors = plt.cm.Set3(range(len(data)))
            
            wedges, texts, autotexts = ax.pie(
                data, 
                labels=data.index, 
                autopct="%1.1f%%",
                startangle=90,
                colors=colors,
                textprops={'fontsize': 11}
            )
            
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
                autotext.set_fontsize(11)
            
            for text in texts:
                text.set_fontsize(12)
                text.set_fontweight('bold')
            
            ax.axis("equal")
            plt.title("Veri Kaynaklarının Coğrafi Dağılımı", fontsize=14, fontweight='bold', pad=20)
            st.pyplot(fig)
            plt.close()
        
        with col2:
            st.markdown("#### 🏆 Top 5 Ülke")
            for i, (country, count) in enumerate(data.head(5).items(), 1):
                percentage = (count / len(df)) * 100
                st.metric(
                    f"{i}. {country}", 
                    f"{count:,} kişi",
                    f"{percentage:.1f}%"
                )
        
        st.info("**📖 Nasıl Yorumlanır?** Bu pasta grafiği, anket katılımcılarının hangi ülkelerden geldiğini gösterir. Büyük dilimler daha fazla katılımcı olan ülkeleri temsil eder. Maaş tahminlerinin o ülke için daha güvenilir olduğu anlamına gelir (daha fazla veri = daha iyi model).")
        
        # Ülke istatistikleri tablosu
        with st.expander("📋 Detaylı Ülke İstatistikleri"):
            country_stats = pd.DataFrame({
                'Kişi Sayısı': df['Country'].value_counts(),
                'Yüzde (%)': (df['Country'].value_counts() / len(df) * 100).round(2),
                'Ortalama Maaş ($)': df.groupby('Country')['Salary'].mean().round(0),
                'Medyan Maaş ($)': df.groupby('Country')['Salary'].median().round(0)
            })
            st.dataframe(country_stats, use_container_width=True)

            st.info("""
            **📊 Ortalama vs Medyan Maaş - Ne Fark Eder?**
            
            **📈 Ortalama Maaş (Mean):**
            - Tüm maaşların toplamı ÷ kişi sayısı
            - ⚠️ Aşırı yüksek maaşlardan etkilenir
            - Birkaç CEO/senior maaşı ortalamayı yukarı çeker
            
            **📊 Medyan Maaş (Median):**
            - Maaşları sıralayınca tam ortadaki değer
            - ✅ Aşırı değerlerden ETKİLENMEZ (daha güvenilir!)
            - Çalışanların %50'si bunun altında, %50'si üstünde kazanıyor
            
            **💡 Hangi İstatistik Daha Gerçekçi?**
            - **MEDYAN** → Tipik bir geliştiricinin gerçek maaşını gösterir
            - **ORTALAMA** → Birkaç yüksek maaş varsa şişebilir
            
            🎯 İş ararken **medyan maaşa** bakın!
            """)
    
    with demo_tabs[1]:
        st.markdown("### Eğitim Düzeyine Göre Dağılım")
        
        education_data = df["EdLevel"].value_counts()
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            fig, ax = plt.subplots(figsize=(12, 8))
            colors = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444']
            
            bars = ax.barh(education_data.index, education_data.values, color=colors)
            ax.set_xlabel('Kişi Sayısı', fontsize=12, fontweight='bold')
            ax.set_ylabel('Eğitim Düzeyi', fontsize=12, fontweight='bold')
            ax.set_title('Eğitim Seviyesi Dağılımı', fontsize=14, fontweight='bold', pad=20)
            
            # Değerleri bar'ların üzerine yazalım
            for i, (bar, value) in enumerate(zip(bars, education_data.values)):
                ax.text(value + max(education_data.values)*0.02, i, f'{value:,}', 
                       va='center', fontsize=11, fontweight='bold')
            
            ax.grid(axis='x', alpha=0.3)
            plt.tight_layout()
            st.pyplot(fig)
            plt.close()
        
        with col2:
            st.markdown("#### 📚 Eğitim İstatistikleri")
            total = len(df)
            for edu, count in education_data.items():
                percentage = (count / total) * 100
                st.metric(
                    edu.split('(')[0].strip(),  # Türkçe kısmı al
                    f"{count:,} kişi",
                    f"{percentage:.1f}%"
                )
        
        st.info("**📖 Nasıl Yorumlanır?** Bu yatay bar grafiği, geliştiricilerin eğitim seviyelerini gösterir. Uzun çubuklar o eğitim seviyesine sahip daha fazla kişi olduğunu gösterir. Eğitim seviyesi ile maaş arasındaki ilişkiyi görmek için aşağıdaki '🎓 Eğitime Göre' sekmesine bakın.")
        
        # Eğitim istatistikleri
        with st.expander("📋 Detaylı Eğitim Düzeyi İstatistikleri"):
            education_stats = pd.DataFrame({
                'Kişi Sayısı': df['EdLevel'].value_counts(),
                'Yüzde (%)': (df['EdLevel'].value_counts() / len(df) * 100).round(2),
                'Ortalama Maaş ($)': df.groupby('EdLevel')['Salary'].mean().round(0),
                'Medyan Maaş ($)': df.groupby('EdLevel')['Salary'].median().round(0)
            })
            st.dataframe(education_stats, use_container_width=True)
    
    st.markdown("---")
    
    # Yeni bölümler: Diller ve Öğrenme Kanalları
    st.markdown("## 🌐 Anket İçgörüleri")
    
    st.info(f"""
    **ℹ️ Not:** Bu bölümdeki analizler **veri setindeki tüm {len(df_full):,} katılımcıyı** içerir (filtrelenmemiş ham veri). 
    Dil ve öğrenme kanalı tercihleri maaş analizinden bağımsız olduğu için tüm anket verileri kullanılmıştır.
    """)
    
    insight_tabs = st.tabs(["💻 Popüler Diller", "📚 Öğrenme Kanalları"])
    
    with insight_tabs[0]:
        st.markdown(f"### En Çok Kullanılan Programlama Dilleri")
        st.caption(f"📊 Toplam {len(df_full):,} katılımcının verisi")
        
        if 'LanguageHaveWorkedWith' in df_full.columns:
            # Dilleri parse et (noktalı virgülle ayrılmış)
            languages = df_full['LanguageHaveWorkedWith'].dropna()
            language_list = []
            for langs in languages:
                if isinstance(langs, str):
                    language_list.extend(langs.split(';'))
            
            # En çok kullanılan 15 dili al
            language_counts = Counter(language_list)
            top_languages = dict(language_counts.most_common(15))
            
            if top_languages:
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    fig, ax = plt.subplots(figsize=(12, 10))
                    colors = plt.cm.viridis(np.linspace(0, 1, len(top_languages)))
                    
                    bars = ax.barh(list(top_languages.keys()), list(top_languages.values()), color=colors)
                    ax.set_xlabel('Kullanım Sayısı', fontsize=12, fontweight='bold')
                    ax.set_ylabel('Programlama Dili', fontsize=12, fontweight='bold')
                    ax.set_title('2025 Yılı En Popüler Programlama Dilleri (Top 15)', fontsize=14, fontweight='bold', pad=20)
                    
                    # Değerleri bar'ların üzerine yazalım
                    for i, (bar, value) in enumerate(zip(bars, top_languages.values())):
                        ax.text(value + max(top_languages.values())*0.01, i, f'{value:,}', 
                               va='center', fontsize=10, fontweight='bold')
                    
                    ax.grid(axis='x', alpha=0.3)
                    plt.tight_layout()
                    st.pyplot(fig)
                    plt.close()
                
                with col2:
                    st.markdown("#### 🏆 Top 5 Dil")
                    medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"]
                    for i, ((lang, count), medal) in enumerate(zip(list(top_languages.items())[:5], medals), 1):
                        total_responses = len(languages)
                        percentage = (count / total_responses) * 100
                        st.metric(
                            f"{medal} {lang}", 
                            f"{count:,} kullanıcı",
                            f"{percentage:.1f}%"
                        )
                
                st.info("**📖 Nasıl Yorumlanır?** Bu grafik, ankete katılan geliştiricilerin en çok kullandığı programlama dillerini gösterir. Uzun çubuklar o dili kullanan daha fazla geliştirici olduğunu gösterir. Bu, hangi dillerin popüler olduğunu ve iş piyasasında hangi dillere talep olduğunu anlamanıza yardımcı olur.")
            else:
                st.warning("⚠️ Dil verisi bulunamadı")
        else:
            st.warning("⚠️ Dil verisi mevcut değil")
    
    with insight_tabs[1]:
        st.markdown(f"### Geliştiriciler Nasıl Kod Öğreniyor?")
        st.caption(f"📊 Toplam {len(df_full):,} katılımcının verisi")
        
        if 'LearnCode' in df_full.columns:
            # Öğrenme kanallarını parse et
            learn_methods = df_full['LearnCode'].dropna()
            method_list = []
            for methods in learn_methods:
                if isinstance(methods, str):
                    method_list.extend(methods.split(';'))
            
            # En çok kullanılan 12 öğrenme kanalını al
            method_counts = Counter(method_list)
            top_methods = dict(method_counts.most_common(12))
            
            if top_methods:
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    fig, ax = plt.subplots(figsize=(12, 10))
                    colors = plt.cm.plasma(np.linspace(0, 1, len(top_methods)))
                    
                    bars = ax.barh(list(top_methods.keys()), list(top_methods.values()), color=colors)
                    ax.set_xlabel('Kullanım Sayısı', fontsize=12, fontweight='bold')
                    ax.set_ylabel('Öğrenme Kanalı', fontsize=12, fontweight='bold')
                    ax.set_title('En Popüler Kod Öğrenme Kanalları (Top 12)', fontsize=14, fontweight='bold', pad=20)
                    
                    # Değerleri bar'ların üzerine yazalım
                    for i, (bar, value) in enumerate(zip(bars, top_methods.values())):
                        ax.text(value + max(top_methods.values())*0.01, i, f'{value:,}', 
                               va='center', fontsize=10, fontweight='bold')
                    
                    ax.grid(axis='x', alpha=0.3)
                    plt.tight_layout()
                    st.pyplot(fig)
                    plt.close()
                
                with col2:
                    st.markdown("#### 🏆 Top 5 Kanal")
                    medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"]
                    for i, ((method, count), medal) in enumerate(zip(list(top_methods.items())[:5], medals), 1):
                        total_responses = len(learn_methods)
                        percentage = (count / total_responses) * 100
                        st.metric(
                            f"{medal} {method}", 
                            f"{count:,} kullanıcı",
                            f"{percentage:.1f}%"
                        )
                
                st.info("**📖 Nasıl Yorumlanır?** Bu grafik, geliştiricilerin kod öğrenmek için en çok kullandıkları kaynakları gösterir. Online kurslar, Stack Overflow, YouTube gibi platformların ne kadar popüler olduğunu görebilirsiniz. Kendi öğrenme yolunuzu planlarken bu bilgiler yol gösterici olabilir.")
            else:
                st.warning("⚠️ Öğrenme kanalı verisi bulunamadı")
        else:
            st.warning("⚠️ Öğrenme kanalı verisi mevcut değil")
    
    st.markdown("---")
    
    # Maaş analizleri
    st.markdown("## 💰 Maaş Analizleri")
    
    tabs = st.tabs(["🌍 Ülkelere Göre", "⏱️ Deneyime Göre", "🎓 Eğitime Göre", "📊 Dağılım Analizi"])
    
    with tabs[0]:
        st.markdown("### Ülkelere Göre Ortalama Maaş Karşılaştırması")
        
        sort_option = st.radio("Sıralama:", ["Yüksekten Düşüğe", "Düşükten Yükseğe"], horizontal=True)
        ascending = (sort_option == "Düşükten Yükseğe")
        
        data = df.groupby(["Country"])["Salary"].agg(['mean', 'median', 'std']).sort_values('mean', ascending=ascending)
        
        fig, ax = plt.subplots(figsize=(12, 8))
        
        x_pos = np.arange(len(data))
        bars = ax.barh(x_pos, data['mean'], xerr=data['std'], 
                      color='#3b82f6', alpha=0.7, capsize=5)
        
        ax.set_yticks(x_pos)
        ax.set_yticklabels(data.index, fontsize=10)
        ax.set_xlabel('Ortalama Yıllık Maaş ($)', fontsize=11, fontweight='bold')
        ax.set_title('Ülkelere Göre Ortalama Maaş (±Std. Sapma)', fontsize=12, fontweight='bold', pad=20)
        ax.grid(axis='x', alpha=0.3)
        
        # Değerleri ekleyelim
        for i, (mean_val, std_val) in enumerate(zip(data['mean'], data['std'])):
            ax.text(mean_val + std_val + 2000, i, f'${mean_val:,.0f}', 
                   va='center', fontsize=9, fontweight='bold')
        
        st.pyplot(fig)
        plt.close()
        
        st.info("**📖 Nasıl Yorumlanır?** Bu yatay bar grafiği, her ülkenin ortalama maaşını gösterir. Uzun çubuklar daha yüksek maaş demektir. Hata çubukları (±) standart sapmayı gösterir - uzun hata çubukları o ülkede maaş dağılımının geniş olduğunu (bazıları çok az, bazıları çok fazla kazanıyor), kısa olanlar ise maaşların birbirine yakın olduğunu gösterir.")
        
        # İstatistiksel testler
        with st.expander("📊 İstatistiksel Analizler"):
            st.markdown("**ANOVA Test Sonuçları (Ülkeler Arası Maaş Farkı)**")
            try:
                countries = df['Country'].unique()
                # En az 2 örneği olan ülkeleri filtrele
                groups = [df[df['Country'] == country]['Salary'].values 
                         for country in countries 
                         if len(df[df['Country'] == country]) >= 2]
                
                if len(groups) >= 2:
                    f_stat, p_value = stats.f_oneway(*groups)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("F-istatistiği", f"{f_stat:.2f}")
                    with col2:
                        st.metric("P-değeri", f"{p_value:.4e}")
                    
                    if p_value < 0.05:
                        st.success("✅ Ülkeler arasında istatistiksel olarak anlamlı maaş farkı var (p < 0.05)")
                    else:
                        st.warning("⚠️ Ülkeler arasında istatistiksel olarak anlamlı fark yok (p ≥ 0.05)")
                else:
                    st.info("ℹ️ ANOVA testi için yeterli ülke grubu yok (en az 2 grup gerekli)")
            except Exception as e:
                st.warning(f"⚠️ ANOVA testi yapılamadı: Yeterli veri yok")
    
    with tabs[1]:
        st.markdown("### Deneyime Göre Maaş Trendi")
        
        data = df.groupby(["YearsCodePro"])["Salary"].agg(['mean', 'count']).reset_index()
        data = data[data['count'] >= 5]  # En az 5 kişi olan deneyim seviyelerini göster
        
        if len(data) >= 3:
            fig, ax = plt.subplots(figsize=(14, 7))
            
            # Scatter plot
            scatter = ax.scatter(data['YearsCodePro'], data['mean'], 
                               s=data['count']*5, alpha=0.6, c=data['mean'], 
                               cmap='viridis', edgecolors='black', linewidth=1)
            
            # Trend çizgisi
            try:
                z = np.polyfit(data['YearsCodePro'], data['mean'], 2)
                p = np.poly1d(z)
                ax.plot(data['YearsCodePro'], p(data['YearsCodePro']), 
                       "r--", linewidth=2, label='Trend Çizgisi', alpha=0.8)
            except:
                pass  # Trend çizgisi çizilemezse devam et
            
            ax.set_xlabel('Deneyim Yılı', fontsize=11, fontweight='bold')
            ax.set_ylabel('Ortalama Maaş ($)', fontsize=11, fontweight='bold')
            ax.set_title('Deneyim vs Maaş İlişkisi (Nokta büyüklüğü = veri sayısı)', 
                        fontsize=12, fontweight='bold', pad=20)
            ax.grid(True, alpha=0.3)
            ax.legend(fontsize=10)
            
            # Colorbar
            cbar = plt.colorbar(scatter, ax=ax)
            cbar.set_label('Maaş ($)', fontsize=10, fontweight='bold')
            
            st.pyplot(fig)
            plt.close()
            
            st.info("**📖 Nasıl Yorumlanır?** Bu scatter plot, deneyim yılı ile maaş arasındaki ilişkiyi gösterir. Her nokta bir deneyim seviyesini temsil eder. Büyük noktalar o deneyim seviyesinde daha fazla kişi olduğunu gösterir. Kırmızı kesik çizgi genel trendi gösterir - yukarı eğilimli ise deneyim arttıkça maaş artıyor demektir. Nokta renkleri de maaş seviyesini gösterir (sarı=yüksek, mor=düşük).")
        else:
            st.warning("⚠️ Deneyim analizi için yeterli veri yok (en az 3 farklı deneyim seviyesi gerekli)")
        
        # Korelasyon analizi
        with st.expander("📊 Korelasyon Analizi"):
            try:
                correlation = df['YearsCodePro'].corr(df['Salary'])
                st.metric("Pearson Korelasyon Katsayısı", f"{correlation:.3f}")
                
                if correlation > 0.5:
                    st.success("✅ Güçlü pozitif korelasyon: Deneyim arttıkça maaş artıyor")
                elif correlation > 0.3:
                    st.info("ℹ️ Orta düzey pozitif korelasyon var")
                else:
                    st.warning("⚠️ Zayıf korelasyon")
            except:
                st.warning("⚠️ Korelasyon analizi için yeterli veri yok")
    
    with tabs[2]:
        st.markdown("### Eğitim Düzeyine Göre Maaş Dağılımı")
        
        education_order = ["Less than a Bachelors (Lisans Altı)", "Bachelor's degree (Lisans)", 
                          "Master's degree (Yüksek Lisans)", "Post grad (Doktora)"]
        
        # Violin plot
        positions = []
        valid_data = []
        for i, edu in enumerate(education_order):
            if edu in df['EdLevel'].unique():
                data_edu = df[df['EdLevel'] == edu]['Salary']
                if len(data_edu) > 0:
                    valid_data.append((i, data_edu))
                    positions.append(i)
        
        if len(valid_data) > 0:
            fig, ax = plt.subplots(figsize=(12, 7))
            
            for pos, data_edu in valid_data:
                # Violin plot
                try:
                    parts = ax.violinplot([data_edu], positions=[pos], 
                                         widths=0.7, showmeans=True, showmedians=True)
                    
                    for pc in parts['bodies']:
                        pc.set_facecolor('#3b82f6')
                        pc.set_alpha(0.6)
                except:
                    pass  # Violin plot çizilemezse devam et
            
            ax.set_xticks(range(len(education_order)))
            # Sadece Türkçe kısımları göster (parantez içi)
            short_labels = [edu.split('(')[1].replace(')', '') if '(' in edu else edu for edu in education_order]
            ax.set_xticklabels(short_labels, rotation=15, ha='right', fontsize=10)
            ax.set_ylabel('Maaş ($)', fontsize=11, fontweight='bold')
            ax.set_title('Eğitim Düzeyine Göre Maaş Dağılımı (Violin Plot)', 
                        fontsize=12, fontweight='bold', pad=20)
            ax.grid(axis='y', alpha=0.3)
            
            st.pyplot(fig)
            plt.close()
            
            st.info("**📖 Nasıl Yorumlanır?** Violin plot, her eğitim seviyesi için maaş dağılımını gösterir. Geniş bölgeler o maaş aralığında daha fazla kişi olduğunu gösterir. Ortadaki çizgiler medyanı (kalın) ve ortalamayı (ince) gösterir. Bir violin'in yukarı uzaması o eğitim seviyesinde yüksek maaşlı kişiler olduğunu gösterir.")
        else:
            st.warning("⚠️ Eğitim düzeyi analizi için yeterli veri yok")
        
        # Box plot
        if len(valid_data) > 0:
            st.markdown("#### Box Plot Analizi")
            
            try:
                fig, ax = plt.subplots(figsize=(12, 6))
                df.boxplot(column='Salary', by='EdLevel', ax=ax, patch_artist=True)
                ax.set_xlabel('Eğitim Düzeyi', fontsize=11, fontweight='bold')
                ax.set_ylabel('Maaş ($)', fontsize=11, fontweight='bold')
                ax.set_title('Eğitim Düzeyine Göre Maaş Box Plot', fontsize=12, fontweight='bold')
                plt.suptitle('')  # Varsayılan başlığı kaldır
                ax.grid(True, alpha=0.3)
                
                st.pyplot(fig)
                plt.close()
                
                st.info("**📖 Nasıl Yorumlanır?** Box plot, maaş dağılımını 5 sayıyla özetler: Kutunun alt kenarı %25'lik dilim (Q1), ortadaki çizgi medyan (%50), üst kenar %75'lik dilim (Q3). Bıyıklar (whiskers) min/max değerleri gösterir. Kutunun dışındaki noktalar aykırı değerlerdir (outlier). Uzun kutu = geniş maaş dağılımı, kısa kutu = dar maaş dağılımı.")
            except:
                st.info("ℹ️ Box plot çizilemedi")
    
    with tabs[3]:
        st.markdown("### Maaş Dağılım Analizi")
        
        # Histogram
        fig, ax = plt.subplots(figsize=(14, 7))
        
        n, bins, patches = ax.hist(df['Salary'], bins=50, 
                                   color='#3b82f6', alpha=0.7, edgecolor='black')
        
        # Normal dağılım overlay
        mu = df['Salary'].mean()
        sigma = df['Salary'].std()
        x = np.linspace(df['Salary'].min(), df['Salary'].max(), 100)
        y = stats.norm.pdf(x, mu, sigma) * len(df) * (bins[1] - bins[0])
        ax.plot(x, y, 'r--', linewidth=2, label='Normal Dağılım')
        
        ax.set_xlabel('Maaş ($)', fontsize=11, fontweight='bold')
        ax.set_ylabel('Frekans', fontsize=11, fontweight='bold')
        ax.set_title('Maaş Dağılımı Histogramı', fontsize=12, fontweight='bold', pad=20)
        ax.legend()
        ax.grid(axis='y', alpha=0.3)
        
        st.pyplot(fig)
        plt.close()
        
        st.info("**📖 Nasıl Yorumlanır?** Histogram, maaşların nasıl dağıldığını gösterir. Her çubuk bir maaş aralığını temsil eder, yükseklik o aralıkta kaç kişi olduğunu gösterir. Kırmızı kesik çizgi teorik normal dağılımı gösterir. Eğer mavi çubuklar kırmızı çizgiye benziyorsa, maaşlar 'normal' dağılmış demektir. Sağa kayık = çoğu insan düşük kazanıyor, birkaç kişi çok yüksek.")
        
        # Dağılım istatistikleri
        with st.expander("📊 Dağılım İstatistikleri"):
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Çarpıklık (Skewness)", f"{stats.skew(df['Salary']):.3f}")
            with col2:
                st.metric("Basıklık (Kurtosis)", f"{stats.kurtosis(df['Salary']):.3f}")
            with col3:
                q1 = df['Salary'].quantile(0.25)
                q3 = df['Salary'].quantile(0.75)
                iqr = q3 - q1
                st.metric("IQR", f"${iqr:,.0f}")
            with col4:
                st.metric("Varyasyon Katsayısı", 
                         f"{(df['Salary'].std() / df['Salary'].mean() * 100):.1f}%")
            
            # Shapiro-Wilk normallik testi
            st.markdown("**Shapiro-Wilk Normallik Testi**")
            try:
                if len(df) >= 3:
                    sample = df['Salary'].sample(min(5000, len(df)))
                    stat, p_value = stats.shapiro(sample)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Test İstatistiği", f"{stat:.4f}")
                    with col2:
                        st.metric("P-değeri", f"{p_value:.4e}")
                    
                    if p_value < 0.05:
                        st.warning("⚠️ Veriler normal dağılmıyor (p < 0.05)")
                    else:
                        st.success("✅ Veriler normal dağılıyor (p ≥ 0.05)")
                else:
                    st.info("ℹ️ Shapiro-Wilk testi için yeterli veri yok (en az 3 örnek gerekli)")
            except Exception as e:
                st.warning("⚠️ Normallik testi yapılamadı: Yeterli veri yok")
    
    st.markdown("---")
    
    # Veri tablosu
    with st.expander("📋 Ham Veri Görüntüleme"):
        st.dataframe(df.head(100), use_container_width=True)
        st.download_button(
            label="📥 CSV İndir",
            data=df.to_csv(index=False).encode('utf-8'),
            file_name='salary_data.csv',
            mime='text/csv',
        )
