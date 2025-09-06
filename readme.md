# CarPriceAnalyzer

**A project to collect, store, and analyze car prices in Tunisia compared to the EU and USA.**  

---

## Project Overview

CarPriceAnalyzer is a data-driven project that scrapes car prices from Tunisian websites (like Automobile.tn, Automax.tn) and compares them with prices in richer countries. The goal is to understand price differences, trends, and market dynamics, given the relatively low income levels in Tunisia.

---

## Features

- **Web Scraping:** Collect car data (name, price, specifications) using Scrapy.  
- **Database Storage:** Store scraped data in MongoDB with collections for cars, sellers, and manufacturers.  
- **Price Analysis:** Compare car prices across Tunisia, EU, and USA.  
- **Extensible:** Can be expanded for visualizations, predictive models, and dashboards.  

---

## Folder Structure

CarPriceAnalyzer/
├── scrapers/ # Scrapy spiders and pipelines
│ ├── automobiletn.py
│ ├── pipelines.py
│ └── settings.py
├── data/ # CSVs or other processed datasets
├── scripts/ # Analysis scripts, e.g., comparison or visualization
├── README.md
└── scrapy.cfg

---

## Installation

1. Clone the repository:
```bash
git clone https://github.com/ElAbdoulyMed/car-price-analyzer.git
cd CarPriceAnalyzer

2. Clone the repository:
```bash
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows

