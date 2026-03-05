# Flipkart Review Scraper & Sentiment Analysis

A web-based tool that scrapes customer reviews from Flipkart product pages and performs sentiment analysis to classify reviews as **Positive, Neutral, or Negative**.

The system automatically collects reviews using **Selenium**, processes them using **Natural Language Processing (NLP)**, and visualizes insights through interactive charts.

This project demonstrates practical implementation of **Web Scraping, Sentiment Analysis, and Data Visualization** in Python.



# Features

* Scrape product reviews from Flipkart
* Perform sentiment analysis using **NLTK VADER**
* Visualize results using **Plotly charts**
* Analyze rating distribution
* Display positive / neutral / negative review breakdown
* Export analyzed data as CSV
* Simple and interactive **Streamlit interface**


## How It Works

1. User enters a Flipkart product URL
2. Selenium automatically opens the review page
3. The system extracts:

   * Review text
   * Ratings
   * Reviewer information
4. Text is cleaned and processed
5. **VADER Sentiment Analyzer** calculates sentiment scores
6. Results are displayed using interactive charts and tables

---

# Tech Stack

* **Python**
* **Streamlit**
* **Selenium**
* **BeautifulSoup**
* **NLTK**
* **Plotly**
* **Pandas**


# Installation

pip install -r requirements.txt


# Running the Application

Start the Streamlit server:

streamlit run app.py

The application will open in your browser:

http://localhost:8501


# Output

The system provides:

* Total number of reviews analyzed
* Average rating
* Positive / Neutral / Negative sentiment percentage
* Sentiment distribution chart
* Rating histogram
* Review data table
* Downloadable CSV dataset


# Important Notes

# ChromeDriver Compatibility

ChromeDriver must match your installed Chrome browser version.

Check Chrome version:

chrome://settings/help

Download the matching ChromeDriver from:

https://chromedriver.chromium.org/downloads

Replace the existing chromedriver if required.

# Flipkart Website Structure

Flipkart frequently updates its HTML structure and class names.

If scraping stops working:

1. Inspect the Flipkart review page using **Developer Tools (F12)**
2. Identify the updated class names
3. Update selectors in:

sentiment_analysis.py

# Anti-Scraping Limitations

Flipkart may implement anti-bot protection.

To reduce blocking:

* Avoid scraping too many pages
* Limit request frequency
* Use small page counts

# Troubleshooting

**Problem:** Selenium browser not opening
**Solution:** Update ChromeDriver to match your Chrome version.

**Problem:** Reviews not appearing
**Solution:** Flipkart class names may have changed.

**Problem:** Streamlit not installed

pip install streamlit

# Future Improvements

* Word cloud visualization of reviews
* Deep learning sentiment models (BERT, RoBERTa)
* Multi-platform review scraping
* Automated analytics dashboard
* Cloud deployment


# Author

**Sumit Jaishigurung**

B.Tech – Computer Science & Engineering
NIT Mizoram

Email: [sumitjiashigurung@gmail.com](mailto:sumitjiashigurung@gmail.com)

LinkedIn:
https://www.linkedin.com/in/sumit-jiashigurung-a271a02b5

 If you found this project useful, consider giving it a star.
