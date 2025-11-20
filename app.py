import streamlit as st
import yt_dlp
import os
import shutil
import time
import glob
import re

# --- 0. CONFIG & SETUP ---
st.set_page_config(
    page_title="NEXUS COMMANDER V5",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Setup Folder Kerja
DOWNLOAD_DIR = "downloads"
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

# --- 1. UI STYLING (INDUSTRIAL CLEAN) ---
st.markdown("""
    <style>
    /* Clean Dark Theme overrides */
    [data-testid="stAppViewContainer"] {background-color: #0e1117;}
    [data-testid="stHeader"] {background-color: rgba(0,0,0,0);}
    
    /* Card Container Style */
    .css-card {
        border: 1px solid #2d2d2d;
        border-radius: 8px;
        padding: 20px;
        background-color: #161b22;
        margin-bottom: 20px;
    }
    
    /* Status Indicators */
    .status-badge {
        padding: 4px 8px;
        border-radius: 4px;
        font-weight: bold;
        font-size: 0.8em;
        font-family: monospace;
    }
    .ready {background-color: #238636; color: white;}
    .busy {background-color: #d29922; color: black;}
    .error {background-color: #da3633; color: white;}
    
    /* Typography */
    h1, h2, h3 {font-family: 'Segoe UI', sans-serif; font-weight: 600;}
    code {font-family: 'Consolas', monospace;}
    </style>
""", unsafe_allow_html=True)

# --- 2. SIDEBAR: COOKIES & INFO ---
with st.sidebar:
    st.header("🔐 SECURITY ACCESS")
    st.warning("Server Cloud (Streamlit) sering diblokir oleh YouTube/TikTok. Gunakan Cookies agar download berhasil 100%.")
    
    with st.expander("🍪 Paste Cookies.txt (Wajib untuk Cloud)", expanded=True):
        cookies_content = st.text_area(
            "Tempel isi Netscape Cookies di sini",
            height=150,
            help="Gunakan ekstensi browser 'Get cookies.txt LOCALLY' saat login di YouTube, lalu copas isinya kesini."
        )
    
    st.divider()
    st.info(f"📂 Storage: {DOWNLOAD_DIR}")
    if st.button("🧹 Bersihkan Sampah / Reset"):
        if os.path.exists(DOWNLOAD_DIR):
            shutil.rmtree(DOWNLOAD_DIR)
            os.makedirs(DOWNLOAD_DIR)
        st.toast("Workspace Cleaned!", icon="🧹")
        time.sleep(1)
        st.rerun()

# --- 3. MAIN HEADER ---
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.title("NEXUS COMMANDER // V5")
    st.caption("ROBUST BATCH MEDIA DOWNLOADER ENGINE")
with col_h2:
    ffmpeg_ok = shutil.which("ffmpeg") is not None
    st.markdown(
        f"""
        <div style="text-align:right; margin-top:10px;">
            <span class="status-badge {'ready' if ffmpeg_ok else 'error'}">
                FFMPEG: {'ACTIVE' if ffmpeg_ok else 'MISSING'}
            </span>
            <span class="status-badge {'ready' if cookies_content else 'busy'}">
                COOKIES: {'LOADED' if cookies_content else 'MISSING'}
            </span>
        </div>
        """, 
        unsafe_allow_html=True
    )

# --- 4. INPUT AREA ---
st.markdown("### 📡 1. INPUT LINKS")
input_text = st.text_area(
    "Masukkan Link (Satu per baris)", 
    height=150,
    placeholder="https://www.youtube.com/watch?v=...\nhttps://www.tiktok.com/@user/video/..."
)

# --- 5. CONFIGURATION ---
st.markdown("### ⚙️ 2. CONFIGURATION")
c1, c2, c3 = st.columns(3)

with c1:
    dl_mode = st.selectbox("Mode Operasi", ["Video + Audio (MP4)", "Audio Only (MP3)", "Thumbnail Only"])
with c2:
    quality = "Best"
    if "Video" in dl_mode:
        quality = st.selectbox("Resolusi Maksimal", ["1080p", "720p", "480p", "Best Available"])
with c3:
    naming = st.selectbox("Format Nama File", ["Judul Asli", "Channel - Judul", "Tanggal - Judul"])

# Options Checkbox
with st.expander("🛠️ Opsi Lanjutan"):
    col_o1, col_o2, col_o3 = st.columns(3)
    with col_o1: opt_thumb = st.checkbox("Simpan Thumbnail", value=True)
    with col_o2: opt_meta = st.checkbox("Simpan JSON Info", value=False)
    with col_o3: opt_embed = st.checkbox("Embed Thumbnail (MP3/MP4)", value=True)

# --- 6. LOGIC CORE (ROBUST ENGINE) ---
def get_cookies_file():
    if not cookies_content.strip(): return None
    cookie_path = "temp_cookies.txt"
    with open(cookie_path, "w") as f:
        f.write(cookies_content)
    return cookie_path

def get_ydl_opts(mode, qual, name_fmt, cookie_path):
    # Base Template
    name_templates = {
        "Judul Asli": "%(title)s",
        "Channel - Judul": "%(uploader)s - %(title)s",
        "Tanggal - Judul": "%(upload_date)s - %(title)s"
    }
    template = name_templates.get(name_fmt, "%(title)s")
    
    opts = {
        'outtmpl': f'{DOWNLOAD_DIR}/{template}.%(ext)s',
        'restrictfilenames': True,
        'quiet': True,
        'no_warnings': True,
        'ignoreerrors': True,
        'writethumbnail': opt_thumb,
        'writeinfojson': opt_meta,
    }

    # Authentication
    if cookie_path:
        opts['cookiefile'] = cookie_path
    else:
        # Fallback User Agent spoofing
        opts['user_agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'

    # Mode Specifics
    if "Audio" in mode:
        opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [
                {'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'},
                {'key': 'EmbedThumbnail'} if opt_embed else {}
            ],
        })
        # Remove empty dicts from list if opt_embed is false
        opts['postprocessors'] = [p for p in opts['postprocessors'] if p]
        
    elif "Thumbnail" in mode:
        opts['skip_download'] = True
        opts['writethumbnail'] = True
        
    else: # Video Mode
        # Resolution Mapping
        h_map = {"1080p": 1080, "720p": 720, "480p": 480}
        if qual in h_map:
            h = h_map[qual]
            opts['format'] = f"bestvideo[height<={h}]+bestaudio/best[height<={h}]"
        else:
            opts['format'] = "bestvideo+bestaudio/best"
            
        opts['merge_output_format'] = 'mp4'
        if opt_embed: opts['writethumbnail'] = True

    return opts

