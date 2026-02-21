# 🎬 Movie Recommender 

A full-stack Machine Learning application that suggests movies based on content similarity. This project utilizes **Natural Language Processing (NLP)** and **Cosine Similarity** to provide an interactive recommendation experience.



## 🚀 Overview
This system analyzes movie metadata—specifically plot summaries and genres—to recommend films with similar themes. It demonstrates a complete ML pipeline from **Data Engineering** in Python to a **Frontend Web Application** with real-time API integration.

## 🛠️ Technical Stack
* **Language:** Python 3.11
* **ML Libraries:** Scikit-learn (CountVectorizer, Cosine Similarity), Pandas, NumPy
* **Web Framework:** Streamlit
* **API:** TMDB (The Movie Database)
* **Data Persistence:** Pickle

## 🧬 How It Works
* **Preprocessing:** Merged `overview` and `genre` columns into a unified "tags" column to create a rich textual profile for each film.
* **Vectorization:** Converted text tags into a 10,000-dimensional vector space using the **Bag of Words** model (`CountVectorizer`).
* **Similarity Engine:** Calculated the **Cosine Similarity** between movie vectors to generate a pre-computed similarity matrix.
* **Frontend Logic:** When a user selects a movie, the system identifies the top 5 closest vectors and fetches high-resolution posters dynamically via the **TMDB API**.



## ⚡ Engineering Challenges Solved
* **API Stability:** Resolved `ConnectionResetError: [WinError 10054]` by implementing `requests.Session()` and **HTTP Retry Logic**, ensuring stable communication with external servers.
* **Performance Optimization:** Integrated **Streamlit Caching** (`@st.cache_data`) and controlled delays (`time.sleep`) to prevent rate-limiting and improve response times.
* **UI/UX Reliability:** Developed a fallback mechanism to display placeholder images when the external API fails to return a poster.

## 📂 Project Structure
```plaintext
Movie Recommender
  ├── app.py                # Main Streamlit application
  ├── recommender.py        # ML model training and pickle generation
  ├── movies.csv            # Dataset containing movie metadata
  ├── movies_list.pkl       # Serialized movie dataframe
  ├── similarity.pkl        # Serialized similarity matrix
