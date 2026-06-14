import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import io # Ditambahkan untuk membaca file upload

# --- 1. CONFIG HALAMAN & TEMPLATE UTAMA ---
st.set_page_config(
    page_title="Aktuaria Modern UI", 
    page_icon="📱", 
    layout="wide",
    initial_sidebar_state="expanded" 
)

# --- INISIALISASI SESSION STATE UNTUK TABEL KEHIDUPAN ---
if "file_tabel" not in st.session_state:
    st.session_state.file_tabel = "Tabel_Mortalitas_Lengkap.xlsx"

# --- 2. CSS SUNTIKAN: TEMA WARNA BARU & ANIMASI ---
st.markdown("""
<style>
    /* === Latar Belakang Utama === */
    .stApp { 
        background-color: #eafdf8 !important; 
        color: #00033D !important; 
        font-family: 'Segoe UI', sans-serif; 
    }
    
    /* === PENGATURAN SIDEBAR (MENU TETAP) === */
    [data-testid="stSidebar"] { 
        background-color: #00033D !important; 
        border-right: 2px solid #0033ff;
    }
    
    /* Menyembunyikan header default bawaan sidebar */
    [data-testid="stSidebarNav"] { display: none; }
    
    /* Warna teks menu di sidebar */
    [data-testid="stSidebar"] .stRadio p { color: #eafdf8 !important; font-weight: 800; font-size: 16px; margin-bottom: 10px; }
    
    /* Styling tombol radio navigasi pada sidebar */
    [data-testid="stSidebar"] div.row-widget.stRadio > div { flex-direction: column; gap: 10px; }
    [data-testid="stSidebar"] div.row-widget.stRadio > div > label { 
        background-color: rgba(151, 125, 255, 0.1); 
        padding: 15px 20px; 
        border-radius: 12px; 
        cursor: pointer; 
        transition: all 0.3s ease;
        border: 1px solid transparent;
        width: 100%;
    }
    [data-testid="stSidebar"] div.row-widget.stRadio > div > label:hover { 
        background-color: rgba(151, 125, 255, 0.3); 
        border-color: #977dff;
        transform: translateX(5px);
    }
    /* Warna Aktif pada Tab */
    [data-testid="stSidebar"] div.row-widget.stRadio > div > label[data-checked="true"] { 
        background-color: #0033ff !important; 
        box-shadow: 0px 6px 15px rgba(0, 51, 255, 0.4) !important;
        border-color: #eafdf8;
    }
    [data-testid="stSidebar"] div.row-widget.stRadio > div > label p { margin-bottom: 0px !important; }

    /* === ANIMASI 3D LOGO === */
    .logo-3d-container { perspective: 1000px; margin-bottom: 40px; margin-top: 20px; display: flex; justify-content: center; }
    .logo-3d {
        background: linear-gradient(135deg, #0033ff 0%, #977dff 100%);
        border-radius: 50%;
        width: 80px; height: 80px;
        display: flex; align-items: center; justify-content: center;
        color: #eafdf8; font-size: 28px; font-weight: 900;
        box-shadow: 0 10px 25px rgba(0, 51, 255, 0.4), inset 0 -3px 6px rgba(0,0,0,0.2);
        cursor: pointer;
        transform-style: preserve-3d;
        animation: float3d 4s ease-in-out infinite; 
    }
    .logo-3d:hover { animation: spin3d 1.5s linear infinite; box-shadow: 0 0 20px rgba(151, 125, 255, 0.8); }
    
    @keyframes float3d {
        0% { transform: translateY(0px) rotateY(0deg); }
        50% { transform: translateY(-10px) rotateY(20deg); }
        100% { transform: translateY(0px) rotateY(0deg); }
    }
    @keyframes spin3d { 0% { transform: rotateY(0deg); } 100% { transform: rotateY(360deg); } }

    /* === KARTU HASIL (RESULT BARS) SAMA BESAR & ANIMASI === */
    [data-testid="column"] { display: flex !important; flex-direction: column !important; }
    [data-testid="column"] > div { display: flex !important; flex-direction: column !important; flex: 1; height: 100%; }
    
    .card-result {
        background: linear-gradient(135deg, #977dff 0%, #765de0 100%); 
        padding: 24px; 
        border-radius: 20px; 
        box-shadow: 0px 10px 20px rgba(0, 3, 61, 0.1); 
        height: 100%; 
        min-height: 250px; 
        display: flex; 
        flex-direction: column; 
        border: 2px solid transparent;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1); 
        cursor: pointer;
        opacity: 0;
        animation: popIn 0.6s ease-out forwards;
    }
    
    .card-result:hover { 
        transform: translateY(-8px) scale(1.02); 
        box-shadow: 0px 20px 35px rgba(0, 51, 255, 0.3); 
        border-color: #eafdf8; 
    }
    .card-result:active { transform: scale(0.97); }
    
    .card-result .card-label { font-size: 15px; color: #00033D; font-weight: 800; margin-bottom: 8px; }
    .card-result .card-value { font-size: 32px; font-weight: 900; color: #eafdf8; line-height: 1.2; text-shadow: 1px 1px 2px rgba(0,0,0,0.1);}
    .card-result .card-subtext { font-size: 14px; color: #eafdf8; margin-top: auto; padding-top: 15px; font-weight: 600; line-height: 1.4; opacity: 0.9;}

    @keyframes popIn {
        0% { opacity: 0; transform: translateY(30px) scale(0.95); }
        100% { opacity: 1; transform: translateY(0) scale(1); }
    }

    /* === STYLING INPUT BOX STREAMLIT === */
    div[data-baseweb="select"] > div, div[data-baseweb="base-input"] {
        border-radius: 12px !important; background-color: white !important; border: 2px solid #977dff !important; color: #00033D !important;
    }
    div[data-baseweb="select"] > div:focus-within, div[data-baseweb="base-input"]:focus-within {
        border: 2px solid #0033ff !important; box-shadow: 0px 0px 10px rgba(0, 51, 255, 0.3) !important;
    }

    /* === PLOTLY & DATAFRAME CARDS === */
    [data-testid="stPlotlyChart"], [data-testid="stDataFrame"], [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: white !important; 
        border-radius: 20px !important;
        box-shadow: 0px 8px 20px rgba(0, 3, 61, 0.06) !important; 
        border: 1px solid rgba(151, 125, 255, 0.3) !important;
        padding: 15px !important;
        animation: popIn 0.8s ease-out forwards;
    }

    /* Header Texts */
    .header-title { color: #00033D; font-size: 36px; font-weight: 900; margin-bottom: 5px; }
    .header-subtitle { color: #0033ff; font-size: 16px; font-weight: 700; margin-bottom: 30px; }
    
    p, li, span { color: #00033D; }
</style>
""", unsafe_allow_html=True)

