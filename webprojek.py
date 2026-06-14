import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# --- 1. CONFIG HALAMAN & TEMPLATE UTAMA ---
st.set_page_config(
    page_title="Aktuaria Modern UI", 
    page_icon="📱", 
    layout="wide",
    initial_sidebar_state="collapsed" 
)

# --- 2. CSS SUNTIKAN: TEMA PALET ESTETIK & ANIMASI 3D ---
st.markdown("""
<style>
    /* Background Utama - Warm Off-White / Cream */
    .stApp { 
        background: linear-gradient(135deg, #F8F7F2 0%, #EFECE1 100%) !important; 
        color: #2A2A2A !important; font-family: 'Segoe UI', sans-serif; 
    }
    
    /* Menyembunyikan tombol expand/collapse sidebar bawaan */
    [data-testid="collapsedControl"] { display: none; }
    
    /* === PENGATURAN TOP BAR & NAVIGASI PILL === */
    div.row-widget.stRadio > div { 
        flex-direction: row; justify-content: center; 
        background: #FFFFFF; padding: 8px; border-radius: 40px; 
        box-shadow: 0px 8px 25px rgba(61, 64, 91, 0.06); 
        margin-bottom: 25px; flex-wrap: wrap; 
        border: 1px solid #E8E5D1;
    }
    div.row-widget.stRadio > div > label { 
        background-color: transparent; padding: 10px 24px; border-radius: 30px; 
        margin: 5px; cursor: pointer; transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
    }
    div.row-widget.stRadio > div > label:hover { 
        background-color: #F4F1DE; transform: translateY(-2px);
    }
    div.row-widget.stRadio > div > label:active { transform: scale(0.92); }
    
    /* Warna aktif - Terracotta (Coral/Orange) */
    div.row-widget.stRadio > div > label[data-checked="true"] { 
        background: linear-gradient(135deg, #E07A5F 0%, #C85A3F 100%) !important; 
        box-shadow: 0px 6px 15px rgba(224, 122, 95, 0.35) !important;
    }
    div.row-widget.stRadio > div > label[data-checked="true"] p { color: white !important; font-weight: 700; }
    div.row-widget.stRadio p { color: #6D6D6D; font-weight: 600; font-size: 15px; margin: 0; }
    
    /* === ANIMASI 3D LOGO === */
    .logo-3d-container {
        perspective: 1000px;
        margin-bottom: 10px;
    }
    .logo-3d {
        /* Gradien Navy ke Terracotta */
        background: linear-gradient(135deg, #3D405B 0%, #E07A5F 100%);
        border-radius: 50%;
        width: 50px; height: 50px;
        display: flex; align-items: center; justify-content: center;
        color: white; font-size: 20px; font-weight: bold;
        box-shadow: 0 10px 25px rgba(61, 64, 91, 0.4), inset 0 -3px 6px rgba(0,0,0,0.2);
        cursor: pointer;
        transform-style: preserve-3d;
        animation: float3d 5s ease-in-out infinite; 
    }
    /* Efek putar koin saat disorot */
    .logo-3d:hover {
        animation: spin3d 1.5s linear infinite;
        box-shadow: 0 0 20px rgba(224, 122, 95, 0.6);
    }
    
    @keyframes float3d {
        0% { transform: translateY(0px) rotateY(0deg) rotateX(0deg); }
        25% { transform: translateY(-6px) rotateY(15deg) rotateX(10deg); }
        50% { transform: translateY(0px) rotateY(0deg) rotateX(0deg); }
        75% { transform: translateY(6px) rotateY(-15deg) rotateX(-10deg); }
        100% { transform: translateY(0px) rotateY(0deg) rotateX(0deg); }
    }
    @keyframes spin3d {
        0% { transform: rotateY(0deg); }
        100% { transform: rotateY(360deg); }
    }

    /* === ANIMASI GRADASI BACKGROUND PADA CONTAINER TOP BAR === */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background: linear-gradient(270deg, #FFFFFF, #F8F7F2, #EFECE1, #FFFFFF) !important;
        background-size: 800% 800% !important;
        animation: gradientFlow 15s ease infinite !important; 
        border-radius: 24px !important;
        border: 1px solid #E8E5D1 !important;
        box-shadow: 0px 12px 30px rgba(61, 64, 91, 0.05) !important;
        padding: 20px 25px 25px 25px !important;
        transition: transform 0.2s ease;
    }
    [data-testid="stVerticalBlockBorderWrapper"]:hover {
        transform: translateY(-2px);
        box-shadow: 0px 16px 35px rgba(61, 64, 91, 0.1) !important;
    }
    
    @keyframes gradientFlow {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* === STYLING INPUT BOX STREAMLIT === */
    div[data-baseweb="select"] > div, div[data-baseweb="base-input"] {
        border-radius: 12px !important;
        background-color: rgba(255, 255, 255, 0.8) !important;
        border: 2px solid transparent !important;
        transition: all 0.2s ease-in-out !important;
    }
    div[data-baseweb="select"] > div:hover, div[data-baseweb="base-input"]:hover { background-color: #FFFFFF !important; }
    div[data-baseweb="select"] > div:focus-within, div[data-baseweb="base-input"]:focus-within {
        border: 2px solid #E07A5F !important;
        background-color: #FFFFFF !important;
        box-shadow: 0px 0px 15px rgba(224, 122, 95, 0.15) !important;
    }
    
    /* === MENGUBAH PLOTLY CHART MENJADI KARTU === */
    [data-testid="stPlotlyChart"] {
        background-color: #FFFFFF; padding: 20px; border-radius: 24px;
        box-shadow: 0px 8px 20px rgba(61, 64, 91, 0.04); border: 1px solid #E8E5D1;
        transition: all 0.2s cubic-bezier(0.25, 0.8, 0.25, 1);
    }
    [data-testid="stPlotlyChart"]:hover {
        transform: translateY(-4px); box-shadow: 0px 15px 30px rgba(61, 64, 91, 0.08); border-color: #D3D0C2;
    }

    /* === MENGUBAH DATAFRAME MENJADI KARTU === */
    [data-testid="stDataFrame"] {
        border-radius: 20px !important;
        box-shadow: 0px 8px 20px rgba(61, 64, 91, 0.04) !important; 
        border: 1px solid #E8E5D1 !important; overflow: hidden !important; 
        transition: all 0.2s ease;
    }
    [data-testid="stDataFrame"]:hover {
        transform: translateY(-3px); box-shadow: 0px 12px 25px rgba(61, 64, 91, 0.08) !important;
    }

    /* === GAYA KARTU MANUAL (TEMA NAVY BLUE) === */
    .card-blue {
        background: linear-gradient(135deg, #3D405B 0%, #2A2C40 100%);
        padding: 24px; border-radius: 24px; 
        box-shadow: 0px 15px 30px rgba(61, 64, 91, 0.2); 
        height: 100%; min-height: 150px;
        display: flex; flex-direction: column; justify-content: center;
        transition: all 0.2s cubic-bezier(0.25, 0.8, 0.25, 1); cursor: pointer;
        position: relative; overflow: hidden;
    }
    /* Efek cahaya mengkilap pada kartu gelap */
    .card-blue::after {
        content: ''; position: absolute; top: -50%; left: -50%;
        width: 200%; height: 200%;
        background: linear-gradient(to right, rgba(255,255,255,0) 0%, rgba(255,255,255,0.05) 50%, rgba(255,255,255,0) 100%);
        transform: rotate(30deg); animation: shine 6s infinite;
    }
    @keyframes shine { 0% { transform: translateX(-100%) rotate(30deg); } 20%, 100% { transform: translateX(100%) rotate(30deg); } }
    
    .card-blue:hover { transform: translateY(-5px); box-shadow: 0px 20px 40px rgba(61, 64, 91, 0.3); }
    .card-blue:active { transform: scale(0.96); box-shadow: 0px 5px 15px rgba(61, 64, 91, 0.15); }
    .card-blue .card-label { font-size: 14px; color: #F4F1DE; font-weight: 600; margin-bottom: 8px; position: relative; z-index: 2;}
    .card-blue .card-value { font-size: 32px; font-weight: 800; color: #FFFFFF; line-height: 1.2; position: relative; z-index: 2;}
    .card-blue .card-subtext { font-size: 13px; color: #D3D0C2; margin-top: 10px; font-weight: 500; position: relative; z-index: 2;}
    
    .card-white {
        background-color: #FFFFFF; padding: 24px; border-radius: 24px;
        box-shadow: 0px 8px 20px rgba(61, 64, 91, 0.04); 
        height: 100%; min-height: 150px;
        display: flex; flex-direction: column; justify-content: center;
        border: 1px solid #E8E5D1; transition: all 0.2s cubic-bezier(0.25, 0.8, 0.25, 1); cursor: pointer;
    }
    .card-white:hover { transform: translateY(-4px); box-shadow: 0px 15px 30px rgba(61, 64, 91, 0.08); border-color: #D3D0C2; }
    .card-white:active { transform: scale(0.97); box-shadow: 0px 4px 10px rgba(61, 64, 91, 0.05); }
    .card-white .card-label { font-size: 14px; color: #6D6D6D; font-weight: 600; margin-bottom: 8px; }
    .card-white .card-value { font-size: 28px; font-weight: 800; color: #2A2A2A; line-height: 1.2; }
    .card-white .card-subtext { font-size: 13px; color: #8C8C8C; margin-top: 10px; font-weight: 500;}
    
    /* Header Texts */
    .header-title { color: #2A2A2A; font-size: 30px; font-weight: 800; margin-bottom: 5px; }
    .header-subtitle { color: #6D6D6D; font-size: 15px; font-weight: 500; margin-bottom: 25px; }
    [data-testid="column"] > div { height: 100%; }
</style>
""", unsafe_allow_html=True)

