# 🇱🇰 Sri Lankan FX Rate Aggregator

> **Empowering traders and individuals with real-time transparency across the Sri Lankan banking landscape.**

---

## 📖 The Problem
For years, identifying the best exchange rate in Sri Lanka required manually visiting dozen of different bank websites, each with its own confusing table structure, hidden fees, and varying update frequencies. For traders and businesses moving significant capital, a 0.50 LKR difference per dollar can mean thousands in lost or gained revenue.

## 🎯 The Mission
This project aims to be the **Single Source of Truth** for Sri Lankan Foreign Exchange (FX) rates. We programmatically scrape, normalize, and aggregate data from all major local banks into a single, clean dataset.

**Our goal is to help you answer one question instantly:** *"Which bank should I use to transfer my money today?"*

---

## 🚀 Key Features
- **Multi-Bank Intelligence**: Unified logic to scrape diverse bank structures.
- **Data Normalization**: We handle the mess. Whether a bank calls it "US DOLLAR" or "USD", it's standardized here.
- **Automated Database**: Runs daily via GitHub Actions; no manual execution required.
- **Data History**: View the entire history of rates in the `data/fxrates_master.csv` file.
- **Developer First**: Clean CSV outputs and Docker support for easy integration into your own apps.

---

## 📊 Data Access
The "database" for this project is stored as a flat-file CSV:
📍 **[data/fxrates_master.csv](file:///Users/rithikahettiarachchi/Documents/Projects/sriLankaFXRates/sri-lankan-exchange-rates/data/fxrates_master.csv)**

This file is automatically updated every morning at **09:30 AM SL Time**. You can pull this repo at any time to get the latest historical data.

---

## 🛠 Supported Banks
| Bank | Status | Last Checked |
| :--- | :--- | :--- |
| **Nations Trust Bank (NTB)** | ✅ Operational | Daily |
| **Bank of Ceylon (BOC)** | ✅ Operational | Daily |
| **Sampath Bank** | ✅ Operational | Daily |
| **Commercial Bank** | ✅ Operational | Daily |

---

## 🚦 Getting Started (Quick Start)

Follow these steps to run the aggregator on your local machine.

### 1. Prerequisites
Ensure you have **Python 3.10+** installed.

### 2. Installation
```bash
# Clone the repository
git clone https://github.com/Designated-AICoder/sri-lankan-exchange-rates.git
cd sri-lankan-exchange-rates

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Run the Scraper
```bash
python main.py
```
**Output:** You will see a success message, and the data will be saved to `data/fxrates_master.csv`.

---

## 🧪 Development & Testing

We take data accuracy seriously. To run the validation suite:
```bash
pytest
```

---

## 🤝 Contributing & Feature Development
We believe in open transparency and community-driven development. Beyond adding new bank scrapers, we welcome **Merge Requests (MRs)** and **Issues** for any features you believe would make this tool more useful for the Sri Lankan community:

- **Analysis Tools**: Functions to identify the "Best Rate of the Day."
- **API Development**: Exposing the data via a lightweight FastAPI or Flask wrapper.
- **Frontend Dashboards**: Building a visual comparison table for traders.
- **Notification Systems**: Alerting users via Telegram/WhatsApp when rates hit a certain threshold.

If you have an idea that can help Sri Lankans manage their money better, open an issue or submit a feature development request!

---

## ⚖️ License
This project is open-source and available under the [MIT License](LICENSE).