# --- 3. CORE MATHEMATICS ENGINE ---
class KalkulatorAktuariaLengkap:
    def __init__(self, data_source):
        # Mengecek apakah input adalah bytes (dari file uploader)
        if isinstance(data_source, bytes):
            data_source = io.BytesIO(data_source)
            
        self.df = pd.read_excel(data_source)
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
            A1_m2 = A1_m2_diskrit * (1 + bunga) 
        else:
            A1, A_whole, A1_m2 = A1_diskrit, A_whole_diskrit, A1_m2_diskrit
            
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
                A1_sisa = A1_sisa_diskrit * ((1 + bunga) ** 0.5) if tipe == "Kontinu" else A1_sisa_diskrit
                cadangan = (A1_sisa + E_sisa) - (P_tahunan * ax_sisa)
            
            list_tahun.append(t)
            list_cadangan.append(max(0.0, cadangan * manfaat))
            
        return pd.DataFrame({"Tahun Ke-": list_tahun, "Cadangan (Rp)": list_cadangan})

# --- 4. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown("""
        <div class='logo-3d-container'>
            <div class='logo-3d'>AK</div>
        </div>
    """, unsafe_allow_html=True)
    
    menu_halaman = st.radio(
        "Navigasi", 
        ["📊 Dashboard", "📈 Simulator Cadangan", "📋 Tabel Kehidupan", "💡 Edukasi Asuransi"], 
        label_visibility="collapsed"
    )

# --- MENGINISIALISASI VARIABEL DEFAULT ---
in_tipe, in_usia, in_n, in_bunga, in_manfaat = "Diskrit", 35, 20, 0.06, 200000000

# --- TAMPILKAN PENGATURAN HANYA PADA HALAMAN YANG MEMBUTUHKAN ---
if menu_halaman in ["📊 Dashboard", "📈 Simulator Cadangan", "💡 Edukasi Asuransi"]:
    with st.container(border=True):
        st.markdown("<p style='font-size:18px; color:#00033D; font-weight:900; margin-bottom: 5px;'>⚙️ Pengaturan Profil Pengguna</p>", unsafe_allow_html=True)
        c_in1, c_in2, c_in3, c_in4, c_in5 = st.columns(5)
        with c_in1: in_tipe = st.selectbox("Model", ["Diskrit", "Kontinu"])
        with c_in2: in_usia = st.number_input("Usia Saat Ini", min_value=5, max_value=90, value=35)
        with c_in3: in_n = st.number_input("Masa Asuransi (Thn)", min_value=1, max_value=50, value=20)
        with c_in4: in_bunga = st.number_input("Asumsi Bunga (%)", min_value=0.5, max_value=15.0, value=6.0, step=0.5) / 100
        with c_in5: in_manfaat = st.number_input("Target Santunan (Rp)", min_value=1000000, value=200000000, step=10000000)
    st.write("") 

try:
    # Memuat tabel kehidupan dari session state (Bisa dari Excel bawaan atau file custom yang diunggah)
    engine = KalkulatorAktuariaLengkap(st.session_state.file_tabel)
    calc_data = engine.hitung_semua(in_usia, in_n, in_bunga, in_manfaat, in_tipe)
except Exception as e:
    st.error(f"Gagal memuat basis data: {e}. Pastikan format tabel sesuai (Kolom Pertama: Usia, Kolom Kedua: qx).")
    st.stop()


# --- HALAMAN 1: DASHBOARD PREMI UTAMA ---
if menu_halaman == "📊 Dashboard":
    st.markdown("<div class='header-title'>Ringkasan Perlindungan Anda</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='header-subtitle'>Menerjemahkan angka aktuaria model <b>{in_tipe}</b> menjadi wawasan finansial.</div>", unsafe_allow_html=True)
    
    # Baris Pertama
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""<div class='card-result'>
            <div class='card-label'>🔥 Proteksi Murni (Term Life)</div>
            <div class='card-value'>Rp {calc_data['A1_berjangka']*in_manfaat:,.0f}</div>
            <div class='card-subtext'>Paling murah. Murni untuk uang duka. Uang hangus jika Anda sehat walafiat di akhir masa asuransi.</div>
        </div>""", unsafe_allow_html=True)

    with c2:
        st.markdown(f"""<div class='card-result'>
            <div class='card-label'>❤️ Seumur Hidup (Whole Life)</div>
            <div class='card-value'>Rp {calc_data['A_seumurhidup']*in_manfaat:,.0f}</div>
            <div class='card-subtext'>Harga menengah. Pasti cair kapanpun tutup usia. Sangat cocok disiapkan sebagai warisan mutlak.</div>
        </div>""", unsafe_allow_html=True)

    with c3:
        st.markdown(f"""<div class='card-result'>
            <div class='card-label'>🍃 Proteksi + Tabungan (Dwiguna)</div>
            <div class='card-value'>Rp {calc_data['A_dwiguna']*in_manfaat:,.0f}</div>
            <div class='card-subtext'>Paling premium. Memiliki kepastian asuransi sekaligus tabungan utuh yang pasti cair.</div>
        </div>""", unsafe_allow_html=True)

    st.write("")
    
    # Perhitungan Insight
    lx_awal = engine.df.loc[engine.df['Usia'] == in_usia, 'lx'].values[0]
    lx_akhir_data = engine.df.loc[engine.df['Usia'] == in_usia + in_n, 'lx']
    lx_akhir = lx_akhir_data.values[0] if not lx_akhir_data.empty else 0
    peluang_hidup = (lx_akhir / lx_awal) * 100 if lx_awal > 0 else 0
    
    premi_thn = calc_data['premi_tahunan'] * in_manfaat
    leverage = in_manfaat / premi_thn if premi_thn > 0 else 0

    # Baris Kedua: Insight
    c4, c5 = st.columns(2)
    with c4:
        st.markdown(f"""<div class='card-result'>
            <div class='card-label'>✨ Daya Ungkit Uang Anda (Leverage)</div>
            <div class='card-value'>{leverage:,.1f} x Lipat</div>
            <div class='card-subtext'>Dengan premi <b style='color:#00033D;'>Rp {premi_thn:,.0f}</b> per tahun, jika risiko terjadi di tahun pertama, uang Anda membesar seketika menjadi <b style='color:#00033D;'>Rp {in_manfaat:,.0f}</b>.</div>
        </div>""", unsafe_allow_html=True)
    with c5:
        st.markdown(f"""<div class='card-result'>
            <div class='card-label'>📊 Peluang Sehat Hingga Kontrak Usai</div>
            <div class='card-value'>{peluang_hidup:,.1f} %</div>
            <div class='card-subtext'>Secara statistik tabel mortalitas, ini adalah persentase peluang kesehatan Anda hidup selama {in_n} tahun ke depan.</div>
        </div>""", unsafe_allow_html=True)

    st.write("")

    # Baris Ketiga: Grafik Alokasi 
    col_chart, col_text = st.columns([2, 1.2])
    with col_chart:
        st.markdown("<p style='font-size:18px; color:#00033D; font-weight:900; margin-bottom: 5px;'>Komposisi Penggunaan Uang Anda</p>", unsafe_allow_html=True)
        p_pro = calc_data['A1_berjangka']
        p_tab = calc_data['E_murni']
        
        fig = px.pie(
            names=["Biaya Risiko (Proteksi)", "Tabungan Murni"],
            values=[p_pro, p_tab],
            hole=0.65,
            color_discrete_sequence=['#0033ff', '#977dff'] # Tema biru & ungu
        )
        fig.update_traces(sort=False) 
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color="#00033D", size=14, weight="bold"), margin=dict(t=15, b=15, l=10, r=10),
            legend=dict(orientation="h", y=-0.15, x=0.5, xanchor="center")
        )
        st.plotly_chart(fig, use_container_width=True)
        
    with col_text:
        st.markdown("<p style='font-size:18px; color:#00033D; font-weight:900; margin-bottom: 5px;'>Kesimpulan Analisis</p>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class='card-result' style='justify-content: start;'>
            <h5 style="margin-top:0px; color:#00033D; font-weight:900;">💡 Breakdown Premi Anda</h5>
            <p style='font-size:14px; line-height:1.7; color:#eafdf8; margin-bottom: 10px; font-weight:600;'>
            <span style='color:#00033D; font-weight:800;'>• {(p_pro/(p_pro+p_tab))*100:.2f}% (Biru):</span><br>
            Merupakan porsi biaya risiko untuk menanggung asuransi jiwa Anda.<br><br>
            <span style='color:#00033D; font-weight:800;'>• {(p_tab/(p_pro+p_tab))*100:.2f}% (Ungu):</span><br>
            Merupakan porsi dana riil yang ditabung oleh perusahaan yang nantinya akan Anda terima kembali.
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
        st.markdown("<p style='font-size:18px; color:#00033D; font-weight:900; margin-bottom: 5px;'>Kurva Pertumbuhan Tunai</p>", unsafe_allow_html=True)
        fig_line = go.Figure()
        fig_line.add_trace(go.Scatter(
            x=df_cadangan["Tahun Ke-"], y=df_cadangan["Cadangan (Rp)"],
            mode='lines+markers', name='Cadangan',
            line=dict(color='#0033ff', width=5, shape='spline'), 
            marker=dict(size=10, color='#eafdf8', line=dict(color='#977dff', width=3))
        ))
        
        fig_line.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color="#00033D", weight="bold"), 
            xaxis_title="Tahun Polis Berjalan", yaxis_title="Saldo Tunai (Rp)",
            xaxis=dict(showgrid=True, gridcolor='rgba(151, 125, 255, 0.3)'),
            yaxis=dict(showgrid=True, gridcolor='rgba(151, 125, 255, 0.3)'),
            margin=dict(t=20, b=20, l=10, r=10)
        )
        st.plotly_chart(fig_line, use_container_width=True)
        
    with c_right:
        st.markdown("<p style='font-size:18px; color:#00033D; font-weight:900; margin-bottom: 5px;'>Tabel Proyeksi Saldo</p>", unsafe_allow_html=True)
        st.dataframe(
            df_cadangan.style.format({"Cadangan (Rp)": "Rp {:,.0f}"}),
            use_container_width=True, height=450
        )

