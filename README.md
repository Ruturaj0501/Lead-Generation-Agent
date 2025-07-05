# 🏢 Company Info & Financial Analyzer

This Streamlit app helps you analyze any company's business summary and financial profile using Gemini (Google's LLM) and dynamic web scraping. Just enter a company name, and the app will:

- Ask Gemini to return official and relevant URLs (homepage, About Us, Wikipedia).
- Scrape these URLs using **BeautifulSoup** and **Playwright** as a fallback.
- Extract content and analyze:
  - A **2–3 line business summary**
  - A **financial/fundamental report** (business model, revenue, profit insights, etc.)

---

## 🚀 Features

- ✅ LLM-powered URL extraction (Gemini)
- ✅ Robust scraping using BS4 and Playwright
- ✅ Multi-level content cleaning and extraction
- ✅ AI-generated business and financial analysis
- ✅ Streamlit UI with dynamic feedback and error handling

---

## 🛠 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/company-analyzer.git
cd company-analyzer
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate     # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**requirements.txt**

```txt
streamlit
requests
beautifulsoup4
python-dotenv
langchain
langchain-google-genai
playwright
```

Also install Playwright's Chromium browser engine:

```bash
playwright install chromium
```

### 4. Add your Gemini API Key

Create a `.env` file in the root directory:

```env
GOOGLE_API_KEY=your_google_gemini_api_key
```

---

## ▶️ Run the App

```bash
streamlit run app.py
```

---

## 📊 Dataset

This app **does not use a fixed dataset**. All content is scraped live from URLs returned by Gemini, including:

- Official company websites
- Wikipedia pages
- "About Us" sections
- Investor relations pages (if found)

The scraped content is then analyzed using Gemini LLM.

---

## 🧠 AI Models Used

- [`gemini-1.5-flash-latest`](https://ai.google.dev/)
  - Used for:
    - Getting company URLs
    - Summarizing business profiles
    - Performing financial and fundamental analysis

---

## 🧩 Folder Structure

```
company-analyzer/
├── app.py              # Main Streamlit application
├── .env                # Gemini API key
├── requirements.txt    # Python dependencies
└── README.md           # You're reading it!
```

---

## ⚠️ Notes

- Some websites with heavy JS may require Playwright scraping; BS4 might fail.
- Avoid searching for obscure startups as they may lack scrapeable online presence.
- Rate limits or temporary blocks can occur if too many requests are made quickly.

---

## 📄 License

MIT License. Feel free to modify and use it.

---

## 🙌 Acknowledgments

- [LangChain](https://www.langchain.com/)
- [Google Generative AI](https://ai.google.dev/)
- [Streamlit](https://streamlit.io/)
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)
- [Playwright](https://playwright.dev/)