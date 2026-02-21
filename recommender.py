import pandas as pd
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# 1. Load and Clean Data
movies = pd.read_csv('movies.csv')
movies = movies[['id', 'title', 'overview', 'genre']]

# Fill missing values to avoid errors during string concatenation
movies['overview'] = movies['overview'].fillna('')
movies['genre'] = movies['genre'].fillna('')

# 2. Feature Engineering
movies['tag'] = movies['overview'] + " " + movies['genre']
new_df = movies.drop(columns=['overview', 'genre'])

# 3. Vectorization (Bag of Words)
cv = CountVectorizer(max_features=10000, stop_words='english')
vector = cv.fit_transform(new_df['tag'].values.astype('U')).toarray()

# 4. Calculate Similarity Matrix
similarity = cosine_similarity(vector)

# 5. Recommendation Function
def recommend(movie_title):
    try:
        # Get the index of the movie that matches the title
        index = new_df[new_df['title'] == movie_title].index[0]
        
        # Calculate distances and sort (top 5 excluding the movie itself)
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        
        print(f"Recommendations for '{movie_title}':")
        for i in distances[1:6]:
            print(f"- {new_df.iloc[i[0]].title}")
            
    except IndexError:
        print("Movie not found in the database.")

# 6. Save models for your Web App (Streamlit/Flask)
pickle.dump(new_df, open('movies_list.pkl', 'wb'))
pickle.dump(similarity, open('similarity.pkl', 'wb'))