# --- HALAMAN 3: TABEL MORTALITAS & DATA KEHIDUPAN ---
elif menu_halaman == "📋 Tabel Kehidupan":
    st.markdown("<div class='header-title'>Tabel Statistik Kehidupan</div>", unsafe_allow_html=True)
    st.markdown("<div class='header-subtitle'>Data dasar yang digunakan untuk menghitung probabilitas risiko aktuaria.</div>", unsafe_allow_html=True)
    
    # --- FITUR BARU: GANTI TABEL KEHIDUPAN ---
    with st.expander("⚙️ Konfigurasi: Ganti Tabel Mortalitas Kustom", expanded=False):
        st.info("Anda dapat menggunakan tabel mortalitas buatan sendiri. Format harus berupa file **Excel (.xlsx)**. **Kolom Pertama** berisi data Usia, dan **Kolom Kedua** berisi nilai qx (Peluang Meninggal).")
        
        c_up1, c_up2 = st.columns([3, 1])
        with c_up1:
            file_baru = st.file_uploader("Unggah Tabel Anda", type=["xlsx", "xls"], label_visibility="collapsed")
        
        with c_up2:
            st.write("") # Spacer margin
            if st.button("🔄 Reset ke Default", use_container_width=True):
                st.session_state.file_tabel = "Tabel_Mortalitas_Lengkap.xlsx"
                st.rerun()

        if file_baru is not None:
            bytes_data = file_baru.getvalue()
            # Mencegah rerun looping jika data yang diupload sama dengan yang di state
            if isinstance(st.session_state.file_tabel, str) or st.session_state.file_tabel != bytes_data:
                st.session_state.file_tabel = bytes_data
                st.rerun()
                
    st.write("") # Spasi sebelum tabel
    
    df_tampil = engine.df[['Usia', 'qx', 'lx', 'dx']].copy()
    st.dataframe(
        df_tampil.style.format({"qx": "{:.5f}", "lx": "{:,.2f}", "dx": "{:,.2f}"}),
        use_container_width=True, height=550
    )

