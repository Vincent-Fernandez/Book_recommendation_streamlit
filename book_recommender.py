# Import libraries
import os
import re
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def get_book_recommendations(books_user_likes=None):
    # Define the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Load the CSV file
    csv_path = os.path.join(current_dir, "Goodreads_best1500books.csv")
    df = pd.read_csv(csv_path)

    # Rename the first column to 'index'
    df.rename(columns={df.columns[0]: 'index'}, inplace=True)

    # Data preparation/cleaning

    # Remove text between parentheses in 'book_name' column
    df['book_name'] = df['book_name'].apply(lambda x: re.sub(r'\([^)]*\)', '', x))

    # Replace commas in 'no_of_raters' column
    df["no_of_raters"] = df["no_of_raters"].str.replace(",", "")

    # Replace certain strings in 'avg_rating' column with NaN values and drop rows with NaN values
    df = df[~df['avg_rating'].isin(['it', 'liked', 'really'])].dropna(subset=['avg_rating'])

    # Convert 'avg_rating' and 'no_of_raters' columns to float
    df["avg_rating"] = df["avg_rating"].astype(float)
    df["no_of_raters"] = df["no_of_raters"].astype(float)

    # Define list of features to use for recommendation
    features = ['author_name', 'book_genre', 'year_published']

    # Fill any missing values in these columns with an empty string
    for feature in features:
        df[feature] = df[feature].fillna('')

    # Define function to combine feature values for each row into a single string
    def combined_features(row):
        return str(row['author_name']) + " " + str(row['book_genre']) + " " + str(row['year_published'])

    # Apply the function to each row to create a new column 'combined_features'
    df["combined_features"] = df.apply(combined_features, axis=1)

    # Use CountVectorizer to convert 'combined_features' column into a matrix of token counts
    cv = CountVectorizer()
    count_matrix = cv.fit_transform(df["combined_features"])

    # Use cosine similarity to calculate similarity scores between all books based on their 'combined_features' token counts
    cosine_sim = cosine_similarity(count_matrix)

    # Define a function to get the index of a book by its name
    def get_index_from_book_name(book_name):
        return df[df.book_name == book_name]["index"].values[0]

    if books_user_likes:
        # Get the index of the book the user likes
        books_index = get_index_from_book_name(books_user_likes)

        # Get the similarity scores between the book the user likes and all other books
        similar_books = list(enumerate(cosine_sim[books_index]))

        # Sort the list of books by their similarity score (highest to lowest), and exclude the book the user likes
        sorted_similar_books = sorted(similar_books, key=lambda x: x[1], reverse=True)[1:16]

        # Define a function to get the name of a book by its index
        def get_book_name_from_index(index):
            return df[df.index == index]["book_name"].values[0]

        # Create a list of the names of the 15 most similar books
        result = []
        for book in sorted_similar_books:
            result.append(get_book_name_from_index(book[0]))

        # Return the list of recommended books and the DataFrame
        return result, df
    else:
        # If no book is provided, just return the DataFrame
        return None, df
