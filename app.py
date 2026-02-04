import pandas as pd
import streamlit as st
import os
import yfinance as yf
import plotly.graph_objects as go
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool

load_dotenv()


# --- ΕΡΓΑΛΕΙΑ ---
@tool
def get_stock_price(ticker: str):
    """Βρίσκει την τρέχουσα τιμή μιας μετοχής."""
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1d")
        if not hist.empty:
            price = hist['Close'].iloc[-1]
            return f"Η τιμή της {ticker} είναι {price:.2f}$"
        return "Δεν βρέθηκε τιμή."
    except Exception as e:
        return f"Σφάλμα κατά την ανάκτηση τιμής: {e}"


@tool
def search_news(query: str):
    """Ψάχνει ειδήσεις στο internet."""
    search = TavilySearchResults(max_results=3)
    return search.invoke(query)


# --- UI SETTINGS ---
st.set_page_config(page_title="AI Financial Agent", layout="wide")
st.title("📈 Smart Financial Advisor Pro")

# Sidebar
with st.sidebar:
    st.header("Ρυθμίσεις")
    selected_ticker = st.text_input("Σύμβολο Μετοχής για Γράφημα:", value="NVDA").upper()
    days = st.slider("Ημέρες ιστορικού:", 5, 60, 30)

# --- FETCH DATA ---
# Χρησιμοποιούμε try/except εδώ για να μην κρασάρει όλη η σελίδα αν η Yahoo έχει θέμα
try:
    stock_info = yf.Ticker(selected_ticker)
    data = yf.download(selected_ticker, period="3mo", interval="1d")
    info = stock_info.info
except:
    info = {}
    data = pd.DataFrame()

# --- MAIN LAYOUT ---
col1, col2 = st.columns([1, 1])

with col1:
    user_input = st.text_input("Ρώτησε τον Agent:", placeholder="π.χ. Τι νέα υπάρχουν για την NVDA;")

    if 'agent_response' not in st.session_state:
        st.session_state.agent_response = ""

    if st.button("Ανάλυση"):
        if user_input:
            with st.spinner("Ο Agent ερευνά..."):
                llm = ChatGroq(model_name="llama-3.1-8b-instant", temperature=0)
                tools = [get_stock_price, search_news]
                agent = create_react_agent(llm, tools)
                result = agent.invoke({"messages": [("human", user_input)]})
                st.session_state.agent_response = result["messages"][-1].content
                st.info(st.session_state.agent_response)
        else:
            st.warning("Παρακαλώ εισάγετε μια ερώτηση.")

    if st.session_state.agent_response:
        report_text = f"Financial Report for {selected_ticker}\n" + "=" * 30 + f"\n\nAnalysis:\n{st.session_state.agent_response}"
        st.download_button(
            label="📄 Λήψη Αναφοράς (txt)",
            data=report_text,
            file_name=f"{selected_ticker}_report.txt",
            mime="text/plain"
        )

with col2:
    st.subheader(f"Στατιστικά: {selected_ticker}")
    m1, m2, m3 = st.columns(3)

    # Ασφαλής ανάκτηση δεδομένων (Metrics)
    price = info.get('currentPrice') or info.get('regularMarketPrice', 'N/A')
    mcap = info.get('marketCap')
    if isinstance(mcap, (int, float)):
        mcap_str = f"{mcap / 1e9:.1f}B"
    else:
        mcap_str = "N/A"
    pe = info.get('trailingPE', 'N/A')

    m1.metric("Τιμή", f"{price}$" if price != 'N/A' else "N/A")
    m2.metric("Market Cap", mcap_str)
    m3.metric("P/E Ratio", pe)

    # Το Γράφημα
    if not data.empty:
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)

        data['MA20'] = data['Close'].rolling(window=20).mean()
        fig = go.Figure()
        fig.add_trace(go.Candlestick(x=data.index, open=data['Open'], high=data['High'],
                                     low=data['Low'], close=data['Close'], name="Τιμή"))
        fig.add_trace(go.Scatter(x=data.index, y=data['MA20'], line=dict(color='orange', width=1.5), name="MA 20"))

        fig.update_layout(template="plotly_dark", height=400, xaxis_rangeslider_visible=False,
                          margin=dict(l=10, r=10, t=30, b=10))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("Δεν βρέθηκαν δεδομένα για το γράφημα. Βεβαιωθείτε ότι το σύμβολο είναι σωστό.")