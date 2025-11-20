import streamlit as st
import yt_dlp
import os
import time
import shutil

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="NEXUS DOWNLOADER",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CUSTOM CSS (CYBER-INDUSTRIAL THEME) ---
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background-color: #0a0a0a;
        color: #e5e5e5;
        font-family: 'Courier New', Courier, monospace;
    }
    
    /* Inputs */
    .stTextArea textarea, .stSelectbox div[data-baseweb="select"] {
        background-color: #050505 !important;
        color: #ccff00 !important;
        border: 1px solid #333 !important;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #ccff00 !important;
        text-transform: uppercase;
        letter-spacing: 2px;
        border-bottom: 2px solid #333;
        padding-bottom: 10px;
    }
    
    /* Buttons */
    .stButton > button {
        width: 100%;
        background-color: #ccff00;
        color: #000000;
        border: none;
        font-weight: bold;
        text-transform: uppercase;
        padding: 15px;
        transition: all 0.3s;
    }
    .stButton > button:hover {
        background-color: #b3ff00;
        box-shadow: 0 0 15px rgba(204, 255, 0, 0.4);
        color: #000000;
    }

    /* Success/Error/Info Boxes */
    .stAlert {
        background-color: #111;
        border: 1px solid #333;
        color: #eee;
    }
    
    /* Custom Container Borders */
    .css-1r6slb0 {
        border: 1px solid #333;
        padding: 20px;
    }
    
    /* Progress Bar */
    .stProgress > div > div > div > div {
        background-color: #ccff00;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HELPER FUNCTIONS ---
def format_size(bytes):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes < 1024:
            return f"{bytes:.2f} {unit}"
        bytes /= 1024

def download_video(url, options):
    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            # yt-dlp sometimes changes extension (mkv/webm -> mp4), find the actual file
            base, _ = os.path.splitext(filename)
            for ext in ['mp4', 'mkv', 'webm', 'mp3']:
                if os.path.exists(f"{base}.{ext}"):
                    return f"{base}.{ext}", info.get('title', 'Unknown')
            return filename, info.get('title', 'Unknown')
    except Exception as e:
        return None, str(e)

# --- MAIN UI ---
def main():
    st.title("⚡ NEXUS_BATCH_DOWNLOADER v.PY")
    
    # Layout: 2 Columns (Input vs Config)
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### > INPUT_SOURCE")
        input_links = st.text_area(
            "Paste links here (One per line)", 
            height=200,
            placeholder="https://youtube.com/...\nhttps://tiktok.com/...\nhttps://instagram.com/...",
            label_visibility="collapsed"
        )
        
        process_btn = st.button("INITIATE_DOWNLOAD_SEQUENCE")

    with col2:
        st.markdown("### > CONFIGURATION")
        
        format_type = st.selectbox("OUTPUT_FORMAT", ["Video (Best Quality)", "Audio Only (MP3)"])
        
        # Logic Mapping
        ydl_opts = {
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'quiet': True,
            'no_warnings': True,
            'restrictfilenames': True, # Avoid weird chars in filenames
        }

        if format_type == "Audio Only (MP3)":
            ydl_opts.update({
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            })
        else:
            ydl_opts.update({
                'format': 'bestvideo+bestaudio/best', # Requires ffmpeg installed on server
                'merge_output_format': 'mp4',
            })

        st.info("SERVER STATUS: ONLINE\nENGINE: yt-dlp/stable")

    # --- PROCESSING LOGIC ---
    if process_btn and input_links:
        links = [l.strip() for l in input_links.split('\n') if l.strip()]
        
        if not links:
            st.error("ERR: No valid links detected.")
        else:
            # Create downloads folder if not exists
            if not os.path.exists('downloads'):
                os.makedirs('downloads')

            st.markdown("### > EXECUTION_LOGS")
            log_container = st.container()
            
            progress_bar = st.progress(0)
            
            for i, link in enumerate(links):
                with log_container:
                    st.write(f"[{i+1}/{len(links)}] Connecting to target: `{link}`...")
                
                # Actual Download
                file_path, title_or_error = download_video(link, ydl_opts)
                
                if file_path and os.path.exists(file_path):
                    st.success(f"SUCCESS: {title_or_error}")
                    
                    # Create Download Button for User
                    with open(file_path, "rb") as f:
                        st.download_button(
                            label=f"⬇ SAVE: {title_or_error[:20]}...",
                            data=f,
                            file_name=os.path.basename(file_path),
                            mime="application/octet-stream"
                        )
                    
                    # Optional: Clean up server space immediately to avoid bloating
                    # os.remove(file_path) 
                else:
                    st.error(f"FAILED: {title_or_error}")

                # Update Progress
                progress_bar.progress((i + 1) / len(links))
                time.sleep(0.5) # UI breathing room

            st.success("BATCH_PROCESS_COMPLETED.")

if __name__ == "__main__":
    main()