# --- HALAMAN 4: EDUKASI ASURANSI (SIMULASI UNTUK AWAM) ---
elif menu_halaman == "💡 Edukasi Asuransi":
    st.markdown("<div class='header-title'>Simulasi Realita Asuransi</div>", unsafe_allow_html=True)
    st.markdown("<div class='header-subtitle'>Pahami konsep asuransi dengan simulasi kartu yang interaktif.</div>", unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown("<p style='font-size:18px; color:#00033D; font-weight:900; margin-bottom: 5px;'>Pilih Topik Pembelajaran</p>", unsafe_allow_html=True)
        topik_edukasi = st.selectbox("Topik:", [
            "1. Pilih Asuransi: Mana Paling Cuan?",
            "2. Rahasia Harga: Cicilan vs Tunai",
            "3. Mesin Waktu: Mengapa Membatalkan Polis Rugi?",
            "4. Kalkulator Risiko: Harga Menunda Asuransi"
        ], label_visibility="collapsed")
        
    st.write("")

    if "Pilih Asuransi" in topik_edukasi:
        budget_bulanan = st.number_input("Coba masukkan budget asuransi bulanan Anda (Rp):", value=500000, step=50000)
        budget_tahunan = budget_bulanan * 12
        
        a_term = calc_data['A1_berjangka']
        a_whole = calc_data['A_seumurhidup']
        a_endow = calc_data['A_dwiguna']
        
        up_term = (budget_tahunan * calc_data['ax_n']) / a_term if a_term else 0
        up_whole = (budget_tahunan * calc_data['ax_whole']) / a_whole if a_whole else 0
        up_endow = (budget_tahunan * calc_data['ax_n']) / a_endow if a_endow else 0
        
        c_mod1, c_mod2, c_mod3 = st.columns(3)
        with c_mod1:
            st.markdown(f"""<div class='card-result'>
                <div class='card-label'>🔥 Uang Santunan Term Life</div>
                <div class='card-value'>Rp {up_term:,.0f}</div>
                <div class='card-subtext'>Dengan budget Anda, ini adalah perlindungan MAKSIMAL. Namun ingat, murni uang hangus.</div>
            </div>""", unsafe_allow_html=True)
        with c_mod2:
            st.markdown(f"""<div class='card-result'>
                <div class='card-label'>❤️ Uang Santunan Whole Life</div>
                <div class='card-value'>Rp {up_whole:,.0f}</div>
                <div class='card-subtext'>Santunan lebih kecil dari Term Life, tetapi PASTI CAIR untuk ahli waris tanpa ada risiko uang hangus.</div>
            </div>""", unsafe_allow_html=True)
        with c_mod3:
            st.markdown(f"""<div class='card-result'>
                <div class='card-label'>🍃 Uang Santunan Dwiguna</div>
                <div class='card-value'>Rp {up_endow:,.0f}</div>
                <div class='card-subtext'>Santunan terkecil, karena uang Anda terbagi besar untuk ditabung sebagai dana pensiun di akhir masa polis.</div>
            </div>""", unsafe_allow_html=True)

    elif "Rahasia Harga" in topik_edukasi:
        total_premi_kasar = calc_data['premi_tahunan'] * in_manfaat * in_n
        c_mod1, c_mod2 = st.columns(2)
        with c_mod1:
            st.markdown(f"""<div class='card-result'>
                <div class='card-label'>Total Premi Jika Dicicil ({in_n} Thn)</div>
                <div class='card-value'>Rp {total_premi_kasar:,.0f}</div>
                <div class='card-subtext'>Perusahaan asuransi memutar cicilan ini melalui instrumen investasi agar kelak setara dengan nilai Rp {in_manfaat:,.0f}.</div>
            </div>""", unsafe_allow_html=True)
        with c_mod2:
            st.markdown(f"""<div class='card-result'>
                <div class='card-label'>Harga Asli Hari Ini (Premi Tunggal)</div>
                <div class='card-value'>Rp {calc_data['A_dwiguna']*in_manfaat:,.0f}</div>
                <div class='card-subtext'>Ini adalah nilai tunai atau harga pokok matematis perlindungan Anda jika dibayar lunas seketika hari ini.</div>
            </div>""", unsafe_allow_html=True)

    elif "Mesin Waktu" in topik_edukasi:
        tahun_batal = st.slider("Coba simulasikan membatalkan asuransi di Tahun Ke-", 1, int(in_n), min(3, int(in_n)))
        df_cadangan = engine.hitung_alur_cadangan(in_usia, in_n, in_bunga, in_manfaat, in_tipe)
        row_cad = df_cadangan[df_cadangan['Tahun Ke-'] == tahun_batal]
        nilai_cair = row_cad['Cadangan (Rp)'].values[0] if not row_cad.empty else 0
        total_dibayar = calc_data['premi_tahunan'] * in_manfaat * tahun_batal
        
        c_mod1, c_mod2 = st.columns(2)
        with c_mod1:
            st.markdown(f"""<div class='card-result'>
                <div class='card-label'>Total Setoran Mengendap</div>
                <div class='card-value'>Rp {total_dibayar:,.0f}</div>
                <div class='card-subtext'>Total dana yang sudah Anda cicil selama masa evaluasi asuransi ini.</div>
            </div>""", unsafe_allow_html=True)
        with c_mod2:
            st.markdown(f"""<div class='card-result'>
                <div class='card-label'>Nilai Pencairan Anda Sekarang</div>
                <div class='card-value'>Rp {nilai_cair:,.0f}</div>
                <div class='card-subtext'>Sebagian uang Anda telah dialokasikan membiayai proteksi, inilah sisa murni tabungan atau cadangan premi Anda saat membatalkan polis.</div>
            </div>""", unsafe_allow_html=True)

    elif "Kalkulator Risiko" in topik_edukasi:
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
            st.markdown(f"""<div class='card-result'>
                <div class='card-label'>Mulai Sekarang (Usia {in_usia})</div>
                <div class='card-value'>Rp {premi_sekarang:,.0f} / Thn</div>
                <div class='card-subtext'>Risiko kematian secara statistik hanyalah {qx_now*1000:.1f} per 1.000 jiwa. Ini adalah harga paling optimal.</div>
            </div>""", unsafe_allow_html=True)
        with c_mod2:
            st.markdown(f"""<div class='card-result'>
                <div class='card-label'>Menunda 10 Tahun (Usia {usia_delay})</div>
                <div class='card-value'>Rp {premi_nanti:,.0f} / Thn</div>
                <div class='card-subtext'>Risiko melonjak ({qx_delay*1000:.1f} per 1.000)! Harga premi yang harus Anda cicil melonjak tajam sekitar <b style='color:#00033D;'>{kenaikan:.1f}%</b> selamanya.</div>
            </div>""", unsafe_allow_html=True)
