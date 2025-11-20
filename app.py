import streamlit as st
import yt_dlp
import os
import shutil
import time
import random
import re
import glob
from datetime import datetime

# --- 0. SYSTEM CONFIGURATION ---
st.set_page_config(
    page_title="NEXUS TANK V8: OVERDRIVE",
    page_icon="☣️",
    layout="wide",
    initial_sidebar_state="collapsed" # Sidebar tertutup default agar rapi di HP
)

# Ganti nama folder sesuai request
DOWNLOAD_DIR = "Nexus_Downloads"
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

# --- 1. CYBERPUNK UI INJECTION (RESPONSIVE & ANIMATED) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');

    /* --- MAIN THEME --- */
    .stApp {
        background-color: #000000;
        background-image: radial-gradient(#112 15%, transparent 16%), radial-gradient(#112 15%, transparent 16%);
        background-size: 60px 60px;
        background-position: 0 0, 30px 30px;
        color: #0f0;
        font-family: 'Share Tech Mono', monospace;
    }

    /* --- TYPOGRAPHY & GLITCH EFFECT --- */
    h1, h2, h3 {
        color: #0f0 !important;
        text-transform: uppercase;
        text-shadow: 2px 2px 0px #003300; 
        letter-spacing: 2px;
    }
    
    h1 {
        animation: glitch 1s linear infinite;
    }

    @keyframes glitch {
        2%, 64% { transform: translate(2px,0) skew(0deg); }
        4%, 60% { transform: translate(-2px,0) skew(0deg); }
        62% { transform: translate(0,0) skew(5deg); }
    }

    /* --- INPUT FIELDS (Mobile Friendly) --- */
    .stTextArea textarea, .stTextInput input, .stSelectbox div[data-baseweb="select"] {
        background-color: #0a0a0a !important;
        color: #0f0 !important;
        border: 1px solid #333 !important;
        border-left: 3px solid #0f0 !important;
        border-radius: 0px;
        font-size: 16px; /* Cegah zoom di iOS */
    }
    
    /* --- BUTTONS (Holographic Style) --- */
    div.stButton > button {
        background: linear-gradient(45deg, #000, #111);
        color: #0f0 !important;
        border: 1px solid #0f0 !important;
        box-shadow: 0 0 5px #0f0;
        border-radius: 0px;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 3px;
        width: 100%; /* Full width di HP */
        padding: 0.5rem 1rem;
    }
    div.stButton > button:hover {
        background: #0f0 !important;
        color: #000 !important;
        box-shadow: 0 0 20px #0f0;
        text-shadow: none;
    }
    
    /* --- CUSTOM CARDS & ALERTS --- */
    .nexus-card {
        border: 1px solid #1a1a1a;
        padding: 15px;
        background: rgba(10, 20, 10, 0.9);
        box-shadow: inset 0 0 20px rgba(0, 255, 0, 0.05);
        margin-bottom: 15px;
        position: relative;
    }
    .nexus-card::before {
        content: "SYSTEM_READY";
        position: absolute;
        top: -10px;
        right: 10px;
        background: #000;
        color: #0f0;
        font-size: 0.7em;
        padding: 0 5px;
        border: 1px solid #333;
    }

    /* --- TERMINAL LOG ANIMATION --- */
    .terminal-log {
        font-family: 'Courier New', Courier, monospace;
        font-size: 0.9em;
        color: #00ff41;
        background-color: #000;
        padding: 10px;
        border-left: 2px solid #0f0;
        margin-top: 10px;
        height: 150px;
        overflow-y: auto;
    }

    /* --- MOBILE RESPONSIVENESS OVERRIDES --- */
    @media (max-width: 640px) {
        h1 { font-size: 1.8rem !important; }
        .stTabs [data-baseweb="tab-list"] {
            flex-wrap: wrap;
        }
        .stTabs [data-baseweb="tab"] {
            flex-grow: 1;
            text-align: center;
        }
        /* Sembunyikan elemen ribet di HP */
        .hide-mobile { display: none; }
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. UTILITY ENGINES ---
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

# --- 3. ANIMATION ENGINE (VISUAL ONLY) ---
def simulate_hacking(log_placeholder):
    """Fungsi untuk membuat efek loading yang keren ala hacker"""
    lines = [
        "CONNECTING TO NEURAL NETWORK...",
        "BYPASSING MAINFRAME FIREWALL...",
        "DECRYPTING VIDEO SIGNATURE...",
        "ESTABLISHING SECURE HANDSHAKE...",
        "INJECTING PAYLOAD...",
        "ACCESS GRANTED."
    ]
    log_text = ""
    for line in lines:
        time.sleep(random.uniform(0.1, 0.4))
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_text += f"[{timestamp}] > {line}\n"
        log_placeholder.code(log_text, language="bash")

# --- 4. SIDEBAR: COMMAND CENTER ---
with st.sidebar:
    st.image("https://img.icons8.com/nolan/96/matrix-desktop.png", width=60)
    st.markdown("## 🕹️ CONTROL PANEL")
    
    st.markdown("### 🔐 ACCESS KEY")
    cookies_txt = st.text_area("Cookies.txt (Optional)", height=80, help="Paste Netscape Cookies untuk akses premium/18+")
    
    st.markdown("### 🛡️ STEALTH CONFIG")
    use_stealth = st.checkbox("User-Agent Rotation", value=True)
    proxy_url = st.text_input("Proxy Node IP", placeholder="http://user:pass@ip:port")
    
    st.divider()
    
    if st.button("☢️ NUKE STORAGE"):
        if cleanup_vault():
            st.toast("SYSTEM PURGED.", icon="💥")
    
    st.caption(f"Storage: {len(os.listdir(DOWNLOAD_DIR))} Files")

# --- 5. MAIN INTERFACE ---
col_logo, col_title = st.columns([1, 5])
with col_logo:
    st.write("") # Spacing
    st.markdown("# ☣️")
with col_title:
    st.markdown("# NEXUS TANK V8 <br><span style='font-size:0.4em; color:#666; letter-spacing:5px;'>OVERDRIVE EDITION</span>", unsafe_allow_html=True)

# TABS
tab_core, tab_god, tab_files, tab_logs = st.tabs(["⬇️ TERMINAL", "⚡ OVERDRIVE", "📦 DOWNLOADS", "📟 LOGS"])

# === TAB 1: CORE TERMINAL ===
with tab_core:
    st.markdown('<div class="nexus-card">', unsafe_allow_html=True)
    target_urls = st.text_area("TARGET URLS (Universal Support: YT, IG, TT, FB)", height=120, placeholder="Paste link here. Supports Multi-line.")
    st.markdown('</div>', unsafe_allow_html=True)

    # Responsive Controls
    c1, c2 = st.columns(2)
    with c1:
        dl_mode = st.selectbox("PROTOCOL", ["📺 VIDEO (High-Res)", "🎵 AUDIO (Hi-Fi)", "🖼️ METADATA ONLY"])
    with c2:
        if "VIDEO" in dl_mode:
            video_res = st.select_slider("RESOLUTION CAP", options=["480p", "720p", "1080p", "4K"], value="1080p")
        elif "AUDIO" in dl_mode:
            audio_fmt = st.selectbox("CODEC", ["mp3", "m4a", "flac"], index=0)

    st.write("")
    if st.button("🚀 INITIATE DOWNLOAD SEQUENCE", type="primary", use_container_width=True):
        if not target_urls.strip():
            st.error("⚠️ NO TARGET DETECTED.")
        else:
            urls = [u.strip() for u in target_urls.split('\n') if u.strip()]
            
            # UI Elements for Progress
            status_box = st.status("⚙️ SYSTEM PROCESS RUNNING...", expanded=True)
            log_placeholder = st.empty()
            prog_bar = st.progress(0)
            
            with status_box:
                # 1. Animation Phase
                st.write("Initializing handshake...")
                simulate_hacking(log_placeholder)
                
                # 2. Setup Phase
                cookie_file = "nexus_cookies.txt"
                if cookies_txt:
                    with open(cookie_file, "w") as f: f.write(cookies_txt)
                
                ydl_opts = {
                    'outtmpl': f'{DOWNLOAD_DIR}/%(title)s [%(id)s].%(ext)s',
                    'restrictfilenames': True,
                    'quiet': True,
                    'no_warnings': True,
                    'nocheckcertificate': True,
                    'ignoreerrors': True,
                    'writethumbnail': True,
                }

                if use_stealth: ydl_opts['user_agent'] = get_random_user_agent()
                if proxy_url: ydl_opts['proxy'] = proxy_url

                # Config Logic
                if "VIDEO" in dl_mode:
                    res_map = {"480p": "480", "720p": "720", "1080p": "1080", "4K": "2160"}
                    h = res_map.get(video_res, "2160")
                    ydl_opts['format'] = f'bestvideo[height<={h}]+bestaudio/best[height<={h}]'
                    ydl_opts['merge_output_format'] = 'mp4'
                elif "AUDIO" in dl_mode:
                    ydl_opts['format'] = 'bestaudio/best'
                    ydl_opts['postprocessors'] = [
                        {'key': 'FFmpegExtractAudio', 'preferredcodec': audio_fmt},
                        {'key': 'FFmpegMetadata'},
                        {'key': 'EmbedThumbnail'},
                    ]
                elif "METADATA" in dl_mode:
                    ydl_opts['writethumbnail'] = True
                    ydl_opts['skip_download'] = True

                # SponsorBlock Logic
                if st.session_state.get('sb_active', False):
                    ydl_opts['postprocessors'].append({
                        'key': 'SponsorBlock',
                        'categories': ['sponsor', 'intro', 'outro', 'selfpromo'],
                        'when': 'after_filter'
                    })

                # 3. Execution Phase
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    success_count = 0
                    for i, url in enumerate(urls):
                        try:
                            prog_bar.progress((i / len(urls)))
                            st.write(f"Downloading: {url}...")
                            ydl.extract_info(url, download=True)
                            success_count += 1
                        except Exception as e:
                            st.error(f"Failed: {url}")
                
                # Cleanup
                if os.path.exists(cookie_file): os.remove(cookie_file)
                prog_bar.progress(100)
                
            if success_count > 0:
                st.balloons()
                st.success(f"✅ SEQUENCE COMPLETE. {success_count} FILES SECURED.")
                time.sleep(1)
                st.rerun() # Auto refresh to show files

# === TAB 2: OVERDRIVE (GOD FEATURES) ===
with tab_god:
    st.markdown("### ⚡ OVERDRIVE SETTINGS")
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="nexus-card">', unsafe_allow_html=True)
        st.markdown("**🛡️ AD-BLOCKER ENGINE**")
        sb_active = st.toggle("Auto-Skip Sponsors & Intros", key='sb_active')
        st.caption("Menggunakan AI SponsorBlock untuk menghapus iklan di dalam video secara otomatis.")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with c2:
        st.markdown('<div class="nexus-card">', unsafe_allow_html=True)
        st.markdown("**🤖 UNIVERSAL PARSER**")
        st.info("Nexus Tank V8 mendukung: YouTube, Instagram Reels, TikTok (No Watermark), Twitter/X Videos, dan Facebook Watch.")
        st.markdown('</div>', unsafe_allow_html=True)

# === TAB 3: DOWNLOADS ===
with tab_files:
    st.markdown("### 📦 DOWNLOADS")
    
    files = sorted([os.path.join(DOWNLOAD_DIR, f) for f in os.listdir(DOWNLOAD_DIR)], key=os.path.getmtime, reverse=True)
    
    if not files:
        st.info("📁 Folder kosong. Mulai download sesuatu!")
    else:
        # Bulk Actions
        c_zip, c_info = st.columns([1, 2])
        with c_zip:
            if st.button("📦 ZIP ALL FILES"):
                shutil.make_archive("Nexus_Batch", 'zip', DOWNLOAD_DIR)
                with open("Nexus_Batch.zip", "rb") as f:
                    st.download_button("⬇️ DOWNLOAD ZIP", f, f"Nexus_Batch_{int(time.time())}.zip", "application/zip")
        
        st.divider()
        
        # File List (Mobile Friendly Card View)
        for f_path in files:
            f_name = os.path.basename(f_path)
            if f_name.endswith('.part') or f_name.endswith('.ytdl'): continue
            
            f_size = format_bytes(os.path.getsize(f_path))
            f_ext = f_name.split('.')[-1].upper()
            
            st.markdown(f"""
            <div style="background:#111; border:1px solid #333; padding:10px; margin-bottom:10px; border-radius:5px;">
                <div style="color:#0f0; font-weight:bold; word-wrap:break-word;">{f_name}</div>
                <div style="display:flex; justify-content:space-between; color:#888; font-size:0.8em; margin-top:5px;">
                    <span>TYPE: {f_ext}</span>
                    <span>SIZE: {f_size}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            with open(f_path, "rb") as fb:
                st.download_button(f"⬇️ Download {f_name}", fb, f_name, key=f_path, use_container_width=True)

# === TAB 4: LOGS ===
with tab_logs:
    st.subheader("📟 SYSTEM DIAGNOSTICS")
    col1, col2 = st.columns(2)
    col1.metric("FFmpeg Core", "DETECTED" if shutil.which("ffmpeg") else "MISSING")
    col2.metric("Write Access", "GRANTED" if os.access(DOWNLOAD_DIR, os.W_OK) else "DENIED")
    
    st.text_area("Debug Log", value="System initialized...\nReady for input...", height=200, disabled=True)

# --- FOOTER ---
st.markdown("---")
st.markdown("<div style='text-align:center; color:#444; font-size:0.7em;'>NEXUS TANK V8 // OVERDRIVE EDITION // MOBILE OPTIMIZED</div>", unsafe_allow_html=True)
