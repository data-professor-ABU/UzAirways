import streamlit as st
import pandas as pd

# Sahifa sozlamalari
st.set_page_config(page_title="Dashboard", page_icon="📈", layout="wide")
st.header("O'ZBEKISTON HAVO YO'LLARI TOG'RISIDA CHIQADIGAN XABARLAR JAMLANMASI")
st.markdown("##")

# Sidebar: faqat reklam matni
with st.sidebar:
    st.markdown("### Bu yerda sizning reklamangiz bo'lishi mumkin edi")

# CSS yuklash
with open('style.css') as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Ma'lumotlarni yuklash

df_sources = {
    "KUN.uz Rasmiy sayti": pd.read_excel('data/kunuzofficial_filtered_last_month.xlsx'),
    "Gazeta.uz Rasmiy sayti": pd.read_excel('data/gazetauz_uzb_filtered_last_month.xlsx'),
    "Bakiroo rasmiy kanali": pd.read_excel('data/the_bakiroo_filtered_last_month.xlsx')
}


# Tablar yaratish
tab_names = list(df_sources.keys())
tabs = st.tabs(tab_names)

# Har bir tab uchun kontent
def display_tab(df_text):
    col1, col2 = st.columns([2, 1])

    with col1:
        for i, row in df_text.iterrows():
            with st.expander(f"{row['date']}"):
                st.write(row['post'])

    with col2:
        # CSS style for background color
        st.markdown("""
            <style>
            .stat-container {
                background-color: #28a745; /* Yashil rang */
                padding: 20px;
                border-radius: 10px;
                color: white;
            }
            .red-text {
                color: red; /* Qizil rang */
            }
            .green-text {
                color: green; /* Yashil rang */
                font-size: 4em; /* Yozuvni kattaroq qilish */
                font-weight: bold;
            }
            .metric-text {
                font-size: 2.5em; /* Kattaroq font-size */
                font-weight: bold;
                color: green;
            }
            </style>
        """, unsafe_allow_html=True)
        
        # st.markdown('<div class="stat-container">', unsafe_allow_html=True)
        
        # st.subheader("POSTLAR STATISTIKASI")
        
        # Yashil rangda "POSTLAR SONI" - st.metric
        st.metric(
            label="POSTLAR SONI",
            value=f"{len(df_text)}",
            delta="0",  # Natija uchun delta qo'yilmaydi
            delta_color="normal"
        )
        
        # Sana ustunini to'g'ri formatlash (faqat sana, soatsiz)
        df_text['date'] = pd.to_datetime(df_text['date']).dt.date
        
        # Unikal sanalarni olish
        unique_dates = df_text['date'].dropna().unique()
        
        st.write("UNIKAL SANALAR ")
        st.markdown(f'<p class="red-text">{", ".join(map(str, unique_dates))}</p>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

# Har bir tabni ko‘rsatish
for tab, name in zip(tabs, tab_names):
    with tab:
        display_tab(df_sources[name])
