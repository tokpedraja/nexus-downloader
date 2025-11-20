import streamlit as st
import yt_dlp
import os
import time
import shutil
import zipfile

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="NEXUS BATCH DOWNLOADER V4.5",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. CSS HARDCORE (Dark Mode Force) ---
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #050505 !important; }
    [data-testid="stHeader"] { background-color: rgba(0,0,0,0) !important; }
    * { font-family: 'JetBrains Mono', monospace !important; }
    
    .cyber-card {
        border: 1px solid #333; background-color: #0a0a0a;
        padding: 20px; margin-bottom: 25px; border-left: 5px solid #ccff00;
        box-shadow: 0px 0px 20px rgba(0,0,0,0.5);
    }
    .cyber-header {
        color: #ccff00; font-size: 1.2rem; font-weight: 800;
        margin-bottom: 15px; border-bottom: 1px solid #333;
        padding-bottom: 10px; text-transform: uppercase; letter-spacing: 2px;
    }
    .stTextArea textarea, .stTextInput input, .stSelectbox div[data-baseweb="select"] > div {
        background-color: #111 !important; color: #ccff00 !important;
        border: 1px solid #444 !important; border-radius: 0px !important;
    }
    .stButton > button {
        background-color: #ccff00 !important; color: #000 !important;
        font-weight: 900 !important; border-radius: 0px !important;
        padding: 15px !important; text-transform: uppercase !important;
    }
    .stButton > button:hover { box-shadow: 0 0 20px #ccff00 !important; }
    .stProgress > div > div > div > div { background-color: #ccff00 !important; }
    </style>
""", unsafe_allow_html=True)

# --- 3. INIT SESSION STATE (Supaya Log Gak Hilang) ---
if 'logs' not in st.session_state: st.session_state.logs = []
if 'download_complete' not in st.session_state: st.session_state.download_complete = False
if 'processing' not in st.session_state: st.session_state.processing = False

# --- 4. HEADER ---
st.markdown("""
    <div style="margin-bottom: 30px; border-bottom: 2px solid #222; padding-bottom: 20px;">
        <h1 style="margin:0; font-size: 3rem; line-height: 1; color: white; font-weight: 900;">
            NEXUS<span style="color:#ccff00;">_CORE_V4.5</span>
        </h1>
        <code style="color: #666;">SYSTEM_STATUS: ONLINE // COOKIES_SUPPORT_ENABLED</code>
    </div>
""", unsafe_allow_html=True)

# --- 5. MAIN LAYOUT ---
col_left, col_right = st.columns([1.8, 1.2])

with col_left:
    st.markdown('<div class="cyber-card"><div class="cyber-header">📡 SIGNAL_INPUT</div>', unsafe_allow_html=True)
    input_links = st.text_area("Links", height=150, placeholder="https://youtube.com/...\nhttps://tiktok.com/...", label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

    # TERMINAL (Mengambil data dari Session State agar persistent)
    st.markdown('<div class="cyber-card"><div class="cyber-header">📟 SYSTEM_LOGS</div>', unsafe_allow_html=True)
    log_text = "\n".join(st.session_state.logs) if st.session_state.logs else "> SYSTEM_IDLE... READY"
    st.code(log_text, language="bash")
    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    st.markdown('<div class="cyber-card"><div class="cyber-header">⚙️ CONFIG_MATRIX</div>', unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["MAIN", "ADVANCED"])
    
    with tab1:
        format_mode = st.selectbox("Mode", ["Video + Audio (MP4)", "Audio Only (MP3)"], label_visibility="collapsed")
        res = st.select_slider("Quality", options=["360p", "720p", "1080p", "BEST"], value="1080p") if "Video" in format_mode else "Best"
        
    with tab2:
        st.markdown("##### 🍪 COOKIES (NETSCAPE FORMAT)")
        st.caption("Wajib untuk YouTube/TikTok di Cloud. Gunakan ekstensi 'Get cookies.txt' di browser.")
        cookies_txt = st.text_area("Paste Cookies Content Here", height=100)
        
        st.markdown("##### OPTIONS")
        opt_browser = st.checkbox("User-Agent Spoofing", True)

    st.write("")
    # Cek FFmpeg dulu
    ffmpeg_status = "✅ FFmpeg Detected" if shutil.which('ffmpeg') else "❌ FFmpeg Missing (Check packages.txt)"
    st.caption(ffmpeg_status)
    
    process_btn = st.button("INITIALIZE DOWNLOAD", disabled=st.session_state.processing)
    st.markdown('</div>', unsafe_allow_html=True)

# --- 6. LOGIC ---
def log_msg(msg, status="INFO"):
    icon = "🟡" if status=="INFO" else "🟢" if status=="SUCCESS" else "🔴"
    timestamp = time.strftime('%H:%M:%S')
    st.session_state.logs.append(f"[{timestamp}] {icon} {msg}")

if process_btn:
    # 1. Reset State
    st.session_state.logs = []
    st.session_state.download_complete = False
    st.session_state.processing = True
    st.rerun() # Rerun untuk update UI tombol jadi disabled

# Logika Proses berjalan jika state processing = True
if st.session_state.processing and not st.session_state.download_complete:
    links = [l.strip() for l in input_links.split('\n') if l.strip()]
    
    if not links:
        log_msg("NO LINKS DETECTED", "ERROR")
        st.session_state.processing = False
    else:
        # Setup Folder
        if os.path.exists('downloads'): shutil.rmtree('downloads')
        os.makedirs('downloads')

        # Simpan Cookies Sementara jika ada
        cookie_file = None
        if cookies_txt.strip():
            cookie_file = "cookies.txt"
            with open(cookie_file, "w") as f:
                f.write(cookies_txt)
            log_msg("COOKIES LOADED", "INFO")

        # Config yt-dlp
        ydl_opts = {
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'quiet': True, 'no_warnings': True, 'ignoreerrors': True, # Jangan stop kalau 1 gagal
            'restrictfilenames': True,
        }

        if cookie_file: ydl_opts['cookiefile'] = cookie_file
        if opt_browser: ydl_opts['user_agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'

        # Format
        if "Audio" in format_mode:
            ydl_opts.update({'format': 'bestaudio/best', 'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3'}]})
        else:
            h = {"1080p": 1080, "720p": 720, "360p": 360}.get(res, 1080)
            if res == "BEST":
                ydl_opts['format'] = "bestvideo+bestaudio/best"
            else:
                ydl_opts['format'] = f"bestvideo[height<={h}]+bestaudio/best[height<={h}]"
            ydl_opts['merge_output_format'] = 'mp4'

        # EKSEKUSI
        progress = st.progress(0)
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            for i, link in enumerate(links):
                try:
                    log_msg(f"CONNECTING: {link[:30]}...", "INFO")
                    st.rerun() # Force UI Update per log (agak lambat tapi user liat prosesnya)
                    
                    info = ydl.extract_info(link, download=True)
                    title = info.get('title', 'Unknown')
                    log_msg(f"SAVED: {title}", "SUCCESS")
                    
                except Exception as e:
                    log_msg(f"FAILED: {str(e)[:50]}", "ERROR")
                
                progress.progress((i + 1) / len(links))

        # Cleanup Cookies
        if cookie_file and os.path.exists(cookie_file): os.remove(cookie_file)
        
        st.session_state.processing = False
        st.session_state.download_complete = True
        st.rerun()

# --- 7. RESULT ---
if st.session_state.download_complete and os.path.exists('downloads'):
    files = os.listdir('downloads')
    if files:
        st.markdown('<div class="cyber-card"><div class="cyber-header">💾 STORAGE</div>', unsafe_allow_html=True)
        
        # ZIP BUTTON
        shutil.make_archive("batch_result", 'zip', "downloads")
        with open("batch_result.zip", "rb") as fp:
            st.download_button("📦 DOWNLOAD ALL (ZIP)", fp, "NEXUS_BATCH.zip", "application/zip", use_container_width=True)
        
        st.markdown("---")
        
        # LIST FILES
        for f in files:
            col1, col2 = st.columns([4, 1])
            with col1: st.code(f, language="text")
            with col2:
                with open(os.path.join('downloads', f), "rb") as fp:
                    st.download_button("⬇ DOWNLOAD", fp, f, key=f)
        st.markdown('</div>', unsafe_allow_html=True)
