import os
from dotenv import load_dotenv
import streamlit as st
import requests
from bs4 import BeautifulSoup
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.document_loaders import PlaywrightURLLoader
import re


try:
    load_dotenv()
    
    if 'GOOGLE_API_KEY' not in os.environ:
        os.environ['GOOGLE_API_KEY'] = os.getenv('GOOGLE_API_KEY')
    if not os.getenv('GOOGLE_API_KEY'):
        st.error("🚨 GOOGLE_API_KEY not found. Please set it in your .env file or as a secret.")
        st.stop()
except ImportError:
    st.error("python-dotenv is not installed. Please run `pip install python-dotenv`")
    st.stop()


# --- LLM & Scraping Functions ---

def get_company_websites(company_name):
    st.write(f"Asking Gemini for websites related to '{company_name}'...")
    query = f"""
    Please provide the most relevant URLs for the company: "{company_name}".
    Include their official homepage, their 'About Us' page, and their Wikipedia page if they exist.
    List each URL on a new line. Do not add any other text, just the URLs.

    Example for 'Google':
    https://about.google/
    https://en.wikipedia.org/wiki/Google
    """
    try:
        model = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", temperature=0)
        response = model.invoke(query)
        return response.content if hasattr(response, 'content') else str(response)
    except Exception as e:
        st.error(f"Error calling Gemini API: {e}")
        return ""

def is_valid_url(url):
    blacklist = ["linkedin.com", "facebook.com", "instagram.com", "youtube.com", "twitter.com", "x.com"]
    return url.startswith("http") and not any(domain in url.lower() for domain in blacklist)

def scrape_with_bs4(url):
    st.write(f"Attempting to scrape with BS4: {url}")
    try:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
            )
        }
        resp = requests.get(url, headers=headers, timeout=15)
        
        resp.raise_for_status()

        soup = BeautifulSoup(resp.text, 'html.parser')

       
        for element in soup(["script", "style", "nav", "header", "footer", "aside"]):
            element.decompose()

       
        body = soup.find('body')
        if not body:
            st.warning(f"BS4: No <body> tag found on {url}")
            return None

        text = body.get_text(separator=' ', strip=True)
        return text if text else None

    except requests.exceptions.RequestException as e:
        st.warning(f"BS4 request failed for {url}: {e}")
        return None
    except Exception as e:
        st.warning(f"BS4 failed to parse {url}: {e}")
        return None


def scrape_with_playwright(url):
    st.write(f"Falling back to Playwright for: {url}")
    try:
        loader = PlaywrightURLLoader(
            urls=[url],
            remove_selectors=["nav", "header", "footer", "aside", "script", "style"],
            browser_type="chromium"
        )
        docs = loader.load()
        if not docs or not docs[0].page_content.strip():
            st.warning(f"Playwright got no content from {url}")
            return None
        return docs[0].page_content

    except Exception as e:
        st.warning(f"Playwright failed for {url}: {e}")
        return None

def analyze_text(info_text, analysis_type):
    prompts = {
        "summary": "Give a brief summary of the following company in about 2 to 3 lines based on this content:\n",
        "financial": "Based on this content, provide a detailed analysis of the company's financials and fundamental health. Look for revenue, profit, market position, and key business segments. If no specific financial data is present, infer the company's business model and stability:\n"
    }
    
    if not info_text or not info_text.strip():
        return "Not enough information to analyze."

    prompt = prompts[analysis_type] + f"{info_text[:4000]}"

    try:
        model = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest")
        response = model.invoke(prompt)
        return response.content if hasattr(response, 'content') else str(response)
    except Exception as e:
        return f"Error during {analysis_type} analysis: {e}"



st.set_page_config(layout="wide")
st.title("Company Info & Financial Analyzer")
st.write("Enter a company name to fetch its web data, summarize its business, and analyze its financial profile.")

company = st.text_input("Enter the Company Name", placeholder="e.g., Microsoft, Reliance Industries, etc.")

if company:
    website_info = get_company_websites(company)
    
    if not website_info:
        st.error("Could not fetch website information. The API might be down or the company name is too obscure.")
        st.stop()
        
    st.subheader("🤖 Gemini's Response for URLs")
    st.text_area("Raw LLM Output", website_info, height=100)

    urls = re.findall(r'https?://[^\s/$.?#].[^\s]*', website_info)
    valid_urls = list(set([url for url in urls if is_valid_url(url)]))

    if not valid_urls:
        st.error("No valid, non-social media URLs were found in the response.")
        st.stop()

    st.subheader("🔗 Valid URLs to Scrape")
    st.write(valid_urls)

  
    full_text = ""
    with st.spinner("Scraping websites... (Trying BS4 first, then Playwright as fallback)"):
        for url in valid_urls:
            text = scrape_with_bs4(url)
            if not text or len(text.strip()) < 100: 
                text = scrape_with_playwright(url)
            
            if text:
                st.success(f"Successfully scraped content from {url}")
                full_text += f"\n\n--- Content from {url} ---\n{text}"
            else:
                st.error(f"Failed to scrape any content from {url}")

    
    if full_text.strip():
        st.subheader("Company Summary")
        with st.spinner("Generating company summary..."):
            summary = analyze_text(full_text, "summary")
            st.write(summary)

        st.subheader("Financials & Fundamentals")
        with st.spinner("Extracting financials & fundamentals..."):
            finance_info = analyze_text(full_text, "financial")
            st.write(finance_info)
            
        with st.expander("Show all scraped text"):
            st.text_area("Full Scraped Content", full_text, height=300)
    else:
        st.error("No content could be scraped from any of the URLs. Cannot perform analysis.")