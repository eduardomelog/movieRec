## Movie Recommendation Model

This project features a movie recommendation model that uses user-based collaborative filtering. The idea is to suggest movies to a specific user based on the preferences of others with similar tastes.

### How the Model Works

1. **User-Based Collaborative Filtering**:
   - The model looks at the ratings given by different users to various movies and tries to find users who have similar tastes.
   - We calculate how similar users are using Pearson correlation.
   - Once we know who’s similar, we recommend movies that these similar users have enjoyed but that the target user hasn’t seen yet.

2. **User-Movie Matrix**:
   - We create a matrix that maps users to the movies they've rated.
   - This matrix is crucial for figuring out which users are similar and what recommendations to make.

3. **The Recommendation Process**:
   - For a given user, we identify other users with similar rating patterns.
   - We then recommend the top-rated movies from these similar users, focusing on movies the target user hasn’t watched yet.

### Dataset

- The model is built using the MovieLens 100k dataset, which contains 100,000 ratings from users on various movies.

### Step-by-Step

1. **Loading Data**: We start by loading the movie and rating data.
2. **Building the Matrix**: Next, we create a matrix showing each user’s ratings for each movie.
3. **Calculating Similarities**: We then calculate similarities between users based on their ratings.
4. **Making Recommendations**: Finally, we generate personalized movie recommendations based on those similarities.
