# sentiment_analysis.py

import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import time
from urllib.parse import urlparse, parse_qs
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import numpy as np
import re
import emoji
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter

class FlipkartReviewAnalyzer:
    def __init__(self, chrome_driver_path):
        self.setup_selenium(chrome_driver_path)
        self.initialize_nltk()
        self.sia = SentimentIntensityAnalyzer()
        
    def setup_selenium(self, chrome_driver_path):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        service = Service(chrome_driver_path)
        self.driver = webdriver.Chrome(service=service, options=chrome_options)

    def initialize_nltk(self):
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
        try:
            nltk.data.find('sentiment/vader_lexicon.zip')
        except LookupError:
            nltk.download('vader_lexicon')
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('stopwords')

    def get_review_link(self, product_url):
        try:
            if "flipkart.com" not in product_url or "pid=" not in product_url:
                return "Invalid Flipkart product URL"
            
            parsed_url = urlparse(product_url)
            query_params = parse_qs(parsed_url.query)
            product_id = query_params.get("pid", [None])[0]
            lid = query_params.get("lid", [None])[0]

            if not product_id or not lid:
                return "Invalid Flipkart URL: Missing required parameters"

            base_url = "https://www.flipkart.com/"
            remaining_url = product_url[len(base_url):]
            product_name = remaining_url.split("/p")[0]
            
            return f"https://www.flipkart.com/{product_name}/product-reviews/{product_id}?pid={product_id}&lid={lid}&marketplace=FLIPKART"
        except Exception as e:
            return f"Error processing URL: {str(e)}"

    def scrape_reviews(self, review_url, num_pages=2):
        customer_names, review_title, ratings, comments = [], [], [], []

        for i in range(1, num_pages + 1):
            url = f"{review_url}&page={i}"
            self.driver.get(url)
            time.sleep(5)

            read_more_buttons = self.driver.find_elements(By.XPATH, "//span[text()='READ MORE']")
            for button in read_more_buttons:
                try:
                    button.click()
                    time.sleep(1)
                except:
                    continue

            soup = BeautifulSoup(self.driver.page_source, 'lxml')
            
            names = soup.find_all('p', class_='zJ1ZGa ZDi3w2')
            customer_names.extend([name.get_text() for name in names])

            titles = soup.find_all('p', class_='qW2QI1')
            review_title.extend([t.get_text() for t in titles])

            rats = soup.find_all('div', class_='MKiFS6 ojKpP6')
            ratings.extend([r.get_text() if r.get_text() else '0' for r in rats])

            cmts = soup.find_all('div', class_='G4PxIA')
            comments.extend([c.get_text(strip=True) for c in cmts])

        return self.create_dataframe(customer_names, review_title, ratings, comments)

    def create_dataframe(self, customer_names, review_title, ratings, comments):
        min_length = min(len(customer_names), len(review_title), len(ratings), len(comments))
        data = {
            'Customer Name': customer_names[:min_length],
            'Review Title': review_title[:min_length],
            'Rating': ratings[:min_length],
            'Comment': comments[:min_length]
        }
        df = pd.DataFrame(data)
        # Convert Rating to numeric immediately
        df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')
        return df

    def analyze_sentiment(self, df):
        # Convert text columns
        df['Comment_Processed'] = df['Comment'].apply(self.convert_emojis_to_text)
        df['Title_Processed'] = df['Review Title'].fillna('').apply(self.convert_emojis_to_text)
        
        # Combine processed text
        df['Combined_Text'] = df['Title_Processed'] + ' ' + df['Comment_Processed']
        df['Combined_Text'] = df['Combined_Text'].apply(self.preprocess_text)
        
        # Calculate sentiment scores
        df['Sentiment_Score'] = df['Combined_Text'].apply(
            lambda x: self.sia.polarity_scores(x)['compound']
        )
        
        # Classify sentiment
        df['Sentiment'] = df['Sentiment_Score'].apply(self.classify_sentiment)
        
        # Clean up temporary columns
        df = df.drop(['Comment_Processed', 'Title_Processed'], axis=1)
        
        return df

    @staticmethod
    def convert_emojis_to_text(text):
        if pd.isna(text):
            return ""
        return emoji.demojize(str(text))

    @staticmethod
    def preprocess_text(text):
        if pd.isna(text):
            return ""
        text = str(text)
        # Remove special characters but keep emoji descriptions
        text = re.sub(r'[^\w\s:_]', ' ', text)
        return text.lower().strip()

    @staticmethod
    def classify_sentiment(score):
        if score >= 0.05:
            return 'Positive'
        elif score <= -0.05:
            return 'Negative'
        else:
            return 'Neutral'

    def get_top_words(self, text_series, n=10):
        all_text = ' '.join(text_series.fillna(''))
        tokens = word_tokenize(all_text.lower())
        stop_words = set(stopwords.words('english'))
        filtered_tokens = [
            word for word in tokens 
            if word.isalpha() and word not in stop_words and len(word) > 2
        ]
        return Counter(filtered_tokens).most_common(n)

    def cleanup(self):
        self.driver.quit()