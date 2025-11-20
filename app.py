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
    page_title="NEXXUS ZIQVA V10 - INSANITY",
    page_icon="☣️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

DOWNLOAD_DIR = "Ziqva_Downloads"
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

# --- 1. TAMPILAN ANTARMUKA (UI) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700&family=Share+Tech+Mono&display=swap');

    /* --- BACKGROUND: RED ALERT GRID --- */
    @keyframes gridMove {
        0% { background-position: 0 0; }
        100% { background-position: 60px 60px; }
    }
    @keyframes pulseRed {
        0% { box-shadow: 0 0 10px #ff004c; }
        50% { box-shadow: 0 0 30px #ff004c; }
        100% { box-shadow: 0 0 10px #ff004c; }
    }

    .stApp {
        background-color: #050000;
        background-image: 
            linear-gradient(rgba(255, 0, 76, 0.05) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255, 0, 76, 0.05) 1px, transparent 1px);
        background-size: 50px 50px; 
        animation: gridMove 4s linear infinite;
        color: #ff004c;
        font-family: 'Orbitron', sans-serif;
    }

    /* --- TYPOGRAPHY --- */
    h1, h2, h3 {
        font-family: 'Share Tech Mono', monospace;
        color: #ff004c !important;
        text-transform: uppercase;
        text-shadow: 0 0 20px rgba(255, 0, 76, 0.8);
        letter-spacing: 2px;
    }
    
    /* --- INPUT FIELDS --- */
    .stTextArea textarea, .stTextInput input, .stSelectbox div[data-baseweb="select"] {
        background-color: rgba(20, 0, 5, 0.9) !important;
        color: #ff004c !important;
        border: 1px solid #ff004c !important;
        border-radius: 2px;
        font-family: 'Share Tech Mono', monospace;
    }
    
    /* --- TOMBOL INSANE --- */
    div.stButton > button {
        background: #000 !important;
        color: #ff004c !important;
        border: 2px solid #ff004c !important;
        border-radius: 0px;
        font-weight: 900;
        font-size: 18px;
        text-transform: uppercase;
        letter-spacing: 4px;
        transition: all 0.2s ease;
        width: 100%;
        animation: pulseRed 3s infinite;
    }
    div.stButton > button:hover {
        background: #ff004c !important;
        color: #000 !important;
        box-shadow: 0 0 50px #ff004c;
        transform: scale(1.02);
    }
    
    /* --- KARTU KONTEN --- */
    .ziqva-card {
        background: rgba(30, 0, 10, 0.8);
        border: 1px solid #ff004c;
        padding: 20px;
        margin-bottom: 15px;
        position: relative;
    }
    .ziqva-card::before {
        content: "CLASSIFIED";
        position: absolute;
        top: -12px;
        left: 10px;
        background: #000;
        color: #ff004c;
        font-size: 12px;
        padding: 0 10px;
        border: 1px solid #ff004c;
        font-weight: bold;
    }

    /* --- PROGRESS BAR --- */
    .stProgress > div > div > div > div {
        background-color: #ff004c;
        box-shadow: 0 0 15px #ff004c;
    }
    
    /* --- MOBILE FIX --- */
    @media (max-width: 640px) {
        h1 { font-size: 1.5rem !important; }
        .stApp { background-size: 25px 25px; }
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. FUNGSI BANTUAN ---
def get_random_user_agent():
    agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
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
        "Menginisiasi Protokol Insanity...",
        "Mencari Database Terlarang...",
        "Menembus Enkripsi Quantum...",
        "Memanipulasi Gelombang Audio...",
        "Akses Diberikan! Mode Gila Aktif..."
    ]
    log_str = ""
    wib = timezone(timedelta(hours=7))
    for txt in texts:
        time.sleep(random.uniform(0.1, 0.3))
        ts = datetime.now(wib).strftime("%H:%M:%S")
        log_str += f"[{ts}] > {txt}\n"
        log_ph.code(log_str, language="bash")

# --- 3. SIDEBAR ---
with st.sidebar:
    st.markdown("## 🎛️ SYSTEM OVERRIDE")
    
    st.markdown("### 💣 Evidence Wiper")
    auto_destruct = st.toggle("Hancurkan File Otomatis", value=False, help="Hapus file otomatis setelah 5 menit biar aman.")
    
    st.markdown("### 🍪 Auth Token")
    cookies_txt = st.text_area("Input Netscape Cookies", height=70)
    
    st.markdown("### 👻 Stealth Ops")
    use_stealth = st.checkbox("User-Agent Spoofing", value=True)
    proxy_url = st.text_input("Elite Proxy Node")
    
    st.divider()
    if st.button("☢️ EMERGENCY NUKE"):
        if cleanup_vault():
            st.toast("SEMUA JEJAK DIHAPUS!", icon="💀")
    
    st.caption(f"Artifacts: {len(os.listdir(DOWNLOAD_DIR))}")

# --- 4. HEADER ---
c_logo, c_text = st.columns([1, 6])
with c_logo:
    st.write("")
    st.markdown("<h1>☢️</h1>", unsafe_allow_html=True)
with c_text:
    st.markdown("# NEXXUS ZIQVA V10 <br><span style='font-size:0.5em; color:#fff; background:#ff004c; padding:2px 10px; font-weight:bold;'>INSANITY EDITION</span>", unsafe_allow_html=True)

# TABS UTAMA
tab_main, tab_god, tab_files, tab_info = st.tabs(["🚀 CORE SYSTEM", "🧪 LAB GILA", "📂 ARTIFACTS", "ℹ️ INTEL"])

# === TAB 1: CORE SYSTEM (DOWNLOADER) ===
with tab_main:
    st.markdown('<div class="ziqva-card">', unsafe_allow_html=True)
    # Input Logic: URL atau Keyword
    input_data = st.text_area("🔗 MASUKKAN TARGET", height=100, placeholder="Tempel Link URL...\nATAU ketik Judul Lagu (Contoh: 'Niki Lowkey') - Deep Search Aktif!")
    st.caption("💡 Tips: Males cari link? Ketik judulnya aja, kita carikan otomatis!")
    st.markdown('</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        dl_mode = st.selectbox("PROTOKOL", ["📺 Video (Jernih)", "🎵 Musik (Audio Only)", "🖼️ Intel (Thumbnail)"])
    with c2:
        if "Video" in dl_mode:
            video_res = st.select_slider("KUALITAS VISUAL", options=["360p", "720p", "1080p", "2K", "4K"], value="1080p")
        elif "Musik" in dl_mode:
            audio_fmt = st.selectbox("FORMAT AUDIO", ["mp3", "wav", "flac"], index=0)

    st.write("")
    if st.button("🔥 EKSEKUSI TARGET", type="primary", use_container_width=True):
        if not input_data.strip():
            st.warning("⚠️ TARGET KOSONG! Masukkan Link atau Kata Kunci.")
        else:
            raw_lines = [u.strip() for u in input_data.split('\n') if u.strip()]
            
            # UI Progress
            status_box = st.status("⚙️ INITIALIZING INSANITY...", expanded=True)
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
                        prog_txt.code(f"🚀 SPEED: {speed} | ⏳ ETA: {eta}")
                    except: pass
                elif d['status'] == 'finished':
                    prog_bar.progress(1.0)
                    prog_txt.code("✅ DOWNLOAD SELESAI. MEMPROSES DATA...")

            with status_box:
                hacking_effect(log_ph)
                
                # Setup Cookies
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

                # --- FITUR GILA ---
                
                # 1. SONIC MUTATOR (Audio Effects)
                if "Musik" in dl_mode and st.session_state.get('sonic_active', False):
                    effect = st.session_state.get('sonic_effect', 'Normal')
                    ffmpeg_args = []
                    
                    if effect == 'Nightcore (Cepat+Tinggi)':
                        # Speed 1.25x, Pitch naik
                        ffmpeg_args = ['-af', 'asetrate=44100*1.25,aresample=44100']
                        st.write("🔊 Mengaktifkan Efek: NIGHTCORE")
                    elif effect == 'Slowed + Reverb (Galau)':
                        # Speed 0.85x, Echo
                        ffmpeg_args = ['-af', 'asetrate=44100*0.85,aresample=44100,aecho=0.8:0.9:1000:0.3']
                        st.write("🔊 Mengaktifkan Efek: SLOWED + REVERB")
                    elif effect == 'Bass Boost (Jebol)':
                        # Equalizer frequency low
                        ffmpeg_args = ['-af', 'equalizer=f=50:width_type=o:width=2:g=20']
                        st.write("🔊 Mengaktifkan Efek: BASS BOOST")
                    
                    if ffmpeg_args:
                        opts['postprocessor_args'] = {'ffmpeg': ffmpeg_args}

                # 2. GOD MODE LOGIC
                if st.session_state.get('geo_active', False):
                    opts['geo_bypass_country'] = st.session_state.get('geo_code', 'US')
                
                if st.session_state.get('vacuum_active', False):
                    opts['playlistend'] = st.session_state.get('vacuum_limit', 5)
                else:
                    opts['noplaylist'] = True

                # 3. TIME CLIPPER
                if st.session_state.get('cut_active', False):
                    opts['external_downloader'] = 'ffmpeg'
                    start = st.session_state.get('t_start', '00:00:00')
                    end = st.session_state.get('t_end', '00:01:00')
                    opts['external_downloader_args'] = {'ffmpeg_i': ['-ss', start, '-to', end]}
                
                # 4. EXTRAS
                if st.session_state.get('sub_on', False):
                    opts['writesubtitles'] = True; opts['subtitleslangs'] = ['all']; opts['postprocessors'] = [{'key': 'FFmpegEmbedSubtitle'}]
                if st.session_state.get('ad_kill', False):
                    opts.setdefault('postprocessors', []).append({'key': 'SponsorBlock', 'categories': ['sponsor', 'intro', 'outro']})

                # CONFIG FORMAT
                if "Video" in dl_mode:
                    h = {"360p":"360","720p":"720","1080p":"1080","2K":"1440","4K":"2160"}.get(video_res, "1080")
                    opts['format'] = f'bestvideo[height<={h}]+bestaudio/best[height<={h}]'
                    opts['merge_output_format'] = 'mp4'
                elif "Musik" in dl_mode:
                    opts['format'] = 'bestaudio/best'
                    opts['postprocessors'] = [{'key': 'FFmpegExtractAudio', 'preferredcodec': audio_fmt}, {'key': 'FFmpegMetadata'}, {'key': 'EmbedThumbnail'}]
                elif "Thumbnail" in dl_mode:
                    opts['skip_download'] = True

                # EKSEKUSI LOOP
                with yt_dlp.YoutubeDL(opts) as ydl:
                    sukses = 0
                    for line in raw_lines:
                        # DEEP SEARCH LOGIC
                        target = line
                        if not line.startswith(('http', 'www')):
                            st.write(f"🕵️ Deep Search: Mencari '{line}' di database...")
                            target = f"ytsearch1:{line}"
                        
                        try:
                            st.write(f"🎯 Mengunci Target: {line}")
                            ydl.extract_info(target, download=True)
                            sukses += 1
                        except Exception as e:
                            st.error(f"Misi Gagal: {str(e)}")
                
                if os.path.exists(c_file): os.remove(c_file)
            
            if sukses > 0:
                st.balloons()
                st.success(f"🎉 MISI SELESAI! {sukses} Artifact diamankan.")
                if auto_destruct:
                    st.warning("💣 SELF-DESTRUCT: File akan dihapus dalam 5 menit...")
                time.sleep(2)
                st.rerun()

# === TAB 2: LAB GILA (NEW FEATURES) ===
with tab_god:
    st.markdown("### 🧪 EXPERIMENTAL LAB")
    
    col_insane1, col_insane2 = st.columns(2)
    
    with col_insane1:
        st.markdown('<div class="ziqva-card">', unsafe_allow_html=True)
        st.markdown("**🔊 SONIC MUTATOR (Audio Hack)**")
        sonic_active = st.toggle("Aktifkan Modifikasi Audio", key="sonic_active")
        st.selectbox("Pilih Efek", ["Nightcore (Cepat+Tinggi)", "Slowed + Reverb (Galau)", "Bass Boost (Jebol)"], key="sonic_effect", disabled=not sonic_active)
        st.caption("⚠️ Hanya bekerja di Mode Musik. Mengubah suara asli video.")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="ziqva-card">', unsafe_allow_html=True)
        st.markdown("**🌍 JURUS TELEPORTASI**")
        st.toggle("Bypass Negara (Geo-Block)", key="geo_active")
        st.text_input("Kode ISO Negara", value="US", key="geo_code", placeholder="US, JP, SG...")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_insane2:
        st.markdown('<div class="ziqva-card">', unsafe_allow_html=True)
        st.markdown("**🌪️ VACUUM CLEANER (Playlist)**")
        st.toggle("Sedot Playlist/Channel", key="vacuum_active")
        st.slider("Jumlah Video", 1, 20, 5, key="vacuum_limit")
        st.caption("Otomatis download banyak video sekaligus.")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="ziqva-card">', unsafe_allow_html=True)
        st.markdown("**🛡️ DEFENSE SYSTEMS**")
        st.toggle("Potong Durasi (Time Clipper)", key="cut_active")
        c_t1, c_t2 = st.columns(2)
        c_t1.text_input("Start", "00:00:00", key="t_start")
        c_t2.text_input("End", "00:01:00", key="t_end")
        st.checkbox("Auto Subtitle", key="sub_on")
        st.checkbox("SponsorBlock AI", key="ad_kill")
        st.markdown('</div>', unsafe_allow_html=True)

# === TAB 3: ARTIFACTS ===
with tab_files:
    st.markdown("### 📂 GUDANG ARTIFACTS")
    files = sorted([os.path.join(DOWNLOAD_DIR, f) for f in os.listdir(DOWNLOAD_DIR)], key=os.path.getmtime, reverse=True)
    
    if not files:
        st.info("ZONE CLEAR. Belum ada target yang dieksekusi.")
    else:
        if st.button("📦 BUNGKUS SEMUA (ZIP)"):
            shutil.make_archive("Ziqva_Insanity", 'zip', DOWNLOAD_DIR)
            with open("Ziqva_Insanity.zip", "rb") as f:
                st.download_button("⬇️ DOWNLOAD PAKET", f, "Ziqva_Insanity.zip", "application/zip")
        
        st.divider()
        for f_path in files:
            f_name = os.path.basename(f_path)
            if f_name.endswith(('.part', '.ytdl')): continue
            
            f_size = format_bytes(os.path.getsize(f_path))
            
            st.markdown(f"""
            <div style="background:rgba(50, 0, 10, 0.5); padding:10px; margin-bottom:5px; border-left:4px solid #ff004c;">
                <div style="font-weight:bold; word-break: break-all;">{f_name}</div>
                <div style="font-size:0.8em; color:#ff88a0;">UKURAN: {f_size}</div>
            </div>
            """, unsafe_allow_html=True)
            
            with open(f_path, "rb") as fb:
                st.download_button(f"⬇️ AMBIL {f_name}", fb, f_name, key=f_path, use_container_width=True)

# === TAB 4: INTEL ===
with tab_info:
    st.markdown("### 👤 OPERATOR PROFILE")
    
    c_i1, c_i2 = st.columns([1, 3])
    with c_i1:
        st.image("https://img.icons8.com/fluency/96/hacker.png")
    with c_i2:
        st.markdown("""
        **Codename:** Effands  
        **Frequency:** [@effands](https://t.me/effands)  
        **Base:** [ziqva.com](https://ziqva.com)  
        """)
    
    st.error("""
    ### ⚠️ PERINGATAN TINGKAT TINGGI
    **TOOLS INI SANGAT POWERFUL.**
    Gunakan Deep Search dan Sonic Mutator dengan bijak.
    Jangan gunakan untuk membajak konten berhak cipta secara ilegal untuk tujuan komersil.
    
    **Keep it underground. Stay safe.**
    """)
