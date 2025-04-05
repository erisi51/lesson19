import streamlit as st
import pandas as pd
import plotly.express as px



st.header("Displaying dataframes")

df = pd.DataFrame({
    'Name' : ['Alice' , 'Michael' , 'Tony'],
    'Age' : [24 , 156 ,8],
    "City" : ["Prishtina" , "New york" , "Paris"]
})

st.dataframe(df)


books_df = pd.read_csv('Lesson18/test.csv')

st.title('Bestselling book analysis')
st.write('This app analyzes the Amazon top selling books')



st.sidebar.header("Add new book data")
with st.sidebar.form("book_form"):
    new_name = st.text_input("Book name")
    new_author = st.text_input("Author name")
    new_user_rating = st.slider("User rating" , 0.5 , 5.0 , 0.0 , 0.1)
    new_review = st.number_input('Review' , min_value=0 ,step=1)
    new_price = st.number_input('Price' , min_value=0 , step=1)
    new_year = st.number_input('Year' , min_value = 2009, max_value=2022, step=1)
    new_Genre = st.selectbox("Genre" , books_df['Genre'].unique())
    submit_button = st.form_submit_button(label="Add Book")

    if submit_button:
        new_data={
            'Name': new_name,
            'Author': new_author,
            'User Rating': new_user_rating,
            'Previews': new_review,
            'Price': new_price,
            'Year': new_year,
            'Genre': new_Genre,
        }

books_df = pd.concat([pd.DataFrame(new_data, index=[0]), books_df] , ignore_index=True)
books_df.to_csv( 'bestsellers_with_categories_2022_03_27.csv', index=False)
st.sidebar.success("New book Added Successfully!")

st.sidebar.header("Filter options")
selected_author = st.sidebar.selectbox("Select author", ['All'] +list(books_df['Author'].unique()))
selected_Year = st.sidebar.selectbox("Select Year", ['All'] + list(books_df['Year'].unique()))
selected_genre = st.sidebar.selectbox("Select Genre", ['All'] + list(books_df['Genre'].unique()))
min_rating = st.sidebar.slider("Minimum User Rating", 0.0, 5.0, 0.0, 0.1)
max_price = st.sidebar.slider("Maximum Price", 0, books_df['Price'].max(), books_df['Price'].max())

st.subheader('Summary')
total_books = books_df.shape[0]
unique_titles = books_df['Name'].nunique()
average_rating = books_df['User Rating'].mean()
average_price = books_df['Price'].mean()


col1 , col2, col3 , col4 = st.columns(4)

col1.metric("Total books" , total_books)
col2.metric("Unique titles" , unique_titles)
col3.metric("Average rating" , f"{average_rating:.2f}")
col4.metric("Average price" , f"{average_price:.2f}")


st.subheader("Preview")
st.write(books_df.head())


col1,col2 = st.columns(2)
with col1:
    st.subheader("Top 10 book titles")
    top_titles = books_df['Name'].value_counts().head(10)
    st.bar_chart(top_titles)
with col2:
    st.subheader("Top 10 Authors")
    top_authors = books_df['Author'].value_counts().head(10)
    st.bar_chart( top_authors)

st.subheader("Genre Distribution")
fig = px.pie(books_df, names='Genre', title='Most liked Genre (2009-2022)', color='Genre', color_discrete_sequence=px.colors.sequential.Plasma)


st.plotly_chart(fig)


st.subheader("Number of fiction vs nonfiction books over the years")
size = books_df.groupby(['Year' , 'Genre']).size().reset_index(name='Count')
fig = px.bar(size, x='Year', y='Count' , color='Genre' ,title='Number of fiction vs non-fiction books from 2009-2022',
             color_discrete_sequence=px.colors.sequential.Plasma, barmode='group')
st.plotly_chart(fig)



st.header('Top 15 Authors by counts of books over the years')
top_authors = books_df['Author'].value_counts().head(15).reset_index()
top_authors.columns = ['Author', 'Count']
fig = px.bar(top_authors, x ='Count' , y ='Author' , orientation='h',
             title ='Top 15 author by counts of book published',
             labels={'Count': 'Counts of book published' , 'Author':'Author'},
             color='Count' , color_continuous_scale=px.colors.sequential.Plasma)
st.plotly_chart(fig)

st.subheader("Filter data by genre")
genre_filter = st.selectbox('Select Genre' , books_df['Genre'].unique())
filter_df = books_df[books_df['Genre'] == genre_filter]
st.write(filter_df)

