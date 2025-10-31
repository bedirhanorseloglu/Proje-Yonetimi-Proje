import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy import stats

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
    if 'Bachelor's degree' in x:
        return 'Bachelor's degree'
    if 'Master's degree' in x:
        return 'Master's degree'
    if 'Professional degree' in x or 'Other doctoral' in x:
        return 'Post grad'
    return 'Less than a Bachelors'

@st.cache_data
def load_data():
    df = pd.read_csv("survey_results_public.csv")
    df = df[["Country", "EdLevel", "YearsCodePro", "Employment", "ConvertedCompYearly"]]
    df = df[df["ConvertedCompYearly"].notnull()]
    df = df.dropna()
    df = df[df["Employment"] == "Employed, full-time"]
    df = df.drop("Employment", axis=1)

    country_map = shorten_categories(df.Country.value_counts(), 400)
    df["Country"] = df["Country"].map(country_map)
    df = df[df["ConvertedCompYearly"] <= 250000]
    df = df[df["ConvertedCompYearly"] >= 10000]
    df = df[df['Country'] != 'Other']

    df['YearsCodePro'] = df['YearsCodePro'].apply(clean_experience)
    df['EdLevel'] = df['EdLevel'].apply(clean_education)
    df = df.rename({"ConvertedCompYearly": "Salary"}, axis=1)
    return df

df = load_data()

