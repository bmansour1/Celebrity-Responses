import requests
import pandas as pd
import sqlalchemy as db
import random
import openai

def check_response(response):
        # Check the status of the request
    if response.status_code == 200:
        # Good
        return
    else:
        # Print an error message if the request was unsuccessful
        print(f"Error: {response.status_code}")
        print(response.text)

def pick_category():
    list_of_categories = ['business','crime','domestic','education','entertainment','environment','food','health','lifestyle','other','politics','science','sports','technology','top','tourism','world']
    for cat in list_of_categories: print(cat)
    category = input('Pick a category from this list of categories: ')
    if category not in list_of_categories:
        print(f"The category '{category}' is not listed. Try Again")
        return pick_category()
    else:
        print(f"You choose the category '{category}'")
        return category

def get_news(category):
    # Replace 'YOUR_API_KEY' with your actual API key from NewsData.io
    API_KEY = 'pub_4732238994f3ac13b52e07481e490b40f357d'
    BASE_URL = 'https://newsdata.io/api/1/news'

    # Set up the parameters for the request
    params = {
        'apikey': API_KEY, #API KEY
        'language': 'en',   # Language preference
        'category': category,  # Category preference
    }

    # Make the GET request to the API
    response = requests.get(BASE_URL, params=params)
    check_response(response)
    data = response.json()
    data_len = len(data['results'])
    index = random.randint(1, data_len-1)
    news = data['results'][index]['description']
    print(f"The news pertaining to the category {category} is:")
    print(news)
    return news

def pick_celebrity():
    celeb = input('Enter Celebrity You Want to Hear From Regarding This News: ')
    return celeb

def get_response(category, news, celeb):
    #HERE Prompt ChatGPT with the following prompt:
    prompt = f"Given the category, {category}, and the news about the category, {news}, reply to this news as if you are {celeb}, make sure to outline their personality in your repsonse, if you don't know {celeb}, reply I don't know who {celeb} is."
    #HERE Print the ChatGPT output 
    again = input("Type 'again' to hear from another celebrity: ")
    if (again == 'again'):
        main()
    else:
        print("Thanks for playing!")

def main():
    category = pick_category()
    news = get_news(category)
    celeb = pick_celebrity() 
    get_response(category, news, celeb)

main()
