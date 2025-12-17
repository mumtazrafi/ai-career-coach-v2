import streamlit as st
import google.generativeai as genai
from pypdf import PdfReader
import time

# --- PAGE CONFIG ---
st.set_page_config(page_title="AI Career Coach V2", page_icon="🚀", layout="wide")

# --- CUSTOM CSS (DARK MODE) ---
st.markdown("""
    <style>
    /* 1. Force Dark Background */
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    
    /* 2. Big Title Styling - Neon Blue */
    .big-title {
        font-size: 3.5rem !important;
        font-weight: 800;
        background: -webkit-linear-gradient(45deg, #4facfe, #00f2fe);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
        text-align: center;
    }
    .subtitle {
        font-size: 1.2rem;
        color: #B0B0B0;
        text-align: center;
        margin-bottom: 2rem;
    }

    /* 3. Button Styling - Dark Tech Look */
    div.stButton > button {
        width: 100%;
        background-color: #1F2937;
        color: #E5E7EB;
        border: 1px solid #374151;
        border-radius: 8px;
        font-weight: 600;
        height: 3em;
        transition: all 0.2s ease;
    }
    div.stButton > button:hover {
        background-color: #2563EB;
        color: white;
        border-color: #2563EB;
        transform: scale(1.02);
    }

    /* 4. Container Styling (Command Center) */
    [data-testid="stVerticalBlock"] > [style*="flex-direction: column;"] > [data-testid="stVerticalBlock"] {
        background-color: #161B22; /* Darker card background */
        border: 1px solid #30363D;
        padding: 20px;
        border-radius: 10px;
    }
    
    /* 5. Inputs */
    .stTextArea textarea {
        background-color: #0D1117;
        color: #C9D1D9;
        border: 1px solid #30363D;
    }
    </style>
""", unsafe_allow_html=True)

# --- SESSION STATE ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""
if "job_description" not in st.session_state:
    st.session_state.job_description = ""

# --- SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Settings")
    if "GOOGLE_API_KEY" in st.secrets:
        api_key = st.secrets["GOOGLE_API_KEY"]
        st.success("✅ Connected")
    else:
        api_key = st.text_input("Enter Google API Key:", type="password")

    st.divider()
    
    # 1. Resume
    st.subheader("1. Your Resume")
    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
    if uploaded_file and not st.session_state.resume_text:
        try:
            reader = PdfReader(uploaded_file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""
            st.session_state.resume_text = text
            st.success("✅ Resume Loaded")
        except Exception as e:
            st.error(f"Error: {e}")

    # 2. Target Job (Persistent)
    st.subheader("2. Target Job")
    def update_jd():
        st.session_state.job_description = st.session_state.jd_input

    st.text_area(
        "Paste Job Description:", 
        height=200, 
        key="jd_input",
        value=st.session_state.job_description,
        on_change=update_jd,
        placeholder="Paste the full job posting here..."
    )

    if st.button("🗑️ Reset All"):
        st.session_state.clear()
        st.rerun()

# --- BRAIN: SMART FALLBACK ENGINE ---
def generate_response(system_instruction, user_prompt, _api_key):
    # YOUR REQUESTED MODEL ORDER
    models_to_try = [
        "gemini-2.5-flash",       # Fast & Smart (Low Quota)
        "gemini-2.5-flash-lite",  # Backup Speed
        "gemma-3-27b-it",         # High Intelligence (Open Model)
        "gemini-1.5-flash"        # The Tank (High Quota)
    ]
    
    genai.configure(api_key=_api_key)
    
    full_content = f"{system_instruction}\n\nUSER REQUEST: {user_prompt}"

    last_error = None
    for model_name in models_to_try:
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(full_content)
            return response.text, model_name
        except Exception as e:
            error_str = str(e)
            if "429" in error_str or "ResourceExhausted" in error_str or "404" in error_str:
                continue
            last_error = e
            continue
            
    raise Exception(f"All models are busy. Last error: {last_error}")

# --- MAIN UI ---
# Big Gradient Title
st.markdown('<p class="big-title">AI Career Coach V2</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Resume Matcher • Cover Letter Writer • Interview Prep</p>', unsafe_allow_html=True)

# --- COMMAND CENTER V2 (Dark Mode) ---
if st.session_state.resume_text and st.session_state.job_description:
    with st.container():
        st.markdown("### ⚡ Command Center")
        
        # Row 1: Analysis
        c1, c2, c3 = st.columns(3)
        action = None
        
        with c1:
            if st.button("📊 Match Score"):
                action = "Compare my resume to the JD. Give a strict 0-10 score, list the gaps, and explain WHY."
        with c2:
            if st.button("🚩 Find Red Flags"):
                action = "Roast my resume based on this JD. Be brutal. What keywords am I missing? What experience is weak?"
        with c3:
            if st.button("✍️ Rewrite Bullet"):
                action = "Pick my weakest bullet point relevant to this job and rewrite it using 'Action-Result' format."
        
        # Row 2: Creation
        c4, c5, c6 = st.columns(3)
        
        with c4:
            if st.button("📝 Cover Letter"):
                action = "Write a tailored cover letter for this job using the 'Hook-Story-Close' framework. Use facts from my resume."
        with c5:
            if st.button("🎤 Interview Prep"):
                action = "Generate 3 tough behavioral questions specific to this JD and my resume. Provide 'STAR method' talking points."
        with c6:
            if st.button("👋 Cold DM (LinkedIn)"):
                action = "Write a short, punchy LinkedIn connection note (under 300 chars) to the hiring manager."

else:
    action = None
    col1, col2 = st.columns(2)
    with col1:
        st.info("👈 Step 1: Upload your Resume PDF.")
    with col2:
        st.info("👈 Step 2: Paste the Job Description.")

# --- CHAT HISTORY ---
st.divider()
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "model" in message:
            st.caption(f"🤖 {message['model']}")

# --- INPUT HANDLING ---
chat_input = st.chat_input("Ask a specific question...")
final_prompt = action if action else chat_input

if final_prompt:
    if not api_key:
        st.warning("⚠️ API Key missing."); st.stop()
    
    # Add User Message
    st.session_state.messages.append({"role": "user", "content": final_prompt})
    with st.chat_message("user"):
        st.markdown(final_prompt)
        
    # --- CONTEXT BUILDER ---
    jd_text = st.session_state.job_description if st.session_state.job_description else "NO JD PROVIDED."
    
    system_instruction = f"""
    ROLE: You are an Expert Tech Recruiter and Career Coach.
    
    === CANDIDATE RESUME ===
    {st.session_state.resume_text}
    
    === TARGET JOB DESCRIPTION ===
    {jd_text}
    
    INSTRUCTIONS:
    - Answer based ONLY on the documents above.
    - Be concise, direct, and actionable.
    - If suggesting changes, show "Before" and "After".
    """

    # --- GENERATE ---
    with st.chat_message("assistant"):
        placeholder = st.empty()
        with st.spinner("Analyzing..."):
            try:
                response_text, used_model = generate_response(system_instruction, final_prompt, api_key)
                
                placeholder.markdown(response_text)
                
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": response_text, 
                    "model": used_model
                })
                
                # Feedback Toast
                if "gemini-2.5" in used_model:
                    st.toast(f"⚡ Speed Mode ({used_model})", icon="🚀")
                elif "gemma" in used_model:
                    st.toast(f"🧠 Intelligence Mode ({used_model})", icon="🧠")
                else:
                    st.toast(f"🛡️ Backup Mode ({used_model})", icon="🛡️")
                    
            except Exception as e:
                st.error(f"Error: {e}")
