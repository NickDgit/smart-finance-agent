import os
import yfinance as yf
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool

# 1. Φόρτωση κλειδιών
load_dotenv()

# --- ΟΡΙΣΜΟΣ ΕΡΓΑΛΕΙΩΝ ---

@tool
def get_stock_price(ticker: str):
    """Χρησιμοποίησε αυτό το εργαλείο για να βρεις την τρέχουσα τιμή μιας μετοχής.
    Δώσε το σύμβολο της μετοχής (π.χ. AAPL, NVDA, TSLA)."""
    stock = yf.Ticker(ticker)
    price = stock.fast_info['last_price']
    return f"Η τρέχουσα τιμή της μετοχής {ticker} είναι {price:.2f}$"

@tool
def save_to_csv(content: str):
    """Χρησιμοποίησε αυτό το εργαλείο για να αποθηκεύσεις την έρευνα ή τα δεδομένα σε ένα αρχείο CSV."""
    filename = "market_research.csv"
    with open(filename, "w", encoding="utf-8-sig") as f:
        f.write(content)
    return f"Το αρχείο {filename} δημιουργήθηκε επιτυχώς!"

# -----------------------------

# 2. Ρύθμιση AI και Εργαλείων
llm = ChatGroq(model_name="llama-3.1-8b-instant", temperature=0)
search_tool = TavilySearchResults(max_results=3)

# Προσθέτουμε όλα τα εργαλεία στη λίστα
tools = [search_tool, get_stock_price, save_to_csv]

# 3. Δημιουργία Agent
agent_executor = create_react_agent(llm, tools)

# 4. Η Εντολή
query = (
    "Βρες την τιμή της μετοχής της NVIDIA (NVDA). "
    "Μετά βρες τις τελευταίες 2 ειδήσεις για την εταιρεία. "
    "Τέλος, αποθήκευσε την τιμή και τις ειδήσεις σε ένα αρχείο CSV."
)

print("--- Ο Agent ξεκινά την εργασία ---")
try:
    result = agent_executor.invoke({"messages": [("human", query)]})
    print("\nΟλοκληρώθηκε!")
    print(result["messages"][-1].content)
except Exception as e:
    print(f"Σφάλμα: {e}")