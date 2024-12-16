import pandas as pd
import streamlit as st
import requests
import json
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient
from dotenv import load_dotenv
import os
from typing import List, Tuple

# Load environment variables
load_dotenv()

azure_key = os.getenv('AZURE_KEY')
azure_endpoint = os.getenv('AZURE_ENDPOINT')
tripadvisor_key = os.getenv('TRIPADVISOR_KEY')

# Initialise Azure Text Analytics Client
credential = AzureKeyCredential(azure_key)
ai_client = TextAnalyticsClient(endpoint=azure_endpoint, credential=credential)

def search_locations(search_query: str, language: str = 'en') -> List[Tuple[str, str]]:
    """
    Search for locations (hotels) on Tripadvisor by name.
    
    Parameters
    ----------
    search_query : str
        The search query (use a city name e.g. Sydney.
    language : str, optional
        Language code for the search results. Defaults to 'en'.
        
    Returns
    -------
    List[Tuple[str, str]]
        A list of tuples where each tuple consists of:
        (location_id, location_name).
    """
    url = f"https://api.content.tripadvisor.com/api/v1/location/search?searchQuery={search_query}&category=hotels&language={language}&key={tripadvisor_key}"
    response = requests.get(url)
    if response.status_code != 200:
        return []
    data = json.loads(response.text).get('data', [])
    return [(record.get('location_id'), record.get('name')) for record in data]

def fetch_reviews(location_id: str, language: str = 'en') -> List[Tuple[str, str, str]]:
    """
    Fetch reviews for a given Tripadvisor location.
    
    Parameters
    ----------
    location_id : str
        The Tripadvisor location ID.
    language : str, optional
        Language code for the reviews. Defaults to 'en'.
        
    Returns
    -------
    List[Tuple[str, str, str]]
        A list of tuples where each tuple consists of:
        (review_text, published_date, review_url).
    """
    url = f"https://api.content.tripadvisor.com/api/v1/location/{location_id}/reviews?language={language}&key={tripadvisor_key}"
    response = requests.get(url)
    if response.status_code != 200:
        return []
    data = json.loads(response.text).get('data', [])
    return [(record.get('text'), record.get('published_date'), record.get('url')) for record in data]

def analyse_sentiment(reviews: List[Tuple[str, str, str]]) -> List[Tuple[str, str, str, str]]:
    """
    Perform sentiment analysis on a list of reviews using Azure Text Analytics.
    
    Parameters
    ----------
    reviews : List[Tuple[str, str, str]]
        A list of tuples where each tuple consists of:
        (review_text, published_date, review_url).
        
    Returns
    -------
    List[Tuple[str, str, str, str]]
        A list of tuples where each tuple consists of:
        (review_text, published_date, review_url, sentiment).
    """
    sentiments = []
    for text, date, url in reviews:
        analysis = ai_client.analyze_sentiment(documents=[text], model_version='latest')[0]
        sentiments.append((text, pd.to_datetime(date).strftime("%B %d, %Y"), url, analysis.sentiment))
    return sentiments

# Streamlit UI
st.title("Tripadvisor Review Sentiment Analyser")

# Step 1: Search for a location
search_query = st.text_input("Enter a location name (e.g., Sydney):")
if search_query:
    locations = search_locations(search_query)
    if locations:
        location_name = st.selectbox("Select a location:", [name for _, name in locations])
        location_id = [id for id, name in locations if name == location_name][0]

        # Step 2: Fetch reviews for the selected location
        reviews = fetch_reviews(location_id)
        if reviews:
            st.subheader(f"Reviews for {location_name}")
            sentiments = analyse_sentiment(reviews)

            # Display reviews with sentiment
            for text, date, url, sentiment in sentiments:
                st.write(f"**Date:** {date}")
                st.write(f"**Sentiment:** {sentiment.capitalize()}")
                st.write(f"**Review:** {text}")
                st.write(f"[Read more]({url})")
                st.write("---")
        else:
            st.warning("No reviews found for the selected location.")
    else:
        st.warning("No locations found. Try a different query.")
