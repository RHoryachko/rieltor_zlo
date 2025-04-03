import json
import requests
import logging
import os
from dotenv import load_dotenv

from realtor_detector import is_realtor_listing, get_user_real_estate_listings_count, is_business_user

logger = logging.getLogger(__name__)


def parse_listing_data(listing):
    """
    Extract relevant data from a single listing.
    
    Args:
        listing (dict): Raw listing data from the API
        
    Returns:
        dict: Parsed listing data with standardized fields
    """
    try:
        logger.debug(f"Processing listing {listing.get('id', 'unknown')}")
        
        user = listing.get('user', {})
        user_uuid = user.get('uuid')
        listings_count = get_user_real_estate_listings_count(user_uuid) if user_uuid else 0
        is_business = is_business_user(user_uuid) if user_uuid else False
        
        location = listing.get('location', {})
        district = location.get('district', {})
        district_name = district.get('name', 'Unknown')
        
        contact = listing.get('contact', {})
        owner_name = contact.get('name', 'Unknown')
        phone_number = contact.get('phone', False)
        
        price = None
        params = listing.get('params', [])
        for param in params:
            if param.get('key') == 'price':
                price_value = param.get('value', {})
                price = price_value.get('value')
                break
        
        listing_id = listing.get('id')
        title = listing.get('title', '')
        url = listing.get('url', '')
        description = listing.get('description', '')
        created_time = listing.get('created_time', '')
        last_refresh_time = listing.get('last_refresh_time', '')
        
        # Log extracted values for debugging
        logger.debug(f"Extracted values for listing {listing_id}:")
        logger.debug(f"  District: {district_name}")
        logger.debug(f"  Owner: {owner_name}")
        logger.debug(f"  Price: {price}")
        logger.debug(f"  Title: {title}")
        logger.debug(f"  URL: {url}")
        
        if not all([listing_id, district_name, owner_name, price, title, url]):
            missing_fields = []
            if not listing_id: missing_fields.append('id')
            if not district_name: missing_fields.append('district_name')
            if not owner_name: missing_fields.append('owner_name')
            if not price: missing_fields.append('price')
            if not title: missing_fields.append('title')
            if not url: missing_fields.append('url')
            logger.warning(f"Missing required fields in listing {listing_id}: {', '.join(missing_fields)}")
            return None
            
        return {
            'id': listing_id,
            'district_name': district_name,
            'owner_name': owner_name,
            'price': price,
            'title': title,
            'phone_number': phone_number,
            'url': url,
            'is_realtor': is_business or is_realtor_listing(listing),
            'listings_count': listings_count,
            'description': description,
            'created_time': created_time,
            'last_refresh_time': last_refresh_time
        }
    except Exception as e:
        logger.error(f"Error parsing listing data: {str(e)}")
        return None

def process_listings(data):
    """
    Process raw listings data from the API.
    
    Args:
        data (dict): Raw API response data
        
    Returns:
        list: List of parsed listing dictionaries
    """
    try:
        # print("\n=== Raw Response Body ===")
        # print(data)
        # print("\n=== Starting to process listings ===")
        # print(f"Raw data structure: {json.dumps(data, indent=2, ensure_ascii=False)}")
        
        # Extract listings from the nested data structure
        listings = data.get("data", {}).get("clientCompatibleListings", {}).get("data", [])
        # print(f"\nFound {len(listings)} listings in response")
        
        if not listings:
            # print("Warning: No listings found in the data")
            return []
            
        parsed_listings = []
        
        # Process all listings
        for i, listing in enumerate(listings, 1):
            # print(f"\nProcessing listing {i}/{len(listings)}")
            # print(f"Listing ID: {listing.get('id', 'unknown')}")
            try:
                parsed = parse_listing_data(listing)
                if parsed:
                    # print(f"Successfully parsed listing {listing.get('id', 'unknown')}")
                    parsed_listings.append(parsed)
                else:
                    print(f"Failed to parse listing {listing.get('id', 'unknown')}")
            except Exception as e:
                print(f"Error parsing listing {listing.get('id', 'unknown')}: {str(e)}")
                continue
                
        # print(f"\n=== Processing complete ===")
        # print(f"Successfully processed {len(parsed_listings)} out of {len(listings)} listings")
        return parsed_listings
        
    except Exception as e:
        print(f"Error processing listings: {str(e)}")
        return []

def print_listing_info(listing_data):
    """
    Print formatted listing information to console.
    
    Args:
        listing_data (dict): Parsed listing data
    """
    if not listing_data:
        print("Invalid listing data")
        return
        
    # print("\nListing Information:")
    # print(f"ID: {listing_data['id']}")
    # print(f"District: {listing_data['district_name']}")
    # print(f"Owner Name: {listing_data['owner_name']}")
    # print(f"Price: {listing_data['price']} UAH")
    # print(f"Title: {listing_data['title']}")
    # print(f"Phone Number: {'Yes' if listing_data['phone_number'] else 'No'}")
    # print(f"URL: {listing_data['url']}")
    # print("-" * 40)
