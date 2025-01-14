import requests
import json
import time
import boto3
from datetime import datetime
from decimal import Decimal 

API_KEY = 'ENTER YOUR API KEY'

YELP_API_URL = 'https://api.yelp.com/v3/businesses/search'

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('yelp-restaurants')

def convert_to_decimal(data):
    if isinstance(data, list):
        return [convert_to_decimal(item) for item in data]
    elif isinstance(data, dict):
        return {k: convert_to_decimal(v) for k, v in data.items()}
    elif isinstance(data, float):
        return Decimal(str(data))
    else:
        return data

def scrape_yelp(cuisine, location='Manhattan', limit=50, price_filter=None):
    headers = {
        'Authorization': f'Bearer {API_KEY}'
    }

    restaurants = []
    offset = 0

    while True:
        params = {
            'term': f'{cuisine} restaurants',
            'location': location,
            'limit': limit,
            'offset': offset,
        }

        if price_filter:
            params['price'] = price_filter

        response = requests.get(YELP_API_URL, headers=headers, params=params)
        if response.status_code != 200:
            print(f"Error: {response.status_code}, {response.text}")
            break

        data = response.json()
        businesses = data.get('businesses', [])
        if not businesses:
            break

        for business in businesses:
            restaurant = {
                'BusinessID': business.get('id'),
                'Name': business.get('name'),
                'Address': ', '.join(business.get('location', {}).get('display_address', [])),
                'Coordinates': convert_to_decimal(business.get('coordinates', {})),
                'NumberOfReviews': Decimal(str(business.get('review_count', 0))),
                'Rating': Decimal(str(business.get('rating', 0))),
                'ZipCode': business.get('location', {}).get('zip_code'),
                'insertedAtTimestamp': datetime.now().isoformat(),
                'Cuisine': cuisine,
            }
            restaurants.append(restaurant)
            try:
                table.put_item(Item=restaurant)
            except:
                print("Failed")

        print(f"Scraped {len(businesses)} {cuisine} restaurants (offset={offset}, price={price_filter})")
        offset += limit
        if offset >= 240:
            break 

        time.sleep(1)

    return restaurants

if __name__ == "__main__":
    cuisines = ['Chinese', 'Italian', 'Mexican', 'Japanese', 'Indian']
    for cuisine in cuisines:
        print(f"Scraping {cuisine} restaurants=...")
        scrape_yelp(cuisine)