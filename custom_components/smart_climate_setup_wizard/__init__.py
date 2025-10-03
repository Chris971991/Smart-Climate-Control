"""The Smart Climate Control Setup Wizard integration."""
from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

_LOGGER = logging.getLogger(__name__)

DOMAIN = "smart_climate_setup_wizard"


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Smart Climate Control Setup Wizard from a config entry."""
    # Store the config entry data
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = entry.data

    room_name = entry.data.get("room_name")

    _LOGGER.info(
        "Smart Climate Control Setup Wizard loaded for room: %s",
        room_name,
    )

    # Note: Notification is now created during config flow completion,
    # not here, to avoid showing it on every restart

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    # Note: This does NOT delete the helper entities
    # Users must manually delete helpers if they want to remove them
    hass.data[DOMAIN].pop(entry.entry_id)

    _LOGGER.info(
        "Smart Climate Control Setup Wizard unloaded for room: %s (helpers remain)",
        entry.data.get("room_name"),
    )

    return True


async def async_remove_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Handle removal of an entry."""
    _LOGGER.info(
        "Smart Climate Control Setup Wizard entry removed for room: %s. "
        "Helper entities remain and must be deleted manually if desired.",
        entry.data.get("room_name"),
    )