from reviews_utils import *
import pandas as pd
from util import local_settings
from openai import OpenAI

# OpenAI API Key
client = OpenAI(api_key=local_settings.OPENAI_API_KEY)

# Load the CSV files into DataFrames
trip_df = pd.read_csv('./data/cleanTripLisbon.csv', index_col='Unnamed: 0')
customer_df = pd.read_csv('./data/customer_data.csv')

# Create reviews_df
reviews_df = pd.DataFrame(columns=['Username', 'Place', 'OverallRating', 'Review', 'Rating'])

# Remove rows with no reviews
trip_bot_df = trip_df[trip_df['ReviewsNo'] != 0]

# Select top 200 rows
trip_bot_df = trip_bot_df.head(200).copy()

# Create a list of column names containing "Rating"
rating_columns = [col for col in trip_df.columns if 'Rating' in col if col != 'Rating']

# Create dataframe to check if number of reviews does not exceed number of trips
copy_customer = customer_df[['Username', 'Planned Trips']].copy()
copy_customer['ReviewsNo'] = 0

# Define messages
messages =  [
    {'role':'system', 'content':'\
        You are ReviewBot, an automated service that creates reviews about places to visit in Lisbon!\
        As ReviewBot, embody the voice of different types of visitors sharing experiences and recommendations.\
        Use informal language.\
        The length of the review must be between 10 and 100 words.'},
]

# Generate reviews
trip_bot_df.apply(lambda row: generate_reviews(row, reviews_df, copy_customer, rating_columns, messages, client), axis = 1)

# Save reviews
reviews_df.to_csv('./data/reviews.csv', index=False)