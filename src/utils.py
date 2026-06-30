"""
Utility functions for the ASTD Auto Place educational demonstration.
Includes logging setup, privilege checks, and common helpers.
"""

import logging
import os
import sys
import platform


def setup_logging(level="INFO", log_file="astd_bot.log"):
    """Configure and return a logger instance."""
    logger = logging.getLogger("ASTD Bot")
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))

    # File handler
    fh = logging.FileHandler(log_file, encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    ))

    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))

    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger


def check_privileges():
    """Check if the script is running with elevated privileges."""
    try:
        if platform.system() == "Windows":
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        else:
            return os.geteuid() == 0
    except Exception:
        return False


def check_dependencies():
    """Verify that all required packages are available."""
    missing = []
    try:
        import keyboard  # noqa: F401
    except ImportError:
        missing.append("keyboard")
    try:
        import pyautogui  # noqa: F401
    except ImportError:
        missing.append("pyautogui")
    try:
        import cv2  # noqa: F401
    except ImportError:
        missing.append("opencv-python")
    try:
        import numpy  # noqa: F401
    except ImportError:
        missing.append("numpy")
    try:
        from PIL import Image  # noqa: F401
    except ImportError:
        missing.append("pillow")
    return missing


def safe_click(x, y, duration=0.1):
    """Perform a mouse click with basic error handling."""
    try:
        import pyautogui
        pyautogui.click(x, y, duration=duration)
    except Exception as e:
        logging.getLogger("ASTD Bot").error(
            "Click failed at ({}, {}): {}".format(x, y, e)
        )


def safe_key_press(key, delay=0.05):
    """Press a key with basic error handling."""
    try:
        import pyautogui
        pyautogui.press(key)
    except Exception as e:
        logging.getLogger("ASTD Bot").error(
            "Key press failed for '{}': {}".format(key, e)
        )


def scale_coordinates(x_pct, y_pct, width, height):
    """Convert percentage-based coordinates to absolute pixel values."""
    return int(x_pct * width), int(y_pct * height)


def format_duration(seconds):
    """Format seconds into a human-readable duration string."""
    hours, remainder = divmod(int(seconds), 3600)
    minutes, secs = divmod(remainder, 60)
    if hours > 0:
        return "{}h {}m {}s".format(hours, minutes, secs)
    elif minutes > 0:
        return "{}m {}s".format(minutes, secs)
    return "{}s".format(secs)
