import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

def fetch_product_data(url):
    """Fetch product title and price from the given URL."""
    
    # Request headers to mimic a real browser
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }

    try:
        # Make a GET request to fetch the raw HTML content
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)

        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(response.content, 'lxml')

        # Extract the product title
        product_title_tag = soup.find('span', {'id': 'productTitle'})
        product_title = product_title_tag.get_text().strip() if product_title_tag else 'N/A'

        # Extract the price
        price_tag = soup.find('span', {'class': 'a-price-whole'})
        price = price_tag.get_text().strip() if price_tag else 'N/A'

        return product_title, price

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None, None

def save_to_csv(data, file_path='products.csv'):
    """Save product data to a CSV file."""
    df = pd.DataFrame(data)

    # Check if the file already exists
    if not os.path.exists(file_path):
        # If file doesn't exist, create a new CSV and add the header
        df.to_csv(file_path, mode='w', index=False)
        print(f"Data saved to {file_path}.")
    else:
        # If file exists, append the data without writing the header again
        df.to_csv(file_path, mode='a', header=False, index=False)
        print(f"Data appended to {file_path}.")

def main():
    # URL of the Amazon product page
    url = "https://www.amazon.in/Apple-iPhone-16-128-GB/dp/B0DGJH8RYG/ref=sr_1_1_sspa?crid=I7OINS8GQINE&keywords=iphone+16&qid=1729149091&sprefix=iphone+16%2Caps%2C311&sr=8-1-spons&psc=1"
    
    # Fetch product data
    product_title, price = fetch_product_data(url)

    if product_title and price:
        # Prepare the data to store in CSV
        product_data = {
            'Product Title': [product_title],
            'Price': [price]
        }
        save_to_csv(product_data)

if __name__ == "__main__":
    main()
