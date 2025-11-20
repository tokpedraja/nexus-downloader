import streamlit as st
import yt_dlp
import os
import shutil
import time
import random
import re
from datetime import datetime, timedelta, timezone

# --- 0. SYSTEM CONFIGURATION ---
st.set_page_config(
    page_title="NEXUS TANK V9: ULTIMATE",
    page_icon="☣️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

DOWNLOAD_DIR = "Nexus_Downloads"
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

# --- 1. CYBERPUNK UI INJECTION (NEW BACKGROUND & ANIMATION) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');

    /* --- ANIMATED BACKGROUND (CYBER GRID) --- */
    @keyframes gridMove {
        0% { background-position: 0 0; }
        100% { background-position: 50px 50px; }
    }

    .stApp {
        background-color: #050505;
        background-image: 
            linear-gradient(rgba(0, 255, 65, 0.05) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 255, 65, 0.05) 1px, transparent 1px);
        background-size: 40px 40px; /* Ukuran Grid */
        animation: gridMove 4s linear infinite; /* Gerakan Grid */
        color: #0f0;
        font-family: 'Share Tech Mono', monospace;
    }

    /* --- TYPOGRAPHY & GLOW --- */
    h1, h2, h3, h4 {
        color: #00ff41 !important;
        text-transform: uppercase;
        text-shadow: 0 0 10px rgba(0, 255, 65, 0.5);
        letter-spacing: 1px;
    }
    
    /* --- INPUT FIELDS (Mobile Optimized) --- */
    .stTextArea textarea, .stTextInput input, .stSelectbox div[data-baseweb="select"] {
        background-color: rgba(0, 0, 0, 0.8) !important;
        color: #0f0 !important;
        border: 1px solid #333 !important;
        border-left: 3px solid #0f0 !important;
        border-radius: 0px;
    }
    
    /* --- BUTTONS (Neon Style) --- */
    div.stButton > button {
        background: #000 !important;
        color: #0f0 !important;
        border: 1px solid #0f0 !important;
        box-shadow: 0 0 5px #0f0;
        transition: all 0.3s ease;
        text-transform: uppercase;
        font-weight: bold;
        width: 100%;
    }
    div.stButton > button:hover {
        background: #0f0 !important;
        color: #000 !important;
        box-shadow: 0 0 20px #0f0, inset 0 0 10px #000;
    }
    
    /* --- PROGRESS BAR COLOR --- */
    .stProgress > div > div > div > div {
        background-color: #0f0;
    }

    /* --- MOBILE FIXES --- */
    @media (max-width: 640px) {
        .stApp { background-size: 20px 20px; } /* Grid lebih kecil di HP */
        h1 { font-size: 1.5rem !important; }
    }
    
    /* --- CARD STYLE --- */
    .nexus-card {
        background: rgba(10, 20, 10, 0.85);
        border: 1px solid #1f1;
        padding: 15px;
        margin-bottom: 10px;
        backdrop-filter: blur(2px);
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. HELPER FUNCTIONS ---
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

# --- 3. HACKER ANIMATION ---
def simulate_hacking(log_placeholder):
    lines = [
        "INITIALIZING NEURAL LINK...",
        "BYPASSING GEO-BLOCKING...",
        "INJECTING PACKET STREAM...",
        "OPTIMIZING BANDWIDTH...",
        "ACCESS GRANTED."
    ]
    log_text = ""
    wib = timezone(timedelta(hours=7))
    
    for line in lines:
        time.sleep(random.uniform(0.1, 0.3)) 
        timestamp = datetime.now(wib).strftime("%H:%M:%S")
        log_text += f"[{timestamp}] > {line}\n"
        log_placeholder.code(log_text, language="bash")

# --- 4. SIDEBAR ---
with st.sidebar:
    st.image("https://img.icons8.com/nolan/96/matrix-desktop.png", width=60)
    st.markdown("## 🕹️ SYSTEM CONTROL")
    
    st.markdown("### 🔐 AUTH")
    cookies_txt = st.text_area("Cookies (Netscape)", height=70, help="Wajib untuk video premium/login.")
    
    st.markdown("### 🛡️ PROXY")
    use_stealth = st.checkbox("Anti-Bot Rotation", value=True)
    proxy_url = st.text_input("Custom Proxy IP")
    
    st.divider()
    if st.button("☢️ PURGE DATA"):
        if cleanup_vault():
            st.toast("MEMORY WIPED.", icon="💥")
    
    st.caption(f"Files: {len(os.listdir(DOWNLOAD_DIR))}")

# --- 5. MAIN INTERFACE ---
col_logo, col_title = st.columns([1, 6])
with col_logo:
    st.write("") 
    st.markdown("<h1>☢️</h1>", unsafe_allow_html=True)
with col_title:
    st.markdown("# NEXUS TANK V9 <br><span style='font-size:0.4em; color:#888; letter-spacing:4px;'>ULTIMATE EDITION</span>", unsafe_allow_html=True)

# TABS
tab_core, tab_sniper, tab_files, tab_logs = st.tabs(["⬇️ TERMINAL", "🎯 SNIPER MODE", "📦 STORAGE", "📟 LOGS"])

# === TAB 1: CORE TERMINAL (DOWNLOADER) ===
with tab_core:
    st.markdown('<div class="nexus-card">', unsafe_allow_html=True)
    target_urls = st.text_area("TARGET URLS (YouTube, TikTok, IG, FB, Twitter)", height=100, placeholder="Paste links here...")
    st.markdown('</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        dl_mode = st.selectbox("PROTOCOL", ["📺 VIDEO (Best)", "🎵 AUDIO (Convert)", "🖼️ THUMBNAIL"])
    with c2:
        if "VIDEO" in dl_mode:
            video_res = st.select_slider("RESOLUTION LIMIT", options=["360p", "720p", "1080p", "4K"], value="1080p")
        elif "AUDIO" in dl_mode:
            audio_fmt = st.selectbox("FORMAT", ["mp3", "m4a", "flac"], index=0)

    st.write("")
    if st.button("🚀 EXECUTE DOWNLOAD", type="primary", use_container_width=True):
        if not target_urls.strip():
            st.error("⚠️ NO TARGET DETECTED.")
        else:
            urls = [u.strip() for u in target_urls.split('\n') if u.strip()]
            
            # PROGRESS UI
            status_cont = st.status("⚙️ INITIALIZING...", expanded=True)
            log_ph = st.empty()
            
            # --- PROGRESS HOOK (The Secret Sauce) ---
            # Kita butuh placeholder di luar hook agar bisa diupdate
            prog_bar = st.progress(0)
            prog_text = st.empty()

            def progress_hook(d):
                if d['status'] == 'downloading':
                    try:
                        # Parse percentage
                        p = d.get('_percent_str', '0%').replace('%','')
                        val = float(p) / 100
                        prog_bar.progress(min(val, 1.0))
                        
                        # Tampilkan Detail Statistik Real-time
                        speed = d.get('_speed_str', 'N/A')
                        eta = d.get('_eta_str', 'N/A')
                        percent = d.get('_percent_str', '0%')
                        prog_text.code(f"⚡ SPEED: {speed} | ⏳ ETA: {eta} | 🔋 DONE: {percent}")
                    except:
                        pass
                elif d['status'] == 'finished':
                    prog_bar.progress(1.0)
                    prog_text.code("✅ DOWNLOAD FINISHED. CONVERTING...")

            with status_cont:
                st.write("Handshake protocol...")
                simulate_hacking(log_ph)
                
                # Cookie Setup
                cookie_file = "nexus_cookies.txt"
                if cookies_txt:
                    with open(cookie_file, "w") as f: f.write(cookies_txt)
                
                # YTDL CONFIG
                ydl_opts = {
                    'outtmpl': f'{DOWNLOAD_DIR}/%(title)s [%(id)s].%(ext)s',
                    'restrictfilenames': True,
                    'quiet': True,
                    'no_warnings': True,
                    'ignoreerrors': True,
                    'writethumbnail': True,
                    'progress_hooks': [progress_hook], # Attach Hook
                }

                if use_stealth: ydl_opts['user_agent'] = get_random_user_agent()
                if proxy_url: ydl_opts['proxy'] = proxy_url

                # SNIPER MODE CHECK (Time Range)
                if st.session_state.get('sniper_active', False):
                    start_t = st.session_state.get('sniper_start', '00:00:00')
                    end_t = st.session_state.get('sniper_end', '00:01:00')
                    # Gunakan command external downloader args untuk memotong
                    ydl_opts['download_ranges'] = yt_dlp.utils.download_range_func(None, [(0, 0)]) # Dummy to trigger
                    # NOTE: yt-dlp internal range agak tricky, kita pakai post-processor args via ffmpeg lebih stabil biasanya, 
                    # tapi fitur 'download_ranges' callback lebih native jika didukung.
                    # Cara paling ampuh di yt-dlp modern adalah:
                    ydl_opts['external_downloader'] = 'ffmpeg'
                    ydl_opts['external_downloader_args'] = {'ffmpeg_i': ['-ss', start_t, '-to', end_t]}

                # SUBTITLE CHECK
                if st.session_state.get('sub_active', False):
                    ydl_opts['writesubtitles'] = True
                    ydl_opts['subtitleslangs'] = ['en', 'id', 'all']
                    ydl_opts['postprocessors'] = [{'key': 'FFmpegEmbedSubtitle'}]

                # MODE CONFIG
                if "VIDEO" in dl_mode:
                    res_map = {"360p": "360", "720p": "720", "1080p": "1080", "4K": "2160"}
                    h = res_map.get(video_res, "1080")
                    ydl_opts['format'] = f'bestvideo[height<={h}]+bestaudio/best[height<={h}]'
                    ydl_opts['merge_output_format'] = 'mp4'
                elif "AUDIO" in dl_mode:
                    ydl_opts['format'] = 'bestaudio/best'
                    ydl_opts['postprocessors'] = [
                        {'key': 'FFmpegExtractAudio', 'preferredcodec': audio_fmt},
                        {'key': 'FFmpegMetadata'},
                        {'key': 'EmbedThumbnail'},
                    ]
                elif "THUMBNAIL" in dl_mode:
                    ydl_opts['skip_download'] = True

                # SPONSOR BLOCK
                if st.session_state.get('sb_active', False):
                    ydl_opts.setdefault('postprocessors', []).append({
                        'key': 'SponsorBlock',
                        'categories': ['sponsor', 'intro', 'outro'],
                    })

                # EXECUTION
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    success = 0
                    for i, url in enumerate(urls):
                        try:
                            st.write(f"Targeting: {url}")
                            ydl.extract_info(url, download=True)
                            success += 1
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
                
                if os.path.exists(cookie_file): os.remove(cookie_file)
                
            if success > 0:
                st.balloons()
                st.success(f"✅ MISSION SUCCESS. {success} FILES SECURED.")
                time.sleep(1.5)
                st.rerun()

# === TAB 2: SNIPER MODE (SECRET FEATURES) ===
with tab_sniper:
    st.markdown("### 🎯 SNIPER TOOLS")
    st.caption("Fitur rahasia untuk manipulasi download tingkat lanjut.")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="nexus-card">', unsafe_allow_html=True)
        st.markdown("**⏱️ TIME CLIPPER**")
        sniper_active = st.toggle("Enable Time Slice", key="sniper_active")
        
        sc1, sc2 = st.columns(2)
        with sc1: 
            st.text_input("Start (HH:MM:SS)", value="00:00:00", key="sniper_start", disabled=not sniper_active)
        with sc2:
            st.text_input("End (HH:MM:SS)", value="00:01:00", key="sniper_end", disabled=not sniper_active)
        
        st.caption("⚠️ Hanya download bagian durasi ini. Berguna untuk ambil klip/meme.")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with c2:
        st.markdown('<div class="nexus-card">', unsafe_allow_html=True)
        st.markdown("**📝 SUBTITLE INJECTOR**")
        sub_active = st.toggle("Auto-Burn Subtitles", key="sub_active")
        st.caption("Otomatis download & embed subtitle (Indonesia/English) ke dalam video jika tersedia.")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="nexus-card">', unsafe_allow_html=True)
        st.markdown("**🚫 AD-KILLER**")
        sb_active = st.toggle("SponsorBlock AI", key="sb_active")
        st.caption("Auto-skip segmen sponsor & intro youtuber.")
        st.markdown('</div>', unsafe_allow_html=True)

# === TAB 3: STORAGE ===
with tab_files:
    st.markdown("### 📦 SECURE VAULT")
    files = sorted([os.path.join(DOWNLOAD_DIR, f) for f in os.listdir(DOWNLOAD_DIR)], key=os.path.getmtime, reverse=True)
    
    if not files:
        st.info("📁 VAULT IS EMPTY.")
    else:
        if st.button("📦 ZIP ALL FILES"):
            shutil.make_archive("Nexus_Ultima", 'zip', DOWNLOAD_DIR)
            with open("Nexus_Ultima.zip", "rb") as f:
                st.download_button("⬇️ DOWNLOAD ZIP", f, f"Nexus_Ultima_{int(time.time())}.zip", "application/zip")
        
        st.divider()
        for f_path in files:
            f_name = os.path.basename(f_path)
            if f_name.endswith('.part') or f_name.endswith('.ytdl'): continue
            f_size = format_bytes(os.path.getsize(f_path))
            
            st.markdown(f"""
            <div style="background:rgba(0,20,0,0.6); border:1px dashed #0f0; padding:10px; margin-bottom:8px;">
                <div style="color:#fff; font-weight:bold;">{f_name}</div>
                <small style="color:#0f0;">SIZE: {f_size}</small>
            </div>
            """, unsafe_allow_html=True)
            
            with open(f_path, "rb") as fb:
                st.download_button(f"⬇️ GET", fb, f_name, key=f_path, use_container_width=True)

# === TAB 4: LOGS ===
with tab_logs:
    st.subheader("📟 DEBUG CONSOLE")
    c1, c2 = st.columns(2)
    c1.metric("FFmpeg Status", "ONLINE" if shutil.which("ffmpeg") else "CRITICAL FAIL")
    c2.metric("Storage Write", "OK" if os.access(DOWNLOAD_DIR, os.W_OK) else "LOCKED")
    st.text_area("System Log", "Waiting for input signal...", height=150)
    st.caption("Nexus Tank V9.0 Build 2025")
