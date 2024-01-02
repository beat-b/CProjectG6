from reviews_utils import *
import pandas as pd
from util import local_settings
from openai import OpenAI
import warnings
warnings.filterwarnings('ignore')

# OpenAI API Key
client = OpenAI(api_key=local_settings.OPENAI_API_KEY)

# Load the CSV files into DataFrames
trip_df = pd.read_csv('./data/cleanTripLisbon.csv', index_col='Unnamed: 0')
reviews_df = pd.read_csv('./data/reviews.csv')
copy_customer = pd.read_csv('./data/copy_customer.csv')

# Get last reviewd activity
last_place = reviews_df['Place'].iloc[-1]

# Remove rows with no reviews
trip_bot_df = trip_df[trip_df['ReviewsNo'] != 0]

# Select top 200 rows
trip_bot_df = trip_bot_df.head(200).copy()

# Select activities without any review
trip_bot_df = trip_bot_df.iloc[trip_bot_df[trip_bot_df['Name'] == last_place].index[0]:]

# Create a list of column names containing "Rating"
rating_columns = [col for col in trip_df.columns if 'Rating' in col if col != 'Rating']

# Define messages
messages =  [
    {'role':'system', 'content':'\
        You are ReviewBot, an automated service that creates reviews about places to visit in Lisbon!\
        As ReviewBot, embody the voice of different types of visitors sharing experiences and recommendations.\
        Use informal language.\
        The length of the review must be between 10 and 100 words.'},
]

# Generate reviews
for _, row in trip_bot_df.iterrows():

    # Check if row has 3 or fewer reviews
    if row['ReviewsNo'] <= 3:
        # For loop for the number of reviews
        for i in range(row['ReviewsNo']):
            # Choose random customer
            customer = copy_customer.sample(n=1)
            # Define rating
            rating = get_rating(row, rating_columns)
            # Define prompt
            prompt = row['Name']
            # Get response
            response = get_completion(prompt, client, messages=messages, temperature=1)
            # Create dictionary with new information
            review_dict = {
                'Username': customer['Username'].values[0],
                'Place': row['Name'],
                'OverallRating': row['Rating'],
                'Review': response,
                'Rating': rating
            }
            # Transform dictionary into DataFrame
            review_dict = pd.DataFrame([review_dict])
            # Join DataFrames
            reviews_df = pd.concat([reviews_df, review_dict], ignore_index=True)
            # Count if the number of reviews does not exceed the number of trips for the customer
            copy_customer['ReviewsNo'].iloc[customer.index[0]] += 1
    else:
        # For loop to create 3 reviews
        for i in range(3):
            # Choose random customer
            customer = copy_customer.sample(n=1)
            # Define rating
            rating = get_rating(row, rating_columns)
            # Define prompt
            prompt = row['Name']
            # Get response
            response = get_completion(prompt, client, messages=messages, temperature=1)
            # Create dictionary with new information
            review_dict = {
                'Username': customer['Username'].values[0],
                'Place': row['Name'],
                'OverallRating': row['Rating'],
                'Review': response,
                'Rating': rating
            }
            # Transform dictionary into DataFrame
            review_dict = pd.DataFrame([review_dict])
            # Join DataFrames
            reviews_df = pd.concat([reviews_df, review_dict], ignore_index=True)
            # Count if the number of reviews does not exceed the number of trips for the customer
            copy_customer['ReviewsNo'].iloc[customer.index[0]] += 1
    # Save reviews
    reviews_df.to_csv('./data/reviews.csv', index=False)
    # Save customers
    copy_customer.to_csv('./data/copy_customer.csv', index=False)

# Save final reviews
reviews_df.to_csv('./data/reviews.csv', index=False)
# Save final customers
copy_customer.to_csv('./data/copy_customer.csv', index=False)