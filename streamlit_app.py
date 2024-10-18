import streamlit as st

def main():
    # Set up the main page
    st.title("Simple Streamlit App with Sidebar")
    st.write("Welcome to the main content area!")

    # Set up the sidebar
    st.sidebar.header("Sidebar Options")
    
    # Add some elements to the sidebar
    name = st.sidebar.text_input("Enter your name:")
    age = st.sidebar.slider("Select your age:", 1, 100, 25)
    favorite_color = st.sidebar.selectbox(
        "Choose your favorite color:",
        ["Red", "Green", "Blue", "Yellow", "Purple"]
    )

    # Display the user's inputs in the main content area
    if name:
        st.write(f"Hello, {name}!")
    st.write(f"You are {age} years old.")
    st.write(f"Your favorite color is {favorite_color}.")

if __name__ == "__main__":
    main()