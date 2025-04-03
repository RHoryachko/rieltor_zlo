import requests
import logging

logger = logging.getLogger(__name__)


def get_user_real_estate_listings_count(user_id):
    """
    Get the number of real estate listings for a user from provided JSON data.
    
    Args:
        user_id (str): OLX user UUID
        
    Returns:
        int: Number of real estate listings or 0 if error
    """
    try:
        url = f"https://www.olx.ua/api/v1/offers/?offset=0&limit=10&category_id=0&sort_by=created_at%3Adesc&query=&user_id={user_id}"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            real_estate_count = 0
            for listing in data.get('data', []):
                if listing.get('category', {}).get('type') == 'real_estate':
                    real_estate_count += 1

            logger.info(f"User {user_id} has {real_estate_count} real estate listings")
            return real_estate_count
        else:
            logger.error(f"Failed to get user listings. Status code: {response.status_code}")
            return 0
        
    except Exception as e:
        logger.error(f"Error checking real estate listings count for user {user_id}: {e}")
        return 0


def is_business_user(user_id):
    """
    Check if a user is a business account by making a request to OLX API.
    
    Args:
        user_id (int): OLX user ID
        
    Returns:
        bool: True if user is a business account, False otherwise
    """
    try:
        url = f"https://www.olx.ua/api/v1/users/{user_id}/"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            is_business = data.get('data', {}).get('is_business', False)
            logger.info(f"User {user_id} is business: {is_business}")
            return is_business
        else:
            logger.error(f"Failed to get user data. Status code: {response.status_code}")
            return False
    except Exception as e:
        logger.error(f"Error checking business status for user {user_id}: {e}")
        return False


def is_realtor_listing(listing):
    """
    Analyze listing description and user type to determine if it's from a realtor.
    
    Args:
        listing (dict): Listing data including description
        
    Returns:
        bool: True if listing appears to be from a realtor, False otherwise
    """
    # First check if user is a business account
    user_id = listing.get('user', {}).get('id')
    if user_id and is_business_user(user_id):
        return True
        
    # Check if user has too many listings (5 or more)
    user_uuid = listing.get('user', {}).get('uuid')
    if user_uuid:
        listings_count = get_user_real_estate_listings_count(user_uuid)
        if listings_count >= 2:
            logger.info(f"User {user_uuid} has {listings_count} listings - likely not a realtor")
            return False
        
    # If not a business account and not too many listings, check description keywords
    # Keywords that might indicate a realtor listing
    realtor_keywords = [
        'рієлтор', 'ріелтор', 'ріелторська', 'рієлторська',
        'агентство', 'агент', 'агентка',
        'брокер', 'брокерська',
        'посередник', 'посередництво',
        'агентство нерухомості', 'агент нерухомості',
        'офіс нерухомості', 'компанія нерухомості',
        'професійний', 'професійна',
        'квартира під ключ', 'квартири під ключ',
        'пропозиція від агентства', 'пропозиція від агента',
        'здійснюємо показ', 'проводимо показ',
        'допоможемо підібрати', 'допоможемо знайти',
        'великий вибір', 'широкий вибір',
        'гарантуємо', 'гарантуємо якість',
        'офіційний договір', 'офіційна угода',
        'професійна консультація', 'консультація спеціаліста'
    ]
    
    # Keywords that might indicate a private listing
    private_keywords = [
        'оренда від власника', 'оренда від господаря',
        'продаж від власника', 'продаж від господаря',
        'без посередників', 'без рієлторів',
        'без комісії', 'без додаткових витрат',
        'без агентства', 'без агентів',
        'прямий контакт', 'контакт з власником',
        'здає власник', 'продає власник',
        'орендодавець', 'власник квартири',
        'господар квартири', 'господар оселі'
    ]
    
    description = listing.get('description', '').lower()
    
    # Count matches for each category
    realtor_matches = sum(1 for keyword in realtor_keywords if keyword in description)
    private_matches = sum(1 for keyword in private_keywords if keyword in description)
    
    # If there are more realtor keyword matches than private ones, consider it a realtor listing
    return realtor_matches > private_matches 