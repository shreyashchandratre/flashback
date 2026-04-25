import streamlit as st
import yt_dlp
import os
import json
import glob
import subprocess
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="FlashBack — Content Architect",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Montserrat:wght@700;800&display=swap');
    :root {
        --purple: #a855f7; --purple2: #7c3aed;
        --teal: #2dd4bf;   --teal2: #0d9488;
        --bg: #080b14;     --glass: rgba(255,255,255,0.04);
        --glass-border: rgba(168,85,247,0.18);
        --text: #e2e8f0;   --muted: #94a3b8;
    }
    html, body, [data-testid="stAppViewContainer"], .stApp {
        background: var(--bg) !important;
        font-family: 'Inter', sans-serif !important;
        color: var(--text) !important;
    }
    [data-testid="stAppViewContainer"] {
        background:
            radial-gradient(ellipse 80% 60% at 10% 0%, rgba(124,58,237,0.18) 0%, transparent 60%),
            radial-gradient(ellipse 60% 50% at 90% 100%, rgba(45,212,191,0.12) 0%, transparent 55%),
            var(--bg) !important;
    }
    [data-testid="block-container"] { padding-top: 2rem !important; }
    [data-testid="stSidebar"] {
        background: rgba(13,17,32,0.92) !important;
        border-right: 1px solid var(--glass-border) !important;
        backdrop-filter: blur(20px) !important;
    }
    [data-testid="stSidebar"] * { color: var(--text) !important; }
    [data-testid="stSidebar"] hr { border-color: rgba(168,85,247,0.2) !important; }
    [data-testid="stTextInput"] input {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(168,85,247,0.3) !important;
        border-radius: 10px !important;
        color: var(--text) !important;
        font-family: 'Inter', sans-serif !important;
        transition: border-color 0.3s, box-shadow 0.3s !important;
    }
    [data-testid="stTextInput"] input:focus {
        border-color: var(--purple) !important;
        box-shadow: 0 0 0 3px rgba(168,85,247,0.15), 0 0 20px rgba(168,85,247,0.1) !important;
    }
    .stButton > button {
        background: linear-gradient(135deg, var(--purple2), var(--teal2)) !important;
        color: #fff !important; border: none !important;
        border-radius: 12px !important; padding: 0.65rem 1.2rem !important;
        font-family: 'Inter', sans-serif !important; font-weight: 600 !important;
        font-size: 0.9rem !important; letter-spacing: 0.04em !important;
        width: 100% !important; transition: all 0.3s ease !important;
        box-shadow: 0 0 20px rgba(124,58,237,0.3) !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 0 35px rgba(124,58,237,0.55), 0 0 15px rgba(45,212,191,0.25) !important;
    }
    .stTabs [data-baseweb="tab-list"] {
        background: transparent !important;
        padding: 6px 0 !important; gap: 10px !important;
        border: none !important;
    }
    .stTabs [data-baseweb="tab"] {
        background: rgba(255,255,255,0.05) !important; 
        border: 1px solid rgba(168,85,247,0.3) !important;
        border-radius: 12px !important;
        color: var(--text) !important; 
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important; 
        padding: 8px 16px !important;
        transition: all 0.3s ease !important;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(168,85,247,0.15) !important;
        border-color: rgba(168,85,247,0.6) !important;
        transform: translateY(-2px) !important;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, var(--purple2), var(--teal2)) !important;
        color: #fff !important; 
        border-color: transparent !important;
        box-shadow: 0 4px 15px rgba(124,58,237,0.4) !important;
    }
    .stTabs [aria-selected="true"] p { color: #fff !important; font-weight: 700 !important; }
    .glass-card {
        background: var(--glass); border: 1px solid var(--glass-border);
        border-radius: 18px; padding: 28px 32px; margin-bottom: 20px;
        backdrop-filter: blur(24px); -webkit-backdrop-filter: blur(24px);
        box-shadow: 0 8px 32px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.06);
        color: var(--text); line-height: 1.75; font-size: 0.95rem;
    }
    .glass-card-teal {
        border-color: rgba(45,212,191,0.22);
        box-shadow: 0 8px 32px rgba(0,0,0,0.4), 0 0 30px rgba(45,212,191,0.06), inset 0 1px 0 rgba(255,255,255,0.06);
    }
    .hero-title {
        font-family: 'Montserrat', sans-serif; font-size: 2.8rem; font-weight: 800;
        background: linear-gradient(135deg, #c084fc 0%, #a855f7 40%, #2dd4bf 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        background-clip: text; letter-spacing: -0.02em; line-height: 1.1; margin-bottom: 0.4rem;
    }
    .hero-sub {
        color: var(--muted); font-size: 1rem; font-weight: 400;
        letter-spacing: 0.06em; text-transform: uppercase; margin-bottom: 2rem;
    }
    .section-label {
        font-family: 'Inter', sans-serif; font-size: 0.72rem; font-weight: 600;
        letter-spacing: 0.14em; text-transform: uppercase; color: var(--purple);
        margin-bottom: 10px; display: flex; align-items: center; gap: 8px;
    }
    .section-label::after {
        content: ''; flex: 1; height: 1px;
        background: linear-gradient(90deg, rgba(168,85,247,0.4), transparent);
    }
    .takeaway-item {
        display: flex; align-items: flex-start; gap: 12px;
        padding: 12px 0; border-bottom: 1px solid rgba(168,85,247,0.08); font-size: 0.93rem;
    }
    .takeaway-item:last-child { border-bottom: none; }
    .takeaway-dot {
        width: 8px; height: 8px; border-radius: 50%;
        background: linear-gradient(135deg, var(--purple), var(--teal));
        margin-top: 6px; flex-shrink: 0; box-shadow: 0 0 8px rgba(168,85,247,0.6);
    }
    .timeline-item {
        display: flex; gap: 18px; padding: 14px 0;
        border-bottom: 1px solid rgba(45,212,191,0.08); align-items: flex-start;
    }
    .timeline-item:last-child { border-bottom: none; }
    .timeline-stamp {
        font-family: 'Montserrat', sans-serif; font-size: 0.72rem; font-weight: 700;
        color: var(--teal); letter-spacing: 0.08em; background: rgba(45,212,191,0.1);
        border: 1px solid rgba(45,212,191,0.25); border-radius: 6px; padding: 3px 10px;
        white-space: nowrap; box-shadow: 0 0 10px rgba(45,212,191,0.15);
        flex-shrink: 0; margin-top: 2px;
    }
    .timeline-text { font-size: 0.93rem; color: var(--text); line-height: 1.6; }
    .processing-wrap {
        display: flex; flex-direction: column; align-items: center;
        justify-content: center; padding: 60px 20px; gap: 24px;
    }
    .antigravity-scene { position: relative; width: 220px; height: 160px; }
    .page {
        position: absolute; width: 52px; height: 66px; border-radius: 4px;
        border: 1px solid rgba(168,85,247,0.5);
        background: linear-gradient(135deg, rgba(124,58,237,0.15), rgba(45,212,191,0.08));
        backdrop-filter: blur(8px);
        box-shadow: 0 0 18px rgba(168,85,247,0.3), inset 0 1px 0 rgba(255,255,255,0.1);
    }
    .page::before {
        content: ''; position: absolute; left: 8px; top: 10px; right: 8px;
        height: 2px; border-radius: 2px; background: rgba(168,85,247,0.4);
        box-shadow: 0 6px 0 rgba(168,85,247,0.25), 0 12px 0 rgba(168,85,247,0.15),
                    0 18px 0 rgba(45,212,191,0.2), 0 24px 0 rgba(45,212,191,0.12);
    }
    .page-1 { left: 20px;  top: 60px; animation: float1 3.2s ease-in-out infinite; }
    .page-2 { left: 85px;  top: 20px; animation: float2 2.8s ease-in-out infinite 0.4s; }
    .page-3 { left: 150px; top: 55px; animation: float3 3.5s ease-in-out infinite 0.8s; }
    .page-4 { left: 55px;  top: 90px; animation: float1 2.6s ease-in-out infinite 1.2s; transform: rotate(-12deg); }
    .page-5 { left: 120px; top: 85px; animation: float2 3.0s ease-in-out infinite 0.6s; transform: rotate(8deg); }
    .sound-wave { display: flex; align-items: center; gap: 4px; height: 36px; }
    .bar {
        width: 4px; border-radius: 3px;
        background: linear-gradient(180deg, var(--purple), var(--teal));
        box-shadow: 0 0 8px rgba(168,85,247,0.5);
    }
    .bar:nth-child(1) { animation: wave 1.1s ease-in-out infinite 0.0s; }
    .bar:nth-child(2) { animation: wave 1.1s ease-in-out infinite 0.1s; }
    .bar:nth-child(3) { animation: wave 1.1s ease-in-out infinite 0.2s; }
    .bar:nth-child(4) { animation: wave 1.1s ease-in-out infinite 0.3s; }
    .bar:nth-child(5) { animation: wave 1.1s ease-in-out infinite 0.4s; }
    .bar:nth-child(6) { animation: wave 1.1s ease-in-out infinite 0.3s; }
    .bar:nth-child(7) { animation: wave 1.1s ease-in-out infinite 0.2s; }
    .bar:nth-child(8) { animation: wave 1.1s ease-in-out infinite 0.1s; }
    .bar:nth-child(9) { animation: wave 1.1s ease-in-out infinite 0.0s; }
    .processing-label {
        font-family: 'Montserrat', sans-serif; font-size: 1.1rem; font-weight: 700;
        letter-spacing: 0.12em; text-transform: uppercase;
        background: linear-gradient(135deg, var(--purple), var(--teal));
        -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
    }
    .processing-sub { font-size: 0.82rem; color: var(--muted); letter-spacing: 0.06em; }
    .step-badge {
        display: inline-flex; align-items: center; gap: 8px; padding: 8px 16px;
        border-radius: 30px; font-size: 0.82rem; font-weight: 600;
        letter-spacing: 0.04em; border: 1px solid;
    }
    .step-pending { background: rgba(148,163,184,0.08); border-color: rgba(148,163,184,0.2); color: var(--muted); }
    .step-active  { background: rgba(168,85,247,0.12); border-color: rgba(168,85,247,0.4); color: #c084fc;
                    box-shadow: 0 0 16px rgba(168,85,247,0.2); animation: pulse-badge 1.5s ease-in-out infinite; }
    .step-done    { background: rgba(45,212,191,0.1); border-color: rgba(45,212,191,0.35); color: var(--teal);
                    box-shadow: 0 0 12px rgba(45,212,191,0.15); }
    .transcript-box {
        max-height: 420px; overflow-y: auto; font-size: 0.9rem;
        line-height: 1.85; color: var(--muted); padding-right: 8px;
    }
    .transcript-box::-webkit-scrollbar { width: 4px; }
    .transcript-box::-webkit-scrollbar-track { background: transparent; }
    .transcript-box::-webkit-scrollbar-thumb { background: rgba(168,85,247,0.3); border-radius: 4px; }
    /* ── Summary toggle radio ── */
    div[data-testid="stRadio"] > div {
        display: flex; gap: 8px; flex-direction: row !important;
    }
    div[data-testid="stRadio"] label {
        background: rgba(255,255,255,0.04) !important;
        border: 1px solid rgba(168,85,247,0.25) !important;
        border-radius: 30px !important; padding: 6px 20px !important;
        color: var(--muted) !important; font-size: 0.85rem !important;
        font-weight: 500 !important; cursor: pointer !important;
        transition: all 0.2s !important;
    }
    div[data-testid="stRadio"] label:has(input:checked) {
        background: linear-gradient(135deg, rgba(124,58,237,0.35), rgba(13,148,136,0.25)) !important;
        border-color: rgba(168,85,247,0.5) !important;
        color: #fff !important;
        box-shadow: 0 0 14px rgba(168,85,247,0.25) !important;
    }
    div[data-testid="stRadio"] input { display: none !important; }
    .sidebar-section {
        font-size: 0.7rem; font-weight: 700; letter-spacing: 0.14em;
        text-transform: uppercase; color: var(--purple) !important; margin: 1.2rem 0 0.5rem;
    }
    .powered-by {
        font-size: 0.72rem; color: var(--muted) !important;
        letter-spacing: 0.06em; text-align: center; padding-top: 8px;
    }
    @keyframes float1 { 0%,100% { transform: translateY(0px) rotate(-6deg); } 50% { transform: translateY(-22px) rotate(-3deg); } }
    @keyframes float2 { 0%,100% { transform: translateY(0px) rotate(4deg);  } 50% { transform: translateY(-28px) rotate(8deg);  } }
    @keyframes float3 { 0%,100% { transform: translateY(0px) rotate(10deg); } 50% { transform: translateY(-18px) rotate(6deg);  } }
    @keyframes wave   { 0%,100% { height: 8px;  } 50% { height: 32px; } }
    @keyframes pulse-badge {
        0%,100% { box-shadow: 0 0 16px rgba(168,85,247,0.2); }
        50%      { box-shadow: 0 0 28px rgba(168,85,247,0.45); }
    }
    #MainMenu, footer, header { visibility: hidden; }
    [data-testid="stDecoration"] { display: none; }
</style>
""", unsafe_allow_html=True)

# ── HTML Templates ────────────────────────────────────────────────────────────
ANIM_HTML = (
    '<div class="processing-wrap">'
    '<div class="antigravity-scene">'
    '<div class="page page-1"></div><div class="page page-2"></div>'
    '<div class="page page-3"></div><div class="page page-4"></div>'
    '<div class="page page-5"></div>'
    '</div>'
    '<div class="sound-wave">'
    '<div class="bar"></div><div class="bar"></div><div class="bar"></div>'
    '<div class="bar"></div><div class="bar"></div><div class="bar"></div>'
    '<div class="bar"></div><div class="bar"></div><div class="bar"></div>'
    '</div>'
    '<div class="processing-label">{label}</div>'
    '<div class="processing-sub">{sub}</div>'
    '</div>'
)


def anim(label, sub):
    return ANIM_HTML.format(label=label, sub=sub)


def badge(icon, text, state):
    return f'<span class="step-badge step-{state}">{icon} {text}</span>'


# ── Backend ───────────────────────────────────────────────────────────────────
def download_audio(url):
    cookies_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cookies.txt')
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'temp_audio.%(ext)s',
        'quiet': True,
        'no_warnings': True,
        'retries': 10,
        'fragment_retries': 10,
        # spoof a real browser to reduce bot detection
        'http_headers': {
            'User-Agent': (
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/125.0.0.0 Safari/537.36'
            ),
        },
        'extractor_args': {'youtube': {'player_client': ['android', 'ios', 'web']}},
    }
    if os.path.exists(cookies_file):
        ydl_opts['cookiefile'] = cookies_file

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            return filename
    except Exception as e:
        err = str(e)
        if 'Sign in' in err or 'bot' in err.lower():
            st.error(
                "YouTube is blocking the download. "
                "Please export your cookies:\n\n"
                "1. Install the **Get cookies.txt LOCALLY** Chrome extension\n"
                "2. Go to youtube.com while logged in\n"
                "3. Click the extension → Export → save as `cookies.txt` "
                "in the project folder\n"
                "4. Re-run the analysis"
            )
        else:
            st.error(f"Download error: {e}")
        return None


def transcribe_audio(file_path, client, anim_ph=None):
    file_size = os.path.getsize(file_path)
    limit = 24 * 1024 * 1024 # 24 MB API limit
    
    if file_size <= limit:
        if anim_ph:
            anim_ph.markdown(anim("Step 2/3", "Transcribing audio to text via Whisper...<br><span style='font-size:0.8em;color:var(--teal)'>Processing short video natively...</span>"), unsafe_allow_html=True)
            
        import time
        try:
            for attempt in range(3):
                try:
                    with open(file_path, "rb") as f:
                        result = client.audio.transcriptions.create(
                            file=(os.path.basename(file_path), f.read()),
                            model="whisper-large-v3-turbo",
                            response_format="text"
                        )
                    return result
                except Exception as e:
                    if attempt == 2:
                        st.error(f"Transcription error: {e}")
                        return None
                    time.sleep(3)
        finally:
            if os.path.exists(file_path):
                try: os.remove(file_path)
                except Exception: pass

    # If the file is larger than 24MB, split it with ffmpeg
    chunk_duration = 600 # 10 minutes per segment to ensure much smaller uploads
    full_transcript = []
    base_name = "chunk_temp"
    ext = os.path.splitext(file_path)[1]
    
    try:
        import imageio_ffmpeg
        ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
        
        subprocess.run([
            ffmpeg_exe, '-y', '-i', file_path, '-f', 'segment', 
            '-segment_time', str(chunk_duration), '-c', 'copy', 
            f'{base_name}_%03d{ext}'
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        chunks = sorted(glob.glob(f'{base_name}_*{ext}'))
        
        import concurrent.futures
        import time
        results = [None] * len(chunks)
        total_chunks = len(chunks)
        completed = 0
        
        if anim_ph:
            anim_ph.markdown(anim("Step 2/3", f"Transcribing audio to text via Whisper...<br><span style='font-size:0.8em;color:var(--teal)'>Processing segments (0/{total_chunks})</span>"), unsafe_allow_html=True)
        
        def process_segment(idx_chunk):
            idx, chunk = idx_chunk
            for attempt in range(3):
                try:
                    with open(chunk, "rb") as f:
                        res = client.audio.transcriptions.create(
                            file=(os.path.basename(chunk), f.read()),
                            model="whisper-large-v3-turbo",
                            response_format="text"
                        )
                        return idx, res
                except Exception as loop_e:
                    if attempt == 2:
                        raise loop_e
                    time.sleep(3)
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            futures = [executor.submit(process_segment, item) for item in enumerate(chunks)]
            for future in concurrent.futures.as_completed(futures):
                idx, text = future.result()
                results[idx] = text
                completed += 1
                if anim_ph:
                    anim_ph.markdown(anim("Step 2/3", f"Transcribing audio to text via Whisper...<br><span style='font-size:0.8em;color:var(--teal)'>Processing segments ({completed}/{total_chunks})</span>"), unsafe_allow_html=True)
                
        return " ".join(results)
        
    except FileNotFoundError:
        st.error("ffmpeg is not installed on this system. Cannot split and process long videos.")
        return None
    except Exception as e:
        st.error(f"Transcription chunking error: {e}")
        return None
    finally:
        if os.path.exists(file_path):
            try: os.remove(file_path)
            except Exception: pass
        for chunk in glob.glob(f'{base_name}_*{ext}'):
            try: os.remove(chunk)
            except Exception: pass


def analyze_content(transcript, client):
    prompt = (
        "You are a High-Density Content Architect. Analyze the transcript and respond STRICTLY "
        "in valid JSON with this structure:\n"
        '{"concise_summary": ["3 short bullet points, one sentence each"],'
        '"detailed_summary": ["5-7 detailed bullet points with full context and explanation"],'
        '"chronological_chapters": ["chapter 1","chapter 2"],'
        '"actionable_takeaways": ["takeaway 1","takeaway 2"]}\n\n'
        f"Transcript:\n{transcript}"
    )
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        st.error(f"Analysis error: {e}")
        return None


def answer_question(transcript, question, client):
    prompt = (
        "You are a helpful assistant. Use the following transcript to answer the user's question concisely. "
        "If the answer is not in the transcript, state that clearly.\n\n"
        f"Transcript:\n{transcript}\n\nQuestion: {question}"
    )
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"


# ── UI ────────────────────────────────────────────────────────────────────────
def main():
    with st.sidebar:
        st.markdown('<div class="hero-title" style="font-size:1.6rem;">⚡ FlashBack</div>', unsafe_allow_html=True)
        st.markdown('<div style="color:#94a3b8;font-size:0.78rem;letter-spacing:0.08em;margin-bottom:1.2rem;">CONTENT ARCHITECT</div>', unsafe_allow_html=True)
        st.markdown("---")
        st.markdown('<div class="sidebar-section">📡 Source</div>', unsafe_allow_html=True)
        youtube_url = st.text_input("Enter your YT URL", placeholder="https://youtu.be/...")
        st.markdown("<br>", unsafe_allow_html=True)
        process_btn = st.button("⚡  Analyse Content")
        st.markdown("---")
        st.markdown('<div class="powered-by">yt-dlp · Whisper-v3-turbo · Llama-3.3-70b</div>', unsafe_allow_html=True)

    st.markdown('<div class="hero-title">FlashBack</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">YouTube &amp; Podcast Intelligence Engine</div>', unsafe_allow_html=True)

    if "processed_url" not in st.session_state:
        st.session_state.processed_url = None

    if process_btn:
        st.session_state.processed_url = youtube_url

    if not st.session_state.processed_url or st.session_state.processed_url != youtube_url:
        st.markdown(anim("Ready to Analyse", "Paste a URL in the sidebar and hit Analyse Content"), unsafe_allow_html=True)
        return

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        st.error("GROQ_API_KEY not found in .env file.")
        return
    if not youtube_url:
        st.sidebar.error("Please provide a YouTube / Podcast URL.")
        return

    col1, col2, col3 = st.columns(3)
    dl_ph = col1.empty()
    tr_ph = col2.empty()
    an_ph = col3.empty()

    def set_badges(dl, tr, an):
        dl_ph.markdown(badge("⬇", "Download",  dl), unsafe_allow_html=True)
        tr_ph.markdown(badge("🎙", "Transcribe", tr), unsafe_allow_html=True)
        an_ph.markdown(badge("🧠", "Analyse",   an), unsafe_allow_html=True)

    anim_ph = st.empty()
    cache_key = f"data_{youtube_url}"

    if cache_key in st.session_state:
        transcript, analysis = st.session_state[cache_key]
        set_badges("done", "done", "done")
    else:
        # Step 1: Download
        set_badges("active", "pending", "pending")
        anim_ph.markdown(anim("Step 1/3", "Downloading audio...<br><span style='font-size:0.7em;font-weight:400;color:gray;'>(This may take a minute for long videos)</span>"), unsafe_allow_html=True)
        audio_file = download_audio(youtube_url)
        if not audio_file:
            st.session_state.processed_url = None
            anim_ph.empty()
            return
            
        # Step 2: Transcribe
        set_badges("done", "active", "pending")
        anim_ph.markdown(anim("Step 2/3", "Transcribing audio to text via Whisper..."), unsafe_allow_html=True)
        client = Groq(api_key=api_key, timeout=600.0, max_retries=2)
        transcript = transcribe_audio(audio_file, client, anim_ph=anim_ph)
        if not transcript:
            st.session_state.processed_url = None
            anim_ph.empty()
            return
            
        # Step 3: Analyze
        set_badges("done", "done", "active")
        anim_ph.markdown(anim("Step 3/3", "Structuring insights with Llama 3 70B..."), unsafe_allow_html=True)
        analysis = analyze_content(transcript, client)
        if not analysis:
            st.session_state.processed_url = None
            anim_ph.empty()
            return
            
        st.session_state[cache_key] = (transcript, analysis)
        set_badges("done", "done", "done")

    anim_ph.empty()

    st.markdown("<br>", unsafe_allow_html=True)
    tab_summary, tab_chapters, tab_transcript, tab_qa = st.tabs([
        "✦  Key Takeaways", "⏱  Timeline", "📜  Full Transcript", "❓  Q&A"
    ])

    with tab_summary:
        # ── Summary toggle ────────────────────────────────────────────────
        mode = st.radio(
            "Summary mode",
            ["⚡ Concise", "📖 Detailed"],
            horizontal=True,
            label_visibility="collapsed"
        )
        st.markdown("<br>", unsafe_allow_html=True)

        if mode == "⚡ Concise":
            st.markdown('<div class="section-label">Concise Summary</div>', unsafe_allow_html=True)
            bullets = analysis.get('concise_summary', [])
        else:
            st.markdown('<div class="section-label">Detailed Summary</div>', unsafe_allow_html=True)
            bullets = analysis.get('detailed_summary', [])

        html = '<div class="glass-card">'
        for b in bullets:
            html += f'<div class="takeaway-item"><div class="takeaway-dot"></div><div>{b}</div></div>'
        st.markdown(html + '</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-label">Actionable Takeaways</div>', unsafe_allow_html=True)
        html = '<div class="glass-card glass-card-teal">'
        for t in analysis.get('actionable_takeaways', []):
            html += f'<div class="takeaway-item"><div class="takeaway-dot"></div><div>{t}</div></div>'
        st.markdown(html + '</div>', unsafe_allow_html=True)

    with tab_chapters:
        st.markdown('<div class="section-label">Chronological Index</div>', unsafe_allow_html=True)
        html = '<div class="glass-card glass-card-teal">'
        for i, chapter in enumerate(analysis.get('chronological_chapters', [])):
            parts = chapter.split(' ', 1) if chapter else ['', chapter]
            if len(parts) == 2 and any(c.isdigit() for c in parts[0]):
                stamp, text = parts[0], parts[1]
            else:
                stamp, text = f"{i+1:02d}", chapter
            html += f'<div class="timeline-item"><span class="timeline-stamp">{stamp}</span><span class="timeline-text">{text}</span></div>'
        st.markdown(html + '</div>', unsafe_allow_html=True)

    with tab_transcript:
        st.markdown('<div class="section-label">Raw Transcript</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="glass-card"><div class="transcript-box">{transcript}</div></div>',
            unsafe_allow_html=True
        )

    with tab_qa:
        st.markdown('<div class="section-label">Ask About the Content</div>', unsafe_allow_html=True)
        
        qa_history_key = f"qa_history_{youtube_url}"
        if qa_history_key not in st.session_state:
            st.session_state[qa_history_key] = []
            
        for item in st.session_state[qa_history_key]:
            with st.chat_message("user"):
                st.write(item["q"])
            with st.chat_message("assistant"):
                st.write(item["a"])
                
        if prompt_text := st.chat_input("Ask a question about the video..."):
            with st.chat_message("user"):
                st.write(prompt_text)
                
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    client = Groq(api_key=api_key, timeout=60.0)
                    answer = answer_question(transcript, prompt_text, client)
                st.write(answer)
                
            st.session_state[qa_history_key].append({"q": prompt_text, "a": answer})


if __name__ == "__main__":
    main()
