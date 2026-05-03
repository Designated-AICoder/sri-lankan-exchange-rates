# Sri Lankan Exchange Rates Scraper 🇱🇰

A robust, modular Python scraper designed to aggregate foreign exchange rates from multiple Sri Lankan banks into a unified dataset.

## 🎯 Goal
To help traders and businesses identify the best exchange rates across different banks in real-time.

## 🚀 Features
- **Modular Scrapers**: Easily extensible architecture for adding new banks.
- **Data Normalization**: Standardizes currency codes (e.g., "US DOLLARS" → "USD") across different bank formats.
- **Persistence**: Saves data to a structured CSV for historical analysis.
- **Dockerized**: Ready for containerized deployment.
- **Quality Assured**: Includes unit tests for scrapers and normalization logic.

## 🛠 Supported Banks
- [x] Nations Trust Bank (NTB)
- [ ] Bank of Ceylon (BOC) - *Coming Soon*
- [ ] Sampath Bank - *Coming Soon*
- [ ] Commercial Bank - *Coming Soon*

## 📦 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Designated-AICoder/sri-lankan-exchange-rates.git
   cd sri-lankan-exchange-rates
   ```

2. **Setup Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

## 🏃 Usage

Run the main scraper:
```bash
python main.py
```
The data will be saved to `data/fxrates_master.csv`.

## 🧪 Testing

Run tests using pytest:
```bash
pytest
```

## 🐳 Docker

Build and run the container:
```bash
docker build -t lk-fx-scraper .
docker run lk-fx-scraper
```