def show_explore_page():
    st.title("📊 Veri Keşfi ve İstatistiksel Analiz")
    st.markdown("### Stack Overflow Geliştirici Anketi 2024 - Detaylı Analiz")
    
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
    
    # Veri dağılımı
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📍 Ülkelere Göre Veri Dağılımı")
        
        data = df["Country"].value_counts()
        
        fig, ax = plt.subplots(figsize=(10, 8))
        colors = plt.cm.Set3(range(len(data)))
        
        wedges, texts, autotexts = ax.pie(
            data, 
            labels=data.index, 
            autopct="%1.1f%%",
            startangle=90,
            colors=colors,
            textprops={'fontsize': 9}
        )
        
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        
        ax.axis("equal")
        plt.title("Veri Kaynaklarının Coğrafi Dağılımı", fontsize=12, fontweight='bold', pad=20)
        st.pyplot(fig)
        plt.close()
        
        # Ülke istatistikleri tablosu
        with st.expander("📋 Detaylı Ülke İstatistikleri"):
            country_stats = pd.DataFrame({
                'Kişi Sayısı': df['Country'].value_counts(),
                'Yüzde (%)': (df['Country'].value_counts() / len(df) * 100).round(2),
                'Ortalama Maaş ($)': df.groupby('Country')['Salary'].mean().round(0),
                'Medyan Maaş ($)': df.groupby('Country')['Salary'].median().round(0)
            })
            st.dataframe(country_stats, use_container_width=True)
    
    with col2:
        st.markdown("### 🎓 Eğitim Düzeyi Dağılımı")
        
        education_data = df["EdLevel"].value_counts()
        
        fig, ax = plt.subplots(figsize=(10, 8))
        colors = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444']
        
        bars = ax.barh(education_data.index, education_data.values, color=colors)
        ax.set_xlabel('Kişi Sayısı', fontsize=11, fontweight='bold')
        ax.set_title('Eğitim Seviyesi Dağılımı', fontsize=12, fontweight='bold', pad=20)
        
        # Değerleri bar'ların üzerine yazalım
        for i, (bar, value) in enumerate(zip(bars, education_data.values)):
            ax.text(value + 50, i, f'{value:,}', 
                   va='center', fontsize=10, fontweight='bold')
        
        ax.grid(axis='x', alpha=0.3)
        st.pyplot(fig)
        plt.close()
        
        # Eğitim istatistikleri
        with st.expander("📋 Eğitim Düzeyi İstatistikleri"):
            education_stats = pd.DataFrame({
                'Kişi Sayısı': df['EdLevel'].value_counts(),
                'Yüzde (%)': (df['EdLevel'].value_counts() / len(df) * 100).round(2),
                'Ortalama Maaş ($)': df.groupby('EdLevel')['Salary'].mean().round(0)
            })
            st.dataframe(education_stats, use_container_width=True)
    
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
        
        # İstatistiksel testler
        with st.expander("📊 İstatistiksel Analizler"):
            st.markdown("**ANOVA Test Sonuçları (Ülkeler Arası Maaş Farkı)**")
            countries = df['Country'].unique()
            groups = [df[df['Country'] == country]['Salary'].values for country in countries]
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
    
    with tabs[1]:
        st.markdown("### Deneyime Göre Maaş Trendi")
        
        data = df.groupby(["YearsCodePro"])["Salary"].agg(['mean', 'count']).reset_index()
        data = data[data['count'] >= 5]  # En az 5 kişi olan deneyim seviyelerini göster
        
        fig, ax = plt.subplots(figsize=(14, 7))
        
        # Scatter plot
        scatter = ax.scatter(data['YearsCodePro'], data['mean'], 
                           s=data['count']*5, alpha=0.6, c=data['mean'], 
                           cmap='viridis', edgecolors='black', linewidth=1)
        
        # Trend çizgisi
        z = np.polyfit(data['YearsCodePro'], data['mean'], 2)
        p = np.poly1d(z)
        ax.plot(data['YearsCodePro'], p(data['YearsCodePro']), 
               "r--", linewidth=2, label='Trend Çizgisi', alpha=0.8)
        
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
        
        # Korelasyon analizi
        with st.expander("📊 Korelasyon Analizi"):
            correlation = df['YearsCodePro'].corr(df['Salary'])
            st.metric("Pearson Korelasyon Katsayısı", f"{correlation:.3f}")
            
            if correlation > 0.5:
                st.success("✅ Güçlü pozitif korelasyon: Deneyim arttıkça maaş artıyor")
            elif correlation > 0.3:
                st.info("ℹ️ Orta düzey pozitif korelasyon var")
            else:
                st.warning("⚠️ Zayıf korelasyon")
    
    with tabs[2]:
        st.markdown("### Eğitim Düzeyine Göre Maaş Dağılımı")
        
        fig, ax = plt.subplots(figsize=(12, 7))
        
        education_order = ['Less than a Bachelors', "Bachelor's degree", 
                          "Master's degree", 'Post grad']
        
        positions = []
        for i, edu in enumerate(education_order):
            if edu in df['EdLevel'].unique():
                data_edu = df[df['EdLevel'] == edu]['Salary']
                
                # Violin plot
                parts = ax.violinplot([data_edu], positions=[i], 
                                     widths=0.7, showmeans=True, showmedians=True)
                
                for pc in parts['bodies']:
                    pc.set_facecolor('#3b82f6')
                    pc.set_alpha(0.6)
                
                positions.append(i)
        
        ax.set_xticks(range(len(education_order)))
        ax.set_xticklabels(education_order, rotation=15, ha='right')
        ax.set_ylabel('Maaş ($)', fontsize=11, fontweight='bold')
        ax.set_title('Eğitim Düzeyine Göre Maaş Dağılımı (Violin Plot)', 
                    fontsize=12, fontweight='bold', pad=20)
        ax.grid(axis='y', alpha=0.3)
        
        st.pyplot(fig)
        plt.close()
        
        # Box plot
        st.markdown("#### Box Plot Analizi")
        
        fig, ax = plt.subplots(figsize=(12, 6))
        df.boxplot(column='Salary', by='EdLevel', ax=ax, patch_artist=True)
        ax.set_xlabel('Eğitim Düzeyi', fontsize=11, fontweight='bold')
        ax.set_ylabel('Maaş ($)', fontsize=11, fontweight='bold')
        ax.set_title('Eğitim Düzeyine Göre Maaş Box Plot', fontsize=12, fontweight='bold')
        plt.suptitle('')  # Varsayılan başlığı kaldır
        ax.grid(True, alpha=0.3)
        
        st.pyplot(fig)
        plt.close()
    
    with tabs[3]:
        st.markdown("### Maaş Dağılım Analizi")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Histogram
            fig, ax = plt.subplots(figsize=(10, 6))
            
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
        
        with col2:
            # Q-Q Plot
            fig, ax = plt.subplots(figsize=(10, 6))
            stats.probplot(df['Salary'], dist="norm", plot=ax)
            ax.set_title('Q-Q Plot (Normallik Testi)', fontsize=12, fontweight='bold', pad=20)
            ax.grid(True, alpha=0.3)
            
            st.pyplot(fig)
            plt.close()
        
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
