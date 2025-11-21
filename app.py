import streamlit as st
import yt_dlp
import os
import shutil
import time
import random
import uuid
from datetime import datetime, timedelta, timezone

# --- 0. KONFIGURASI SISTEM & SESSION ---
st.set_page_config(
    page_title="NEXXUS ZIQVA V10 - PRIVATE",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# MEMBUAT ID UNIK UNTUK SETIAP PENGGUNA (BIAR GAK BENTROK)
if 'user_session_id' not in st.session_state:
    st.session_state['user_session_id'] = str(uuid.uuid4())

# Folder Download Unik per User (Absolute Path biar aman)
BASE_DIR = "Ziqva_Temp_Storage"
DOWNLOAD_DIR = os.path.abspath(os.path.join(BASE_DIR, st.session_state['user_session_id']))

if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

# --- CLASS LOGGER KHUSUS UNTUK MENANGKAP ERROR ---
class MyLogger:
    def debug(self, msg):
        pass
    def warning(self, msg):
        # Filter warning umum agar user tidak panik
        if "JavaScript" not in msg and "deprecated" not in msg:
            st.warning(f"⚠️ Warning: {msg}")
    def error(self, msg):
        # Deteksi spesifik error Bot/Sign In
        if "Sign in" in msg or "bot" in msg:
            st.error("⛔ YOUTUBE BLOCK: Google mendeteksi server ini sebagai Bot.")
            st.info("💡 SOLUSI: Wajib masukkan 'Netscape Cookies' di Sidebar agar dianggap user asli.")
        else:
            st.error(f"❌ Error System: {msg}")

# --- 1. TAMPILAN ANTARMUKA (UI - MATRIX THEME) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700&family=Share+Tech+Mono&display=swap');

    /* --- BACKGROUND: CYBER MATRIX GRID --- */
    @keyframes gridMove {
        0% { background-position: 0 0; }
        100% { background-position: 50px 50px; }
    }
    .stApp {
        background-color: #020502;
        background-image: 
            linear-gradient(rgba(0, 255, 65, 0.08) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 255, 65, 0.08) 1px, transparent 1px);
        background-size: 40px 40px; 
        animation: gridMove 3s linear infinite;
        color: #00ff41;
        font-family: 'Orbitron', sans-serif;
    }

    /* --- TYPOGRAPHY --- */
    h1, h2, h3 {
        font-family: 'Share Tech Mono', monospace;
        color: #00ff41 !important;
        text-transform: uppercase;
        text-shadow: 0 0 15px rgba(0, 255, 65, 0.6);
        letter-spacing: 2px;
    }
    
    /* --- INPUT FIELDS --- */
    .stTextArea textarea, .stTextInput input, .stSelectbox div[data-baseweb="select"] {
        background-color: rgba(0, 20, 0, 0.9) !important;
        color: #00ff41 !important;
        border: 1px solid #00ff41 !important;
        border-radius: 2px;
        font-family: 'Share Tech Mono', monospace;
    }
    
    /* --- BUTTONS --- */
    div.stButton > button {
        background: #000 !important;
        color: #00ff41 !important;
        border: 1px solid #00ff41 !important;
        border-radius: 0px;
        font-weight: 900;
        font-size: 16px;
        text-transform: uppercase;
        letter-spacing: 3px;
        transition: all 0.2s ease;
        width: 100%;
        box-shadow: 0 0 10px rgba(0, 255, 65, 0.2);
    }
    div.stButton > button:hover {
        background: #00ff41 !important;
        color: #000 !important;
        box-shadow: 0 0 30px #00ff41;
        transform: scale(1.01);
    }
    
    /* --- KARTU KONTEN --- */
    .ziqva-card {
        background: rgba(0, 15, 5, 0.85);
        border: 1px solid #00ff41;
        border-left: 5px solid #00ffff;
        padding: 20px;
        margin-bottom: 15px;
        backdrop-filter: blur(4px);
    }

    /* --- PROGRESS BAR --- */
    .stProgress > div > div > div > div {
        background-color: #00ff41;
        background-image: linear-gradient(to right, #00ff41, #00ffff);
    }
    
    /* --- TOAST --- */
    .stToast {
        background-color: #000 !important;
        border: 1px solid #00ff41 !important;
        color: #00ff41 !important;
    }
    
    /* --- WARNING BOX --- */
    .warning-box {
        border: 1px dashed #00ff41;
        background: #051105;
        padding: 15px;
        text-align: center;
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.9em;
        color: #00ff41;
    }
    
    /* --- LOG TERMINAL --- */
    .log-terminal {
        font-family: 'Courier New', monospace;
        font-size: 0.85em;
        background: #000;
        color: #0f0;
        padding: 10px;
        border: 1px solid #333;
        max-height: 300px;
        overflow-y: auto;
    }
    </style>
""", unsafe_allow_html=True)

# --- SECURITY SYSTEM (LOGIN GATE) ---
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

def check_access():
    if st.session_state['access_code'] == 'ziqva.com':
        st.session_state['authenticated'] = True
        st.toast("✅ AKSES DITERIMA! SELAMAT DATANG BOSKU.", icon="🔓")
    else:
        st.session_state['authenticated'] = False
        st.toast("⛔ AKSES DITOLAK: Kode Salah Bos!", icon="☠️")

if not st.session_state['authenticated']:
    st.markdown("<br><br>", unsafe_allow_html=True)
    col_l1, col_l2, col_l3 = st.columns([1,2,1])
    with col_l2:
        st.markdown("""
        <div style='text-align: center; border: 2px solid #00ff41; padding: 30px; background: rgba(0,20,0,0.85); box-shadow: 0 0 20px #00ff41;'>
            <h1 style='color: #00ff41; margin-bottom: 0; text-shadow: 0 0 10px #00ff41;'>🔐 RESTRICTED AREA</h1>
            <p style='color: #00ffff; letter-spacing: 3px; font-weight:bold;'>NEXXUS ZIQVA SECURITY PROTOCOL</p>
            <hr style='border-color: #00ff41;'>
            <p style='font-size: 0.8em; color: #ccc;'>SYSTEM LOCKED. AUTHORIZED PERSONNEL ONLY.</p>
        </div>
        """, unsafe_allow_html=True)
        st.text_input("MASUKKAN KODE AKSES", type="password", key="access_code", on_change=check_access)
        st.button("UNLOCK SYSTEM 🔓", on_click=check_access, use_container_width=True)
        st.markdown("<p style='text-align:center; color:#666; margin-top:20px; font-size:0.7em;'>Hint: ziqva.com</p>", unsafe_allow_html=True)
    st.stop()

# --- 2. FUNGSI BANTUAN ---
def get_random_user_agent():
    # Update UA ke versi mobile/tablet untuk menghindari deteksi PC Bot
    agents = [
        'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1'
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
        st.session_state['latest_file'] = None
        return True
    except:
        return False

def hacking_effect(log_ph):
    texts = [
        "Handshake Protocol VVIP...",
        "Bypassing ISP Throttling...",
        "Injecting Multi-Thread Payload...",
        "Scrubbing Metadata Signatures...",
        "ACCESS GRANTED: GOD MODE."
    ]
    log_str = ""
    wib = timezone(timedelta(hours=7))
    for txt in texts:
        time.sleep(random.uniform(0.1, 0.25))
        ts = datetime.now(wib).strftime("%H:%M:%S")
        log_str += f"[{ts}] > {txt}\n"
        log_ph.code(log_str, language="bash")

# --- 3. SIDEBAR ---
with st.sidebar:
    st.markdown("## 🎛️ SYSTEM OVERRIDE")
    st.markdown("### 💣 Evidence Wiper")
    auto_destruct = st.toggle("Auto-Delete (5 min)", value=False, help="File otomatis meledak (terhapus) 5 menit setelah download.")
    st.markdown("### 🍪 Premium Auth")
    # Tambah pesan penting
    st.info("💡 WAJIB ISI COOKIES JIKA ERROR 'SIGN IN' MUNCUL!")
    cookies_txt = st.text_area("Input Netscape Cookies", height=70)
    st.markdown("### 👻 Stealth Matrix")
    use_stealth = st.checkbox("User-Agent Spoofing", value=True)
    proxy_url = st.text_input("Elite Proxy Node")
    st.divider()
    if st.button("☢️ EMERGENCY WIPER"):
        if cleanup_vault(): st.toast("CACHE CLEARED!", icon="♻️")
    
    user_files = len(os.listdir(DOWNLOAD_DIR)) if os.path.exists(DOWNLOAD_DIR) else 0
    st.caption(f"My Artifacts: {user_files}")

# --- 4. HEADER ---
c_logo, c_text = st.columns([1, 6])
with c_logo:
    st.write("")
    st.markdown("<h1>🧬</h1>", unsafe_allow_html=True)
with c_text:
    st.markdown("# NEXXUS ZIQVA V10 <br><span style='font-size:0.5em; color:#000; background:#00ff41; padding:2px 10px; font-weight:bold; box-shadow: 0 0 10px #00ff41;'>VVIP PRIVATE SESSION</span>", unsafe_allow_html=True)

# TABS UTAMA
tab_main, tab_vvip, tab_files, tab_info = st.tabs(["🚀 CORE TERMINAL", "💎 VVIP VAULT", "📂 DOWNLOADS", "ℹ️ WARNING & LOGS"])

log_placeholder = None

# === ISI TAB INFO & LOGS ===
with tab_info:
    st.markdown("### 👤 OPERATOR INTEL")
    c_i1, c_i2 = st.columns([1, 3])
    with c_i1: st.image("https://img.icons8.com/fluency/96/hacker.png")
    with c_i2:
        st.markdown("""
        **Developer:** Telegram [@effands](https://t.me/effands)  
        **Website:** [ziqva.com](https://ziqva.com)  
        **Email:** cs@ziqva.com
        """)
    st.divider()
    st.markdown("""
    <div class='warning-box'>
    <h3>⚠️ WARNING BOSKU !!</h3>
    <p>Pakailah dengan Bijak. Tools ini gratisan murni buat berbagi & bantu-bantu aja, bukan buat diperjualbelikan ya.</p>
    <p><strong>Segala resiko ditanggung penumpang masing-masing. Dosa tanggung sendiri.</strong></p>
    <hr style="border-color: #00ff41;">
    <p><em>Butuh tools lain yang lebih gila? DM ke telegram aja bos ku.. Siap melayani. 😎</em></p>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    st.markdown("### 📟 LIVE SYSTEM LOGS")
    log_placeholder = st.empty()
    log_placeholder.code("Waiting for command sequence...", language="bash")
    st.success("System Status: **ONLINE** | Session ID: **SECURED**")

# === TAB 1: CORE TERMINAL ===
with tab_main:
    # --- SHOW LAST DOWNLOAD ---
    if 'latest_file' in st.session_state and st.session_state['latest_file']:
        last_f = st.session_state['latest_file']
        if os.path.exists(last_f):
            f_name = os.path.basename(last_f)
            f_size = format_bytes(os.path.getsize(last_f))
            
            st.markdown(f"""
            <div style="background:rgba(0, 50, 0, 0.8); padding:15px; margin-bottom:20px; border:2px solid #00ff41; border-radius:5px; text-align:center;">
                <h3 style='margin:0; color:#00ff41;'>🎉 MISSION SUCCESS!</h3>
                <p style='color:#fff;'>File aman di Private Storage bosku.</p>
                <hr style='border-color:#00ff41;'>
                <p style='font-weight:bold; color:#00ffff;'>{f_name} ({f_size})</p>
            </div>
            """, unsafe_allow_html=True)
            
            col_d1, col_d2, col_d3 = st.columns([1,2,1])
            with col_d2:
                with open(last_f, "rb") as fb:
                    st.download_button(f"⬇️ DOWNLOAD {f_name} SEKARANG", fb, f_name, key="main_dl_btn", type="primary", use_container_width=True)
            st.divider()

    st.markdown('<div class="ziqva-card">', unsafe_allow_html=True)
    input_data = st.text_area("🔗 TARGET INPUT (URL / JUDUL)", height=200, placeholder="Paste URL disini bosku...\nFile akan masuk ke Session Folder Pribadi (Anti Bentrok).")
    st.markdown('</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        dl_mode = st.selectbox("PROTOCOL TYPE", ["📺 Video (Ultra HD)", "🎵 Audio (Hi-Res)", "🖼️ Intel (Thumb Only)"])
    with c2:
        if "Video" in dl_mode:
            video_res = st.select_slider("RESOLUTION LOCK", options=["360p", "720p", "1080p", "2K", "4K", "8K"], value="1080p")
        elif "Audio" in dl_mode:
            audio_fmt = st.selectbox("AUDIO CODEC", ["mp3", "wav", "flac", "m4a"], index=0)

    st.write("")
    if st.button("🔥 INITIATE SEQUENCE", type="primary", use_container_width=True):
        if not input_data.strip():
            st.warning("⚠️ TARGET NOT FOUND.")
        else:
            raw_lines = [u.strip() for u in input_data.split('\n') if u.strip()]
            
            with log_placeholder:
                st.write("⚡ INITIALIZING SEQUENCE...")
            
            status_box = st.status("⚙️ SYSTEM RUNNING...", expanded=True)
            prog_bar = st.progress(0)
            prog_txt = st.empty()

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
                    prog_txt.code("✅ PROCESSING ARTIFACT...")
                    st.session_state['latest_file'] = d['filename']

            with status_box:
                hacking_effect(log_placeholder)
                c_file = f"ziqva_cookies_{st.session_state['user_session_id']}.txt"
                if cookies_txt:
                    with open(c_file, "w") as f: f.write(cookies_txt)
                
                # --- KONFIGURASI YOUTUBE-DL (FIXED LOGIC) ---
                opts = {
                    'outtmpl': f'{DOWNLOAD_DIR}/%(title)s [%(id)s].%(ext)s',
                    'restrictfilenames': True,
                    'quiet': False,
                    'no_warnings': False,
                    'ignoreerrors': False,
                    'writethumbnail': True,
                    'logger': MyLogger(),
                    'progress_hooks': [my_hook],
                    # BYPASS BOT: Gunakan klien Android agar lebih dipercaya YouTube
                    'extractor_args': {
                        'youtube': {
                            'player_client': ['android', 'ios'],
                            'player_skip': ['js', 'web'], # Coba skip JS web yg bikin warning
                        }
                    }
                }

                if use_stealth: opts['user_agent'] = get_random_user_agent()
                if proxy_url: opts['proxy'] = proxy_url

                # VVIP & PRO FEATURES
                ffmpeg_args = []
                if st.session_state.get('vvip_ghost', False):
                    opts['add_metadata'] = False
                    ffmpeg_args.extend(['-map_metadata', '-1', '-bn', '-vn'])
                
                if "Audio" in dl_mode and st.session_state.get('sonic_active', False):
                    effect = st.session_state.get('sonic_effect', 'Normal')
                    if effect == 'Nightcore': ffmpeg_args.extend(['-af', 'asetrate=44100*1.25,aresample=44100'])
                    elif effect == 'Slowed+Reverb': ffmpeg_args.extend(['-af', 'asetrate=44100*0.85,aresample=44100,aecho=0.8:0.9:1000:0.3'])
                    elif effect == 'Bass Boost': ffmpeg_args.extend(['-af', 'equalizer=f=50:width_type=o:width=2:g=20'])
                
                if ffmpeg_args: opts['postprocessor_args'] = {'ffmpeg': ffmpeg_args}
                if st.session_state.get('vvip_speed', False): opts['concurrent_fragment_downloads'] = 10
                if st.session_state.get('vvip_live', False): opts['live_from_start'] = True; opts['wait_for_video'] = (1, 10)
                if st.session_state.get('vvip_godseye', False): opts['writeinfojson'] = True

                if st.session_state.get('geo_active', False): opts['geo_bypass_country'] = st.session_state.get('geo_code', 'US')
                if st.session_state.get('vacuum_active', False): opts['playlistend'] = st.session_state.get('vacuum_limit', 5)
                else: opts['noplaylist'] = True

                if st.session_state.get('cut_active', False):
                    opts['external_downloader'] = 'ffmpeg'
                    start, end = st.session_state.get('t_start', '00:00:00'), st.session_state.get('t_end', '00:01:00')
                    opts['external_downloader_args'] = {'ffmpeg_i': ['-ss', start, '-to', end]}
                
                if st.session_state.get('sub_on', False):
                    opts['writesubtitles'] = True; opts['subtitleslangs'] = ['all']; opts['postprocessors'] = [{'key': 'FFmpegEmbedSubtitle'}]
                if st.session_state.get('ad_kill', False):
                    opts.setdefault('postprocessors', []).append({'key': 'SponsorBlock', 'categories': ['sponsor', 'intro', 'outro']})

                # FORMAT
                if "Video" in dl_mode:
                    h = {"360p":"360","720p":"720","1080p":"1080","2K":"1440","4K":"2160","8K":"4320"}.get(video_res, "1080")
                    opts['format'] = f'bestvideo[height<={h}]+bestaudio/best[height<={h}]'
                    opts['merge_output_format'] = 'mp4'
                elif "Audio" in dl_mode:
                    opts['format'] = 'bestaudio/best'
                    opts['postprocessors'] = [{'key': 'FFmpegExtractAudio', 'preferredcodec': audio_fmt}, {'key': 'FFmpegMetadata'}, {'key': 'EmbedThumbnail'}]
                elif "Intel" in dl_mode:
                    opts['skip_download'] = True; opts['writethumbnail'] = True

                # EKSEKUSI UTAMA
                sukses_count = 0
                
                if not shutil.which("ffmpeg"):
                    st.error("❌ CRITICAL ERROR: FFmpeg belum terinstall di server ini!")
                    st.info("Solusi: Pastikan file 'packages.txt' berisi 'ffmpeg' dan 'nodejs'.")
                else:
                    with yt_dlp.YoutubeDL(opts) as ydl:
                        for line in raw_lines:
                            target = line if line.startswith(('http', 'www')) else f"ytsearch1:{line}"
                            try:
                                info = ydl.extract_info(target, download=True)
                                if info: sukses_count += 1
                            except Exception as e:
                                # Error ditangani Logger, tapi exception tetap ditangkap agar app tidak crash
                                pass
                
                if os.path.exists(c_file): os.remove(c_file)
            
            if sukses_count > 0:
                st.balloons()
                time.sleep(0.5) 
                st.rerun()
            else:
                st.warning("⚠️ Proses selesai tapi tidak ada file yang berhasil di-download. Cek pesan error di atas.")

# === TAB 2: VVIP VAULT ===
with tab_vvip:
    st.markdown("### 💎 CLASSIFIED VVIP TOOLS")
    c_v1, c_v2 = st.columns(2)
    
    with c_v1:
        st.markdown('<div class="ziqva-card">', unsafe_allow_html=True)
        st.markdown("**👁️ GOD'S EYE (NEW)**")
        st.toggle("Extract Metadata Intel (JSON)", key="vvip_godseye")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="ziqva-card">', unsafe_allow_html=True)
        st.markdown("**🚀 HYPER-THREADING**")
        st.toggle("Force 10x Connections", key="vvip_speed")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="ziqva-card">', unsafe_allow_html=True)
        st.markdown("**🔊 SONIC MUTATOR**")
        sonic_active = st.toggle("Audio Modulator", key="sonic_active")
        st.selectbox("Effect", ["Nightcore", "Slowed+Reverb", "Bass Boost"], key="sonic_effect", disabled=not sonic_active)
        st.markdown('</div>', unsafe_allow_html=True)

    with c_v2:
        st.markdown('<div class="ziqva-card">', unsafe_allow_html=True)
        st.markdown("**👻 GHOST PROTOCOL**")
        st.toggle("Metadata Wiper", key="vvip_ghost")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="ziqva-card">', unsafe_allow_html=True)
        st.markdown("**📡 LIVE INTERCEPTOR**")
        st.toggle("Record Live Stream", key="vvip_live")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="ziqva-card">', unsafe_allow_html=True)
        st.markdown("**🌍 UTILS & CLIPPER**")
        st.toggle("Geo-Bypass", key="geo_active")
        if st.session_state.get('geo_active'): st.text_input("ISO Code", "US", key="geo_code")
        st.toggle("Playlist Vacuum", key="vacuum_active")
        if st.session_state.get('vacuum_active'): st.slider("Limit", 1, 50, 5, key="vacuum_limit")
        st.divider()
        st.markdown("**✂️ TIME CLIPPER (Potong)**")
        cut_active = st.toggle("Aktifkan Pemotong", key="cut_active")
        cc1, cc2 = st.columns(2)
        cc1.text_input("Start", "00:00:00", key="t_start", disabled=not cut_active)
        cc2.text_input("End", "00:01:00", key="t_end", disabled=not cut_active)
        st.markdown('</div>', unsafe_allow_html=True)

# === TAB 3: ARTIFACTS ===
with tab_files:
    st.markdown("### 📂 DOWNLOADS STORAGE")
    all_files = []
    if os.path.exists(DOWNLOAD_DIR):
        all_files = sorted([os.path.join(DOWNLOAD_DIR, f) for f in os.listdir(DOWNLOAD_DIR)], key=os.path.getmtime, reverse=True)
    
    display_files = []
    audio_bases = {os.path.splitext(f)[0] for f in all_files if f.endswith(('.mp3', '.m4a', '.wav', '.flac', '.mp4'))}
    
    for f_path in all_files:
        f_name = os.path.basename(f_path)
        base_name = os.path.splitext(f_path)[0]
        ext = os.path.splitext(f_name)[1].lower()
        if f_name.endswith(('.part', '.ytdl')): continue
        if ext in ['.jpg', '.webp', '.png'] and base_name in audio_bases: continue
        display_files.append(f_path)
    
    if not display_files:
        st.info(f"STORAGE EMPTY ({st.session_state['user_session_id']}). WAITING FOR PAYLOAD.")
    else:
        if st.button("📦 EXTRACT ALL (ZIP)"):
            zip_name = f"Ziqva_VVIP_{st.session_state['user_session_id']}"
            shutil.make_archive(zip_name, 'zip', DOWNLOAD_DIR)
            with open(f"{zip_name}.zip", "rb") as f:
                st.download_button("⬇️ DOWNLOAD PACKAGE", f, "Ziqva_VVIP.zip", "application/zip")
        st.divider()
        for f_path in display_files:
            f_name = os.path.basename(f_path)
            f_size = format_bytes(os.path.getsize(f_path))
            icon = "📄"
            if f_name.endswith(('.mp3', '.m4a', '.wav')): icon = "🎵"
            elif f_name.endswith(('.mp4', '.mkv')): icon = "📺"
            elif f_name.endswith(('.jpg', '.png', '.webp')): icon = "🖼️"
            elif f_name.endswith('.json'): icon = "👁️"
            
            st.markdown(f"""
            <div style="background:rgba(0, 20, 0, 0.6); padding:10px; margin-bottom:5px; border-left:4px solid #00ffff;">
                <div style="font-weight:bold; color:#00ff41; word-break: break-all;">{icon} {f_name}</div>
                <div style="font-size:0.8em; color:#00ffff;">SIZE: {f_size}</div>
            </div>
            """, unsafe_allow_html=True)
            with open(f_path, "rb") as fb:
                st.download_button(f"⬇️ GET {f_name}", fb, f_name, key=f_path, use_container_width=True)
