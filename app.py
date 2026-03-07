"""
Streamlit App for the Book Recommendation system.
"""

import os
import numpy as np
import pandas as pd
from pathlib import Path
import streamlit as st  
import subprocess

from book_recommendation_system import logger
from book_recommendation_system.config.configuration import ConfigurationManager
from book_recommendation_system.utils.common import load_bin

class Recommendation:

    def __init__(self, config = ConfigurationManager()):
        try:
            self.config = config.get_model_recommendation_config()
        except Exception as e:
            logger.exception(
                f"Exception occured while Initializing the recommendation "
                f"object: {e}"
            )
            raise 

    def train_engine(self):
        subprocess.run(["python", "main.py"], check=True)

    def fetch_book_with_images(self, suggestions):
        try:
            book_pivot = load_bin(Path(self.config.book_pivot_serialized_objects))
            final_books_data = pd.read_csv(self.config.final_books_path)
            book_names, images = [], []
            for book_id in suggestions:
                book_name = book_pivot.index[book_id]
                index = np.where(final_books_data['title'] == book_name)
                image = final_books_data.iloc[index[0]]['image_url'].tolist()[0]
                book_names.append(book_name)
                images.append(image)
            return book_names, images
        except Exception as e:
            logger.exception(
                f"Exception occured while fetching the book names with images"
                f" :{e}"
            )
            raise
            

    def recommend_book(self, book_name):
        try:
            model = load_bin(Path(self.config.trained_model_path))
            book_pivot = load_bin(Path(self.config.book_pivot_serialized_objects))
            book_id = np.where(book_pivot.index == book_name)[0][0]
            distance, suggestion = model.kneighbors(
                book_pivot.iloc[book_id,:].values.reshape(1,-1),
                n_neighbors=6 
            )
            return self.fetch_book_with_images(suggestion[0])
        except Exception as e:
            logger.exception(
                f"Exception occured while executing the recommend_book: {e}"
            )
            raise

    def recommendation(self, book_name):
        try:
            recommended_books, books_images = self.recommend_book(book_name)
            # logger.info(f">>>>>>>>>>>>>>>>>>>>>>>>>> {recommended_books = }")
            # logger.info(f">>>>>>>>>>>>>>>>>>>>>>>>>> {books_images = }")
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                st.text(recommended_books[1])
                st.image(books_images[1])
            with col2:
                st.text(recommended_books[2])
                st.image(books_images[2])

            with col3:
                st.text(recommended_books[3])
                st.image(books_images[3])
            with col4:
                st.text(recommended_books[4])
                st.image(books_images[4])
            with col5:
                st.text(recommended_books[5])
                st.image(books_images[5])
        except Exception as e:
            logger.exception(
                f"Exception occured during the recommendation: {e}"
            )
            raise


if __name__ == '__main__':

    kaggle_username = os.getenv("KAGGLE_USERNAME")
    kaggle_key = os.getenv("KAGGLE_KEY")

    # Page configuration
    st.set_page_config(
        page_title="📚 Book Recommender",
        page_icon="📚",
        layout="wide"
    )

    # Custom CSS
    st.markdown("""
    <style>
    .main-title{
        font-size:40px;
        font-weight:bold;
        color:#FF4B4B;
    }
    .subtitle{
        font-size:18px;
        color:gray;
    }
    </style>
    """, unsafe_allow_html=True)


    # Header Section
    st.markdown('<p class="main-title">📚 Book Recommendation System</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Discover books similar to the one you love using Collaborative Filtering.</p>', unsafe_allow_html=True)

    st.divider()

    # Sidebar
    with st.sidebar:
        st.title("⚙️ Controls")
        st.info("Train the recommender system and get book suggestions.")

        train_btn = st.button("🚀 Train Model")

        st.markdown("---")
        st.write("Made with ❤️ using Streamlit")


    # Main App
    obj = Recommendation()
    book_names = load_bin(Path(obj.config.book_name_serialized_objects))

    col1, col2 = st.columns([2,1])

    with col1:
        selected_book = st.selectbox(
            "📖 Type or select a book",
            book_names
        )

    with col2:
        st.image(
            "https://cdn-icons-png.flaticon.com/512/29/29302.png",
            width=120
        )


    # Training
    if train_btn:
        if kaggle_username and kaggle_key:
            with st.spinner("Training recommender system... ⏳"):
                obj.train_engine()
            st.success("✅ Model trained successfully!")
        else:
            st.error("❌ Kaggle credentials not found.")
            st.info(
                "This application requires Kaggle API credentials to download the dataset."
            )
            st.code(
                "docker run -e KAGGLE_USERNAME=<your_username> "
                "-e KAGGLE_KEY=<your_key> -p 8080:8080 <image_name>",
                language="bash"
            )
            st.warning(
                "Restart the container with the above environment variables."
            )


    # Recommendation Button
    if st.button("✨ Show Recommendations"):
        with st.spinner("Finding similar books for you..."):
            st.subheader("📚 Recommended Books")
            recommendations = obj.recommendation(selected_book)

        