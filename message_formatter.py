def format_telegram_message(listing_data):
    """
    Format listing data for Telegram message.
    
    Args:
        listing_data (dict): Parsed listing data
        
    Returns:
        str: Formatted message string
    """
    if not listing_data:
        return "Invalid listing data"
        
    if listing_data['is_realtor']:
        realtor_status = "🔴 Рієлтор"
    elif listing_data['listings_count'] >= 5:
        realtor_status = "🟡 МОЖЛИВО НЕ РІЄЛТОР (5+ оголошень)"
    else:
        realtor_status = "🟢 МОЖЛИВО Без рієлтора"
    
    return (
        f"🏠 ВСТВАВАЙ НОВА ХАТА\n\n"
        f"{realtor_status}\n"
        f"📌 {listing_data['title']}\n"
        f"💰 Ціна: {listing_data['price']} UAH\n"
        f"👤 Власник: {listing_data['owner_name']}\n"
        f"📱 Телефон: {'Доступний' if listing_data['phone_number'] else 'Не доступний'}\n"
        f"📊 Кількість оголошень: {listing_data['listings_count']}\n"
        f"📅 Дата створення: {listing_data['created_time']}\n"
        f"🔄 Дата останнього оновлення: {listing_data['last_refresh_time']}\n"
        f"🔗 URL: {listing_data['url']}"
    ) 