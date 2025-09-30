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
    dashboard_card = entry.data.get("dashboard_card_yaml", "")

    _LOGGER.info(
        "Smart Climate Control Setup Wizard setup complete for room: %s",
        room_name,
    )

    # Create persistent notification with dashboard card YAML
    if dashboard_card:
        message = f"""## ✅ {room_name} Climate Control Setup Complete!

**What was created:**
- ✅ All helper entities
- ✅ Complete automation
- ✅ Ready to use immediately!

---

### 🎨 Optional: Add Dashboard Control Card

Copy this YAML and add it to your dashboard for easy mode switching:

```yaml
{dashboard_card}
```

**To add to your dashboard:**
1. Go to your dashboard
2. Click Edit (top right)
3. Click Add Card
4. Search for "Manual" card
5. Paste the YAML above
6. Save!

**Note:** Requires `mushroom` and `card-mod` custom cards (install via HACS)

---

You can dismiss this notification once you've copied the card YAML (if desired)."""

        await hass.services.async_call(
            "persistent_notification",
            "create",
            {
                "title": f"🎉 {room_name} Climate Setup Complete",
                "message": message,
                "notification_id": f"climate_setup_{entry.entry_id}",
            },
        )

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