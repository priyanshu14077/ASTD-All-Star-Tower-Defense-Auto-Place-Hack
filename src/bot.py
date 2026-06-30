"""
Auto-placement bot module for the ASTD educational demonstration.
Handles unit placement, auto-upgrade, auto-raid, and auto-farm logic.
"""

import time
import logging
import threading
from typing import List, Optional

logger = logging.getLogger("ASTD Bot.Core")


class AutoPlaceBot:
    """
    Educational demonstration of an automation bot for tower defense games.
    This class demonstrates patterns for screen-driven automation.
    """

    def __init__(self, config=None):
        """
        Initialize the bot with configuration settings.

        Args:
            config: Configuration module or dict with settings.
        """
        if config is None:
            from . import config
            self.config = config
        else:
            self.config = config

        self._running = False
        self._farm_active = False
        self._raid_active = False
        self._lock = threading.Lock()
        self._placed_units = []
        self._stats = {
            "units_placed": 0,
            "upgrades_performed": 0,
            "raids_completed": 0,
            "farm_iterations": 0,
            "start_time": None,
        }

        try:
            import pyautogui
            self.screen_width, self.screen_height = pyautogui.size()
            pyautogui.FAILSAFE = True
            pyautogui.PAUSE = 0.1
        except Exception as e:
            logger.error("Failed to initialize pyautogui: {}".format(e))
            self.screen_width = 1920
            self.screen_height = 1080

    @property
    def is_running(self):
        """Check if the bot is currently running."""
        return self._running

    def start(self):
        """Start the bot's main automation loop."""
        if self._running:
            logger.warning("Bot is already running")
            return

        self._running = True
        self._stats["start_time"] = time.time()
        logger.info("Bot started")

        self._main_loop()

    def stop(self):
        """Stop the bot gracefully."""
        self._running = False
        logger.info(
            "Bot stopped. Stats: {} placed, {} upgraded, {} raids".format(
                self._stats["units_placed"],
                self._stats["upgrades_performed"],
                self._stats["raids_completed"],
            )
        )

    def _main_loop(self):
        """Main automation loop that runs while the bot is active."""
        while self._running:
            try:
                if self._raid_active:
                    self._auto_raid_cycle()
                elif self._farm_active:
                    self._auto_farm_cycle()
                else:
                    self._auto_place_cycle()

                time.sleep(self.config.DELAY_SCAN)
            except KeyboardInterrupt:
                self.stop()
                break
            except Exception as e:
                logger.error("Error in main loop: {}".format(e))
                time.sleep(1.0)

    def _auto_place_cycle(self):
        """Execute one cycle of the auto-placement logic."""
        from .utils import scale_coordinates, safe_click

        # Scan for empty placement zones
        zones = self._get_placement_zones()

        for zone_x_pct, zone_y_pct in zones:
            if not self._running:
                break

            # Check if this zone already has a unit
            if self._zone_occupied(zone_x_pct, zone_y_pct):
                continue

            # Select a unit from inventory
            self._select_next_unit()
            time.sleep(self.config.DELAY_PLACE)

            # Place the unit at the zone
            px, py = scale_coordinates(
                zone_x_pct, zone_y_pct,
                self.screen_width, self.screen_height
            )
            safe_click(px, py)

            with self._lock:
                self._placed_units.append((zone_x_pct, zone_y_pct))
                self._stats["units_placed"] += 1

            logger.debug(
                "Placed unit at ({:.2f}, {:.2f})".format(
                    zone_x_pct, zone_y_pct
                )
            )
            time.sleep(self.config.DELAY_PLACE)

        # After placing, attempt upgrades
        self._auto_upgrade_cycle()

    def _get_placement_zones(self):
        """
        Get available placement zones from configuration pattern.
        Returns zones that don't already have units placed.
        """
        zones = []
        for coord in self.config.PLACEMENT_PATTERN:
            if coord not in self._placed_units:
                zones.append(coord)
        return zones

    def _zone_occupied(self, x_pct, y_pct):
        """Check if a zone already has a unit placed."""
        return (x_pct, y_pct) in self._placed_units

    def _select_next_unit(self):
        """Select the next available unit from the inventory panel."""
        from .utils import safe_click, scale_coordinates

        # Click on the inventory area to select a unit
        inv_x, inv_y = scale_coordinates(
            0.05, 0.5, self.screen_width, self.screen_height
        )
        safe_click(inv_x, inv_y)
        time.sleep(0.2)

    def _auto_upgrade_cycle(self):
        """Attempt to upgrade all placed units based on priority."""
        from .utils import safe_click, scale_coordinates

        for unit_coord in self._placed_units:
            if not self._running:
                break

            px, py = scale_coordinates(
                unit_coord[0], unit_coord[1],
                self.screen_width, self.screen_height
            )

            # Click on the unit to select it
            safe_click(px, py)
            time.sleep(0.2)

            # Click upgrade button (assumed position)
            up_x, up_y = scale_coordinates(
                0.85, 0.75, self.screen_width, self.screen_height
            )
            safe_click(up_x, up_y)

            with self._lock:
                self._stats["upgrades_performed"] += 1

            logger.debug("Upgraded unit at {}".format(unit_coord))
            time.sleep(self.config.DELAY_UPGRADE)

    def _auto_raid_cycle(self):
        """Execute one cycle of the auto-raid logic."""
        from .utils import safe_click, scale_coordinates

        logger.info("Starting auto-raid cycle")

        # Navigate to raid menu
        raid_x, raid_y = scale_coordinates(
            0.9, 0.5, self.screen_width, self.screen_height
        )
        safe_click(raid_x, raid_y)
        time.sleep(self.config.DELAY_RAID)

        # Select raid (auto-select if configured)
        if self.config.RAID_AUTO_SELECT:
            sel_x, sel_y = scale_coordinates(
                0.5, 0.4, self.screen_width, self.screen_height
            )
            safe_click(sel_x, sel_y)
            time.sleep(0.5)

        # Start raid
        start_x, start_y = scale_coordinates(
            0.5, 0.8, self.screen_width, self.screen_height
        )
        safe_click(start_x, start_y)

        with self._lock:
            self._stats["raids_completed"] += 1

        logger.info(
            "Raid initiated. Total raids: {}".format(
                self._stats["raids_completed"]
            )
        )
        time.sleep(self.config.RAID_DELAY_BETWEEN)

    def _auto_farm_cycle(self):
        """Execute one cycle of the auto-farm logic."""
        from .utils import safe_click, scale_coordinates

        logger.debug("Running auto-farm cycle")

        # Select a farming stage
        stage_x, stage_y = scale_coordinates(
            0.3, 0.4, self.screen_width, self.screen_height
        )
        safe_click(stage_x, stage_y)
        time.sleep(0.5)

        # Start the stage
        start_x, start_y = scale_coordinates(
            0.5, 0.8, self.screen_width, self.screen_height
        )
        safe_click(start_x, start_y)

        with self._lock:
            self._stats["farm_iterations"] += 1

        logger.debug(
            "Farm iteration {}".format(self._stats["farm_iterations"])
        )
        time.sleep(self.config.DELAY_FARM)

    def toggle_farm(self):
        """Toggle the auto-farm mode on or off."""
        self._farm_active = not self._farm_active
        if self._farm_active:
            self._raid_active = False  # Mutually exclusive
        logger.info(
            "Auto-farm {}".format(
                "enabled" if self._farm_active else "disabled"
            )
        )

    def toggle_raid(self):
        """Toggle the auto-raid mode on or off."""
        self._raid_active = not self._raid_active
        if self._raid_active:
            self._farm_active = False  # Mutually exclusive
        logger.info(
            "Auto-raid {}".format(
                "enabled" if self._raid_active else "disabled"
            )
        )

    def reset_state(self):
        """Reset the bot's internal state and statistics."""
        with self._lock:
            self._placed_units.clear()
            self._stats = {k: 0 for k in self._stats}
            self._stats["start_time"] = None
        logger.info("Bot state reset")

    def get_stats(self):
        """Return a copy of the current bot statistics."""
        with self._lock:
            stats = self._stats.copy()
            if stats["start_time"]:
                stats["elapsed_seconds"] = (
                    time.time() - stats["start_time"]
                )
            return stats
