# app.py

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sentiment_analysis import FlipkartReviewAnalyzer
import os

class FlipkartReviewApp:
    def __init__(self):
        st.set_page_config(page_title="Flipkart Review Analyzer", layout="wide")
        self.chrome_driver_path = os.path.join(os.getcwd(), "chromedriver.exe")
        self.initialize_app()

    def initialize_app(self):
        st.title("🛍️ Flipkart Review Analyzer")
        self.setup_sidebar()
        self.main_content()

    def setup_sidebar(self):
        with st.sidebar:
            st.title("⚙️ Settings")
            self.num_pages = st.slider("Pages to analyze", 1, 10, 2)
            st.info("More pages = more reviews but slower analysis")

    def main_content(self):
        st.markdown("### Enter Product URL")
        self.url = st.text_input(
            "Flipkart Product URL",
            placeholder="https://www.flipkart.com/product..."
        )

        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔍 Analyze Reviews", use_container_width=True):
                self.run_analysis()
        with col2:
            if st.button("🗑️ Clear Results", use_container_width=True):
                st.experimental_rerun()

    def run_analysis(self):
        if not self.url:
            st.warning("Please enter a Flipkart product URL")
            return

        try:
            with st.spinner("Analyzing reviews..."):
                analyzer = FlipkartReviewAnalyzer(self.chrome_driver_path)
                review_url = analyzer.get_review_link(self.url)
                
                if "Invalid" in review_url:
                    st.error(review_url)
                    return

                progress_bar = st.progress(0)
                
                # Scraping
                progress_bar.progress(25)
                df = analyzer.scrape_reviews(review_url, self.num_pages)
                
                # Analysis
                progress_bar.progress(50)
                df = analyzer.analyze_sentiment(df)
                
                # Results
                progress_bar.progress(75)
                self.display_results(df)
                
                analyzer.cleanup()
                progress_bar.progress(100)
                st.success("Analysis complete!")

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

    def display_results(self, df):
        st.markdown("## 📊 Analysis Results")

        # Metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Reviews", len(df))
        with col2:
            avg_rating = df['Rating'].mean()
            st.metric("Average Rating", f"{avg_rating:.1f}⭐")
        with col3:
            positive_pct = (df['Sentiment'] == 'Positive').mean() * 100
            st.metric("Positive Reviews", f"{positive_pct:.1f}%")
        with col4:
            negative_pct = (df['Sentiment'] == 'Negative').mean() * 100
            st.metric("Negative Reviews", f"{negative_pct:.1f}%")

        # Sentiment Distribution
        st.markdown("### Sentiment Distribution")
        sentiment_counts = df['Sentiment'].value_counts()
        fig_sentiment = px.pie(
            values=sentiment_counts.values,
            names=sentiment_counts.index,
            title="Review Sentiments",
            color=sentiment_counts.index,
            color_discrete_map={
                'Positive': '#00CC96',
                'Neutral': '#636EFA',
                'Negative': '#EF553B'
            }
        )
        st.plotly_chart(fig_sentiment, use_container_width=True)

        # Rating Distribution
        st.markdown("### Rating Distribution")
        fig_rating = px.histogram(
            df,
            x='Rating',
            color='Sentiment',
            nbins=5,
            title="Ratings by Sentiment",
            color_discrete_map={
                'Positive': '#00CC96',
                'Neutral': '#636EFA',
                'Negative': '#EF553B'
            }
        )
        st.plotly_chart(fig_rating, use_container_width=True)

        # Review Table
        st.markdown("### 📝 Review Details")
        display_df = df[['Customer Name', 'Rating', 'Sentiment', 'Comment']].copy()
        display_df['Rating'] = display_df['Rating'].fillna(0).astype(int)
        st.dataframe(display_df, use_container_width=True)

        # Download button
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download Results",
            data=csv,
            file_name="review_analysis.csv",
            mime="text/csv"
        )

def main():
    FlipkartReviewApp()

if __name__ == "__main__":
    main()