import streamlit as st
import yt_dlp
import os
import time
import shutil

# --- PAGE CONFIGURATION (WAJIB PALING ATAS) ---
st.set_page_config(
    page_title="NEXUS BATCH DOWNLOADER",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- ADVANCED CYBER-INDUSTRIAL CSS ---
# CSS ini "memaksa" tampilan Streamlit menjadi kotak-kotak tegas (Brutalist Style)
st.markdown("""
    <style>
    /* 1. GLOBAL FONT & COLOR */
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'JetBrains Mono', monospace;
        background-color: #050505;
        color: #e0e0e0;
    }

    /* 2. HILANGKAN GARIS MERAH/ORANGE BAWAAN STREAMLIT */
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    footer {visibility: hidden;}

    /* 3. CUSTOM CONTAINERS (KOTAK PANEL) */
    .cyber-card {
        border: 1px solid #333;
        background-color: #0f0f0f;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 4px 4px 0px #1a1a1a;
    }
    
    /* 4. CUSTOM TITLES */
    .cyber-header {
        color: #ccff00;
        font-weight: 800;
        border-bottom: 2px solid #333;
        padding-bottom: 5px;
        margin-bottom: 15px;
        text-transform: uppercase;
        letter-spacing: 2px;
        font-size: 1.2rem;
    }

    /* 5. INPUT FIELDS (TEXTAREA & INPUTS) */
    .stTextArea textarea {
        background-color: #000 !important;
        border: 1px solid #444 !important;
        color: #00ff99 !important; /* Hijau Hacker */
        border-radius: 0px;
    }
    .stTextArea textarea:focus {
        border-color: #ccff00 !important;
        box-shadow: 0 0 10px rgba(204, 255, 0, 0.2);
    }

    /* 6. BUTTONS (TOMBOL DOWNLOAD) */
    .stButton > button {
        background-color: #ccff00 !important;
        color: #000 !important;
        border: none;
        border-radius: 0px;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: 1px;
        padding: 0.75rem 1rem;
        transition: all 0.2s ease;
        width: 100%;
    }
    .stButton > button:hover {
        background-color: #fff !important;
        box-shadow: 0 0 15px #ccff00;
        transform: translateY(-2px);
    }

    /* 7. CHECKBOX & RADIO */
    .stCheckbox label {
        color: #bbb;
    }

    /* 8. PROGRESS BAR */
    .stProgress > div > div > div > div {
        background-color: #ccff00;
    }
    
    /* 9. DOWNLOAD BUTTON (HASIL) */
    .stDownloadButton > button {
        background-color: #1a1a1a !important;
        color: #ccff00 !important;
        border: 1px solid #ccff00 !important;
    }
    .stDownloadButton > button:hover {
        background-color: #ccff00 !important;
        color: #000 !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- HEADER SECTION ---
st.markdown("""
    <div style="border-bottom: 2px solid #ccff00; padding-bottom: 10px; margin-bottom: 30px; display: flex; justify-content: space-between; align-items: center;">
        <div>
            <h1 style="margin:0; padding:0; color:white; font-size: 2rem; letter-spacing: -2px;">NEXUS<span style="color:#ccff00;">_BATCH</span></h1>
            <p style="margin:0; font-size: 0.8rem; color: #666;">UNIVERSAL MEDIA DOWNLOADER // V.3.0-ULTR</p>
        </div>
        <div style="background: #ccff00; color: black; padding: 5px 10px; font-weight: bold; font-size: 0.8rem;">SYSTEM_READY</div>
    </div>
""", unsafe_allow_html=True)

# --- MAIN LAYOUT (2 KOLOM BESAR) ---
col_left, col_right = st.columns([2, 1.2])

with col_left:
    # --- PANEL 1: INPUT ---
    st.markdown('<div class="cyber-card"><div class="cyber-header">1. INPUT SOURCE LINKS</div>', unsafe_allow_html=True)
    input_links = st.text_area(
        "LABEL_HIDDEN", 
        height=250, 
        placeholder="https://youtube.com/watch?v=...\nhttps://tiktok.com/@user/video/...\nhttps://instagram.com/p/...",
        label_visibility="collapsed",
        help="Masukkan satu link per baris"
    )
    st.markdown('</div>', unsafe_allow_html=True) # Close Card

    # --- PANEL 3: LOGS & PREVIEW ---
    st.markdown('<div class="cyber-card"><div class="cyber-header">3. LIVE TERMINAL</div>', unsafe_allow_html=True)
    log_placeholder = st.empty()
    log_placeholder.code("WAITING FOR COMMAND...", language="bash")
    st.markdown('</div>', unsafe_allow_html=True) # Close Card

with col_right:
    # --- PANEL 2: CONFIGURATION ---
    st.markdown('<div class="cyber-card"><div class="cyber-header">2. CONFIGURATION</div>', unsafe_allow_html=True)
    
    st.markdown("**MODE OPERASI**")
    download_mode = st.radio(
        "Pilih Mode:", 
        ["Video + Audio (Best Quality)", "Audio Only (MP3)", "Thumbnail Only"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("**OPSI TAMBAHAN**")
    
    col_opt1, col_opt2 = st.columns(2)
    with col_opt1:
        opt_thumbnail = st.checkbox("Save Thumbnail", value=True, help="Download gambar cover video")
        opt_metadata = st.checkbox("Save Metadata", value=False, help="Simpan info video (JSON)")
    with col_opt2:
        opt_subtitles = st.checkbox("Download Subs", value=False, help="Download subtitle jika tersedia")
        opt_force_mp4 = st.checkbox("Force MP4", value=True, help="Paksa format video jadi MP4")

    st.markdown("---")
    st.markdown("**FOLDER OUTPUT (Server)**")
    st.code("/server/downloads/batch_01", language="bash")
    
    st.write("") # Spacer
    start_btn = st.button("INITIATE DOWNLOAD SEQUENCE")
    st.markdown('</div>', unsafe_allow_html=True) # Close Card

# --- LOGIC PEMROSESAN ---
def get_ydl_opts(mode, save_thumb, save_subs, force_mp4):
    # Dasar konfigurasi
    opts = {
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'quiet': True,
        'no_warnings': True,
        'restrictfilenames': True,
    }
    
    # 1. Konfigurasi Mode
    if mode == "Audio Only (MP3)":
        opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        })
    elif mode == "Thumbnail Only":
        opts.update({
            'writethumbnail': True,
            'skip_download': True, # Jangan download videonya
        })
    else: # Video + Audio
        opts.update({
            'format': 'bestvideo+bestaudio/best',
        })
        if force_mp4:
            opts.update({'merge_output_format': 'mp4'})

    # 2. Opsi Tambahan
    if save_thumb and mode != "Thumbnail Only":
        opts.update({'writethumbnail': True})
    
    if save_subs:
        opts.update({
            'writesubtitles': True,
            'writeautomaticsub': False,
            'subtitleslangs': ['en', 'id'], # Prioritas bahasa
        })

    return opts

# --- EKSEKUSI ---
if start_btn:
    if not input_links.strip():
        st.error("❌ ERROR: INPUT LINK KOSONG!")
    else:
        links = [l.strip() for l in input_links.split('\n') if l.strip()]
        
        # Siapkan Folder
        if os.path.exists('downloads'):
            shutil.rmtree('downloads') # Bersihkan folder lama agar fresh
        os.makedirs('downloads')
        
        # Progress Bar UI
        progress_text = "INITIALIZING..."
        my_bar = st.progress(0, text=progress_text)
        logs = []

        # Loop Download
        opts = get_ydl_opts(download_mode, opt_thumbnail, opt_subtitles, opt_force_mp4)
        
        with yt_dlp.YoutubeDL(opts) as ydl:
            for i, link in enumerate(links):
                try:
                    # Update Log
                    logs.append(f"[{time.strftime('%H:%M:%S')}] CONNECTING: {link[:30]}...")
                    log_placeholder.code("\n".join(logs), language="bash")
                    
                    # Proses Download
                    info = ydl.extract_info(link, download=True)
                    title = info.get('title', 'Unknown File')
                    
                    logs.append(f"[{time.strftime('%H:%M:%S')}] SUCCESS: {title}")
                    log_placeholder.code("\n".join(logs), language="bash")
                    
                except Exception as e:
                    logs.append(f"[{time.strftime('%H:%M:%S')}] ERROR: {str(e)}")
                    log_placeholder.code("\n".join(logs), language="bash")
                
                # Update Bar
                my_bar.progress((i + 1) / len(links), text=f"PROCESSING {i+1}/{len(links)}")

        my_bar.progress(1.0, text="BATCH COMPLETED")
        st.success("✅ SEMUA PROSES SELESAI!")

        # --- TAMPILKAN HASIL DOWNLOAD ---
        st.markdown('<div class="cyber-card"><div class="cyber-header">4. OUTPUT FILES</div>', unsafe_allow_html=True)
        
        files = os.listdir('downloads')
        if not files:
            st.warning("Tidak ada file yang berhasil diunduh.")
        else:
            # Kelompokkan file berdasarkan nama (Video+Thumbnail+Sub jadi satu grup)
            st.write(f"Total Files: {len(files)}")
            for f in files:
                file_path = os.path.join('downloads', f)
                
                # Tentukan Icon berdasarkan ekstensi
                icon = "📄"
                if f.endswith(('.mp4', '.mkv', '.webm')): icon = "🎬 VIDEO"
                elif f.endswith(('.mp3', '.wav', '.m4a')): icon = "🎵 AUDIO"
                elif f.endswith(('.jpg', '.png', '.webp')): icon = "🖼️ IMAGE"
                elif f.endswith(('.srt', '.vtt')): icon = "📝 SUB"

                # Tombol Download Per File
                with open(file_path, "rb") as file_data:
                    st.download_button(
                        label=f"⬇ {icon}: {f}",
                        data=file_data,
                        file_name=f,
                        mime="application/octet-stream",
                        key=f # Unique key
                    )
        st.markdown('</div>', unsafe_allow_html=True)
