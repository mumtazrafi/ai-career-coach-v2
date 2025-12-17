import streamlit as st
import google.generativeai as genai
from pypdf import PdfReader

# --- PAGE CONFIG ---
st.set_page_config(page_title="AI Career Coach V2", page_icon="🚀", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    div.stButton > button {
        width: 100%;
        border-radius: 8px;
        height: 3em;
        font-weight: bold; 
    }
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1E88E5;
        margin-bottom: 0;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
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

# --- BRAIN: GENERATION ENGINE ---
def generate_response(system_instruction, user_prompt, _api_key):
    # V2 uses Gemini 1.5 Flash exclusively for stability and long context
    genai.configure(api_key=_api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    full_content = f"{system_instruction}\n\nUSER REQUEST: {user_prompt}"
    
    try:
        response = model.generate_content(full_content)
        return response.text
    except Exception as e:
        return f"Error: {e}"

# --- MAIN UI ---
st.markdown('<p class="main-header">🚀 AI Career Coach V2</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Resume Matcher • Cover Letter Writer • Interview Prep</p>', unsafe_allow_html=True)

# --- COMMAND CENTER V2 (Expanded) ---
# Only show controls if we have data
if st.session_state.resume_text and st.session_state.job_description:
    with st.container(border=True):
        st.markdown("### ⚡ Command Center")
        
        # Row 1: Analysis Tools
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
        
        # Row 2: Creation Tools (NEW IN V2)
        c4, c5, c6 = st.columns(3)
        
        with c4:
            if st.button("📝 Draft Cover Letter"):
                action = "Write a tailored cover letter for this job. Use the 'Hook-Story-Close' framework. Use specific facts from my resume. Do not use placeholders like [Company Name] - fill them in."
        with c5:
            if st.button("🎤 Interview Prep"):
                action = "Generate 3 tough behavioral interview questions specific to this JD and my resume. Then provide the ideal 'STAR method' talking points for each."
        with c6:
            if st.button("👋 Cold DM (LinkedIn)"):
                action = "Write a short, punchy LinkedIn connection note (under 300 chars) to the hiring manager for this role. Mention a specific skill match."

else:
    action = None
    if not st.session_state.resume_text:
        st.info("👈 Step 1: Upload your Resume PDF.")
    elif not st.session_state.job_description:
        st.info("👈 Step 2: Paste the Job Description.")

# --- CHAT HISTORY ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

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
    - For Cover Letters: Use a professional but modern tone.
    - For Interview Prep: Focus on hard skills found in the JD.
    """

    # --- GENERATE ---
    with st.chat_message("assistant"):
        with st.spinner("Processing..."):
            response_text = generate_response(system_instruction, final_prompt, api_key)
            st.markdown(response_text)
            
            st.session_state.messages.append({
                "role": "assistant", 
                "content": response_text
            })