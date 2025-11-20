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
    page_title="NEXXUS ZIQVA V10 - VVIP",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

DOWNLOAD_DIR = "Ziqva_Downloads"
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

# --- 1. TAMPILAN ANTARMUKA (UI - MATRIX THEME) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700&family=Share+Tech+Mono&display=swap');

    /* --- BACKGROUND: CYBER MATRIX GRID --- */
    @keyframes gridMove {
        0% { background-position: 0 0; }
        100% { background-position: 50px 50px; }
    }
    @keyframes pulseNeon {
        0% { box-shadow: 0 0 5px #00ff41; }
        50% { box-shadow: 0 0 20px #00ff41, 0 0 10px #00ffff; }
        100% { box-shadow: 0 0 5px #00ff41; }
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
    
    /* --- INPUT FIELDS (Matrix Style) --- */
    .stTextArea textarea, .stTextInput input, .stSelectbox div[data-baseweb="select"] {
        background-color: rgba(0, 20, 0, 0.9) !important;
        color: #00ff41 !important;
        border: 1px solid #00ff41 !important;
        border-radius: 2px;
        font-family: 'Share Tech Mono', monospace;
    }
    
    /* --- TOMBOL VVIP --- */
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
    div.stButton > button:active {
        background: #00ffff !important; /* Cyan saat diklik */
    }
    
    /* --- KARTU KONTEN --- */
    .ziqva-card {
        background: rgba(0, 15, 5, 0.85);
        border: 1px solid #00ff41;
        border-left: 5px solid #00ffff; /* Aksen Cyan */
        padding: 20px;
        margin-bottom: 15px;
        position: relative;
        backdrop-filter: blur(4px);
    }
    .ziqva-card::before {
        content: "VVIP_ACCESS";
        position: absolute;
        top: -10px;
        right: 10px;
        background: #000;
        color: #00ffff;
        font-size: 10px;
        padding: 0 5px;
        border: 1px solid #00ffff;
        letter-spacing: 1px;
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

    /* --- MOBILE FIX --- */
    @media (max-width: 640px) {
        h1 { font-size: 1.6rem !important; }
        .stApp { background-size: 20px 20px; }
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. FUNGSI BANTUAN ---
def get_random_user_agent():
    agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
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
    
    st.markdown("### 🍪 Premium Auth")
    cookies_txt = st.text_area("Input Netscape Cookies", height=70)
    
    st.markdown("### 👻 Stealth Matrix")
    use_stealth = st.checkbox("User-Agent Spoofing", value=True)
    proxy_url = st.text_input("Elite Proxy Node")
    
    st.divider()
    if st.button("☢️ EMERGENCY WIPER"):
        if cleanup_vault():
            st.toast("CACHE CLEARED!", icon="♻️")
    
    st.caption(f"Artifacts: {len(os.listdir(DOWNLOAD_DIR))}")

# --- 4. HEADER ---
c_logo, c_text = st.columns([1, 6])
with c_logo:
    st.write("")
    st.markdown("<h1>🧬</h1>", unsafe_allow_html=True)
with c_text:
    st.markdown("# NEXXUS ZIQVA V10 <br><span style='font-size:0.5em; color:#000; background:#00ff41; padding:2px 10px; font-weight:bold; box-shadow: 0 0 10px #00ff41;'>VVIP GOD EDITION</span>", unsafe_allow_html=True)

# TABS UTAMA
tab_main, tab_vvip, tab_files, tab_info = st.tabs(["🚀 CORE TERMINAL", "💎 VVIP VAULT", "📂 ARTIFACTS", "ℹ️ WARNING"])

# === TAB 1: CORE TERMINAL ===
with tab_main:
    st.markdown('<div class="ziqva-card">', unsafe_allow_html=True)
    input_data = st.text_area("🔗 TARGET INPUT (URL / JUDUL)", height=100, placeholder="Paste URL or Type Song Title (Deep Search Active)...")
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
            
            # UI Progress
            status_box = st.status("⚙️ SYSTEM RUNNING...", expanded=True)
            log_ph = st.empty()
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
                    prog_txt.code("✅ DOWNLOAD COMPLETE. PROCESSING...")

            with status_box:
                hacking_effect(log_ph)
                
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

                # --- VVIP FEATURES LOGIC ---
                
                # 1. HYPER-THREADING (Speed Hack)
                if st.session_state.get('vvip_speed', False):
                    # Download file in fragments concurrently (Simulate IDM)
                    opts['concurrent_fragment_downloads'] = 10
                    st.write("🚀 HYPER-THREADING: 10 Parallel Threads Active!")

                # 2. LIVE INTERCEPTOR
                if st.session_state.get('vvip_live', False):
                    opts['live_from_start'] = True
                    opts['wait_for_video'] = (1, 10) # Wait logic
                    st.write("📡 LIVE INTERCEPTOR: Recording Stream from Start...")

                # 3. GHOST METADATA (Anti-Lacak)
                if st.session_state.get('vvip_ghost', False):
                    opts['add_metadata'] = False
                    # Force strip metadata via ffmpeg args
                    opts['postprocessor_args'] = {'ffmpeg': ['-map_metadata', '-1', '-bn', '-vn']}
                    st.write("👻 GHOST PROTOCOL: Stripping all metadata signatures...")

                # 4. SONIC MUTATOR
                if "Audio" in dl_mode and st.session_state.get('sonic_active', False):
                    effect = st.session_state.get('sonic_effect', 'Normal')
                    ffmpeg_args = []
                    if effect == 'Nightcore': ffmpeg_args = ['-af', 'asetrate=44100*1.25,aresample=44100']
                    elif effect == 'Slowed+Reverb': ffmpeg_args = ['-af', 'asetrate=44100*0.85,aresample=44100,aecho=0.8:0.9:1000:0.3']
                    elif effect == 'Bass Boost': ffmpeg_args = ['-af', 'equalizer=f=50:width_type=o:width=2:g=20']
                    if ffmpeg_args: opts['postprocessor_args'] = {'ffmpeg': ffmpeg_args}

                # 5. Standard Pro Features
                if st.session_state.get('geo_active', False):
                    opts['geo_bypass_country'] = st.session_state.get('geo_code', 'US')
                
                if st.session_state.get('vacuum_active', False):
                    opts['playlistend'] = st.session_state.get('vacuum_limit', 5)
                else:
                    opts['noplaylist'] = True

                if st.session_state.get('cut_active', False):
                    opts['external_downloader'] = 'ffmpeg'
                    start, end = st.session_state.get('t_start', '00:00:00'), st.session_state.get('t_end', '00:01:00')
                    opts['external_downloader_args'] = {'ffmpeg_i': ['-ss', start, '-to', end]}
                
                if st.session_state.get('sub_on', False):
                    opts['writesubtitles'] = True; opts['subtitleslangs'] = ['all']; opts['postprocessors'] = [{'key': 'FFmpegEmbedSubtitle'}]
                if st.session_state.get('ad_kill', False):
                    opts.setdefault('postprocessors', []).append({'key': 'SponsorBlock', 'categories': ['sponsor', 'intro', 'outro']})

                # Format Config
                if "Video" in dl_mode:
                    h = {"360p":"360","720p":"720","1080p":"1080","2K":"1440","4K":"2160","8K":"4320"}.get(video_res, "1080")
                    opts['format'] = f'bestvideo[height<={h}]+bestaudio/best[height<={h}]'
                    opts['merge_output_format'] = 'mp4'
                elif "Audio" in dl_mode:
                    opts['format'] = 'bestaudio/best'
                    opts['postprocessors'] = [{'key': 'FFmpegExtractAudio', 'preferredcodec': audio_fmt}, {'key': 'FFmpegMetadata'}, {'key': 'EmbedThumbnail'}]
                elif "Intel" in dl_mode:
                    opts['skip_download'] = True

                # EXECUTION
                with yt_dlp.YoutubeDL(opts) as ydl:
                    sukses = 0
                    for line in raw_lines:
                        target = line
                        if not line.startswith(('http', 'www')):
                            st.write(f"🕵️ Deep Search: Searching Database for '{line}'...")
                            target = f"ytsearch1:{line}"
                        
                        try:
                            st.write(f"🎯 Locking Target: {line}")
                            ydl.extract_info(target, download=True)
                            sukses += 1
                        except Exception as e:
                            st.error(f"Mission Failed: {str(e)}")
                
                if os.path.exists(c_file): os.remove(c_file)
            
            if sukses > 0:
                st.balloons()
                st.success(f"🎉 MISSION ACCOMPLISHED! {sukses} Artifacts Secured.")
                time.sleep(2)
                st.rerun()

# === TAB 2: VVIP VAULT (HIDDEN FEATURES) ===
with tab_vvip:
    st.markdown("### 💎 CLASSIFIED VVIP TOOLS")
    
    c_v1, c_v2 = st.columns(2)
    
    with c_v1:
        st.markdown('<div class="ziqva-card">', unsafe_allow_html=True)
        st.markdown("**🚀 HYPER-THREADING (Speed Hack)**")
        st.toggle("Force 10x Connections (IDM Style)", key="vvip_speed")
        st.caption("Memaksa server membuka 10 jalur koneksi sekaligus. Internet kencang wajib!")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="ziqva-card">', unsafe_allow_html=True)
        st.markdown("**📡 LIVE STREAM INTERCEPTOR**")
        st.toggle("Rekam Live Stream (Real-Time)", key="vvip_live")
        st.caption("Merekam siaran langsung dari awal buffer. Jangan tutup tab saat merekam!")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="ziqva-card">', unsafe_allow_html=True)
        st.markdown("**🔊 SONIC MUTATOR**")
        sonic_active = st.toggle("Audio Modulator", key="sonic_active")
        st.selectbox("Effect", ["Nightcore", "Slowed+Reverb", "Bass Boost"], key="sonic_effect", disabled=not sonic_active)
        st.markdown('</div>', unsafe_allow_html=True)

    with c_v2:
        st.markdown('<div class="ziqva-card">', unsafe_allow_html=True)
        st.markdown("**👻 GHOST PROTOCOL (Metadata Wiper)**")
        st.toggle("Hapus Total Jejak Metadata", key="vvip_ghost")
        st.caption("Menghapus info encoder, GPS, tanggal, dan device ID dari file hasil download. 100% Bersih.")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="ziqva-card">', unsafe_allow_html=True)
        st.markdown("**🌍 TELEPORT & VACUUM**")
        st.toggle("Geo-Block Bypass", key="geo_active")
        st.text_input("ISO Code", "US", key="geo_code")
        st.toggle("Playlist Vacuum", key="vacuum_active")
        st.slider("Qty", 1, 50, 5, key="vacuum_limit")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="ziqva-card">', unsafe_allow_html=True)
        st.markdown("**🛡️ UTILS**")
        st.toggle("Time Clipper", key="cut_active")
        c_t1, c_t2 = st.columns(2)
        c_t1.text_input("Start", "00:00:00", key="t_start")
        c_t2.text_input("End", "00:01:00", key="t_end")
        st.checkbox("Ads Killer", key="ad_kill")
        st.checkbox("Subs Injector", key="sub_on")
        st.markdown('</div>', unsafe_allow_html=True)

# === TAB 3: ARTIFACTS ===
with tab_files:
    st.markdown("### 📂 SECURE STORAGE")
    files = sorted([os.path.join(DOWNLOAD_DIR, f) for f in os.listdir(DOWNLOAD_DIR)], key=os.path.getmtime, reverse=True)
    
    if not files:
        st.info("STORAGE EMPTY. WAITING FOR PAYLOAD.")
    else:
        if st.button("📦 EXTRACT ALL (ZIP)"):
            shutil.make_archive("Ziqva_VVIP", 'zip', DOWNLOAD_DIR)
            with open("Ziqva_VVIP.zip", "rb") as f:
                st.download_button("⬇️ DOWNLOAD PACKAGE", f, "Ziqva_VVIP.zip", "application/zip")
        
        st.divider()
        for f_path in files:
            f_name = os.path.basename(f_path)
            if f_name.endswith(('.part', '.ytdl')): continue
            f_size = format_bytes(os.path.getsize(f_path))
            
            st.markdown(f"""
            <div style="background:rgba(0, 20, 0, 0.6); padding:10px; margin-bottom:5px; border-left:4px solid #00ffff;">
                <div style="font-weight:bold; color:#00ff41; word-break: break-all;">{f_name}</div>
                <div style="font-size:0.8em; color:#00ffff;">SIZE: {f_size}</div>
            </div>
            """, unsafe_allow_html=True)
            
            with open(f_path, "rb") as fb:
                st.download_button(f"⬇️ GET {f_name}", fb, f_name, key=f_path, use_container_width=True)

# === TAB 4: INFO & WARNING (MANDATORY) ===
with tab_info:
    st.markdown("### 👤 OPERATOR INTEL")
    
    c_i1, c_i2 = st.columns([1, 3])
    with c_i1:
        st.image("https://img.icons8.com/fluency/96/hacker.png")
    with c_i2:
        st.markdown("""
        **Developer:** Telegram [@effands](https://t.me/effands)  
        **Website:** [ziqva.com](https://ziqva.com)  
        **Email:** cs@ziqva.com
        """)
    
    st.divider()
    
    # --- WARNING SECTION (SESUAI REQUEST) ---
    st.warning("""
    ### ⚠️ Warning !!
    
    **Pakailah dengan Bijak** tools ini gratis tidak untuk di perjual belikan, murni untuk berbagi. 
    Segara resiko menjadi tanggung jawab pengguna masing-masing.

    **Butuh tools lain, DM ke telegram aja bos ku..**
    """)
    
    st.success("System Status: **ONLINE** | VVIP Access: **GRANTED**")
