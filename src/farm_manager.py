"""
Farm manager module for the ASTD educational demonstration.
Handles resource management: gems, money, free units, and traits.
"""

import time
import logging
from typing import Optional, Dict, Any
from dataclasses import dataclass, field

logger = logging.getLogger("ASTD Bot.FarmManager")


@dataclass
class ResourceState:
    """Data class representing the current resource state."""
    gems: int = 0
    money: int = 0
    units_owned: int = 0
    traits_unlocked: int = 0
    last_updated: float = field(default_factory=time.time)


class FarmManager:
    """
    Educational demonstration of a resource/farm management system.
    Tracks and manages in-game resources with automation patterns.
    """

    def __init__(self, config=None):
        """
        Initialize the farm manager.

        Args:
            config: Configuration module or dict with farm settings.
        """
        if config is None:
            from . import config
            self.config = config
        else:
            self.config = config

        self._state = ResourceState()
        self._farm_active = False
        self._gem_target = self.config.FARM_TARGET_GEMS
        self._money_target = self.config.FARM_TARGET_MONEY
        self._max_iterations = self.config.FARM_MAX_ITERATIONS
        self._iteration_count = 0
        self._history = []

    @property
    def state(self):
        """Return the current resource state."""
        return self._state

    @property
    def is_active(self):
        """Check if farming is currently active."""
        return self._farm_active

    def update_resources(self, gems=None, money=None):
        """
        Update the resource state with new values.

        Args:
            gems: Current gem count (None to skip update).
            money: Current money count (None to skip update).
        """
        if gems is not None:
            self._state.gems = gems
        if money is not None:
            self._state.money = money
        self._state.last_updated = time.time()
        logger.debug(
            "Resources updated - Gems: {}, Money: {}".format(
                self._state.gems, self._state.money
            )
        )

    def start_gem_farm(self):
        """
        Start the gem farming loop.

        Returns:
            True if farming started, False otherwise.
        """
        if self._farm_active:
            logger.warning("Farm is already active")
            return False

        self._farm_active = True
        self._iteration_count = 0
        logger.info(
            "Starting gem farm (target: {})".format(self._gem_target)
        )

        while self._farm_active and self._iteration_count < self._max_iterations:
            self._gem_farm_iteration()
            self._iteration_count += 1

            if self._state.gems >= self._gem_target:
                logger.info("Gem target reached: {}".format(self._state.gems))
                break

            time.sleep(self.config.DELAY_FARM)

        self._farm_active = False
        self._record_history("gem_farm", self._iteration_count)
        return True

    def _gem_farm_iteration(self):
        """Execute one iteration of the gem farming cycle."""
        import pyautogui
        from .utils import safe_click, scale_coordinates

        sw, sh = pyautogui.size()

        # Select a gem-farming stage
        stage_x, stage_y = scale_coordinates(0.35, 0.35, sw, sh)
        safe_click(stage_x, stage_y)
        time.sleep(0.3)

        # Start the stage
        start_x, start_y = scale_coordinates(0.5, 0.8, sw, sh)
        safe_click(start_x, start_y)

        # Simulate gem gain (educational placeholder)
        estimated_gain = 50 + (self._iteration_count * 10)
        self._state.gems += estimated_gain

        logger.debug(
            "Gem farm iteration {}: +{} gems (total: {})".format(
                self._iteration_count, estimated_gain, self._state.gems
            )
        )

    def start_money_farm(self):
        """
        Start the money farming loop.

        Returns:
            True if farming started, False otherwise.
        """
        if self._farm_active:
            logger.warning("Farm is already active")
            return False

        self._farm_active = True
        self._iteration_count = 0
        logger.info(
            "Starting money farm (target: {})".format(self._money_target)
        )

        while self._farm_active and self._iteration_count < self._max_iterations:
            self._money_farm_iteration()
            self._iteration_count += 1

            if self._state.money >= self._money_target:
                logger.info(
                    "Money target reached: {}".format(self._state.money)
                )
                break

            time.sleep(self.config.DELAY_FARM)

        self._farm_active = False
        self._record_history("money_farm", self._iteration_count)
        return True

    def _money_farm_iteration(self):
        """Execute one iteration of the money farming cycle."""
        import pyautogui
        from .utils import safe_click, scale_coordinates

        sw, sh = pyautogui.size()

        # Select a money-farming stage
        stage_x, stage_y = scale_coordinates(0.35, 0.45, sw, sh)
        safe_click(stage_x, stage_y)
        time.sleep(0.3)

        # Start the stage
        start_x, start_y = scale_coordinates(0.5, 0.8, sw, sh)
        safe_click(start_x, start_y)

        # Simulate money gain
        estimated_gain = 200 + (self._iteration_count * 50)
        self._state.money += estimated_gain

        logger.debug(
            "Money farm iteration {}: +{} money (total: {})".format(
                self._iteration_count, estimated_gain, self._state.money
            )
        )

    def stop_farm(self):
        """Stop any active farming operation."""
        self._farm_active = False
        logger.info("Farming stopped")

    def get_free_units(self):
        """
        Check for available free units in the game.
        Educational demonstration of inventory scanning.

        Returns:
            List of detected free unit names (placeholder).
        """
        # In a real implementation, this would scan the game UI
        # for free unit banners or gift buttons
        logger.debug("Scanning for free units...")
        return []

    def claim_free_units(self):
        """
        Attempt to claim any available free units.

        Returns:
            Number of units claimed.
        """
        import pyautogui
        from .utils import safe_click, scale_coordinates

        free_units = self.get_free_units()
        claimed = 0

        sw, sh = pyautogui.size()

        for _ in free_units:
            # Click on the free unit banner
            banner_x, banner_y = scale_coordinates(0.5, 0.3, sw, sh)
            safe_click(banner_x, banner_y)
            time.sleep(0.5)

            # Click claim button
            claim_x, claim_y = scale_coordinates(0.5, 0.6, sw, sh)
            safe_click(claim_x, claim_y)
            time.sleep(0.3)

            claimed += 1
            self._state.units_owned += 1

        if claimed > 0:
            logger.info("Claimed {} free units".format(claimed))
        return claimed

    def manage_traits(self):
        """
        Manage unit traits - check and optimize trait assignments.
        Educational demonstration of trait management logic.

        Returns:
            Dictionary with trait management results.
        """
        results = {
            "traits_checked": 0,
            "traits_unlocked": 0,
            "traits_upgraded": 0,
        }

        # Scan units for trait opportunities
        logger.debug("Starting trait management scan")

        # This would integrate with screen scanning to detect
        # trait slots and available trait options
        for i in range(min(self._state.units_owned, 10)):
            results["traits_checked"] += 1
            # Simulated trait check
            if i % 3 == 0:
                results["traits_unlocked"] += 1
                self._state.traits_unlocked += 1

        logger.info("Trait management complete: {}".format(results))
        return results

    def _record_history(self, farm_type, iterations):
        """Record a farming session in the history log."""
        entry = {
            "type": farm_type,
            "iterations": iterations,
            "timestamp": time.time(),
            "final_gems": self._state.gems,
            "final_money": self._state.money,
        }
        self._history.append(entry)
        logger.debug("Recorded farm history: {}".format(entry))

    def get_history(self):
        """Return the farming history."""
        return self._history.copy()

    def get_summary(self):
        """Return a comprehensive summary of the farm manager state."""
        return {
            "current_state": {
                "gems": self._state.gems,
                "money": self._state.money,
                "units_owned": self._state.units_owned,
                "traits_unlocked": self._state.traits_unlocked,
            },
            "targets": {
                "gems": self._gem_target,
                "money": self._money_target,
            },
            "total_sessions": len(self._history),
            "is_active": self._farm_active,
        }
