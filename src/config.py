"""
Configuration settings for the ASTD Auto Place educational demonstration.
All values are defaults and can be adjusted for different scenarios.
"""

# Hotkey configuration
HOTKEY_START = "f5"
HOTKEY_STOP = "f6"
HOTKEY_TOGGLE_FARM = "f7"
HOTKEY_TOGGLE_RAID = "f8"

# Delay settings (in seconds)
DELAY_PLACE = 0.3
DELAY_UPGRADE = 0.5
DELAY_RAID = 1.0
DELAY_FARM = 2.0
DELAY_SCAN = 0.1

# Placement pattern (grid coordinates as percentage of screen)
PLACEMENT_PATTERN = [
    (0.3, 0.6), (0.4, 0.6), (0.5, 0.6),
    (0.3, 0.5), (0.4, 0.5), (0.5, 0.5),
    (0.3, 0.4), (0.4, 0.4), (0.5, 0.4),
]

# Upgrade priorities (unit types in order of priority)
UPGRADE_PRIORITIES = [
    "legendary",
    "epic",
    "rare",
    "common",
]

# Scan regions (x, y, width, height as percentages)
SCAN_REGION_UNITS = (0.0, 0.0, 0.25, 1.0)
SCAN_REGION_BATTLEFIELD = (0.25, 0.2, 0.75, 0.7)
SCAN_REGION_GEMS = (0.9, 0.0, 0.1, 0.05)
SCAN_REGION_MONEY = (0.8, 0.0, 0.1, 0.05)

# Farm settings
FARM_TARGET_GEMS = 10000
FARM_TARGET_MONEY = 50000
FARM_MAX_ITERATIONS = 100

# Raid settings
RAID_AUTO_SELECT = True
RAID_DELAY_BETWEEN = 5.0

# Logging
LOG_LEVEL = "INFO"
LOG_FILE = "astd_bot.log"

# Screen resolution (target)
TARGET_WIDTH = 1920
TARGET_HEIGHT = 1080
