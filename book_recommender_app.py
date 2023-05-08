import streamlit as st
from book_recommender import get_book_recommendations

st.set_page_config(
    page_title="Book Recommender App",
    initial_sidebar_state="expanded",
    page_icon="📚"
)

def main(df):
    st.title("Book Recommender App")

    st.write("""
    Enter the name of a book you like, and get recommendations for similar books!
    """)

    # Prepare a list of book names for the suggestions
    book_names = df['book_name'].tolist()
    books_user_likes = st.multiselect(
        "Select a book you like:",
        options=book_names,
        max_selections=1)

    if len(books_user_likes) > 1:
        st.warning("Please select only one book.")
    elif books_user_likes:
        try:
            result, _ = get_book_recommendations(books_user_likes[0])

            st.write("Here are 15 recommended books based on your input:")
            for book in result:
                st.write(book)
        except IndexError:
            st.write("Sorry, the book you selected could not be found. Please try another book.")

if __name__ == "__main__":
    # Get the initial recommendations and df
    _, initial_df = get_book_recommendations()
    main(initial_df)
