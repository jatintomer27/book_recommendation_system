## Ecommerce Recommendation system

- Recommender system are of three types
  
1) Content based 

    - In this it will try to match the content and try to give recommendation
  
2) Collaborative filtering

    - Here we more focus on customer side.
    - Like user 1 has purchased some item 1 and item 2
    - Then if user 2 have purchased item 1 then we also recommend him item 2.
    - Here we use clustering.

3) Hybrid

   - It is the mixture of both the types.


- In this project we will use Collaborative filtering technique.
- Here we will use one ecommerce book dataset.


## Steps:

1) Create a github repo and clone it.
2) Create a conda virtual environment.
3) Activate the environments.
4) Create the requirements.txt and list all requirements in that.

###### 

- For the Collaborative filtering we have to convert this data to the pivot table

##### Wha is pivot table ?

- A Pivot Table is a tool (mostly used in Excel / Google Sheets / Pandas) that helps you summarize and analyze data quickly.

- In the pivot table we apply the clustering algo to make clusters and make the recommendations.

- And this is how we do the recommendation in the Collaborative filtering


## All things we have done in EDA and FE

#### Book Table

- From Book table only select the large size image as all other are not necessary
- Check for the unique values in year column of Book table
- Remove the records that have irrelevant year names from Book table
- Remove the future dates and date where value is zero in year column from Book table
- Convert the string value in year column into integer in year column from Book table.
- Drop the null values from the table.
  
#### User Table

- Replace the users age with mean of age whose age is below 5 or above 100 or NaN.
- Convert the age as integer 

#### Ratings Table

- Select only those books from rating table that are available in Book table based on ISBN
- Group the users to count how many no of books each user has rated.
- Filter the users who has read/rated greater than 200 books

#### Overall

- Merge the Filtered Ratings and Book table basd on the ISBN and ceate ratings_with_books.
- Fetch which book is rated how many times and stored in number_ratings table
- Merge number_ratings and ratings_with_books based on title and create final ratings table.
- Filter only those books who has rated more that 50 times.
- Make the pivot table from the filtered final rating book table.
- Make the csr matrix from the pivot table and train on NearestNeighbors algorithm.
- Store the model, book_names, final_ratings, pivot_table as pkl for future use for predict.
- Predict the recommended book for the given book.
- It gives ids of the book it is suggesting as stored in pivot table ( Ids of book based on pivot table).
- Now we can find the book other details from the final_rating table we have stored.