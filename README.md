# 🗳️ Indian General Election Results Dashboard (2024)

This project provides an **end-to-end pipeline** to scrape, extract, and visualize the **Indian General Election Results 2024**.  
It combines **web scraping**, **data cleaning**, and **interactive visualization** to give insights into constituency-level outcomes, party performances, and vote share distributions.

---

## 🚀 Features

- **Web Scraping**: Automatically scrape constituency result pages from the Election Commission of India (ECI).  
- **Data Extraction & Cleaning**: Extract candidate names, party affiliation, votes polled, margins, and NOTA counts into structured CSVs.  
- **Interactive Dashboard**:
  - Winner vs Runner-up comparison
  - NOTA inclusion in analysis
  - Party-wise vote share (pie chart)
  - State-wise seat distribution (bar chart)
  - Top candidates by votes polled
  - Filter by **State/UT** or **Political Party**
- **Screenshots & Logs**: Automatically captures and stores raw pages, screenshots, and logs for reproducibility.

---

## 📸 Visuals

> Update these file names once you add actual screenshots in the `screenshots/` folder.

### 1. Dashboard Home  
![Dashboard Overview](screenshots/dashboard_overall.png)

### 2. Constituency-Level Analysis  
![Constituency Example](screenshots/constituency_example.png)

### 3. Party-Wise Vote Share  
![Party Vote Share](screenshots/party_share.png)

### 4. State-Wise Seat Distribution  
![State Wise Seats](screenshots/state_seats.png)

### 5. Raw Scraped ECI Page  
![Raw ECI Page](screenshots/raw_eci_page.png)

---

## 📂 Project Structure


```


├── app.py # Streamlit dashboard for visualization  
├── extract.py # Extracts data (candidate, votes, party, NOTA, etc.)  
├── scrapper.py # Scrapes results pages & saves text + screenshots  
├── results.csv # Cleaned structured election dataset  
├── logs/ # Logs from scraper runs  
├── saved_pages/ # Raw constituency result pages (text dumps)  
├── screenshots/ # Result screenshots + dashboard visuals  
└── README.md # Project documentation

```

---

## 🛠️ Installation

### Requirements
- Python 3.9+  
- Google Chrome + ChromeDriver (for Selenium)  
- Dependencies (install via pip):

```bash
pip install -r requirements.txt

```

_(If you don’t have a `requirements.txt` yet, create one with:)_

```bash
pip freeze > requirements.txt

```

----------

## ▶️ Usage

1.  **Scrape ECI Results**
    
    ```bash
    python scrapper.py
    
    ```
    
    -   Saves raw constituency pages in `saved_pages/`
        
    -   Captures screenshots in `screenshots/`
        
    -   Logs activity in `logs/`
        
2.  **Extract Clean Data**
    
    ```bash
    python extract.py
    
    ```
    
    -   Parses raw data into `results.csv`
        
3.  **Launch Dashboard**
    
    ```bash
    streamlit run app.py
    
    ```
    
    -   Opens an interactive dashboard in your browser
        
    -   Filter by state/party, compare margins, analyze NOTA, etc.
        

----------

## 🤝 Contributing

Contributions are welcome!  
You can help by:

-   Adding more visualizations (maps, historical comparisons, etc.)
    
-   Improving data cleaning and error handling
    
-   Extending scraper for assembly/bye-elections
    

To contribute:

1.  Fork the repo
    
2.  Create a feature branch (`git checkout -b feature-name`)
    
3.  Commit changes (`git commit -m "Added new feature"`)
    
4.  Push to your fork and open a PR
    

----------

## 👨‍💻 Authors & Acknowledgments

-   Developed by **Dinesh aka 学習者 aka cln35h**
    
-   Thanks to the [Election Commission of India](https://eci.gov.in) for making results public.
    
-   Inspired by open-source election data projects.
    

----------

## 📜 License

This project is licensed under the **MIT License** – free to use, modify, and distribute with attribution.

----------

## 📌 Project Status

✅ Active – continuing to add more visualizations and state-level comparisons.

```

---

👉 This version is **clean, professional, and GitHub-ready**.  

Do you want me to also **auto-generate a `requirements.txt`** for you based on `scrapper.py`, `extract.py`, and `app.py` (so the README’s `pip install -r requirements.txt` works right away)?

```