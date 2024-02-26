# Web Scraper and Analyzer 🌐🤖🛠

This Python script is designed to scrape data from the Ikman.lk website, specifically targeting CT-100 motorbike listings in Sri Lanka. The script extracts key information such as location, price, manufacturing year, and mileage from individual listings.

## ✨ Features

- **Scraping:** Utilizes BeautifulSoup and requests to scrape CT-100 motorbike data from Ikman.lk pages.
- **Metadata Extraction:** Extracts relevant metadata including location, price, manufacturing year, and mileage for each CT-100 listing.
- **Data Analysis:** Computes the average selling prices for CT-100 motorbikes based on their locations.
- **Email Notification:** Sends an email containing a summary of the latest CT-100 selling data and average prices by location.

## 🚀 Usage

1. Clone the repository.
2. Install the required dependencies (`beautifulsoup4`, `requests`, `pandas`).
3. Run the script to collect data and perform analysis.

Make sure to configure the script with your email credentials for the notification feature.

## Getting Started

### Prerequisites

- Python 3.x
- Install dependencies:

  ```bash
  pip install beautifulsoup4 requests pandas
