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
- **Historical Tracking**: Automated daily snapshots to track rate trends over time.
- **Developer First**: Clean CSV outputs and Docker support for easy integration into your own apps.

---

## 🛠 Supported Banks
| Bank | Status | Last Checked |
| :--- | :--- | :--- |
| **Nations Trust Bank (NTB)** | ✅ Operational | Daily |
| **Bank of Ceylon (BOC)** | 🚧 In Progress | - |
| **Sampath Bank** | 🚧 In Progress | - |
| **Commercial Bank** | 🚧 In Progress | - |

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

## 🤝 Contributing
We are looking for contributors to help build scrapers for more banks! If you are interested in helping the Sri Lankan trading community, please check out our `scrapers/` folder for implementation examples.

---

## ⚖️ License
This project is open-source and available under the [MIT License](LICENSE).