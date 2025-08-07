from flask import Flask, render_template, request
import pickle
import numpy as np

# Load data
popular_df = pickle.load(open('ppl_books.pkl', 'rb'))
pt = pickle.load(open('PT.pkl', 'rb'))
books = pickle.load(open('BK.pkl', 'rb'))
similarity = pickle.load(open('SC.pkl', 'rb'))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           book_name=list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           votes=list(popular_df['num_ratings'].values),
                           rating=list(popular_df['avg_rating'].values),
                           available = list(popular_df['Availability'].values)
                           )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books', methods=['POST'])
def recommend_books():
    user_input = request.form.get('user_input')

    # Case-insensitive partial match for book titles
    matching_books = final_ratings[final_ratings['Book-Title'].str.contains(user_input, case=False, na=False)]

    if matching_books.empty:
        return render_template('recommend.html', data=None, message=f"No books found containing the word: '{user_input}'")

    # Group by Book-Title, Book-Author, and Image, then calculate average rating
    grouped = matching_books.groupby(['Book-Title', 'Book-Author', 'Image-URL-M']).agg({'Book-Rating': 'mean'}).reset_index()

    # Sort by average rating in descending order
    sorted_books = grouped.sort_values(by='Book-Rating', ascending=False)

    # Prepare the final result
    data = []
    for _, row in sorted_books.iterrows():
        item = [row['Book-Title'], row['Book-Author'], row['Image-URL-M'], round(row['Book-Rating'], 2)]
        data.append(item)

    return render_template('recommend.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
