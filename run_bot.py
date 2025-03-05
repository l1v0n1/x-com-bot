#!/usr/bin/env python3
"""
Точка входа для запуска бота
"""

import asyncio
from loguru import logger
from x_com_bot.bot import XComBot
from x_com_bot.config import load_config

async def main():
    """Main entry point for the bot"""
    try:
        # Load configuration
        config = load_config()
        
        # Initialize bot
        bot = XComBot(config)
        logger.info("Bot initialized successfully")
        
        # Run the bot
        await bot.run()
        
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())  