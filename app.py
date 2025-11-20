import streamlit as st
import yt_dlp
import os
import shutil
import time
import re
import json

# --- 0. SYSTEM CONFIG ---
st.set_page_config(page_title="NEXUS TANK V6", page_icon="🛡️", layout="wide")

DOWNLOAD_DIR = "downloads"
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

# --- 1. ROBUST CSS (NO NONSENSE) ---
st.markdown("""
    <style>
    .stApp {background-color: #0e1117;}
    .css-card {background-color: #262730; padding: 20px; border-radius: 5px; border: 1px solid #444; margin-bottom: 10px;}
    .status-box {padding: 10px; border-radius: 4px; margin-bottom: 5px; font-family: monospace;}
    .success {background-color: #1f77b4; color: white;}
    .error {background-color: #d62728; color: white;}
    </style>
""", unsafe_allow_html=True)

# --- 2. HELPER FUNCTIONS ---
def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "", name)

def check_cookies_format(content):
    if not content: return False
    # Cek sederhana format Netscape (biasanya diawali # Netscape atau ada 7 kolom)
    if ".google.com" in content or ".youtube.com" in content or "FALSE" in content:
        return True
    return False

# --- 3. SIDEBAR: CONFIG & DIAGNOSTICS ---
with st.sidebar:
    st.header("🔧 CONTROL PANEL")
    
    # COOKIES SECTION
    st.subheader("1. AUTHENTICATION (WAJIB!)")
    st.info("Tanpa Cookies, download di Cloud PASTI GAGAL (HTTP 429/Sign In).")
    cookies_input = st.text_area("Paste Netscape Cookies.txt", height=100, help="Ambil dari ekstensi browser 'Get cookies.txt LOCALLY'")
    
    valid_cookie = check_cookies_format(cookies_input)
    if cookies_input and not valid_cookie:
        st.error("⚠️ Format Cookies sepertinya salah. Pastikan format Netscape!")
    elif valid_cookie:
        st.success("✅ Format Cookies Valid")

    st.divider()
    
    # MAINTENANCE
    if st.button("🧹 Hapus Semua File (Reset)"):
        shutil.rmtree(DOWNLOAD_DIR)
        os.makedirs(DOWNLOAD_DIR)
        st.toast("Workspace Bersih!")

# --- 4. MAIN INTERFACE ---
st.title("🛡️ NEXUS TANK V6")
st.markdown("**Batch Downloader dengan Diagnostic & Raw Logs**")

# TABS UTAMA
tab_dl, tab_diag = st.tabs(["⬇️ DOWNLOADER", "🚑 DIAGNOSTIK"])

