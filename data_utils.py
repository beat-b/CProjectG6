import pandas as pd
import re
import pandas as pd
import re
import nltk
#Preprocessing: tokenization and lemmatization
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.tokenize import PunktSentenceTokenizer
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
sent_tokenizer = PunktSentenceTokenizer()


#
# Clean Data
#

# Function to extract only the time part
def extract_times(time_range):
    """
    Extracts time information from the given time range string.
    
    -----------------
    Parameters:
     - time_range (str): A string representing the schedule time range.
    -----------------
    Returns:
     - tuple: A tuple containing StartTime, EndTime, LunchStart, and LunchEnd as time objects.
    """
    if time_range == 'Closed until further notice':
        return pd.NaT, pd.NaT, pd.NaT, pd.NaT
    elif pd.notna(time_range):
        # Split the string into two parts
        parts = time_range.split(' - ')
        
        # Check if there are exactly two parts
        if len(parts) == 2:
            return pd.to_datetime(parts[0]).time(), pd.to_datetime(parts[1]).time(), pd.NaT, pd.NaT
        else:
            # Has lunch break
            lunch_time = parts[1].split(', ')
            return pd.to_datetime(parts[0]).time(), pd.to_datetime(parts[2]).time(), pd.to_datetime(lunch_time[0]).time(), pd.to_datetime(lunch_time[1]).time()
    else:
        return pd.NaT, pd.NaT, pd.NaT, pd.NaT
    

def select_types(types: str) -> list:
    """
    Selects words between double quotes in a given string.

    -----------------
    Parameters:
     - types (str): A string containing the activity types.
    -----------------
    Returns:
     - list: A list of words of actitity types.
    """
    # Select words between ""
    pattern = r'"([^"]*)"'

    # Find all words between ""
    types = re.findall(pattern, types)

    # Remove the word "Types"
    types = [word for word in types if word != 'Types']

    return types


def duration_time(duration: str|None) -> tuple:
    """
    Extracts minimum and maximum durations from the given duration string.

    -----------------
    Parameters:
     - duration (str|None): A string representing the duration of a activity.
    -----------------
    Returns:
     - tuple: A tuple containing minimum and maximum durations as Timedelta objects.
    """
    duration = str(duration)
    
    if '-' in duration:
        # Split the duration string into parts using '-'
        parts = duration.split('-')
        # Extract minimum and maximum durations as Timedelta objects
        return pd.to_timedelta(f'{parts[0][-1]} hours'), pd.to_timedelta(f'{parts[1][0]} hours')
    
    elif '<' in duration:
        # Extract the numeric value from the duration string
        pattern = r'\d+'
        duration = int(re.findall(pattern, duration)[0])
        # Return minimum duration as NaT and maximum duration as a Timedelta object
        return pd.NaT, pd.to_timedelta(f'{duration} hours')
    
    elif 'More than' in duration:
        # Extract the numeric value from the duration string
        pattern = r'\d+'
        duration = int(re.findall(pattern, duration)[0])
        # Return minimum duration as a Timedelta object and maximum duration as NaT
        return pd.to_timedelta(f'{duration} hours'), pd.NaT
    
    else:
        # If none of the patterns match, return NaT for both minimum and maximum durations
        return pd.NaT, pd.NaT
    
    
def to_number(number: str) -> int:
    """
    Extracts numerical values from the given string.

    -----------------
    Parameters:
     - number (str): A string containing numerical values.
    -----------------
    Returns:
     - int: Extracted numerical value. Returns 0 if the input is None.
    """
    number = str(number)
    if 'nan' in number:
        return 0
    
    # Use regular expression to extract numerical values
    pattern = r'\d+'
    extracted_numbers = re.findall(pattern, number)
    
    # Convert the list of extracted numbers to a single integer
    extracted_number = int(''.join(extracted_numbers))
    
    return extracted_number


def sentiment_preprocessor(raw_text, lowercase=True, leave_punctuation = False, lemmatization=True, tokenized_output=True, sentence_output=True):
    

    # Convert to lowercase if specified
    if lowercase:
        clean_text = raw_text.lower()
    else:
        clean_text = raw_text
    
    # Remove newline characters
    clean_text = re.sub(r'(\*|\\n|\\r|\\t|</?ul>|</?li>)', ' ', clean_text)

    # Remove punctuation if specified
    if not leave_punctuation:
        clean_text = re.sub(r'(\W)', ' ', clean_text)

    # Remove URLs
    clean_text = re.sub(r'(http\S+|www\S+)', ' ', clean_text)

    # Remove isolated consonants
    clean_text = re.sub(r'\b([^aeiou\s])\b', ' ', clean_text)

    # Tokenize
    clean_text = word_tokenize(clean_text)

    # Lemmatize if specified
    if lemmatization:
        clean_text = [lemmatizer.lemmatize(token, pos='v') for token in clean_text]

    # Re-join if tokenized output is not requested
    if not tokenized_output:
        clean_text = " ".join(clean_text)
        # Remove space before punctuation
        clean_text = re.sub(r'(\s)(?!\w)', '', clean_text)

    # Join sentences into a single string if specified
    if sentence_output and not tokenized_output:
        clean_text = " ".join(sent_tokenize(clean_text))

    return clean_text