# --- 3. CORE MATHEMATICS ENGINE ---
class KalkulatorAktuariaLengkap:
    def __init__(self, file_excel):
        self.df = pd.read_excel(file_excel)
        usia_teks = self.df.iloc[:, 0].astype(str).str.replace(',', '.')
        qx_teks = self.df.iloc[:, 1].astype(str).str.replace(',', '.')
        self.df['Usia'] = pd.to_numeric(usia_teks, errors='coerce')
        self.df['qx'] = pd.to_numeric(qx_teks, errors='coerce')
        self.df = self.df.dropna(subset=['Usia', 'qx'])
        
        usia = self.df['Usia'].astype(int).tolist()
        qx = self.df['qx'].tolist()
        
        lx = [100000]
        dx = []
        for q in qx:
            meninggal = lx[-1] * q
            dx.append(meninggal)
            lx.append(lx[-1] - meninggal)
            
        self.df['Usia'] = usia
        self.df['lx'] = lx[:-1]
        self.df['dx'] = dx
        self.omega = int(self.df['Usia'].max()) + 1

    def hitung_A_diskrit(self, usia, n, bunga, momen=1):
        v = 1 / (1 + bunga) if momen == 1 else 1 / ((1 + bunga) ** 2)
        if self.df.loc[self.df['Usia'] == usia, 'lx'].empty: return 0
        lx_awal = self.df.loc[self.df['Usia'] == usia, 'lx'].values[0]
        premi = 0
        for k in range(n):
            if usia + k >= self.omega: break
            data_dx = self.df.loc[self.df['Usia'] == usia + k, 'dx']
            if data_dx.empty: break
            premi += (v ** (k + 1)) * (data_dx.values[0] / lx_awal)
        return premi

    def hitung_E_diskrit(self, usia, n, bunga, momen=1):
        v = 1 / (1 + bunga) if momen == 1 else 1 / ((1 + bunga) ** 2)
        if self.df.loc[self.df['Usia'] == usia, 'lx'].empty: return 0
        lx_awal = self.df.loc[self.df['Usia'] == usia, 'lx'].values[0]
        data_akhir = self.df.loc[self.df['Usia'] == usia + n, 'lx']
        lx_akhir = 0 if (usia + n >= self.omega or data_akhir.empty) else data_akhir.values[0]
        return (v ** n) * (lx_akhir / lx_awal)

    def hitung_semua(self, usia, n, bunga, manfaat, tipe="Diskrit"):
        A1_diskrit = self.hitung_A_diskrit(usia, n, bunga, momen=1)
        E = self.hitung_E_diskrit(usia, n, bunga, momen=1)
        A_whole_diskrit = self.hitung_A_diskrit(usia, self.omega - usia, bunga, momen=1)
        
        A_dwiguna_diskrit = A1_diskrit + E
        d = bunga / (1 + bunga)
        ax_n = (1 - A_dwiguna_diskrit) / d if d != 0 else n
        ax_whole = (1 - A_whole_diskrit) / d if d != 0 else (self.omega - usia)

        A1_m2_diskrit = self.hitung_A_diskrit(usia, n, bunga, momen=2)
        E_m2 = self.hitung_E_diskrit(usia, n, bunga, momen=2)
        
        if tipe == "Kontinu":
            faktor_akselerasi = (1 + bunga) ** 0.5
            A1 = A1_diskrit * faktor_akselerasi
            A_whole = A_whole_diskrit * faktor_akselerasi
            faktor_akselerasi_m2 = (1 + bunga) 
            A1_m2 = A1_m2_diskrit * faktor_akselerasi_m2
        else:
            A1 = A1_diskrit
            A_whole = A_whole_diskrit
            A1_m2 = A1_m2_diskrit
            
        A_dwiguna = A1 + E
        premi_tahunan = A_dwiguna / ax_n if ax_n != 0 else 0
        A_dwiguna_m2 = A1_m2 + E_m2
        var_z = A_dwiguna_m2 - (A_dwiguna ** 2)
        std_dev = np.sqrt(max(0, (manfaat ** 2) * var_z))
        
        return {
            "A1_berjangka": A1, "A_seumurhidup": A_whole, "A_dwiguna": A_dwiguna, "E_murni": E,
            "ax_n": ax_n, "ax_whole": ax_whole, "premi_tahunan": premi_tahunan, "Var_Z": var_z, "Std_Dev": std_dev
        }

    def hitung_alur_cadangan(self, usia, n, bunga, manfaat, tipe="Diskrit"):
        data_hasil = self.hitung_semua(usia, n, bunga, manfaat, tipe)
        P_tahunan = data_hasil['premi_tahunan']
        d = bunga / (1 + bunga)
        list_tahun, list_cadangan = [], []
        
        for t in range(n + 1):
            sisa_masa = n - t
            usia_berjalan = usia + t
            if sisa_masa == 0:
                cadangan = 1.0 
            else:
                A1_sisa_diskrit = self.hitung_A_diskrit(usia_berjalan, sisa_masa, bunga, momen=1)
                E_sisa = self.hitung_E_diskrit(usia_berjalan, sisa_masa, bunga, momen=1)
                A_dwiguna_sisa_diskrit = A1_sisa_diskrit + E_sisa
                ax_sisa = (1 - A_dwiguna_sisa_diskrit) / d if d != 0 else sisa_masa
                
                if tipe == "Kontinu":
                    A1_sisa = A1_sisa_diskrit * ((1 + bunga) ** 0.5)
                else:
                    A1_sisa = A1_sisa_diskrit
                    
                A_dwiguna_sisa = A1_sisa + E_sisa
                cadangan = A_dwiguna_sisa - (P_tahunan * ax_sisa)
            
            list_tahun.append(t)
            list_cadangan.append(max(0.0, cadangan * manfaat))
            
        return pd.DataFrame({"Tahun Ke-": list_tahun, "Cadangan (Rp)": list_cadangan})


