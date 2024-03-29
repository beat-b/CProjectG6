import random
import pandas as pd


def get_random_rating(random_item):
    if random_item == 'ExcellentRating':
        return round(random.uniform(4.1, 5), 1)
    elif random_item == 'VeryGoodRating':
        return round(random.uniform(3.1, 4), 1)
    elif random_item == 'AverageRating':
        return round(random.uniform(2.1, 3), 1)
    elif random_item == 'PoorRating':
        return round(random.uniform(1.1, 2), 1)
    else:
        return round(random.uniform(0, 1), 1)
    
def get_rating(row, rating_columns):
    # Generate weights based on quantities of ratings
    weights = [row[col] / row[rating_columns].sum() for col in rating_columns]
    
    # Use random.choices to pick a random item based on weights
    random_item = random.choices(rating_columns, weights=weights, k=1)[0]

    return get_random_rating(random_item)

def get_completion(prompt, client, model="gpt-3.5-turbo", temperature=1, messages=None):
    if not messages:
        messages = [{"role": "user", "content": prompt}]
    else:
        messages.append({"role": "user", "content": prompt})

    completion = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
    )

    return completion.choices[0].message.content
