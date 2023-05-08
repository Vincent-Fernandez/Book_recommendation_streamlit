import streamlit as st
from book_recommender import get_book_recommendations

st.set_page_config(
    page_title="Book Recommender App",
    initial_sidebar_state="expanded",
    page_icon="📚"
)

def main():
    st.title("Book Recommender App")

    st.write("""
    Enter the name of a book you like, and get recommendations for similar books!
    """)

    books_user_likes = st.text_input("Enter the name of a book you like:")

    if st.button("Recommend"):
        try:
            result = get_book_recommendations(books_user_likes)

            st.write("Here are 15 recommended books based on your input:")
            for book in result:
                st.write(book)
        except IndexError:
            st.write("Sorry, the book you entered could not be found. Please try another book.")

if __name__ == "__main__":
    main()