# --- 7. EXECUTION BUTTON ---
st.markdown("---")
if st.button("🚀 MULAI DOWNLOAD (START ENGINE)", type="primary", use_container_width=True):
    links = [l.strip() for l in input_text.split('\n') if l.strip()]
    
    if not links:
        st.error("❌ Input Kosong! Masukkan link video dulu.")
    else:
        # 1. Setup Session
        cookie_file = get_cookies_file()
        ydl_opts = get_ydl_opts(dl_mode, quality, naming, cookie_file)
        
        # 2. Execution Container (Status Native)
        status_container = st.status("⚙️ Engine Running...", expanded=True)
        results = []
        
        with status_container:
            st.write("🔄 Inisialisasi yt-dlp core...")
            progress_bar = st.progress(0)
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                for i, link in enumerate(links):
                    st.write(f"Target [{i+1}/{len(links)}]: `{link}`")
                    try:
                        info = ydl.extract_info(link, download=True)
                        title = info.get('title', 'Unknown')
                        st.success(f"✅ Berhasil: {title}")
                        results.append(title)
                    except Exception as e:
                        err_msg = str(e)
                        if "Sign in" in err_msg:
                            st.error(f"❌ Gagal (Auth Error): Butuh Cookies! - {link}")
                        else:
                            st.error(f"❌ Gagal: {err_msg[:100]}...")
                    
                    progress_bar.progress((i + 1) / len(links))
            
            status_container.update(label="✅ Proses Selesai!", state="complete", expanded=True)
            
            # Cleanup Cookie Temp
            if cookie_file and os.path.exists(cookie_file):
                os.remove(cookie_file)

# --- 8. RESULTS AREA ---
st.markdown("### 💾 3. STORAGE & RESULTS")

files = []
if os.path.exists(DOWNLOAD_DIR):
    # Scan files (exclude temp/part files)
    files = [f for f in os.listdir(DOWNLOAD_DIR) if not f.endswith(('.part', '.ytdl'))]

if not files:
    st.info("Belum ada file hasil download. Silakan masukkan link dan klik start.")
else:
    c_res1, c_res2 = st.columns([3, 1])
    
    with c_res1:
        st.success(f"Ditemukan {len(files)} file di penyimpanan.")
    
    with c_res2:
        # Auto Zip Logic
        shutil.make_archive("Batch_Download", 'zip', DOWNLOAD_DIR)
        with open("Batch_Download.zip", "rb") as fzip:
            st.download_button(
                "📦 DOWNLOAD SEMUA (ZIP)", 
                fzip, 
                "Nexus_Batch.zip", 
                "application/zip", 
                type="primary"
            )

    # List Individual Files
    for f in files:
        f_path = os.path.join(DOWNLOAD_DIR, f)
        
        # Determine Icon
        icon = "📄"
        if f.endswith(('.mp4', '.mkv')): icon = "🎬"
        elif f.endswith('.mp3'): icon = "🎵"
        elif f.endswith(('.jpg', '.png', '.webp')): icon = "🖼️"
        
        with st.container():
            col_file, col_dl = st.columns([4, 1])
            with col_file:
                st.code(f"{icon} {f}", language="text")
            with col_dl:
                with open(f_path, "rb") as fb:
                    st.download_button("⬇ Unduh", fb, f, key=f)
