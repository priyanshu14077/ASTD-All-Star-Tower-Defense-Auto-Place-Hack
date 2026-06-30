"""
Screen scanning module for the ASTD Auto Place educational demonstration.
Uses OpenCV for template matching and screen element detection.
"""

import time
import logging
from typing import Optional, Tuple, List

import numpy as np

logger = logging.getLogger("ASTD Bot.Scanner")


def capture_screen(region=None):
    """
    Capture a screenshot of the screen or a specific region.

    Args:
        region: (x, y, width, height) in pixels. None for full screen.

    Returns:
        NumPy array of the captured image in BGR format.
    """
    try:
        import pyautogui
        if region:
            screenshot = pyautogui.screenshot(region=region)
        else:
            screenshot = pyautogui.screenshot()
        return np.array(screenshot)[:, :, ::-1]  # RGB to BGR
    except Exception as e:
        logger.error("Screen capture failed: {}".format(e))
        return np.zeros((100, 100, 3), dtype=np.uint8)


def load_template(template_name, template_dir="templates"):
    """
    Load a template image for matching.

    Args:
        template_name: Filename of the template image.
        template_dir: Directory containing template images.

    Returns:
        NumPy array of the template or None if not found.
    """
    import cv2
    import os
    path = os.path.join(template_dir, template_name)
    if not os.path.exists(path):
        logger.warning("Template not found: {}".format(path))
        return None
    template = cv2.imread(path, cv2.IMREAD_COLOR)
    if template is None:
        logger.error("Failed to read template: {}".format(path))
    return template


def find_template(screen, template, threshold=0.8, method=None):
    """
    Find a template image within a screen capture using template matching.

    Args:
        screen: Full screen capture as NumPy array.
        template: Template image to search for.
        threshold: Minimum match confidence (0.0 to 1.0).
        method: OpenCV template matching method. Defaults to TM_CCOEFF_NORMED.

    Returns:
        Tuple of (x, y, width, height) of the best match, or None.
    """
    import cv2
    if method is None:
        method = cv2.TM_CCOEFF_NORMED

    try:
        result = cv2.matchTemplate(screen, template, method)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)

        if max_val >= threshold:
            h, w = template.shape[:2]
            x, y = max_loc
            logger.debug(
                "Template found at ({}, {}) with confidence {:.2f}".format(
                    x, y, max_val
                )
            )
            return (x, y, w, h)
        else:
            logger.debug(
                "Template not found. Best match: {:.2f} < {:.2f}".format(
                    max_val, threshold
                )
            )
            return None
    except Exception as e:
        logger.error("Template matching failed: {}".format(e))
        return None


def detect_unit_positions(
    screen, unit_template, grid_rows=3, grid_cols=3, region=None
):
    """
    Detect unit positions on the battlefield by scanning a grid pattern.

    Args:
        screen: Full screen capture.
        unit_template: Template image of a placed unit.
        grid_rows: Number of rows to scan.
        grid_cols: Number of columns to scan.
        region: Battlefield region (x, y, w, h) in pixels.

    Returns:
        List of (x, y) center coordinates where units were detected.
    """
    import cv2
    positions = []

    if region:
        rx, ry, rw, rh = region
        battlefield = screen[ry:ry + rh, rx:rx + rw]
        offset_x, offset_y = rx, ry
    else:
        battlefield = screen
        offset_x, offset_y = 0, 0

    cell_w = battlefield.shape[1] // grid_cols
    cell_h = battlefield.shape[0] // grid_rows

    for row in range(grid_rows):
        for col in range(grid_cols):
            x1 = col * cell_w
            y1 = row * cell_h
            x2 = x1 + cell_w
            y2 = y1 + cell_h
            cell = battlefield[y1:y2, x1:x2]

            match = find_template(cell, unit_template, threshold=0.75)
            if match:
                mx, my, mw, mh = match
                cx = offset_x + x1 + mx + mw // 2
                cy = offset_y + y1 + my + mh // 2
                positions.append((cx, cy))

    logger.info(
        "Detected {} units on the battlefield".format(len(positions))
    )
    return positions


def detect_placement_zones(screen, region=None):
    """
    Identify valid placement zones on the battlefield.
    Uses edge detection and contour analysis as an educational demonstration.

    Args:
        screen: Full screen capture.
        region: Battlefield region (x, y, w, h) in pixels.

    Returns:
        List of (x, y) coordinates for valid placement positions.
    """
    import cv2
    zones = []

    if region:
        rx, ry, rw, rh = region
        battlefield = screen[ry:ry + rh, rx:rx + rw]
        offset_x, offset_y = rx, ry
    else:
        battlefield = screen
        offset_x, offset_y = 0, 0

    # Convert to grayscale and apply edge detection
    gray = cv2.cvtColor(battlefield, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)

    # Find contours
    contours, _ = cv2.findContours(
        edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    # Filter contours by area to find placement zones
    min_area = 500
    max_area = 5000
    for contour in contours:
        area = cv2.contourArea(contour)
        if min_area < area < max_area:
            M = cv2.moments(contour)
            if M["m00"] > 0:
                cx = int(M["m10"] / M["m00"]) + offset_x
                cy = int(M["m01"] / M["m00"]) + offset_y
                zones.append((cx, cy))

    logger.info("Detected {} placement zones".format(len(zones)))
    return zones


def read_resource_value(screen, region, ocr_model=None):
    """
    Read a numeric resource value (gems, money) from screen region.
    This is a placeholder demonstrating OCR integration.

    Args:
        screen: Full screen capture.
        region: (x, y, w, h) region containing the resource text.
        ocr_model: Optional OCR model/engine for text recognition.

    Returns:
        Integer value of the resource, or None if unreadable.
    """
    # Educational note: In a real implementation, you would use
    # an OCR engine like Tesseract or a custom trained model
    # to extract the numeric value from the screen region.
    logger.debug("OCR placeholder called for region {}".format(region))
    return None


def scan_battlefield_state(screen):
    """
    Perform a full scan of the battlefield and return current state.

    Args:
        screen: Full screen capture.

    Returns:
        Dictionary with battlefield state information.
    """
    state = {
        "timestamp": time.time(),
        "units_detected": 0,
        "empty_zones": 0,
        "active_wave": False,
        "resources": {
            "gems": None,
            "money": None,
        }
    }

    # This would integrate with the detection functions above
    # in a complete implementation.
    logger.debug("Battlefield state scanned: {}".format(state))
    return state
