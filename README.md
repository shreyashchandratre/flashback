# ⚡ FlashBack — Content Architect

FlashBack is an intelligent, high-speed YouTube Content Summarizer and Q&A engine built with **Streamlit** and powered by **Groq (Llama 3 70B)**. 

Instead of dealing with clunky audio downloads or local transcriptions, FlashBack directly taps into YouTube's native transcript API to fetch content *instantly*. This allows it to process even hours-long videos in seconds while using zero local storage.

## ✨ Features

- **🚀 Instant Processing:** Uses `youtube-transcript-api` to bypass audio downloading entirely. Get insights in seconds, not minutes.
- **🧠 Advanced Summarization:** Powered by Llama 3.3 70B via Groq to generate high-density, structured summaries.
  - **⚡ Concise Summary:** Quick, high-level overview.
  - **📖 Detailed Summary:** In-depth breakdown with rich context.
- **⏱️ Chronological Timeline:** Automatically generates a chapter-by-chapter timeline to navigate long videos.
- **🎯 Actionable Takeaways:** Extracts specific, practical lessons from the content.
- **💬 Interactive Q&A:** A built-in, chat-centric Q&A interface allowing you to ask specific questions about the video content.
- **🎨 Premium UI:** Beautiful, dynamic glassmorphism design with responsive micro-animations.

## 🛠️ Tech Stack

- **Frontend:** Streamlit (Custom CSS for a glassmorphism aesthetic)
- **Transcription:** `youtube-transcript-api`
- **LLM Engine:** Llama-3.3-70b-versatile (via Groq API)
- **Environment Management:** `python-dotenv`

## 🚀 Getting Started

### Prerequisites
Make sure you have Python 3.8+ installed on your system.

### 1. Clone the repository
```bash
git clone https://github.com/shreyashchandratre/flashback.git
cd flashback
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up Environment Variables
1. Create a `.env` file in the root directory (you can use `.env.example` as a template).
2. Add your Groq API Key:
```env
GROQ_API_KEY=your_groq_api_key_here
```

### 4. Run the App
```bash
streamlit run app.py
```
The app will automatically open in your default web browser at `http://localhost:8501`.

## 🔒 Security
Your API keys are completely secure. The `.gitignore` file is configured to ensure that `.env` files are never tracked or committed to GitHub.

## 🤝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to check the issues page.
