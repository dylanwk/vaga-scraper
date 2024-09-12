import re, random
from utils.constants import attraction_resturant_keywords as buzz_words



def get_attractions(restaurants, attractions, buzz_words=buzz_words):
    """
    Returns a list of attractions based on the given restaurants and attractions,
    filtered by a list of buzz words.
    Args:
        restaurants (str): A string containing a list of restaurants.
        attractions (str): A string containing a list of attractions.
        buzz_words (list): A list of buzz words used for filtering.
    Returns:
        list: A list of matched attractions, including both restaurants and attractions.
    """
    
    ## Initialize two arrays: resturants, and attractions
    restaurant_items = re.split(r"\n+", restaurants)[1:]
    attraction_items = re.split(r"\n+", attractions)[1:]

    ## Array of most significant resturants/attractions
    matched_items = []

    ## Scan both arrays for values that include buzzwords
    for item in restaurant_items:
        for word in buzz_words:
            if word in item.lower() and len(matched_items) < 2:
                matched_items.append(item)
                restaurant_items.remove(item)
                break

    for item in attraction_items:
        for word in buzz_words:
            if word in item.lower() and len(matched_items) < 5:
                matched_items.append(item)
                attraction_items.remove(item)

                break

    ## if 5 priority resturants/attractions DO NOT exsist, fill with random attractions
    if len(matched_items) < 5:
        remaining_items = restaurant_items + attraction_items
        random.shuffle(remaining_items)

        while len(matched_items) < 5 and remaining_items:
            matched_items.append(remaining_items.pop() + "\n")

    return matched_items