# --- 4. TOP BAR NAVIGATION & INPUTS ---
col_logo, col_space = st.columns([1, 10])
with col_logo:
    # Membungkus logo dengan container untuk efek 3D CSS
    st.markdown("""
        <div class='logo-3d-container'>
            <div class='logo-3d'>AK</div>
        </div>
    """, unsafe_allow_html=True)

menu_halaman = st.radio(
    "Navigasi", 
    ["📊 Dashboard", "📈 Simulator Cadangan", "📋 Tabel Kehidupan", "💡 Edukasi Asuransi"], 
    horizontal=True, 
    label_visibility="collapsed"
)

# Tampilkan Pengaturan Polis di semua halaman
with st.container(border=True):
    # Penambahan ikon dengan warna Navy
    st.markdown("<p style='font-size:16px; color:#3D405B; font-weight:800; margin-bottom: 5px;'>⚙️ Pengaturan Profil Pengguna</p>", unsafe_allow_html=True)
    c_in1, c_in2, c_in3, c_in4, c_in5 = st.columns(5)
    with c_in1: in_tipe = st.selectbox("Model", ["Diskrit", "Kontinu"])
    with c_in2: in_usia = st.number_input("Usia Saat Ini", min_value=5, max_value=90, value=35)
    with c_in3: in_n = st.number_input("Masa Asuransi (Thn)", min_value=1, max_value=50, value=20)
    with c_in4: in_bunga = st.number_input("Asumsi Bunga (%)", min_value=0.5, max_value=15.0, value=6.0, step=0.5) / 100
    with c_in5: in_manfaat = st.number_input("Target Santunan (Rp)", min_value=1000000, value=200000000, step=10000000)

