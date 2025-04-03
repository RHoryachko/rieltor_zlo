import os
import logging
import asyncio

from dotenv import load_dotenv
from telegram import Bot
from telegram.error import RetryAfter, NetworkError, TimedOut

from message_formatter import format_telegram_message

load_dotenv()
# Initialize bot
bot = Bot(token=os.getenv('TELEGRAM_BOT_TOKEN'))


async def send_message_with_retry(chat_id, message, max_retries=3, initial_delay=1):
    """
    Send a message with retry logic.
    
    Args:
        chat_id: Telegram chat ID
        message: Message text
        max_retries: Maximum number of retry attempts
        initial_delay: Initial delay between retries in seconds
        
    Returns:
        bool: True if message was sent successfully, False otherwise
    """
    delay = initial_delay
    for attempt in range(max_retries):
        try:
            await bot.send_message(chat_id=chat_id, text=message)
            return True
        except RetryAfter as e:
            wait_time = e.retry_after
            logging.warning(f"Rate limited. Waiting {wait_time} seconds before retry...")
            await asyncio.sleep(wait_time)
        except (NetworkError, TimedOut) as e:
            if attempt < max_retries - 1:
                logging.warning(f"Network error (attempt {attempt + 1}/{max_retries}): {e}")
                await asyncio.sleep(delay)
                delay *= 2
            else:
                logging.error(f"Failed to send message after {max_retries} attempts: {e}")
                return False
        except Exception as e:
            logging.error(f"Unexpected error while sending message: {e}")
            return False
    return False


async def send_listing_to_chats(listing_data, chat_ids):
    """
    Send listing to multiple Telegram chats.
    
    Args:
        listing_data (dict): Parsed listing data
        chat_ids (list): List of chat IDs to send to
    """
    try:
        message = format_telegram_message(listing_data)
        for chat_id in chat_ids:
            success = await send_message_with_retry(chat_id, message)
            if success:
                logging.info(f"Message for listing {listing_data['id']} sent to chat {chat_id}")
            else:
                logging.error(f"Failed to send message for listing {listing_data['id']} to chat {chat_id}")
    except Exception as e:
        logging.error(f"Error sending message for listing {listing_data['id']}: {e}")


def send_listing_to_chats_sync(listing_data, chat_ids):
    """
    Synchronous wrapper for sending messages to Telegram chats.
    
    Args:
        listing_data (dict): Parsed listing data
        chat_ids (list): List of chat IDs to send to
    """
    asyncio.run(send_listing_to_chats(listing_data, chat_ids)) 