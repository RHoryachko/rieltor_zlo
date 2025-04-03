import os
import logging
import schedule
import time
import requests
import json

from dotenv import load_dotenv

from parser import process_listings, print_listing_info
from database import (
    connect_db,
    create_table_if_not_exists,
    save_listing_to_db,
    mark_listing_as_sent
)
from bot import send_listing_to_chats_sync

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

load_dotenv()
CHAT_IDS = [chat_id.strip() for chat_id in os.getenv('TELEGRAM_CHAT_IDS', '').split(',') if chat_id.strip()]


def process_new_listings():
    """Process new listings and send notifications."""
    try:
        listings_data = get_listings_data()
        
        listings = process_listings(listings_data)
        
        for listing in listings:
            print_listing_info(listing)
            
            sent = save_listing_to_db(listing['id'])
            if sent == 0:
                send_listing_to_chats_sync(listing, CHAT_IDS)
                mark_listing_as_sent(listing['id'])
                
    except Exception as e:
        logger.error(f"Error processing listings: {e}")


def get_listings_data():
    """Get listings data from OLX API"""
    try:
        url = "https://www.olx.ua/apigateway/graphql"
        
        query = """
        query ListingSearchQuery($searchParameters: [SearchParameter!]) {
            clientCompatibleListings(searchParameters: $searchParameters) {
                __typename
                ... on ListingSuccess {
                    data {
                        id
                        location {
                            district {
                                name
                            }
                        }
                        contact {
                            name
                            phone
                        }
                        user {
                            id
                            uuid
                        }
                        params {
                            key
                            value {
                                ... on PriceParam {
                                    value
                                    currency
                                }
                            }
                        }
                        title
                        url
                    }
                }
            }
        }
        """
        
        variables = {
            "searchParameters": [
                {"key": "offset", "value": "0"},
                {"key": "limit", "value": "20"},
                {"key": "query", "value": "оренда 2 кімнатна"},
                {"key": "category_id", "value": "1760"},
                {"key": "region_id", "value": "5"},
                {"key": "city_id", "value": "176"},
                {"key": "currency", "value": "UAH"},
                {"key": "sort_by", "value": "created_at:desc"},
                {"key": "filter_enum_number_of_rooms_string[0]", "value": "dvuhkomnatnye"},
                {"key": "filter_float_price:to", "value": "10000"}
            ]
        }
        
        # Request body
        body = {
            "query": query,
            "variables": variables
        }
        
        # Headers
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        # print("\n=== API Request ===")
        # print(f"URL: {url}")
        # print(f"Body: {json.dumps(body, indent=2, ensure_ascii=False)}")
        
        response = requests.post(url, json=body, headers=headers)
        
        # print("\n=== API Response ===")
        # print(f"Status Code: {response.status_code}")
        # print(f"Headers: {response.headers}")
        # print("\nResponse Body:")
        # print(response.text)
        
        data = response.json()
        
        if not isinstance(data, dict):
            print("Error: Response is not a dictionary")
            return None
            
        return data
        
    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None


def main():
    """Main function to run the bot."""
    try:
        logger.info("Initializing database...")
        create_table_if_not_exists()
        logger.info("Database initialized successfully")
        
        schedule.every(5).minutes.do(process_new_listings)
        logger.info("Scheduler started. Running every 5 minutes...")
        
        logger.info("Running initial check...")
        process_new_listings()
        
        while True:
            schedule.run_pending()
            time.sleep(1)
            
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        raise

if __name__ == "__main__":
    main() 