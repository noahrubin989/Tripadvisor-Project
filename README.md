# Tripadvisor Review Sentiment Analyser

This project is a **Tripadvisor Review Sentiment Analyser**, designed to provide sentiment analysis for hotel reviews using **Azure AI Language** and the **Tripadvisor API**. The app is built with **Streamlit**, offering a user-friendly UI to explore reviews and their associated AI generated sentiments.

## Features

- **Search Locations**:
  - Enter a location name (e.g. Sydney) to search for hotels on Tripadvisor.
  - View a list of matching locations and select one for further exploration.

- **Fetch Reviews**:
  - Retrieve customer reviews for the selected hotel, including review text, publication date, and review URLs.

- **Sentiment Analysis**:
  - Analyse the sentiment of each review (Positive, Negative, Mixed) using Azure Text Analytics.
  - Display sentiment insights alongside the reviews in the Streamlit app.

- **Interactive User Interface**:
  - Built with Streamlit for an intuitive, interactive experience.
  - Dynamically display results with metadata and links for deeper exploration.

## Installation

### Prerequisites

1. **Python 3.7+**
2. **Azure Subscription**
   - Obtain an Azure Key and Endpoint for the Text Analytics API.
3. **Tripadvisor API Key**
   - Register and generate an API key for accessing Tripadvisor data.
4. **Environment Variables**
   - Use a `.env` file to store sensitive keys:
     ```
     AZURE_KEY=<your_azure_key>
     AZURE_ENDPOINT=<your_azure_endpoint>
     TRIPADVISOR_KEY=<your_tripadvisor_key>
     ```

## Key Technologies

- **Streamlit**: Provides the interactive user interface.
- **Azure AI Language**: Performs sentiment analysis using the Text Analytics API.
- **Tripadvisor API**: Fetches location data and customer reviews.
- **dotenv**: Manages environment variables for sensitive data.

