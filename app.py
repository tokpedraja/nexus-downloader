import streamlit as st
import yt_dlp
import os
import time
import shutil
import zipfile

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="NEXUS BATCH DOWNLOADER V4",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. ADVANCED CYBER-INDUSTRIAL CSS ---
st.markdown("""
    <style>
    /* GLOBAL FONTS & COLORS */
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700;800&display=swap');
    
    :root {
        --neon-green: #ccff00;
        --dark-bg: #050505;
        --panel-bg: #0f0f0f;
        --border-color: #333;
        --text-main: #e0e0e0;
    }

    html, body, [class*="css"] {
        font-family: 'JetBrains Mono', monospace;
        background-color: var(--dark-bg);
        color: var(--text-main);
    }

    /* HIDE STREAMLIT BLOAT */
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    footer {visibility: hidden;}

    /* CUSTOM CONTAINERS */
    .cyber-card {
        border: 1px solid var(--border-color);
        background-color: var(--panel-bg);
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 6px 6px 0px #1a1a1a;
        position: relative;
    }
    .cyber-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; width: 4px; height: 100%;
        background: var(--neon-green);
    }
    
    /* HEADERS */
    .cyber-header {
        color: var(--neon-green);
        font-weight: 800;
        border-bottom: 2px solid var(--border-color);
        padding-bottom: 8px;
        margin-bottom: 20px;
        text-transform: uppercase;
        letter-spacing: 2px;
        font-size: 1.1rem;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    /* INPUT FIELDS */
    .stTextArea textarea, .stSelectbox div[data-baseweb="select"], .stTextInput input {
        background-color: #000 !important;
        border: 1px solid #444 !important;
        color: #00ff99 !important;
        border-radius: 0px !important;
    }
    .stTextArea textarea:focus, .stTextInput input:focus {
        border-color: var(--neon-green) !important;
        box-shadow: 0 0 15px rgba(204, 255, 0, 0.1);
    }

    /* BUTTONS */
    .stButton > button {
        background-color: var(--neon-green) !important;
        color: #000 !important;
        border: none;
        border-radius: 0px;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: 1px;
        padding: 1rem;
        transition: all 0.2s ease;
        width: 100%;
    }
    .stButton > button:hover {
        background-color: #fff !important;
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(204,255,0,0.4);
    }

    /* DOWNLOAD BUTTONS */
    .stDownloadButton > button {
        background-color: #111 !important;
        color: var(--neon-green) !important;
        border: 1px solid var(--neon-green) !important;
        border-radius: 0px;
        font-family: 'JetBrains Mono', monospace;
    }
    .stDownloadButton > button:hover {
        background-color: var(--neon-green) !important;
        color: #000 !important;
    }

    /* PROGRESS & STATUS */
    .stProgress > div > div > div > div { background-color: var(--neon-green); }
    .stAlert { background-color: #111; border: 1px solid #333; color: #ccc; }
    
    /* TAB STYLING */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #111;
        border: 1px solid #333;
        border-radius: 0px;
        color: #666;
    }
    .stTabs [aria-selected="true"] {
        background-color: var(--neon-green) !important;
        color: #000 !important;
        border-color: var(--neon-green) !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. HEADER UI ---
st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 20px; border-bottom: 1px solid #333; padding-bottom: 20px;">
        <div>
            <h1 style="margin:0; font-size: 2.5rem; line-height: 1; color: white;">NEXUS<span style="color:#ccff00;">_ULTIMATE</span></h1>
            <small style="color: #666; font-size: 0.8rem; letter-spacing: 1px;">BATCH MEDIA PROCESSING UNIT V.4.0</small>
        </div>
        <div style="text-align: right;">
            <span style="background:#ccff00; color:black; padding:2px 8px; font-weight:bold; font-size:0.7rem;">ONLINE</span>
            <br><span style="color:#444; font-size: 0.7rem;">SECURE_CONNECTION</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- 4. SESSION STATE INIT ---
if 'processing' not in st.session_state:
    st.session_state.processing = False
if 'download_complete' not in st.session_state:
    st.session_state.download_complete = False

# --- 5. MAIN LAYOUT ---
col_left, col_right = st.columns([1.8, 1.2])

with col_left:
    # PANEL INPUT
    st.markdown('<div class="cyber-card"><div class="cyber-header"><span>📡</span> INPUT FEED</div>', unsafe_allow_html=True)
    input_links = st.text_area(
        "Paste Links", 
        height=200, 
        placeholder="https://youtube.com/watch?v=...\nhttps://tiktok.com/@user/video/...\nhttps://instagram.com/reel/...",
        label_visibility="collapsed"
    )
    st.markdown("<small style='color:#444'>Support: YouTube, TikTok, IG, Twitter, FB, SoundCloud, dll.</small>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # PANEL TERMINAL
    st.markdown('<div class="cyber-card"><div class="cyber-header"><span>📟</span> SYSTEM TERMINAL</div>', unsafe_allow_html=True)
    terminal_container = st.empty()
    terminal_container.code("SYSTEM_IDLE... WAITING FOR INPUT", language="bash")
    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    # PANEL CONFIG
    st.markdown('<div class="cyber-card"><div class="cyber-header"><span>⚙️</span> CONFIGURATION MATRIX</div>', unsafe_allow_html=True)
    
    # Tabs untuk Settings yang lebih rapi
    tab1, tab2 = st.tabs(["BASIC", "ADVANCED"])
    
    with tab1:
        st.markdown("**FORMAT OUTPUT**")
        format_mode = st.selectbox("Pilih Format", ["Video + Audio (MP4)", "Audio Only (MP3)", "Thumbnail Only"], label_visibility="collapsed")
        
        if "Video" in format_mode:
            st.markdown("**KUALITAS VIDEO**")
            resolution = st.select_slider(
                "Target Resolusi",
                options=["360p", "480p", "720p", "1080p", "2K/4K (Best)"],
                value="1080p"
            )
        else:
            resolution = "Best" # Dummy for audio
            
    with tab2:
        st.markdown("**NAMING CONVENTION**")
        filename_pattern = st.selectbox(
            "Pola Nama File",
            ["Judul Asli", "Channel - Judul", "Tanggal - Judul", "ID - Judul"],
            index=0
        )
        
        st.markdown("**PLAYLIST CONTROL**")
        playlist_items = st.number_input("Max Video per Playlist (0 = Semua)", 0, 100, 0)
        
        st.markdown("**EXTRAS**")
        c1, c2 = st.columns(2)
        with c1:
            opt_thumb = st.checkbox("Save Thumb", True)
            opt_meta = st.checkbox("Save JSON", False)
        with c2:
            opt_sub = st.checkbox("Get Subs", False)
            opt_browser = st.checkbox("Anti-Block", True, help="Simulasi Browser Chrome")

    st.markdown("---")
    process_btn = st.button("⚡ INITIATE SEQUENCE", disabled=st.session_state.processing)
    st.markdown('</div>', unsafe_allow_html=True)

# --- 6. LOGIC FUNCTIONS ---

def get_filename_template(choice):
    templates = {
        "Judul Asli": "%(title)s.%(ext)s",
        "Channel - Judul": "%(uploader)s - %(title)s.%(ext)s",
        "Tanggal - Judul": "%(upload_date)s - %(title)s.%(ext)s",
        "ID - Judul": "%(id)s - %(title)s.%(ext)s"
    }
    return f"downloads/{templates.get(choice, '%(title)s.%(ext)s')}"

def get_resolution_string(res_choice):
    # Mapping resolusi ke format yt-dlp
    if "4K" in res_choice: return "bestvideo+bestaudio/best"
    
    height_map = {"1080p": 1080, "720p": 720, "480p": 480, "360p": 360}
    h = height_map.get(res_choice, 1080)
    return f"bestvideo[height<={h}]+bestaudio/best[height<={h}]"

def create_zip_archive():
    shutil.make_archive("batch_result", 'zip', "downloads")
    return "batch_result.zip"

# --- 7. EXECUTION CORE ---

if process_btn:
    if not input_links.strip():
        st.error("⚠️ ERROR: LINK INPUT IS EMPTY")
    else:
        st.session_state.processing = True
        links = [l.strip() for l in input_links.split('\n') if l.strip()]
        
        # Reset Workspace
        if os.path.exists('downloads'): shutil.rmtree('downloads')
        os.makedirs('downloads')
        
        logs = []
        progress_bar = st.progress(0, text="INITIALIZING CORE...")
        
        # Setup Options
        out_tmpl = get_filename_template(filename_pattern)
        
        ydl_opts = {
            'outtmpl': out_tmpl,
            'quiet': True,
            'no_warnings': True,
            'restrictfilenames': True,
        }
        
        # Browser Masquerade (Anti-Block)
        if opt_browser:
            ydl_opts['user_agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'

        # Playlist Limit
        if playlist_items > 0:
            ydl_opts['playlistend'] = playlist_items

        # Format Logic
        if "Audio" in format_mode:
            ydl_opts.update({
                'format': 'bestaudio/best',
                'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferredquality': '192'}],
            })
        elif "Thumbnail" in format_mode:
            ydl_opts.update({'writethumbnail': True, 'skip_download': True})
        else:
            ydl_opts.update({
                'format': get_resolution_string(resolution),
                'merge_output_format': 'mp4',
            })

        # Extras
        if opt_thumb and "Thumbnail" not in format_mode: ydl_opts['writethumbnail'] = True
        if opt_meta: ydl_opts['writeinfojson'] = True
        if opt_sub: 
            ydl_opts.update({'writesubtitles': True, 'subtitleslangs': ['en', 'id', 'all']})

        # START LOOP
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            for i, link in enumerate(links):
                try:
                    logs.append(f"[{time.strftime('%H:%M:%S')}] 🟡 CONNECTING: {link[:40]}...")
                    terminal_container.code("\n".join(logs), language="bash")
                    
                    info = ydl.extract_info(link, download=True)
                    title = info.get('title', 'Unknown')
                    
                    logs.append(f"[{time.strftime('%H:%M:%S')}] 🟢 SUCCESS: {title}")
                    terminal_container.code("\n".join(logs), language="bash")
                    
                except Exception as e:
                    logs.append(f"[{time.strftime('%H:%M:%S')}] 🔴 ERROR: {str(e)[:50]}...")
                    terminal_container.code("\n".join(logs), language="bash")
                
                progress_bar.progress((i + 1) / len(links), text=f"PROCESSING {i+1}/{len(links)}")

        st.session_state.processing = False
        st.session_state.download_complete = True
        progress_bar.progress(1.0, text="SEQUENCE COMPLETED")

# --- 8. RESULT AREA (AUTO ZIP) ---
if st.session_state.download_complete and os.path.exists('downloads'):
    st.markdown('<div class="cyber-card"><div class="cyber-header"><span>💾</span> OUTPUT STORAGE</div>', unsafe_allow_html=True)
    
    files = os.listdir('downloads')
    if not files:
        st.warning("No files found.")
    else:
        col_res1, col_res2 = st.columns([3, 1])
        
        with col_res1:
            st.write(f"**Total Files Retrieved:** {len(files)}")
            # Expandable details
            with st.expander("View File List"):
                for f in files:
                    st.code(f, language="text")
        
        with col_res2:
            # ZIP ALL BUTTON
            zip_path = create_zip_archive()
            with open(zip_path, "rb") as fp:
                st.download_button(
                    label="📦 DOWNLOAD ZIP (ALL)",
                    data=fp,
                    file_name=f"NEXUS_BATCH_{int(time.time())}.zip",
                    mime="application/zip",
                    use_container_width=True
                )
        
        st.markdown("---")
        st.markdown("**INDIVIDUAL DOWNLOADS:**")
        
        # Grid Layout for individual files
        cols = st.columns(3)
        for idx, f in enumerate(files):
            file_path = os.path.join('downloads', f)
            # Determine icon
            icon = "📄"
            if f.endswith(('.mp4','.mkv')): icon = "🎬"
            elif f.endswith(('.mp3','.m4a')): icon = "🎵"
            elif f.endswith(('.jpg','.png','.webp')): icon = "🖼️"
            
            with cols[idx % 3]:
                with open(file_path, "rb") as fp:
                    st.download_button(
                        label=f"{icon} {f[:15]}...",
                        data=fp,
                        file_name=f,
                        key=f"btn_{idx}",
                        help=f
                    )
    
    st.markdown('</div>', unsafe_allow_html=True)
