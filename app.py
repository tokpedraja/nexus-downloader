import streamlit as st
import yt_dlp
import os
import shutil
import time
import random
import re
from datetime import datetime, timedelta, timezone

# --- 0. KONFIGURASI SISTEM ---
st.set_page_config(
    page_title="NEXXUS ZIQVA V9 - FREE",
    page_icon="👽",
    layout="wide",
    initial_sidebar_state="collapsed"
)

DOWNLOAD_DIR = "Ziqva_Downloads"
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

# --- 1. TAMPILAN ANTARMUKA (UI) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;700&family=Share+Tech+Mono&display=swap');

    /* --- BACKGROUND BARU: DIGITAL HORIZON --- */
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    .stApp {
        background: linear-gradient(-45deg, #050505, #1a0b2e, #001f0f, #000000);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
        color: #00ffcc;
        font-family: 'Rajdhani', sans-serif;
    }

    /* --- TYPOGRAPHY --- */
    h1, h2, h3 {
        font-family: 'Share Tech Mono', monospace;
        color: #00ffcc !important;
        text-transform: uppercase;
        text-shadow: 0 0 15px rgba(0, 255, 204, 0.4);
    }
    
    /* --- INPUT FIELDS YANG LEBIH SANTAI --- */
    .stTextArea textarea, .stTextInput input, .stSelectbox div[data-baseweb="select"] {
        background-color: rgba(20, 20, 20, 0.7) !important;
        color: #00ffcc !important;
        border: 1px solid #00ffcc !important;
        border-radius: 8px;
        backdrop-filter: blur(5px);
    }
    
    /* --- TOMBOL --- */
    div.stButton > button {
        background: transparent !important;
        color: #00ffcc !important;
        border: 2px solid #00ffcc !important;
        border-radius: 12px;
        font-weight: bold;
        font-size: 16px;
        transition: all 0.3s ease;
        width: 100%;
    }
    div.stButton > button:hover {
        background: #00ffcc !important;
        color: #000 !important;
        box-shadow: 0 0 25px #00ffcc;
        transform: scale(1.02);
    }
    
    /* --- KARTU KONTEN --- */
    .ziqva-card {
        background: rgba(0, 0, 0, 0.6);
        border-left: 4px solid #00ffcc;
        padding: 20px;
        border-radius: 0 10px 10px 0;
        margin-bottom: 15px;
    }

    /* --- PROGRESS BAR --- */
    .stProgress > div > div > div > div {
        background-color: #d600ff; /* Warna ungu neon */
        background-image: linear-gradient(to right, #d600ff, #00ffcc);
    }
    
    /* --- MOBILE FIX --- */
    @media (max-width: 640px) {
        h1 { font-size: 1.8rem !important; }
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. FUNGSI BANTUAN ---
def get_random_user_agent():
    agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1'
    ]
    return random.choice(agents)

def format_bytes(size):
    power = 2**10
    n = 0
    power_labels = {0 : '', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
    while size > power:
        size /= power
        n += 1
    return f"{size:.2f} {power_labels[n]}B"

def cleanup_vault():
    try:
        shutil.rmtree(DOWNLOAD_DIR)
        os.makedirs(DOWNLOAD_DIR)
        return True
    except:
        return False

def hacking_effect(log_ph):
    texts = [
        "Menghubungkan ke satelit Ziqva...",
        "Mencari celah keamanan...",
        "Bypass firewall...",
        "Menyedot kuota target...",
        "Akses Diterima! Gasken..."
    ]
    log_str = ""
    wib = timezone(timedelta(hours=7))
    for txt in texts:
        time.sleep(random.uniform(0.2, 0.4))
        ts = datetime.now(wib).strftime("%H:%M:%S")
        log_str += f"[{ts}] > {txt}\n"
        log_ph.code(log_str, language="bash")

# --- 3. SIDEBAR ---
with st.sidebar:
    st.markdown("## 🎛️ PUSAT KONTROL")
    
    st.markdown("### 🍪 Cookies (Opsional)")
    cookies_txt = st.text_area("Paste disini kalo butuh login", height=70, help="Buat video yang butuh umur 18+ atau premium.")
    
    st.markdown("### 👻 Mode Hantu")
    use_stealth = st.checkbox("Anti-Deteksi", value=True)
    proxy_url = st.text_input("Punya Proxy Sendiri?")
    
    st.divider()
    if st.button("🗑️ BERSIHKAN SAMPAH"):
        if cleanup_vault():
            st.toast("Bersih kinclong bosku!", icon="✨")
    
    st.caption(f"Total File: {len(os.listdir(DOWNLOAD_DIR))}")

# --- 4. HEADER ---
c_logo, c_text = st.columns([1, 6])
with c_logo:
    st.write("")
    st.markdown("<h1>👽</h1>", unsafe_allow_html=True)
with c_text:
    st.markdown("# NEXXUS ZIQVA V9 <br><span style='font-size:0.5em; color:#d600ff; letter-spacing:3px;'>FREE EDITION</span>", unsafe_allow_html=True)

# TABS UTAMA
tab_main, tab_pro, tab_store, tab_info = st.tabs(["🚀 DOWNLOADER", "🛠️ FITUR PRO", "📂 FILE SAYA", "ℹ️ INFO PENTING"])

# === TAB 1: DOWNLOADER UTAMA ===
with tab_main:
    st.markdown('<div class="ziqva-card">', unsafe_allow_html=True)
    target_urls = st.text_area("🔗 TEMPEL LINK DISINI (Bisa banyak baris)", height=100, placeholder="Contoh:\nhttps://youtube.com/watch?v=...\nhttps://tiktok.com/...")
    st.markdown('</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        dl_mode = st.selectbox("MAU FORMAT APA?", ["📺 Video (Paling Jernih)", "🎵 Musik (MP3/M4A)", "🖼️ Cuma Thumbnail"])
    with c2:
        if "Video" in dl_mode:
            video_res = st.select_slider("MENTOK RESOLUSI", options=["360p", "720p", "1080p", "4K"], value="1080p")
        elif "Musik" in dl_mode:
            audio_fmt = st.selectbox("JENIS AUDIO", ["mp3", "m4a", "flac"], index=0)

    st.write("")
    if st.button("🔥 SIKAT BOSKU!", type="primary", use_container_width=True):
        if not target_urls.strip():
            st.warning("⚠️ Link-nya mana bos? Kosong nih.")
        else:
            urls = [u.strip() for u in target_urls.split('\n') if u.strip()]
            
            # UI Progress
            status_box = st.status("⚙️ Sedang memproses...", expanded=True)
            log_ph = st.empty()
            prog_bar = st.progress(0)
            prog_txt = st.empty()

            # Hook Progress
            def my_hook(d):
                if d['status'] == 'downloading':
                    try:
                        p = d.get('_percent_str', '0%').replace('%','')
                        val = float(p) / 100
                        prog_bar.progress(min(val, 1.0))
                        speed = d.get('_speed_str', '-')
                        eta = d.get('_eta_str', '-')
                        prog_txt.code(f"🚀 SPEED: {speed} | ⏳ SISA WAKTU: {eta}")
                    except: pass
                elif d['status'] == 'finished':
                    prog_bar.progress(1.0)
                    prog_txt.code("✅ Download kelar, lagi convert...")

            with status_box:
                hacking_effect(log_ph)
                
                # Setup
                c_file = "ziqva_cookies.txt"
                if cookies_txt:
                    with open(c_file, "w") as f: f.write(cookies_txt)
                
                opts = {
                    'outtmpl': f'{DOWNLOAD_DIR}/%(title)s [%(id)s].%(ext)s',
                    'restrictfilenames': True,
                    'quiet': True,
                    'no_warnings': True,
                    'ignoreerrors': True,
                    'writethumbnail': True,
                    'progress_hooks': [my_hook],
                }

                if use_stealth: opts['user_agent'] = get_random_user_agent()
                if proxy_url: opts['proxy'] = proxy_url

                # Cek Fitur Pro
                if st.session_state.get('cut_active', False):
                    # Fitur potong video
                    opts['external_downloader'] = 'ffmpeg'
                    start = st.session_state.get('t_start', '00:00:00')
                    end = st.session_state.get('t_end', '00:01:00')
                    opts['external_downloader_args'] = {'ffmpeg_i': ['-ss', start, '-to', end]}
                
                if st.session_state.get('sub_on', False):
                    opts['writesubtitles'] = True
                    opts['subtitleslangs'] = ['all']
                    opts['postprocessors'] = [{'key': 'FFmpegEmbedSubtitle'}]

                if st.session_state.get('ad_kill', False):
                    opts.setdefault('postprocessors', []).append({
                        'key': 'SponsorBlock',
                        'categories': ['sponsor', 'intro', 'outro'],
                    })

                # Config Mode
                if "Video" in dl_mode:
                    h_map = {"360p": "360", "720p": "720", "1080p": "1080", "4K": "2160"}
                    h = h_map.get(video_res, "1080")
                    opts['format'] = f'bestvideo[height<={h}]+bestaudio/best[height<={h}]'
                    opts['merge_output_format'] = 'mp4'
                elif "Musik" in dl_mode:
                    opts['format'] = 'bestaudio/best'
                    opts['postprocessors'] = [
                        {'key': 'FFmpegExtractAudio', 'preferredcodec': audio_fmt},
                        {'key': 'FFmpegMetadata'},
                        {'key': 'EmbedThumbnail'},
                    ]
                elif "Thumbnail" in dl_mode:
                    opts['skip_download'] = True

                # Eksekusi
                with yt_dlp.YoutubeDL(opts) as ydl:
                    sukses = 0
                    for link in urls:
                        try:
                            st.write(f"🎯 Target: {link}")
                            ydl.extract_info(link, download=True)
                            sukses += 1
                        except Exception as e:
                            st.error(f"Gagal bos: {str(e)}")
                
                if os.path.exists(c_file): os.remove(c_file)
            
            if sukses > 0:
                st.balloons()
                st.success(f"🎉 MANTAP! {sukses} file berhasil diamankan.")
                time.sleep(2)
                st.rerun()

# === TAB 2: FITUR PRO ===
with tab_pro:
    st.markdown("### 🛠️ OPREK LANJUTAN")
    st.caption("Fitur tambahan buat yang ngerti-ngerti aja.")

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown('<div class="ziqva-card">', unsafe_allow_html=True)
        st.markdown("**✂️ POTONG DURASI**")
        cut_active = st.toggle("Aktifkan Pemotong", key="cut_active")
        c_t1, c_t2 = st.columns(2)
        c_t1.text_input("Mulai", value="00:00:00", key="t_start", disabled=not cut_active)
        c_t2.text_input("Selesai", value="00:01:00", key="t_end", disabled=not cut_active)
        st.caption("Ambil bagian pentingnya aja biar hemat kuota.")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_b:
        st.markdown('<div class="ziqva-card">', unsafe_allow_html=True)
        st.markdown("**📺 SUBTITLE & IKLAN**")
        st.toggle("Tanam Subtitle Otomatis", key="sub_on")
        st.toggle("Hapus Iklan Sponsor (SponsorBlock)", key="ad_kill")
        st.caption("Biar nonton makin nyaman tanpa gangguan.")
        st.markdown('</div>', unsafe_allow_html=True)

# === TAB 3: FILE STORAGE ===
with tab_store:
    st.markdown("### 📂 HASIL DOWNLOAD")
    files = sorted([os.path.join(DOWNLOAD_DIR, f) for f in os.listdir(DOWNLOAD_DIR)], key=os.path.getmtime, reverse=True)
    
    if not files:
        st.info("Belum ada file nih bos. Download dulu gih!")
    else:
        if st.button("📦 BUNGKUS SEMUA (ZIP)"):
            shutil.make_archive("Paket_Ziqva", 'zip', DOWNLOAD_DIR)
            with open("Paket_Ziqva.zip", "rb") as f:
                st.download_button("⬇️ AMBIL ZIP", f, "Paket_Ziqva.zip", "application/zip")
        
        st.divider()
        for f_path in files:
            f_name = os.path.basename(f_path)
            if f_name.endswith(('.part', '.ytdl')): continue
            
            f_size = format_bytes(os.path.getsize(f_path))
            
            st.markdown(f"""
            <div style="background:rgba(255,255,255,0.1); padding:10px; border-radius:5px; margin-bottom:5px; border-left:3px solid #d600ff;">
                <div style="font-weight:bold;">{f_name}</div>
                <div style="font-size:0.8em; color:#aaa;">UKURAN: {f_size}</div>
            </div>
            """, unsafe_allow_html=True)
            
            with open(f_path, "rb") as fb:
                st.download_button(f"⬇️ Ambil {f_name}", fb, f_name, key=f_path, use_container_width=True)

# === TAB 4: ABOUT (REQUESTED) ===
with tab_info:
    st.markdown("### 👤 TENTANG DEVELOPER")
    
    col_info1, col_info2 = st.columns([1, 2])
    with col_info1:
        st.image("https://img.icons8.com/fluency/96/hacker.png", width=100)
    with col_info2:
        st.markdown("""
        **Developer:** Telegram [@effands](https://t.me/effands)  
        **Website:** [ziqva.com](https://ziqva.com)  
        **Email:** cs@ziqva.com
        """)
    
    st.divider()
    
    st.warning("""
    ### ⚠️ PERINGATAN KERAS !!
    **Pakailah dengan Bijak!** Tools ini gratis, tidak untuk diperjualbelikan. 
    Murni niat saya untuk berbagi.
    
    **Segala resiko (dosa/tanggung jawab) ditanggung pengguna masing-masing ya bosku.**
    """)
    
    st.success("""
    **Butuh tools lain yang lebih gila?** Langsung DM ke telegram aja bos ku.. 😎
    """)
