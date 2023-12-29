import pandas as pd

from data_utils import *

# Load the CSV file into a DataFrame
trip_df = pd.read_csv('./data/LisbonTrip_Final.csv')

# Extract a value from the 'Link' column to create a new 'Ranking' column
trip_df['Ranking'] = trip_df['Link'].str.split('.').str[0]

# Convert the 'Ranking' column to numeric values
trip_df['Ranking'] = pd.to_numeric(trip_df['Ranking'], errors='coerce')

# Drop unnecessary columns
trip_df.drop(['web-scraper-order', 'web-scraper-start-url', 'Link'], axis=1, inplace=True)

# Set the 'Ranking' column as the index
trip_df.set_index('Ranking', inplace=True)

# Sort the DataFrame based on the index
trip_df.sort_index(inplace=True)

# Apply the function to create four new columns: 'StartTime', 'EndTime', 'LunchStart', and 'LunchEnd'
trip_df[['StartTime', 'EndTime', 'LunchStart', 'LunchEnd']] = trip_df['Schedule'].apply(extract_times).apply(pd.Series)

# Drop rows of closed activities
trip_df = trip_df[trip_df['Schedule'] != 'Closed until further notice']

# Change rankings
trip_df.reset_index(drop=True, inplace=True)

# Drop the original 'Schedule' column
trip_df.drop('Schedule', axis=1, inplace=True)

# Apply the function to extract types from the 'Types' column
trip_df['Types'] = trip_df['Types'].apply(select_types)

# Apply the duration_time function to create two new columns: 'DurationMin' and 'DurationMax'
trip_df[['DurationMin', 'DurationMax']] = trip_df['Duration'].apply(duration_time).tolist()

# Apply the to_number function to the convert column type to numeric
trip_df['ReviewsNo'] = trip_df['ReviewsNo'].apply(to_number)
trip_df['ExcellentRating'] = trip_df['ExcellentRating'].apply(to_number)
trip_df['VeryGoodRating'] = trip_df['VeryGoodRating'].apply(to_number)
trip_df['AverageRating'] = trip_df['AverageRating'].apply(to_number)
trip_df['PoorRating'] = trip_df['PoorRating'].apply(to_number)
trip_df['TerribleRating'] = trip_df['TerribleRating'].apply(to_number)

# Export csv
trip_df.to_csv('./data/cleanTripLisbon.csv', index=True)
