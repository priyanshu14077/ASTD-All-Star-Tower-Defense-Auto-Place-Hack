"""
Main entry point for the ASTD Auto Place educational demonstration.
Handles initialization, hotkey binding, and bot lifecycle management.
"""

import sys
import time
import logging
import signal

logger = logging.getLogger("ASTD Bot.Main")


def check_environment():
    """
    Verify that the runtime environment meets all requirements.

    Returns:
        True if environment is ready, False otherwise.
    """
    from .utils import check_dependencies, check_privileges

    # Check dependencies
    missing = check_dependencies()
    if missing:
        logger.error(
            "Missing dependencies: {}".format(", ".join(missing))
        )
        logger.error("Install them with: pip install -r requirements.txt")
        return False

    # Check privileges (informational, not blocking)
    if not check_privileges():
        logger.warning(
            "Not running with elevated privileges. "
            "Some automation features may require admin rights."
        )

    logger.info("Environment check passed")
    return True


def setup_hotkeys(bot):
    """
    Register global hotkeys for bot control.

    Args:
        bot: AutoPlaceBot instance to control.
    """
    from . import config
    import keyboard

    def on_start():
        if not bot.is_running:
            logger.info(
                "Hotkey [{}] pressed: Starting bot".format(
                    config.HOTKEY_START
                )
            )
            bot.start()
        else:
            logger.info(
                "Hotkey [{}] pressed: Bot already running".format(
                    config.HOTKEY_START
                )
            )

    def on_stop():
        if bot.is_running:
            logger.info(
                "Hotkey [{}] pressed: Stopping bot".format(
                    config.HOTKEY_STOP
                )
            )
            bot.stop()

    def on_toggle_farm():
        logger.info(
            "Hotkey [{}] pressed: Toggling farm".format(
                config.HOTKEY_TOGGLE_FARM
            )
        )
        bot.toggle_farm()

    def on_toggle_raid():
        logger.info(
            "Hotkey [{}] pressed: Toggling raid".format(
                config.HOTKEY_TOGGLE_RAID
            )
        )
        bot.toggle_raid()

    try:
        keyboard.add_hotkey(config.HOTKEY_START, on_start)
        keyboard.add_hotkey(config.HOTKEY_STOP, on_stop)
        keyboard.add_hotkey(config.HOTKEY_TOGGLE_FARM, on_toggle_farm)
        keyboard.add_hotkey(config.HOTKEY_TOGGLE_RAID, on_toggle_raid)

        logger.info("Hotkeys registered:")
        logger.info("  [{}] - Start bot".format(config.HOTKEY_START))
        logger.info("  [{}] - Stop bot".format(config.HOTKEY_STOP))
        logger.info("  [{}] - Toggle auto-farm".format(
            config.HOTKEY_TOGGLE_FARM
        ))
        logger.info("  [{}] - Toggle auto-raid".format(
            config.HOTKEY_TOGGLE_RAID
        ))
    except Exception as e:
        logger.error("Failed to register hotkeys: {}".format(e))
        logger.error(
            "Try running the script with administrator privileges"
        )


def print_banner():
    """Print the application banner to the console."""
    banner = """
    ================================================
      ASTD Auto Place - Educational Demonstration
      All Star Tower Defense Automation Tool

      This is an educational project demonstrating
      screen automation patterns using Python.
      Use responsibly and in accordance with game TOS.
    ================================================
    """
    print(banner)


def main():
    """Main function - entry point of the application."""
    print_banner()

    # Setup logging
    from .utils import setup_logging
    from . import config
    setup_logging(config.LOG_LEVEL, config.LOG_FILE)

    logger.info("ASTD Auto Place - Educational Demonstration")
    logger.info("Python version: {}".format(sys.version))

    # Check environment
    if not check_environment():
        logger.error("Environment check failed. Exiting.")
        sys.exit(1)

    # Initialize bot
    from .bot import AutoPlaceBot
    bot = AutoPlaceBot(config)

    # Setup hotkeys
    setup_hotkeys(bot)

    # Setup signal handlers for graceful shutdown
    def signal_handler(sig, frame):
        logger.info("Shutdown signal received")
        if bot.is_running:
            bot.stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Main idle loop - hotkeys handle all bot control
    logger.info("Bot is ready. Press hotkeys to control.")
    logger.info("Press Ctrl+C to exit.")

    try:
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        pass
    finally:
        if bot.is_running:
            bot.stop()
        logger.info("Application exited")


if __name__ == "__main__":
    main()
