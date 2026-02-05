# 📈 Smart Financial Advisor Pro

Μια σύγχρονη εφαρμογή οικονομικής ανάλυσης που συνδυάζει **AI Agents**, **Live Market Data** και **Τεχνική Ανάλυση**. 
Ιδανική για επενδυτές που θέλουν γρήγορη πρόσβαση σε τιμές μετοχών, νέα της αγοράς και έξυπνες συμβουλές από τεχνητή νοημοσύνη.



## 🚀 Features

* **AI Financial Agent:** Έξυπνος βοηθός βασισμένος στο Llama 3.1 (Groq) που αναζητά νέα και τιμές σε πραγματικό χρόνο.
* **Live Candlestick Charts:** Διαδραστικά γραφήματα τιμών μέσω της βιβλιοθήκης `yfinance`.
* **Technical Analysis:** Αυτόματος υπολογισμός και απεικόνιση Κινητού Μέσου Όρου (MA 20).
* **Key Financial Metrics:** Άμεση προβολή Market Cap, P/E Ratio και Τρέχουσας Τιμής σε ειδικές κάρτες (metrics).
* **Automated Reporting:** Δυνατότητα λήψης (download) της ανάλυσης του Agent σε αρχείο `.txt`.

## 💻 Installation

**1. Κλωνοποίηση του repository:**
```bash
git clone https://github.com/NickDgit/ai-financial-advisor.git
cd ai-financial-advisor 
```

**2. Εγκατάσταση dependencies:
```
pip install -r requirements.txt
```

3. Ρύθμιση .env:
Δημιουργήστε ένα αρχείο .env στον κεντρικό φάκελο και προσθέστε τα κλειδιά σας:

Απόσπασμα κώδικα
```
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
```
4. Τρέξε την εφαρμογή:

```
streamlit run app.py
```
## 📦 Project Structure
```
ai-financial-advisor/
├─ app.py                # Κύριο αρχείο εφαρμογής (Streamlit & Logic)
├─ requirements.txt      # Λίστα με τις απαραίτητες βιβλιοθήκες
├─ .env                  # API Keys (Προσοχή: Μην το ανεβάσετε στο GitHub)
├─ .gitignore            # Αρχεία που εξαιρούνται από το upload
└─ README.md             # Οδηγίες και περιγραφή project
```
## 🛠️ Technologies

* **Python & Streamlit** (UI Framework)
* **LangChain / LangGraph** (Agent Orchestration)
* **Groq Cloud** (LLM Inference - Llama 3.1)
* **YFinance** (Financial Data API)
* **Plotly** (Financial Charting)

## 🌟 Contributing

Καλωσορίζονται προτάσεις και βελτιώσεις!
1. Κάνε fork του repo.
2. Δημιούργησε ένα νέο branch (git checkout -b feature/όνομα).
3. Κάνε commit τις αλλαγές σου (git commit -m "Περιγραφή").
4. Άνοιξε ένα Pull Request.

## 📜 License
MIT License © 2026