st.write("") # Spacer

try:
    engine = KalkulatorAktuariaLengkap("Tabel_Mortalitas_Lengkap.xlsx")
    calc_data = engine.hitung_semua(in_usia, in_n, in_bunga, in_manfaat, in_tipe)
except Exception as e:
    st.error(f"Gagal memuat basis data: {e}. Pastikan file Excel tersedia di folder yang sama.")
    st.stop()


# --- HALAMAN 1: DASHBOARD PREMI UTAMA ---
if menu_halaman == "📊 Dashboard":
    st.markdown("<div class='header-title'>Ringkasan Perlindungan Anda</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='header-subtitle'>Menerjemahkan angka aktuaria model <b>{in_tipe}</b> menjadi wawasan finansial yang mudah dipahami.</div>", unsafe_allow_html=True)
    
    # 1. Baris Pertama: Kartu Harga dengan Detail Hitungan
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""<div class='card-blue' style='margin-bottom: 5px;'>
            <div class='card-label'>🔥 Proteksi Murni (Term Life)</div>
            <div class='card-value'>Rp {calc_data['A1_berjangka']*in_manfaat:,.0f}</div>
            <div class='card-subtext' style='margin-top:5px;'>Paling murah. Murni untuk uang duka. Hangus jika sehat.</div>
        </div>""", unsafe_allow_html=True)
        # Fitur Detail Matematis
        with st.expander("🧮 Lihat Detail Matematis"):
            if in_tipe == "Diskrit":
                st.markdown(r"$$A_{x:\overline{n}|}^1 = \sum_{k=0}^{n-1} v^{k+1} \cdot _{k|}q_x$$")
            else:
                st.markdown(r"$$\overline{A}_{x:\overline{n}|}^1 \approx A_{x:\overline{n}|}^1 \times (1+i)^{0.5}$$")
            st.markdown(f"<div style='font-size:13px; color:#6D6D6D;'><b>Faktor Aktuaria ($A$):</b> {calc_data['A1_berjangka']:.6f}<br><b>Kalkulasi:</b> {calc_data['A1_berjangka']:.6f} × Rp {in_manfaat:,.0f}</div>", unsafe_allow_html=True)

    with c2:
        st.markdown(f"""<div class='card-blue' style='margin-bottom: 5px;'>
            <div class='card-label'>❤️ Seumur Hidup (Whole Life)</div>
            <div class='card-value'>Rp {calc_data['A_seumurhidup']*in_manfaat:,.0f}</div>
            <div class='card-subtext' style='margin-top:5px;'>Harga menengah. Pasti cair kapanpun tutup usia (Warisan).</div>
        </div>""", unsafe_allow_html=True)
        # Fitur Detail Matematis
        with st.expander("🧮 Lihat Detail Matematis"):
            if in_tipe == "Diskrit":
                st.markdown(r"$$A_x = \sum_{k=0}^{\infty} v^{k+1} \cdot _{k|}q_x$$")
            else:
                st.markdown(r"$$\overline{A}_x \approx A_x \times (1+i)^{0.5}$$")
            st.markdown(f"<div style='font-size:13px; color:#6D6D6D;'><b>Faktor Aktuaria ($A$):</b> {calc_data['A_seumurhidup']:.6f}<br><b>Kalkulasi:</b> {calc_data['A_seumurhidup']:.6f} × Rp {in_manfaat:,.0f}</div>", unsafe_allow_html=True)

    with c3:
        st.markdown(f"""<div class='card-blue' style='margin-bottom: 5px;'>
            <div class='card-label'>🍃 Proteksi + Tabungan (Dwiguna)</div>
            <div class='card-value'>Rp {calc_data['A_dwiguna']*in_manfaat:,.0f}</div>
            <div class='card-subtext' style='margin-top:5px;'>Paling mahal. Ada asuransi & tabungan pasti cair.</div>
        </div>""", unsafe_allow_html=True)
        # Fitur Detail Matematis
        with st.expander("🧮 Lihat Detail Matematis"):
            if in_tipe == "Diskrit":
                st.markdown(r"$$A_{x:\overline{n}|} = A_{x:\overline{n}|}^1 + A_{x:\overline{n}|}^{\ \ 1}$$")
            else:
                st.markdown(r"$$\overline{A}_{x:\overline{n}|} = \overline{A}_{x:\overline{n}|}^1 + A_{x:\overline{n}|}^{\ \ 1}$$")
            st.markdown(f"<div style='font-size:13px; color:#6D6D6D;'><b>Faktor Aktuaria ($A$):</b> {calc_data['A_dwiguna']:.6f}<br><b>Kalkulasi:</b> {calc_data['A_dwiguna']:.6f} × Rp {in_manfaat:,.0f}</div>", unsafe_allow_html=True)

    st.write("")
    
    # Menghitung Peluang Hidup
    lx_awal = engine.df.loc[engine.df['Usia'] == in_usia, 'lx'].values[0]
    lx_akhir_data = engine.df.loc[engine.df['Usia'] == in_usia + in_n, 'lx']
    lx_akhir = lx_akhir_data.values[0] if not lx_akhir_data.empty else 0
    peluang_hidup = (lx_akhir / lx_awal) * 100 if lx_awal > 0 else 0
    
    # Menghitung Leverage
    premi_thn = calc_data['premi_tahunan'] * in_manfaat
    leverage = in_manfaat / premi_thn if premi_thn > 0 else 0

    if peluang_hidup >= 80:
        warna_peluang = "#81B29A" # Sage Green
        teks_peluang = "Peluang sehat <b>sangat tinggi</b>. Memiliki elemen <b>Tabungan</b> sangat masuk akal agar uang tidak hangus."
    elif peluang_hidup >= 60:
        warna_peluang = "#F2CC8F" # Soft Yellow
        teks_peluang = "Peluang sehat <b>cukup baik</b>. Memadukan perlindungan jiwa dengan tabungan adalah pilihan yang seimbang."
    elif peluang_hidup >= 40:
        warna_peluang = "#E07A5F" # Terracotta
        teks_peluang = "Peluang sehat <b>rendah</b>. Risiko mulai meningkat, pertimbangkan untuk memperbesar porsi asuransi jiwa murni."
    else:
        warna_peluang = "#D62828" # Deep Red
        teks_peluang = "Peluang sehat <b>sangat rendah</b>. Sangat disarankan fokus pada asuransi proteksi untuk perlindungan maksimal keluarga."

    # 2. Baris Kedua: Insight
    c4, c5 = st.columns(2)
    with c4:
        st.markdown(f"""<div class='card-white'>
            <div class='card-label'>✨ Daya Ungkit Uang Anda (Leverage)</div>
            <div class='card-value'>{leverage:,.1f} x Lipat</div>
            <div class='card-subtext'>Dengan premi tahunan Dwiguna <b style='color:#E07A5F;'>Rp {premi_thn:,.0f}</b>, jika risiko terjadi di tahun pertama, uang Anda membesar seketika menjadi <b>Rp {in_manfaat:,.0f}</b>.</div>
        </div>""", unsafe_allow_html=True)
    with c5:
        st.markdown(f"""<div class='card-white'>
            <div class='card-label'>📊 Peluang Sehat Hingga Kontrak Usai</div>
            <div style='font-size: 28px; font-weight: 800; color: {warna_peluang}; line-height: 1.2;'>{peluang_hidup:,.1f} %</div>
            <div class='card-subtext'>Secara statistik, ini adalah peluang Anda hidup {in_n} tahun ke depan. {teks_peluang}</div>
        </div>""", unsafe_allow_html=True)

    st.write("")

    # 3. Baris Ketiga: Grafik Alokasi dengan warna Navy dan Sage Green
    col_chart, col_text = st.columns([2, 1.2])
    with col_chart:
        st.markdown("<p style='font-size:16px; color:#3D405B; font-weight:800; margin-bottom: 5px;'>Komposisi Penggunaan Uang Anda (Dwiguna)</p>", unsafe_allow_html=True)
        p_pro = calc_data['A1_berjangka']
        p_tab = calc_data['E_murni']
        
        fig = px.pie(
            names=["Biaya Risiko (Proteksi)", "Tabungan Murni"],
            values=[p_pro, p_tab],
            hole=0.65,
            color_discrete_sequence=['#3D405B', '#81B29A'] # Navy dan Sage Green
        )
        fig.update_traces(sort=False) 
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color="#2A2A2A", size=13), margin=dict(t=15, b=15, l=10, r=10),
            legend=dict(orientation="h", y=-0.15, x=0.5, xanchor="center")
        )
        st.plotly_chart(fig, use_container_width=True)
        
    with col_text:
        st.markdown("<p style='font-size:16px; color:#3D405B; font-weight:800; margin-bottom: 5px;'>Kesimpulan Sistem</p>", unsafe_allow_html=True)
        
        if p_tab > p_pro:
            kesimpulan = "Sebagian besar uang Anda masuk ke <b>Tabungan</b>. Cocok untuk tujuan dana pendidikan atau pensiun pasti."
        else:
            kesimpulan = "Sebagian besar uang Anda digunakan untuk menanggung risiko tinggi. Pastikan perlindungan ini memang Anda butuhkan saat ini."
            
        st.markdown(f"""
        <div class='card-white' style='justify-content: start; border: 1px solid #E8E5D1; box-shadow: none;'>
            <h5 style="margin-top:0px; color:#3D405B; font-weight:800;">💡 Pahami Tagihan Anda</h5>
            <p style='font-size:14px; line-height:1.7; color:#6D6D6D; margin-bottom: 10px; margin-top: 15px;'>
            Banyak yang mengira premi Dwiguna sepenuhnya ditabung. Faktanya:<br><br>
            <span style='color:#3D405B; font-weight:700;'>• {(p_pro/(p_pro+p_tab))*100:.2f}% (Navy Gelap):</span><br>
            Adalah biaya "hangus" untuk membayar proteksi jiwa Anda.<br><br>
            <span style='color:#81B29A; font-weight:700;'>• {(p_tab/(p_pro+p_tab))*100:.2f}% (Hijau Sage):</span><br>
            Barulah dana riil yang ditabung dan akan Anda terima utuh nanti.
            <br><br>
            <b style='color:#2A2A2A;'>Ringkasan:</b> {kesimpulan}
            </p>
        </div>
        """, unsafe_allow_html=True)

# --- HALAMAN 2: SIMULATOR CADANGAN AKHIR ---
elif menu_halaman == "📈 Simulator Cadangan":
    st.markdown("<div class='header-title'>Proyeksi Saldo Nilai Tunai</div>", unsafe_allow_html=True)
    st.markdown("<div class='header-subtitle'>Melihat pertumbuhan uang Anda (cadangan premi) dari tahun ke tahun.</div>", unsafe_allow_html=True)
    
    df_cadangan = engine.hitung_alur_cadangan(in_usia, in_n, in_bunga, in_manfaat, in_tipe)
    
    c_left, c_right = st.columns([2.5, 1])
    with c_left:
        st.markdown("<p style='font-size:16px; color:#3D405B; font-weight:800; margin-bottom: 5px;'>Kurva Pertumbuhan Tunai</p>", unsafe_allow_html=True)
        fig_line = go.Figure()
        fig_line.add_trace(go.Scatter(
            x=df_cadangan["Tahun Ke-"], y=df_cadangan["Cadangan (Rp)"],
            mode='lines+markers', name='Cadangan',
            line=dict(color='#E07A5F', width=4, shape='spline'), 
            marker=dict(size=8, color='#FFFFFF', line=dict(color='#E07A5F', width=2))
        ))
        
        fig_line.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color="#2A2A2A"), xaxis_title="Tahun Polis Berjalan", yaxis_title="Saldo Tunai (Rp)",
            xaxis=dict(showgrid=True, gridcolor='#E8E5D1'),
            yaxis=dict(showgrid=True, gridcolor='#E8E5D1'),
            margin=dict(t=20, b=20, l=10, r=10)
        )
        st.plotly_chart(fig_line, use_container_width=True)
        
    with c_right:
        st.markdown("<p style='font-size:16px; color:#3D405B; font-weight:800; margin-bottom: 5px;'>Tabel Saldo</p>", unsafe_allow_html=True)
        st.dataframe(
            df_cadangan.style.format({"Cadangan (Rp)": "Rp {:,.0f}"}),
            use_container_width=True, height=380
        )

# --- HALAMAN 3: TABEL MORTALITAS & DATA KEHIDUPAN ---
elif menu_halaman == "📋 Tabel Kehidupan":
    st.markdown("<div class='header-title'>Tabel Statistik Kehidupan</div>", unsafe_allow_html=True)
    st.markdown("<div class='header-subtitle'>Data dasar (mortalitas) yang digunakan perusahaan asuransi untuk menghitung risiko.</div>", unsafe_allow_html=True)
    
    df_tampil = engine.df[['Usia', 'qx', 'lx', 'dx']].copy()
    
    st.dataframe(
        df_tampil.style.format({
            "qx": "{:.5f}",
            "lx": "{:,.2f}",
            "dx": "{:,.2f}"
        }),
        use_container_width=True, height=550
    )

# --- HALAMAN 4: EDUKASI ASURANSI (SIMULASI UNTUK AWAM) ---
elif menu_halaman == "💡 Edukasi Asuransi":
    st.markdown("<div class='header-title'>Simulasi Realita Asuransi</div>", unsafe_allow_html=True)
    st.markdown("<div class='header-subtitle'>Memahami rahasia di balik perhitungan asuransi dengan bahasa sehari-hari.</div>", unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown("<p style='font-size:16px; color:#3D405B; font-weight:800; margin-bottom: 5px;'>Pilih Topik Pembelajaran</p>", unsafe_allow_html=True)
        topik_edukasi = st.selectbox("Topik:", [
            "1. Pilih Asuransi: Mana Paling Cuan? (Term vs Whole vs Endowment)",
            "2. Rahasia Harga: Apakah Perusahaan Untung Besar?",
            "3. Mesin Waktu: Mengapa Uang Saya Kecil Jika Berhenti Cepat?",
            "4. Kalkulator Risiko: Harga Menunda Asuransi 10 Tahun"
        ], label_visibility="collapsed")
        
    st.write("")

    # Topik 1
    if "Pilih Asuransi" in topik_edukasi:
        st.info("**Konsep:** Setiap asuransi punya tujuan berbeda. Jika Anda punya budget tetap setiap bulan, lihat seberapa besar Uang Pertanggungan (Santunan) yang bisa keluarga Anda dapatkan berdasarkan jenis asuransinya.")
        
        budget_bulanan = st.number_input("Coba masukkan budget asuransi Anda per bulan (Rp):", value=500000, step=50000)
        budget_tahunan = budget_bulanan * 12
        
        a_term = calc_data['A1_berjangka']
        a_whole = calc_data['A_seumurhidup']
        a_endow = calc_data['A_dwiguna']
        
        up_term = (budget_tahunan * calc_data['ax_n']) / a_term if a_term else 0
        up_whole = (budget_tahunan * calc_data['ax_whole']) / a_whole if a_whole else 0
        up_endow = (budget_tahunan * calc_data['ax_n']) / a_endow if a_endow else 0
        
        st.write("")
        c_mod1, c_mod2, c_mod3 = st.columns(3)
        with c_mod1:
            st.markdown(f"""<div class='card-white' style='height:100%; border-color:#81B29A;'>
                <div class='card-label'>🔥 Proteksi Murni (Term Life)</div>
                <div style='font-size: 24px; font-weight: 800; color: #3D405B;'>Rp {up_term:,.0f}</div>
                <div class='card-subtext'><b>Cocok untuk:</b> Pencari nafkah utama.<br><b>Kelemahan:</b> Jika sehat sampai akhir kontrak ({in_n} thn), uang hangus.</div>
            </div>""", unsafe_allow_html=True)
        with c_mod2:
            st.markdown(f"""<div class='card-white' style='height:100%; border-color:#81B29A;'>
                <div class='card-label'>❤️ Seumur Hidup (Whole Life)</div>
                <div style='font-size: 24px; font-weight: 800; color: #3D405B;'>Rp {up_whole:,.0f}</div>
                <div class='card-subtext'><b>Cocok untuk:</b> Warisan pasti untuk anak.<br><b>Kelemahan:</b> Santunan lebih kecil dari Term Life.</div>
            </div>""", unsafe_allow_html=True)
        with c_mod3:
            st.markdown(f"""<div class='card-white' style='height:100%; border-color:#81B29A;'>
                <div class='card-label'>🍃 Dwiguna (Endowment)</div>
                <div style='font-size: 24px; font-weight: 800; color: #3D405B;'>Rp {up_endow:,.0f}</div>
                <div class='card-subtext'><b>Cocok untuk:</b> Dana pendidikan/pensiun.<br><b>Kelemahan:</b> Santunan meninggalnya paling kecil karena sebagian besar uang ditabung.</div>
            </div>""", unsafe_allow_html=True)

    # Topik 2
    elif "Rahasia Harga" in topik_edukasi:
        st.info("**Konsep:** 'Prinsip Ekuivalensi'. Sederhananya, perusahaan asuransi menghitung premi secara pas-pasan. Nilai semua premi yang dibayar nasabah = Nilai klaim yang akan dicairkan.")
        
        total_premi_kasar = calc_data['premi_tahunan'] * in_manfaat * in_n
        
        c_mod1, c_mod2 = st.columns(2)
        with c_mod1:
            st.markdown(f"""<div class='card-white' style='height:100%;'>
                <div class='card-label'>Total Premi Jika Dicicil ({in_n} Tahun)</div>
                <div class='card-value'>Rp {total_premi_kasar:,.0f}</div>
                <div class='card-subtext'>Total cicilan ini lebih murah dari santunan Rp {in_manfaat:,.0f} karena uang Anda dikembangkan melalui investasi (bunga {in_bunga*100}%).</div>
            </div>""", unsafe_allow_html=True)
        with c_mod2:
            st.markdown(f"""<div class='card-blue' style='height:100%;'>
                <div class='card-label'>Harga Asli Hari Ini (Premi Tunggal)</div>
                <div class='card-value'>Rp {calc_data['A_dwiguna']*in_manfaat:,.0f}</div>
                <div class='card-subtext' style='color:#F4F1DE;'>Jika Anda bayar tunai sekaligus hari ini, inilah harga asli dari risiko dan tabungan asuransi Anda.</div>
            </div>""", unsafe_allow_html=True)

    # Topik 3
    elif "Mesin Waktu" in topik_edukasi:
        st.info("**Konsep:** Kenapa membatalkan polis di tahun-tahun awal sangat merugikan? Karena perusahaan harus memotong biaya medis, operasional agen, dan mencadangkan dana klaim untuk mereka yang kurang beruntung meninggal di tahun pertama.")
        
        tahun_batal = st.slider("Coba simulasikan membatalkan asuransi di Tahun Ke-", 1, int(in_n), min(3, int(in_n)))
        
        df_cadangan = engine.hitung_alur_cadangan(in_usia, in_n, in_bunga, in_manfaat, in_tipe)
        row_cad = df_cadangan[df_cadangan['Tahun Ke-'] == tahun_batal]
        nilai_cair = row_cad['Cadangan (Rp)'].values[0] if not row_cad.empty else 0
        total_dibayar = calc_data['premi_tahunan'] * in_manfaat * tahun_batal
        
        c_mod1, c_mod2 = st.columns(2)
        with c_mod1:
            st.markdown(f"""<div class='card-white' style='height:100%;'>
                <div class='card-label'>Total Premi Yang Telah Disetor</div>
                <div class='card-value'>Rp {total_dibayar:,.0f}</div>
                <div class='card-subtext'>Selama {tahun_batal} tahun berturut-turut.</div>
            </div>""", unsafe_allow_html=True)
        with c_mod2:
            warna_teks = "#D62828" if nilai_cair < total_dibayar else "#81B29A"
            st.markdown(f"""<div class='card-white' style='height:100%; border: 2px solid {warna_teks};'>
                <div class='card-label'>Uang Yang Bisa Dicairkan (Nilai Tunai)</div>
                <div style='font-size: 28px; font-weight: 800; color: {warna_teks};'>Rp {nilai_cair:,.0f}</div>
                <div class='card-subtext'>Sebagian uang Anda telah dialokasikan untuk membayar klaim peserta lain yang meninggal pada periode ini. Itulah prinsip gotong-royong asuransi.</div>
            </div>""", unsafe_allow_html=True)

    # Topik 4
    elif "Kalkulator Risiko" in topik_edukasi:
        st.info("**Konsep:** Harga asuransi ditentukan oleh seberapa besar kemungkinan seseorang tutup usia (Fungsi Mortalitas). Semakin ditunda, statistik risikonya akan melonjak drastis.")
        
        row_now = engine.df[engine.df['Usia'] == in_usia]
        qx_now = row_now['qx'].values[0] if not row_now.empty else 0
        
        usia_delay = min(int(in_usia) + 10, 90)
        row_delay = engine.df[engine.df['Usia'] == usia_delay]
        qx_delay = row_delay['qx'].values[0] if not row_delay.empty else 0
        
        try:
            calc_delay = engine.hitung_semua(usia_delay, in_n, in_bunga, in_manfaat, in_tipe)
            premi_sekarang = calc_data['premi_tahunan'] * in_manfaat
            premi_nanti = calc_delay['premi_tahunan'] * in_manfaat
            kenaikan = ((premi_nanti - premi_sekarang) / premi_sekarang) * 100 if premi_sekarang else 0
        except:
            premi_sekarang, premi_nanti, kenaikan = 0, 0, 0
            
        c_mod1, c_mod2 = st.columns(2)
        with c_mod1:
            st.markdown(f"""<div class='card-white' style='height:100%;'>
                <div class='card-label'>Statistik Risiko Usia {in_usia} Tahun</div>
                <div class='card-value'>{qx_now*1000:.1f} dari 1.000</div>
                <div class='card-subtext'>Orang seusia Anda diproyeksikan akan tutup usia tahun ini.<br><b style='color:#3D405B;'>Premi Tahunan: Rp {premi_sekarang:,.0f}</b></div>
            </div>""", unsafe_allow_html=True)
        with c_mod2:
            st.markdown(f"""<div class='card-blue' style='height:100%;'>
                <div class='card-label'>Statistik Jika Menunda (Usia {usia_delay})</div>
                <div class='card-value'>{qx_delay*1000:.1f} dari 1.000</div>
                <div class='card-subtext' style='color:#F4F1DE;'>Risiko melonjak! Harga premi tahunan Anda akan naik menjadi <b>Rp {premi_nanti:,.0f}</b> (Naik {kenaikan:.1f}%!).</div>
            </div>""", unsafe_allow_html=True)