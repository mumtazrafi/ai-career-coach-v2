import streamlit as st
import google.generativeai as genai
from pypdf import PdfReader

# --- PAGE CONFIG ---
st.set_page_config(page_title="AI Career Coach", page_icon="👔", layout="wide")

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
    # We use a callback to ensure the state is updated immediately
    def update_jd():
        st.session_state.job_description = st.session_state.jd_input

    st.text_area(
        "Paste Job Description:", 
        height=150, 
        key="jd_input",
        value=st.session_state.job_description,
        on_change=update_jd
    )

    if st.button("🗑️ Reset All"):
        st.session_state.clear()
        st.rerun()

# --- BRAIN: SMART FALLBACK ENGINE ---
def generate_response(system_prompt, user_prompt, _api_key):
    # The Order of Battle: Speed -> Intelligence -> Endurance
    models = [
        "gemini-2.5-flash",       # Fast & Smart (Low Quota)
        "gemini-2.5-flash-lite",  # Backup Speed
        "gemma-3-27b-it",         # High Intelligence (Open Model)
        "gemini-1.5-flash"        # The Tank (High Quota)
    ]
    
    genai.configure(api_key=_api_key)
    
    # We combine System + User into one block to ensure context is never lost
    full_content = f"{system_prompt}\n\nUSER REQUEST: {user_prompt}"

    for model_name in models:
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(full_content)
            return response.text, model_name
        except Exception as e:
            # If Rate Limit (429) or Overloaded, try next
            if "429" in str(e) or "ResourceExhausted" in str(e):
                continue
            # If other error, keep trying down the list just in case
            continue
            
    raise Exception("All models are busy. Please wait 1 minute.")

# --- MAIN UI ---
st.title("👔 AI Career Coach")

# --- DASHBOARD CONTROL PANEL (New UI) ---
# We only show this if data is loaded
if st.session_state.resume_text and st.session_state.job_description:
    with st.container(border=True):
        st.markdown("### ⚡ Quick Action")
        c1, c2, c3, c4 = st.columns(4)
        
        action = None
        
        if c1.button("📊 Match Score", use_container_width=True):
            action = "Compare my resume to the JD. Give a strict 0-10 score, list the gaps, and explain WHY."
        
        if c2.button("🚩 Find Red Flags", use_container_width=True):
            action = "Roast my resume based on this JD. Be brutal. What keywords am I missing? What experience is weak?"
            
        if c3.button("✍️ Rewrite Bullet", use_container_width=True):
            action = "Identify my weakest bullet point relevant to this job and rewrite it using 'Action-Result' format."
            
        if c4.button("📧 Cover Letter", use_container_width=True):
            action = "Draft a short, punchy cover letter opening paragraph connecting my specific experience to this job."

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
        
    # --- CONTEXT BUILDER (The Memory Fix) ---
    # We reconstruct the 'Brain' every single time. 
    # The AI is forced to read the Resume + JD on every turn.
    
    system_instruction = f"""
    ROLE: You are an Expert Tech Recruiter and Career Coach.
    
    === CANDIDATE RESUME ===
    {st.session_state.resume_text}
    
    === TARGET JOB DESCRIPTION ===
    {st.session_state.job_description}
    
    INSTRUCTIONS:
    - Answer the user's request based ONLY on the documents above.
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
                
                # Metadata
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": response_text, 
                    "model": used_model
                })
                
                # Feedback Toast
                if "gemini-2.5" in used_model:
                    st.toast(f"⚡ Speed Mode ({used_model})", icon="🚀")
                else:
                    st.toast(f"🛡️ Backup Mode ({used_model})", icon="🛡️")
                    
            except Exception as e:
                st.error(f"Error: {e}")