# 👔 AI Career Coach & Resume Matcher

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](ai-resume-checker-v2.streamlit.app)

A smart, context-aware career assistant built with **Python** and **Google Gemini 1.5 Flash**.

Unlike generic ATS scanners that just look for keywords, this AI understands the *nuance* of your experience. It compares your Resume PDF against a specific Job Description (JD) to provide a strict match score, identify missing skills, and even rewrite your bullet points in real-time.

<img width="1359" height="602" alt="Screenshot 2025-12-17 184359" src="https://github.com/user-attachments/assets/51aed84b-d3c9-4143-8afa-5d4b90b0e703" />

---

## 🚀 Key Features

* **📄 PDF Resume Parsing:** Instantly extracts text from PDF resumes using `pypdf`.
* **🎯 Context-Aware Matching:** "Pins" the Job Description to the AI's memory, ensuring every answer is tailored to the specific role.
* **📊 Strict Scoring:** Provides a 0-10 match score with a breakdown of strengths and critical gaps.
* **🚩 "Roast" Mode:** Identifies red flags, vagueness, or weak verbs that recruiters might spot.
* **✍️ Magic Rewrite:** Automatically rewrites weak bullet points into "Action-Result" format using keywords from the JD.
* **🧠 Persistent Memory:** Remembers your resume and the target job throughout the chat session.
* **🛡️ Smart Fallback:** (Optional) Architecture designed to handle API rate limits gracefully.

---

## 🛠️ Tech Stack

* **Frontend:** [Streamlit](https://streamlit.io/) (Python-based UI).
* **AI Engine:** [Google Gemini](https://deepmind.google/technologies/gemini/) (via `google-generativeai`).
* **Data Processing:** `pypdf` for extracting text from PDF documents.
* **Version Control:** Git & GitHub.
* **Deployment:** Streamlit Cloud.

---

## 💻 How to Run Locally

If you want to run this app on your own machine, follow these steps:

**1. Clone the repository**
```bash
git clone [https://github.com/YOUR_USERNAME/ai-career-coach-v2.git](https://github.com/YOUR_USERNAME/ai-career-coach-v2.git)
cd ai-career-coach-v2

Here is a professional, ready-to-use `README.md` for your project.

Copy the code block below, go to your **GitHub repository**, click **"Add file"** -> **"Create new file"**, name it `README.md`, and paste this content.

**(Make sure to replace the placeholder links with your actual details!)**

```markdown
# 👔 AI Career Coach & Resume Matcher

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](INSERT_YOUR_STREAMLIT_APP_LINK_HERE)

A smart, context-aware career assistant built with **Python** and **Google Gemini 1.5 Flash**.

Unlike generic ATS scanners that just look for keywords, this AI understands the *nuance* of your experience. It compares your Resume PDF against a specific Job Description (JD) to provide a strict match score, identify missing skills, and even rewrite your bullet points in real-time.

![App Screenshot](https://via.placeholder.com/800x400.png?text=Add+Your+Screenshot+Here)
*(Tip: Replace this link with a screenshot of your actual app running!)*

---

## 🚀 Key Features

* **📄 PDF Resume Parsing:** Instantly extracts text from PDF resumes using `pypdf`.
* **🎯 Context-Aware Matching:** "Pins" the Job Description to the AI's memory, ensuring every answer is tailored to the specific role.
* **📊 Strict Scoring:** Provides a 0-10 match score with a breakdown of strengths and critical gaps.
* **🚩 "Roast" Mode:** Identifies red flags, vagueness, or weak verbs that recruiters might spot.
* **✍️ Magic Rewrite:** Automatically rewrites weak bullet points into "Action-Result" format using keywords from the JD.
* **🧠 Persistent Memory:** Remembers your resume and the target job throughout the chat session.
* **🛡️ Smart Fallback:** (Optional) Architecture designed to handle API rate limits gracefully.

---

## 🛠️ Tech Stack

* **Frontend:** [Streamlit](https://streamlit.io/) (Python-based UI).
* **AI Engine:** [Google Gemini 1.5 Flash](https://deepmind.google/technologies/gemini/) (via `google-generativeai`).
* **Data Processing:** `pypdf` for extracting text from PDF documents.
* **Version Control:** Git & GitHub.
* **Deployment:** Streamlit Cloud.

---

## 💻 How to Run Locally

If you want to run this app on your own machine, follow these steps:

**1. Clone the repository**
```bash
git clone [https://github.com/YOUR_USERNAME/ai-career-coach-v2.git](https://github.com/YOUR_USERNAME/ai-career-coach-v2.git)
cd ai-career-coach-v2

```

**2. Install dependencies**

```bash
pip install -r requirements.txt

```

**3. Set up your API Key**
Create a secrets file to store your Google API key securely.

* Create a folder named `.streamlit` in the root directory.
* Inside it, create a file named `secrets.toml`.
* Add your key:

```toml
GOOGLE_API_KEY = "AIzaSy...YOUR_KEY_HERE"

```

**4. Run the app**

```bash
streamlit run app.py

```

---

## 🔒 Security Note

This project uses a `.gitignore` file to ensure API keys and secret configurations are **never** uploaded to the public repository. The app relies on Streamlit's secrets management for secure deployment.

---

## 🤝 Contributing

Feel free to fork this repository and submit pull requests. Future roadmap ideas:

* Add Cover Letter generation.
* Support for multiple resume versions.
* Integration with LinkedIn scraping.