# === TAB 1: DOWNLOADER ===
with tab_dl:
    col1, col2 = st.columns([2, 1])
    with col1:
        input_links = st.text_area("Input Links (Satu per baris)", height=150)
    with col2:
        st.markdown("### Settings")
        mode = st.radio("Mode:", ["Video Best (MP4)", "Audio Only (MP3)", "Thumbnail"])
        opt_meta = st.checkbox("Debug Logs (Verbose)", value=True)

    if st.button("🚀 HAJAR (START DOWNLOAD)", type="primary", use_container_width=True):
        links = [l.strip() for l in input_links.split('\n') if l.strip()]
        
        if not links:
            st.error("❌ Link kosong bro!")
        else:
            # 1. Setup Cookies
            cookie_path = None
            if valid_cookie:
                cookie_path = "cookies_temp.txt"
                with open(cookie_path, "w") as f:
                    f.write(cookies_input)
            
            # 2. Container Progress
            status_cont = st.status("⚙️ Memproses...", expanded=True)
            success_count = 0
            
            with status_cont:
                ydl_opts = {
                    'outtmpl': f'{DOWNLOAD_DIR}/%(title)s.%(ext)s',
                    'restrictfilenames': True,
                    'quiet': False if opt_meta else True, # Verbose jika dicentang
                    'no_warnings': True,
                    'ignoreerrors': True,
                    'nocheckcertificate': True,
                }
                
                if cookie_path:
                    ydl_opts['cookiefile'] = cookie_path
                else:
                    # User Agent Spoofing Basic
                    ydl_opts['user_agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'

                # Mode Config
                if "Audio" in mode:
                    ydl_opts['format'] = 'bestaudio/best'
                    ydl_opts['postprocessors'] = [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3'}]
                elif "Thumbnail" in mode:
                    ydl_opts['writethumbnail'] = True
                    ydl_opts['skip_download'] = True
                else:
                    ydl_opts['format'] = 'bestvideo+bestaudio/best'
                    ydl_opts['merge_output_format'] = 'mp4'

                # EKSEKUSI
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    for i, link in enumerate(links):
                        st.write(f"**[{i+1}/{len(links)}] Target:** `{link}`")
                        try:
                            info = ydl.extract_info(link, download=True)
                            if info:
                                title = info.get('title', 'Unknown')
                                st.success(f"✅ OK: {title}")
                                success_count += 1
                        except Exception as e:
                            err_msg = str(e)
                            st.error(f"❌ GAGAL: {err_msg}")
                            
                            # Analisa Error Sederhana untuk User
                            if "429" in err_msg: st.warning("👉 Penyebab: IP Terblokir (Too Many Requests). Wajib pakai Cookies!")
                            if "Sign in" in err_msg: st.warning("👉 Penyebab: Video butuh login/umur. Wajib pakai Cookies!")
            
            # Cleanup
            if cookie_path and os.path.exists(cookie_path): os.remove(cookie_path)
            
            if success_count > 0:
                st.balloons()
            else:
                st.error("Semua download gagal. Cek tab Diagnostik atau pakai Cookies.")

    # RESULT AREA
    st.divider()
    st.subheader("📂 FILE STORAGE")
    files = [f for f in os.listdir(DOWNLOAD_DIR) if not f.endswith('.part')]
    if files:
        c1, c2 = st.columns([3,1])
        with c1: st.write(f"Total File: {len(files)}")
        with c2:
            shutil.make_archive("Batch_Result", 'zip', DOWNLOAD_DIR)
            with open("Batch_Result.zip", "rb") as f:
                st.download_button("📦 DOWNLOAD ZIP SEMUA", f, "Nexus_Batch.zip")
        
        for f in files:
            p = os.path.join(DOWNLOAD_DIR, f)
            with open(p, "rb") as fb:
                st.download_button(f"⬇ {f}", fb, f)
    else:
        st.info("Folder kosong.")

# === TAB 2: DIAGNOSTIK (UNTUK DEBUG) ===
with tab_diag:
    st.subheader("🚑 System Health Check")
    
    col_d1, col_d2 = st.columns(2)
    
    with col_d1:
        st.markdown("**1. Cek FFmpeg**")
        if shutil.which("ffmpeg"):
            st.success("✅ FFmpeg Terinstall")
            st.code(os.popen("ffmpeg -version").read().split('\n')[0])
        else:
            st.error("❌ FFmpeg TIDAK DITEMUKAN! Cek packages.txt")

    with col_d2:
        st.markdown("**2. Cek Folder Write Access**")
        try:
            test_file = os.path.join(DOWNLOAD_DIR, "test_write.txt")
            with open(test_file, "w") as f: f.write("ok")
            os.remove(test_file)
            st.success("✅ Bisa menulis file")
        except Exception as e:
            st.error(f"❌ Gagal tulis file: {e}")

    st.markdown("**3. Test Koneksi ke YouTube (Tanpa Download)**")
    if st.button("Ping YouTube Metadata"):
        try:
            with yt_dlp.YoutubeDL({'quiet':True}) as ydl:
                info = ydl.extract_info("https://www.youtube.com/watch?v=jNQXAC9IVRw", download=False) # Me at the zoo (pendek)
                st.success(f"✅ Koneksi OK! Judul: {info['title']}")
        except Exception as e:
            st.error(f"❌ Koneksi GAGAL: {e}")
            st.warning("Jika ini gagal, berarti IP Server Streamlit SUDAH DIBLOKIR YouTube. Solusi satu-satunya: Pakai Cookies.")
