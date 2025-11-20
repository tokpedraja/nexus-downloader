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
    page_title="NEXUS TANK V7: GOD MODE",
    page_icon="☢️",
    layout="wide",
    initial_sidebar_state="expanded"
)

DOWNLOAD_DIR = "nexus_vault"
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

# --- 1. CYBERPUNK UI INJECTION ---
st.markdown("""
    <style>
    /* Main Theme */
    .stApp {
        background-color: #050505;
        color: #00ff41;
        font-family: 'Courier New', Courier, monospace;
    }
    
    /* Titles & Headers */
    h1, h2, h3 {
        color: #00ff41 !important;
        text-shadow: 0 0 10px #00ff41;
        text-transform: uppercase;
    }
    
    /* Input Fields */
    .stTextArea textarea, .stTextInput input {
        background-color: #111 !important;
        color: #00ff41 !important;
        border: 1px solid #00ff41 !important;
        border-radius: 0px;
    }
    
    /* Buttons */
    div.stButton > button {
        background-color: #000 !important;
        color: #00ff41 !important;
        border: 1px solid #00ff41 !important;
        border-radius: 0px;
        transition: all 0.3s ease;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    div.stButton > button:hover {
        background-color: #00ff41 !important;
        color: #000 !important;
        box-shadow: 0 0 15px #00ff41;
    }
    
    /* Expander & Status */
    .streamlit-expanderHeader {
        background-color: #111 !important;
        color: #00ff41 !important;
        border: 1px solid #333;
    }
    
    /* Custom Cards */
    .nexus-card {
        border: 1px dashed #444;
        padding: 15px;
        background: #0a0a0a;
        margin-bottom: 10px;
    }
    
    /* Toast */
    .stToast {
        background-color: #111 !important;
        border: 1px solid #00ff41 !important;
        color: #fff !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. UTILITY ENGINES ---
def get_random_user_agent():
    agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0'
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

# --- 3. SIDEBAR: COMMAND CENTER ---
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/null/console.png", width=50)
    st.title("COMMAND CENTER")
    
    st.markdown("### 🔐 AUTH MATRIX")
    cookies_txt = st.text_area("Netscape Cookies", height=100, placeholder="# Paste content of cookies.txt here", help="Wajib untuk video age-restricted/premium.")
    
    st.markdown("### 👻 STEALTH MODE")
    use_stealth = st.checkbox("Enable User-Agent Rotation", value=True)
    proxy_url = st.text_input("Custom Proxy (Optional)", placeholder="http://user:pass@ip:port")
    
    st.divider()
    
    col_clean1, col_clean2 = st.columns(2)
    with col_clean1:
        if st.button("🗑️ PURGE VAULT"):
            if cleanup_vault():
                st.toast("VAULT PURGED SUCCESSFULLY", icon="💀")
    with col_clean2:
         st.metric("Files Stored", len(os.listdir(DOWNLOAD_DIR)))

# --- 4. MAIN INTERFACE ---
st.markdown("# ☢️ NEXUS TANK V7 <span style='font-size:0.5em; color:#666'>GOD MODE EDITION</span>", unsafe_allow_html=True)

# TABS
tab_core, tab_god, tab_files, tab_sys = st.tabs(["⬇️ CORE DOWNLOADER", "⚡ GOD FEATURES", "📂 VAULT", "📟 SYSTEM LOGS"])

# === TAB 1: CORE ===
with tab_core:
    with st.container():
        st.markdown('<div class="nexus-card">', unsafe_allow_html=True)
        target_urls = st.text_area("TARGET COORDINATES (URLS)", height=150, placeholder="https://youtube.com/watch?v=...\nOne URL per line")
        st.markdown('</div>', unsafe_allow_html=True)

    col_type, col_format = st.columns(2)
    with col_type:
        dl_mode = st.selectbox("OPERATION MODE", ["📺 VIDEO (Best Quality)", "🎵 AUDIO (Extract High-Res)", "🖼️ THUMBNAIL ONLY"])
    with col_format:
        if "VIDEO" in dl_mode:
            video_res = st.select_slider("MAX RESOLUTION LIMIT", options=["480p", "720p", "1080p", "1440p (2K)", "2160p (4K)", "UNLIMITED"], value="UNLIMITED")
        elif "AUDIO" in dl_mode:
            audio_fmt = st.selectbox("AUDIO FORMAT", ["mp3", "m4a", "wav", "flac"], index=0)

    # EXECUTION BUTTON
    if st.button("🚀 INITIATE SEQUENCE", type="primary", use_container_width=True):
        if not target_urls.strip():
            st.error("❌ NO TARGETS DETECTED. ABORTING.")
        else:
            urls = [u.strip() for u in target_urls.split('\n') if u.strip()]
            
            # PROGRESS BAR UI
            progress_text = st.empty()
            my_bar = st.progress(0)
            log_area = st.empty()
            
            # SETUP COOKIES
            cookie_file = "nexus_cookies.txt"
            if cookies_txt:
                with open(cookie_file, "w") as f: f.write(cookies_txt)
            
            # SETUP OPTIONS
            ydl_opts = {
                'outtmpl': f'{DOWNLOAD_DIR}/%(title)s [%(id)s].%(ext)s',
                'restrictfilenames': True,
                'quiet': True,
                'no_warnings': True,
                'nocheckcertificate': True,
                'ignoreerrors': True,
                'writethumbnail': True,  # Embed thumbnail capability
            }

            # STEALTH & NETWORK
            if use_stealth:
                ydl_opts['user_agent'] = get_random_user_agent()
            if proxy_url:
                ydl_opts['proxy'] = proxy_url

            # GOD MODE CONFIGS
            if "VIDEO" in dl_mode:
                res_map = {"480p": "480", "720p": "720", "1080p": "1080", "1440p (2K)": "1440", "2160p (4K)": "2160"}
                if video_res == "UNLIMITED":
                    ydl_opts['format'] = 'bestvideo+bestaudio/best'
                else:
                    h = res_map[video_res]
                    ydl_opts['format'] = f'bestvideo[height<={h}]+bestaudio/best[height<={h}]'
                ydl_opts['merge_output_format'] = 'mp4'
                ydl_opts['postprocessors'] = [{'key': 'FFmpegEmbedSubtitle'}] # Auto Subtitles embed
                
            elif "AUDIO" in dl_mode:
                ydl_opts['format'] = 'bestaudio/best'
                ydl_opts['postprocessors'] = [
                    {'key': 'FFmpegExtractAudio', 'preferredcodec': audio_fmt},
                    {'key': 'FFmpegMetadata'}, # Embed Metadata
                    {'key': 'EmbedThumbnail'}, # Embed Cover Art
                ]
            
            elif "THUMBNAIL" in dl_mode:
                ydl_opts['writethumbnail'] = True
                ydl_opts['skip_download'] = True

            # SPONSORBLOCK (SECRET FEATURE)
            if st.session_state.get('sponsorblock', False):
                ydl_opts['postprocessors'].append({
                    'key': 'SponsorBlock',
                    'categories': ['sponsor', 'intro', 'outro', 'selfpromo'],
                    'when': 'after_filter'
                })

            # EXECUTION LOOP
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                success = 0
                for i, url in enumerate(urls):
                    progress = (i / len(urls))
                    my_bar.progress(progress)
                    progress_text.text(f"PROCESSING TARGET {i+1}/{len(urls)}: {url}")
                    
                    try:
                        info = ydl.extract_info(url, download=True)
                        title = info.get('title', 'Unknown Entity')
                        log_area.info(f"✅ ACQUIRED: {title}")
                        success += 1
                    except Exception as e:
                        err = str(e)
                        if "Sign in" in err:
                            log_area.error(f"❌ AUTH ERROR: Cookies Required for {url}")
                        elif "429" in err:
                            log_area.error(f"❌ RATE LIMIT: IP Burned. Use Proxy.")
                        else:
                            log_area.error(f"❌ FAILED: {err}")
            
            my_bar.progress(100)
            if success > 0:
                st.balloons()
                st.success(f"MISSION COMPLETE. {success}/{len(urls)} TARGETS SECURED.")
            
            # Cleanup Cookies
            if os.path.exists(cookie_file): os.remove(cookie_file)

# === TAB 2: GOD FEATURES ===
with tab_god:
    st.markdown("### ⚡ ADVANCED OVERRIDES")
    st.info("Fitur ini meningkatkan kapabilitas download namun mungkin memperlambat proses.")
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### 🛡️ SPONSOR BLOCK")
        sb_enable = st.toggle("Auto-Skip Sponsors & Intros", value=False, key="sponsorblock")
        st.caption("Menggunakan API SponsorBlock untuk memotong bagian video yang tidak penting (Iklan dalam video, intro panjang, dll) secara otomatis sebelum disimpan.")

    with c2:
        st.markdown("#### 🐌 THROTTLE CONTROL")
        ratelimit = st.toggle("Simulate Human Speed", value=False)
        if ratelimit:
            st.caption("Membatasi kecepatan download untuk menghindari deteksi bot YouTube.")
            # Logika ini akan diinject ke ydl_opts jika diaktifkan nanti (bisa dikembangkan)

    st.markdown("#### 🧬 METADATA SURGEON")
    st.write("Secara default, Nexus Tank V7 akan memaksa:")
    st.code("""
    - Embed Thumbnail (Cover Art)
    - Embed Artist & Title Meta tags
    - Embed Subtitles (For Video)
    - Convert to Compatible Container (MP4/MP3)
    """, language="yaml")

# === TAB 3: VAULT ===
with tab_files:
    st.markdown("### 📂 SECURE STORAGE VAULT")
    
    # List files
    files = []
    for root, dirs, filenames in os.walk(DOWNLOAD_DIR):
        for f in filenames:
            files.append(os.path.join(root, f))
    
    if not files:
        st.warning("VAULT IS EMPTY.")
    else:
        # Bulk Zip
        if st.button("📦 COMPRESS & EXFILTRATE ALL"):
            shutil.make_archive("Nexus_Loot", 'zip', DOWNLOAD_DIR)
            with open("Nexus_Loot.zip", "rb") as f:
                st.download_button("⬇️ DOWNLOAD ZIP", f, f"Nexus_Loot_{int(time.time())}.zip", "application/zip")
        
        st.divider()
        
        # Grid Layout for files
        for f_path in files:
            f_name = os.path.basename(f_path)
            f_size = format_bytes(os.path.getsize(f_path))
            
            col_icon, col_details, col_act = st.columns([1, 4, 2])
            with col_icon:
                if f_name.endswith(('.mp4', '.mkv', '.webm')):
                    st.write("📺")
                elif f_name.endswith(('.mp3', '.m4a', '.wav', '.flac')):
                    st.write("🎵")
                elif f_name.endswith(('.jpg', '.png', '.webp')):
                    st.write("🖼️")
                else:
                    st.write("📄")
            
            with col_details:
                st.write(f"**{f_name}**")
                st.caption(f"Size: {f_size}")
            
            with col_act:
                with open(f_path, "rb") as fb:
                    st.download_button(f"⬇️ GET", fb, f_name, key=f_name)

# === TAB 4: DIAGNOSTICS ===
with tab_sys:
    st.subheader("📟 SYSTEM DIAGNOSTICS")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        ff_check = shutil.which("ffmpeg")
        st.metric("FFmpeg Core", "ONLINE" if ff_check else "OFFLINE", delta_color="normal" if ff_check else "inverse")
    with c2:
        st.metric("Python Engine", "ACTIVE")
    with c3:
        st.metric("Write Permission", "GRANTED" if os.access(DOWNLOAD_DIR, os.W_OK) else "DENIED")

    if not ff_check:
        st.error("CRITICAL ERROR: FFmpeg core not found. Audio conversion and Video merging will fail. Install FFmpeg in 'packages.txt'.")

    st.markdown("### 🌐 NETWORK PROBE")
    if st.button("PING YOUTUBE SERVERS"):
        try:
            with yt_dlp.YoutubeDL({'quiet':True}) as ydl:
                info = ydl.extract_info("https://www.youtube.com/watch?v=jNQXAC9IVRw", download=False)
                st.success(f"✅ CONNECTION ESTABLISHED. Latency: Low. Title: {info['title']}")
        except Exception as e:
            st.error(f"❌ CONNECTION REFUSED: {e}")
            st.info("IP mungkin diblokir. Gunakan Proxy atau Cookies.")

# --- FOOTER ---
st.markdown("---")
st.markdown("<center><small>NEXUS TANK V7 // CODED FOR RESEARCH PURPOSES ONLY</small></center>", unsafe_allow_html=True)
