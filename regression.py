import pandas as pd
import numpy as np
import nltk
from data_utils import sentiment_preprocessor
from nltk.tokenize import PunktSentenceTokenizer
from nltk.stem import WordNetLemmatizer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
import pickle

# Preprocessing: tokenization and lemmatization
lemmatizer = WordNetLemmatizer()
sent_tokenizer = PunktSentenceTokenizer()

# Sentiment Analysis with VADER
nltk.download('vader_lexicon')

# Load data
reviews_df = pd.read_csv('./data/reviews.csv')
reviews_df['CleanReview'] = reviews_df['Review'].apply(lambda review: sentiment_preprocessor(
    review, lowercase=False,
    leave_punctuation=True,
    lemmatization=False,
    tokenized_output=False))

# Analyze polarity and add results to the dataframe
vader = SentimentIntensityAnalyzer()
reviews_df['Vader'] = reviews_df['CleanReview'].apply(lambda x: vader.polarity_scores(x))
reviews_df['Negative_vader'] = reviews_df['Vader'].apply(lambda x: x['neg'])
reviews_df['Neutral_vader'] = reviews_df['Vader'].apply(lambda x: x['neu'])
reviews_df['Positive_vader'] = reviews_df['Vader'].apply(lambda x: x['pos'])
reviews_df['Compound_vader'] = reviews_df['Vader'].apply(lambda x: x['compound'])
reviews_df.drop('Vader', axis=1, inplace=True)

# Name of the columns related to Vader
vader_cols = ['Negative_vader', 'Neutral_vader', 'Positive_vader', 'Compound_vader']

# Define features and target variable
X = reviews_df[['Review'] + vader_cols]
y = reviews_df['Rating']

# Split the data into training, validation, and testing sets
X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.3, random_state=42)
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)

# Create a ColumnTransformer to handle different feature types
preprocessor = ColumnTransformer(
    transformers=[
        ('text', TfidfVectorizer(), 'Review'),
        ('numeric', 'passthrough', ['Negative_vader', 'Neutral_vader', 'Positive_vader', 'Compound_vader'])
    ])

# Combine the preprocessor with a regressor (RandomForestRegressor in this case)
model = RandomForestRegressor(n_estimators=100, random_state=42)

# Create a pipeline
pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('model', model)
])

# Fit the model on the training data
pipeline.fit(X_train, y_train)

# Make predictions on the validation set
y_val_pred = pipeline.predict(X_val)

# Evaluate the model on the validation set
rmse_val = np.sqrt(mean_squared_error(y_val, y_val_pred))
print(f'Root Mean Squared Error on Validation Set: {rmse_val}')

# Make predictions on the test set
y_test_pred = pipeline.predict(X_test)

# Evaluate the model on the test set
rmse_test = np.sqrt(mean_squared_error(y_test, y_test_pred))
print(f'Root Mean Squared Error on Test Set: {rmse_test}')

# RegressorWrapper for the RandomForestRegressor model
class RegressorWrapper:
    def __init__(self, model, text_column):
        self.model = model
        self.text_column = text_column

    def predict(self, raw_review: str) -> float:
        # Preprocess the review and extract relevant features
        clean_review = sentiment_preprocessor(
            raw_review, lowercase=False, leave_punctuation=True, lemmatization=False, tokenized_output=False
        )
        review_df = pd.DataFrame({
            'Review': clean_review,
            'Negative_vader': [vader.polarity_scores(clean_review)['neg']],
            'Neutral_vader': [vader.polarity_scores(clean_review)['neu']],
            'Positive_vader': [vader.polarity_scores(clean_review)['pos']],
            'Compound_vader': [vader.polarity_scores(clean_review)['compound']]
        })
        
        # Make predictions using the model
        result = self.model.predict(review_df)
        return result[0]

    def prediction_needs(self, verbosity=True):
        return f"You only need to provide the raw review text to get a prediction."

# Create the RegressorWrapper
rating_regressor = RegressorWrapper(model=pipeline, text_column='Review')

path = "./models/rating_rf_model.pkl"

with open(path, 'wb') as file:
    pickle.dump(rating_regressor, file)

print(f"✅ File {path} was saved successfully")