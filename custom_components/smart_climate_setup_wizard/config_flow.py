"""Config flow for Smart Climate Control Setup Wizard - Complete Guided Setup."""
from __future__ import annotations

import logging
from typing import Any
import yaml
import json
import os
import asyncio
import aiohttp
import tempfile
import shutil
import errno

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant, callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import entity_registry as er, selector
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

DOMAIN = "smart_climate_setup_wizard"

# Helper definitions matching the blueprint requirements
HELPER_DEFINITIONS = {
    # ========================================
    # REQUIRED HELPERS (Always Created)
    # ========================================
    "last_mode": {
        "domain": "input_text",
        "name": "{room} Climate Last Mode",
        "icon": "mdi:thermostat",
        "initial": "off",
        "max_length": 255,
    },
    "last_change": {
        "domain": "input_datetime",
        "name": "{room} Climate Last Change",
        "icon": "mdi:clock-outline",
        "has_date": True,
        "has_time": True,
    },

    # ========================================
    # DYNAMIC ADAPTATION HELPERS
    # ========================================
    "effectiveness_score": {
        "domain": "input_number",
        "name": "{room} Climate Effectiveness Score",
        "icon": "mdi:speedometer",
        "min": 0,
        "max": 100,
        "step": 0.1,
        "initial": 0,
        "unit_of_measurement": "%",
        "mode": "box",
    },
    "temp_history": {
        "domain": "input_number",
        "name": "{room} Climate Temperature History",
        "icon": "mdi:thermometer",
        "min": 0,
        "max": 50,
        "step": 0.1,
        "initial": 0,
        "unit_of_measurement": "°C",
        "mode": "box",
    },
    "trend_direction": {
        "domain": "input_text",
        "name": "{room} Climate Trend Direction",
        "icon": "mdi:trending-up",
        "initial": "stable",
        "max_length": 50,
    },
    "mode_start_time": {
        "domain": "input_datetime",
        "name": "{room} Climate Mode Start Time",
        "icon": "mdi:clock-start",
        "has_date": True,
        "has_time": True,
    },
    "temp_stable_since": {
        "domain": "input_datetime",
        "name": "{room} Temperature Stable Since",
        "icon": "mdi:thermometer-check",
        "has_date": True,
        "has_time": True,
    },
    "last_transition": {
        "domain": "input_text",
        "name": "{room} Climate Last Transition",
        "icon": "mdi:swap-horizontal",
        "initial": "none",
        "max_length": 100,
    },

    # ========================================
    # MANUAL OVERRIDE HELPERS
    # ========================================
    "manual_override": {
        "domain": "input_boolean",
        "name": "{room} Climate Manual Override",
        "icon": "mdi:hand-back-right",
        "initial": False,
    },
    "proximity_override": {
        "domain": "input_boolean",
        "name": "{room} Climate Proximity Override",
        "icon": "mdi:alert-octagon",
        "initial": False,
    },

    # ========================================
    # CONTROL MODE HELPERS
    # ========================================
    "control_mode": {
        "domain": "input_select",
        "name": "{room} Climate Control Mode",
        "icon": "mdi:tune",
        "options": ["Auto", "Smart", "Manual"],
        "initial": "Smart",
    },

    # ========================================
    # SMART MODE / PRESENCE HELPERS
    # ========================================
    "presence_detected": {
        "domain": "input_datetime",
        "name": "{room} Presence Last Detected",
        "icon": "mdi:account-clock",
        "has_date": True,
        "has_time": True,
    },
}

# Feature groups for optional helpers
FEATURE_HELPERS = {
    "dynamic_adaptation": [
        "effectiveness_score",
        "temp_history",
        "trend_direction",
        "mode_start_time",
        "temp_stable_since",
        "last_transition",
    ],
    "manual_override": ["manual_override", "proximity_override"],
    "control_mode": ["control_mode"],
    "smart_mode": ["presence_detected"],
}


def sanitize_room_name(room_name: str) -> str:
    """Convert room name to valid entity ID format."""
    return room_name.lower().replace(" ", "_").replace("-", "_")


class SmartClimateHelperCreatorConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Smart Climate Control Setup Wizard - Complete Guided Setup."""

    VERSION = 2

    def __init__(self):
        """Initialize the config flow."""
        self._room_data = {}
        self._created_helpers = []

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Step 0: Check prerequisites (packages + blueprint)."""
        # Step 0a: Check packages configuration
        packages_configured = await self._check_packages_configured()

        if not packages_configured:
            # Automatically add packages configuration
            try:
                packages_added = await self._add_packages_configuration()
                # Only show restart message if packages were actually added
                if packages_added:
                    return self.async_show_form(
                        step_id="packages_added",
                        data_schema=vol.Schema({}),
                        description_placeholders={
                            "step": "Setup Complete - Restart Required",
                        },
                    )
            except Exception as err:
                _LOGGER.error("Failed to add packages configuration: %s", err)
                # Fall through to manual instructions

        # Step 0b: Check blueprint exists
        blueprint_exists = await self._check_blueprint_exists()

        if not blueprint_exists:
            # Try to download and install blueprint automatically
            _LOGGER.info("Blueprint not found, attempting automatic installation...")
            blueprint_installed = await self._download_blueprint_from_github()

            if blueprint_installed:
                # Success! Show confirmation and proceed
                return self.async_show_form(
                    step_id="blueprint_installed",
                    data_schema=vol.Schema({}),
                )
            else:
                # Download failed, show manual instructions
                return self.async_abort(
                    reason="blueprint_download_failed",
                    description_placeholders={
                        "blueprint_url": "https://github.com/Chris971991/Smart-Climate-Control/blob/main/ultimate_climate_control.yaml",
                        "import_link": "https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https://github.com/Chris971991/Smart-Climate-Control/blob/main/ultimate_climate_control.yaml",
                    },
                )

        # Both packages and blueprint ready, proceed to room setup
        return await self.async_step_room_name()

    async def async_step_packages_added(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Show message that packages were added and restart is needed."""
        return self.async_abort(
            reason="packages_configured",
            description_placeholders={
                "message": "Packages configuration has been added to configuration.yaml. Please restart Home Assistant, then run this wizard again to create your climate control setup."
            }
        )

    async def async_step_blueprint_installed(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Show success message that blueprint was installed."""
        # User clicked Submit/Continue - proceed to room setup
        return await self.async_step_room_name()

    async def async_step_room_name(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Step 1: Room Name."""
        errors = {}

        if user_input is not None:
            room_name = user_input["room_name"]
            sanitized_name = sanitize_room_name(room_name)

            # Check if this room already exists
            await self.async_set_unique_id(f"climate_helpers_{sanitized_name}")
            self._abort_if_unique_id_configured()

            # Store room name
            self._room_data = {"room_name": room_name}
            return await self.async_step_features()

        data_schema = vol.Schema(
            {
                vol.Required("room_name"): cv.string,
            }
        )

        return self.async_show_form(
            step_id="room_name",
            data_schema=data_schema,
            errors=errors,
            description_placeholders={
                "step": "1 of 5",
            },
        )

    async def async_step_features(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Step 2: Feature Selection."""
        errors = {}

        if user_input is not None:
            self._room_data.update(user_input)
            return await self.async_step_climate_entities()

        data_schema = vol.Schema(
            {
                vol.Optional("enable_dynamic_adaptation", default=True): cv.boolean,
                vol.Optional("enable_manual_override", default=True): cv.boolean,
                vol.Optional("enable_control_mode", default=True): cv.boolean,
                vol.Optional("enable_smart_mode", default=True): cv.boolean,
            }
        )

        return self.async_show_form(
            step_id="features",
            data_schema=data_schema,
            errors=errors,
            description_placeholders={
                "room_name": self._room_data["room_name"],
                "step": "2 of 5",
            },
        )

    async def async_step_climate_entities(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Step 3: Select Climate Entities (A/C units)."""
        errors = {}

        if user_input is not None:
            climate_entities = user_input.get("climate_entities")

            # Comprehensive validation
            if not climate_entities or not isinstance(climate_entities, list) or len(climate_entities) == 0:
                errors["base"] = "no_climate_entities"
            elif any(not e or not isinstance(e, str) or e.strip() == "" for e in climate_entities):
                errors["base"] = "invalid_climate_entities"
            else:
                # Check if these climate entities are already used
                selected_entities = climate_entities
                conflicts = await self._check_climate_entity_conflicts(selected_entities)

                if conflicts:
                    errors["base"] = "climate_entities_in_use"
                    errors["conflicting_rooms"] = ", ".join(conflicts)
                else:
                    self._room_data.update(user_input)
                    return await self.async_step_sensors()

        # Get all climate entities
        climate_entities = self.hass.states.async_entity_ids("climate")

        if not climate_entities:
            # No climate entities found!
            return self.async_abort(reason="no_climate_entities")

        data_schema = vol.Schema(
            {
                vol.Required("climate_entities"): selector.EntitySelector(
                    selector.EntitySelectorConfig(
                        domain="climate",
                        multiple=True,
                    )
                ),
            }
        )

        return self.async_show_form(
            step_id="climate_entities",
            data_schema=data_schema,
            errors=errors,
            description_placeholders={
                "room_name": self._room_data["room_name"],
                "step": "3 of 5",
            },
        )

    async def async_step_sensors(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Step 4: Select Optional Sensors."""
        errors = {}

        if user_input is not None:
            # Validate presence sensors if provided
            if user_input.get("room_presence_sensors"):
                sensors = user_input["room_presence_sensors"]
                for sensor in sensors:
                    if self.hass.states.get(sensor) is None:
                        errors["room_presence_sensors"] = "sensor_not_found"
                        break

            # Validate temperature sensor if provided
            if user_input.get("temperature_sensor"):
                temp_sensor = user_input["temperature_sensor"]
                if self.hass.states.get(temp_sensor) is None:
                    errors["temperature_sensor"] = "sensor_not_found"

            if not errors:
                self._room_data.update(user_input)
                # Always go to presence detection step next
                return await self.async_step_presence_detection()

        # Build schema with optional sensors
        data_schema_dict = {}

        # Temperature sensor (optional)
        data_schema_dict[vol.Optional("temperature_sensor")] = selector.EntitySelector(
            selector.EntitySelectorConfig(
                domain="sensor",
                device_class="temperature",
            )
        )

        # Presence sensors (optional, only if smart mode enabled)
        if self._room_data.get("enable_smart_mode", True):
            data_schema_dict[vol.Optional("room_presence_sensors")] = selector.EntitySelector(
                selector.EntitySelectorConfig(
                    domain=["binary_sensor", "sensor"],
                    multiple=True,
                )
            )

        data_schema = vol.Schema(data_schema_dict)

        return self.async_show_form(
            step_id="sensors",
            data_schema=data_schema,
            errors=errors,
            description_placeholders={
                "room_name": self._room_data["room_name"],
                "step": "4 of 5",
            },
        )

    async def async_step_presence_detection(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Step 4.5: Home/Away Presence Detection."""
        errors = {}

        if user_input is not None:
            # Validate person entities if provided
            if user_input.get("presence_persons"):
                persons = user_input["presence_persons"]
                for person in persons:
                    if self.hass.states.get(person) is None:
                        errors["presence_persons"] = "person_not_found"
                        break

            # Validate presence devices if provided
            if user_input.get("presence_devices"):
                devices = user_input["presence_devices"]
                for device in devices:
                    if self.hass.states.get(device) is None:
                        errors["presence_devices"] = "device_not_found"
                        break

            if not errors:
                self._room_data.update(user_input)

                # Determine which mode to default to based on sensors configured
                has_room_sensors = bool(self._room_data.get("room_presence_sensors"))
                has_person_entities = bool(user_input.get("presence_persons"))

                # Auto-select initial control mode
                if has_room_sensors:
                    # Has room sensors → Smart mode
                    self._room_data["default_control_mode"] = "Smart"
                elif has_person_entities:
                    # No room sensors but has person entities → Auto mode
                    self._room_data["default_control_mode"] = "Auto"
                else:
                    # No sensors at all → Smart mode (will just never activate)
                    self._room_data["default_control_mode"] = "Smart"

                # If person entities selected, offer proximity pre-conditioning
                if has_person_entities:
                    return await self.async_step_proximity_detection()
                # Otherwise check if we need to ask about bedroom mode
                elif (self._room_data.get("enable_smart_mode", True) and
                    self._room_data.get("room_presence_sensors")):
                    return await self.async_step_bedroom_mode()
                else:
                    return await self.async_step_temperature()

        # Build schema for presence detection
        data_schema_dict = {}

        # Person entities for home/away detection (recommended)
        data_schema_dict[vol.Optional("presence_persons")] = selector.EntitySelector(
            selector.EntitySelectorConfig(
                domain="person",
                multiple=True,
            )
        )

        # Additional presence devices (optional)
        data_schema_dict[vol.Optional("presence_devices")] = selector.EntitySelector(
            selector.EntitySelectorConfig(
                multiple=True,
            )
        )

        data_schema = vol.Schema(data_schema_dict)

        return self.async_show_form(
            step_id="presence_detection",
            data_schema=data_schema,
            errors=errors,
            description_placeholders={
                "room_name": self._room_data["room_name"],
                "step": "4.5 of 6",
            },
        )

    async def async_step_proximity_detection(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Step 4.6: Optional Proximity-Based Pre-Conditioning Setup."""
        errors = {}

        # Check if Home zone exists
        home_zone = self.hass.states.get("zone.home")
        home_zone_exists = home_zone is not None

        if user_input is not None:
            enable_proximity = user_input.get("enable_proximity", False)

            # If proximity enabled, validate requirements
            if enable_proximity:
                # Check if Home zone exists
                if not home_zone_exists:
                    errors["base"] = "home_zone_not_found"

                # Validate proximity sensor if provided
                if user_input.get("proximity_sensor"):
                    proximity_sensor = user_input["proximity_sensor"]
                    if self.hass.states.get(proximity_sensor) is None:
                        errors["proximity_sensor"] = "proximity_sensor_not_found"

                # Validate direction sensor if provided
                if user_input.get("direction_sensor"):
                    direction_sensor = user_input["direction_sensor"]
                    if self.hass.states.get(direction_sensor) is None:
                        errors["direction_sensor"] = "direction_sensor_not_found"

            if not errors:
                self._room_data.update(user_input)

                # Check if we need to ask about bedroom mode
                if (self._room_data.get("enable_smart_mode", True) and
                    self._room_data.get("room_presence_sensors")):
                    return await self.async_step_bedroom_mode()
                else:
                    return await self.async_step_temperature()

        # Build schema for proximity detection
        data_schema_dict = {}

        # Enable proximity checkbox (always shown)
        data_schema_dict[vol.Optional("enable_proximity", default=False)] = selector.BooleanSelector()

        # Only show sensor fields if Home zone exists (sensors won't work without it)
        if home_zone_exists:
            # Proximity distance sensor
            data_schema_dict[vol.Optional("proximity_sensor", default="sensor.home_nearest_distance")] = selector.EntitySelector(
                selector.EntitySelectorConfig(
                    domain="sensor",
                )
            )

            # Direction sensor
            data_schema_dict[vol.Optional("direction_sensor", default="sensor.home_nearest_direction_of_travel")] = selector.EntitySelector(
                selector.EntitySelectorConfig(
                    domain="sensor",
                )
            )

            # Home zone distance
            data_schema_dict[vol.Optional("home_zone_distance", default=5000)] = selector.NumberSelector(
                selector.NumberSelectorConfig(
                    min=1000,
                    max=10000,
                    step=500,
                    mode="box",
                    unit_of_measurement="m",
                )
            )

        data_schema = vol.Schema(data_schema_dict)

        return self.async_show_form(
            step_id="proximity_detection",
            data_schema=data_schema,
            errors=errors,
            description_placeholders={
                "room_name": self._room_data["room_name"],
                "step": "4.6 of 6",
                "home_zone_status": "✅ Home zone configured" if home_zone_exists else "⚠️ Home zone not found",
            },
        )

    async def async_step_bedroom_mode(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Step 5: Ask if this is a bedroom with bed sensor."""
        errors = {}

        if user_input is not None:
            self._room_data.update(user_input)
            return await self.async_step_temperature()

        data_schema = vol.Schema({
            vol.Optional("is_bedroom_with_bed_sensor", default=False): selector.BooleanSelector()
        })

        return self.async_show_form(
            step_id="bedroom_mode",
            data_schema=data_schema,
            errors=errors,
            description_placeholders={
                "room_name": self._room_data["room_name"],
                "step": "5 of 6",
            },
        )

    async def async_step_temperature(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Step 5: Temperature Settings with Preset Support."""
        errors = {}

        if user_input is not None:
            # Check if preset selected and apply preset width (keep user's target temp!)
            preset = user_input.get("temperature_preset", "custom")
            if preset and preset != "custom":
                # Apply preset comfort zone width (DO NOT override target temperature!)
                presets = {
                    "tight": {"width": 0.5},
                    "balanced": {"width": 1.0},
                    "relaxed": {"width": 1.5},
                }
                if preset in presets:
                    # Only set width, preserve user's target_temperature
                    user_input["comfort_zone_width"] = presets[preset]["width"]

            self._room_data.update(user_input)

            # Continue to behavior settings step
            return await self.async_step_behavior_settings()

        data_schema = vol.Schema(
            {
                vol.Optional("temperature_preset", default="balanced"): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=[
                            {"label": "Tight (±0.5°C) - Precise control, more energy", "value": "tight"},
                            {"label": "Balanced (±1.0°C) ⭐ Recommended", "value": "balanced"},
                            {"label": "Relaxed (±1.5°C) - Energy saving", "value": "relaxed"},
                            {"label": "Custom - I'll set my own values", "value": "custom"},
                        ],
                        mode="dropdown",
                    )
                ),
                vol.Optional("target_temperature", default=22): selector.NumberSelector(
                    selector.NumberSelectorConfig(
                        min=16,
                        max=30,
                        step=0.5,
                        mode="box",
                        unit_of_measurement="°C",
                    )
                ),
                vol.Optional("comfort_zone_width", default=1.0): selector.NumberSelector(
                    selector.NumberSelectorConfig(
                        min=0.5,
                        max=5.0,
                        step=0.1,
                        mode="box",
                        unit_of_measurement="°C",
                    )
                ),
                vol.Optional("enable_heating", default=True): selector.BooleanSelector(),
                vol.Optional("enable_cooling", default=True): selector.BooleanSelector(),
            }
        )

        return self.async_show_form(
            step_id="temperature",
            data_schema=data_schema,
            errors=errors,
            description_placeholders={
                "room_name": self._room_data["room_name"],
                "step": "5 of 6",
            },
        )

    async def async_step_behavior_settings(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Step 5.5: Behavior & Notification Settings."""
        errors = {}

        if user_input is not None:
            self._room_data.update(user_input)

            # Continue to advanced escalation step
            return await self.async_step_advanced_escalation()

        # Build schema for behavior settings
        data_schema = vol.Schema(
            {
                vol.Optional("away_mode_action", default="eco"): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=[
                            {"label": "Off - Turn AC completely off (maximum savings)", "value": "off"},
                            {"label": "Eco - Reduce to eco mode ⭐ Recommended", "value": "eco"},
                            {"label": "Maintain - Keep current temperature", "value": "maintain"},
                        ],
                        mode="dropdown",
                    )
                ),
                vol.Optional("smart_mode_behavior", default="eco"): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=[
                            {"label": "Off - Turn off completely (maximum savings)", "value": "off"},
                            {"label": "Eco - Reduce to eco mode ⭐ Recommended", "value": "eco"},
                            {"label": "Maintain - Keep current temperature", "value": "maintain"},
                        ],
                        mode="dropdown",
                    )
                ),
                vol.Optional("stability_behavior", default="off"): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=[
                            {"label": "Off - Turn off when stable ⭐ Recommended", "value": "off"},
                            {"label": "Eco - Switch to eco mode when stable", "value": "eco"},
                        ],
                        mode="dropdown",
                    )
                ),
                vol.Optional("enable_eco_mode", default=True): selector.BooleanSelector(),
                vol.Optional("enable_notifications", default=False): selector.BooleanSelector(),
            }
        )

        return self.async_show_form(
            step_id="behavior_settings",
            data_schema=data_schema,
            errors=errors,
            description_placeholders={
                "room_name": self._room_data["room_name"],
                "step": "5.5 of 6",
            },
        )

    async def async_step_advanced_escalation(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Step 5.6: Advanced Escalation Settings (Wrong-Direction Boost)."""
        errors = {}

        if user_input is not None:
            self._room_data.update(user_input)

            # Continue to compressor protection step
            return await self.async_step_compressor_protection()

        # Build schema for advanced escalation settings
        data_schema = vol.Schema(
            {
                vol.Optional("enable_wrong_direction_escalation", default=False): selector.BooleanSelector(),
                vol.Optional("wrong_direction_escalation_per_check", default=1): selector.NumberSelector(
                    selector.NumberSelectorConfig(
                        min=0,
                        max=2,
                        step=1,
                        mode="slider",
                    )
                ),
                vol.Optional("wrong_direction_min_rate", default=0.05): selector.NumberSelector(
                    selector.NumberSelectorConfig(
                        min=0.01,
                        max=0.20,
                        step=0.01,
                        mode="slider",
                        unit_of_measurement="°C/min",
                    )
                ),
            }
        )

        return self.async_show_form(
            step_id="advanced_escalation",
            data_schema=data_schema,
            errors=errors,
            description_placeholders={
                "room_name": self._room_data["room_name"],
                "step": "5.6 of 6",
            },
        )

    async def async_step_compressor_protection(self, user_input=None):
        """Step 5.75: Compressor Protection Settings."""
        errors = {}

        if user_input is not None:
            self._room_data.update(user_input)

            # Continue to create step
            return await self.async_step_create()

        # Build schema for compressor protection settings
        data_schema = vol.Schema(
            {
                vol.Optional("min_runtime_minutes", default=15): selector.NumberSelector(
                    selector.NumberSelectorConfig(
                        min=5,
                        max=30,
                        step=1,
                        unit_of_measurement="minutes",
                        mode="slider",
                    )
                ),
                vol.Optional("min_off_time_minutes", default=10): selector.NumberSelector(
                    selector.NumberSelectorConfig(
                        min=3,
                        max=15,
                        step=1,
                        unit_of_measurement="minutes",
                        mode="slider",
                    )
                ),
                vol.Optional("enforce_off_time_protection", default=True): selector.BooleanSelector(),
            }
        )

        return self.async_show_form(
            step_id="compressor_protection",
            data_schema=data_schema,
            errors=errors,
            description_placeholders={
                "room_name": self._room_data["room_name"],
                "step": "5.8 of 6",
            },
        )

    async def _check_climate_entity_conflicts(self, selected_entities: list[str]) -> list[str]:
        """Check if climate entities are already used in other integrations."""
        conflicts = []

        # Check all existing config entries for this integration
        for entry in self.hass.config_entries.async_entries(DOMAIN):
            existing_entities = entry.data.get("climate_entities", [])

            # Check for overlap
            overlap = set(selected_entities) & set(existing_entities)
            if overlap:
                conflicts.append(entry.data.get("room_name", "Unknown Room"))

        return conflicts

    async def _check_helper_exists(self, entity_id: str) -> bool:
        """Check if a helper entity already exists."""
        return self.hass.states.get(entity_id) is not None

    async def _check_packages_configured(self) -> bool:
        """Check if packages are configured in configuration.yaml.

        Uses text search instead of YAML parsing to avoid issues with
        Home Assistant-specific tags like !include, !include_dir_named, etc.
        """
        try:
            config_path = self.hass.config.path("configuration.yaml")

            def check_config():
                if not os.path.exists(config_path):
                    return False

                with open(config_path, "r", encoding="utf-8") as f:
                    content = f.read()

                # Check for packages: configuration under homeassistant:
                # Look for patterns like:
                #   homeassistant:
                #     packages: ...
                # or
                #   packages: ...  (if homeassistant: is on a different line)

                lines = content.split('\n')
                in_homeassistant_section = False

                for line in lines:
                    stripped = line.strip()

                    # Check if we're in homeassistant section
                    if stripped.startswith('homeassistant:'):
                        in_homeassistant_section = True
                        continue

                    # If we find packages: under homeassistant section
                    if in_homeassistant_section and stripped.startswith('packages:'):
                        _LOGGER.info("Found packages configuration in configuration.yaml")
                        return True

                    # If we hit another top-level section, we're no longer in homeassistant
                    if in_homeassistant_section and line and not line[0].isspace() and ':' in line:
                        in_homeassistant_section = False

                _LOGGER.info("Packages configuration not found in configuration.yaml")
                return False

            return await self.hass.async_add_executor_job(check_config)

        except Exception as err:
            _LOGGER.error("Failed to check packages configuration: %s", err)
            return False

    async def _add_packages_configuration(self) -> bool:
        """Add packages configuration to configuration.yaml.

        Returns:
            True if packages were added, False if already configured.
        """
        config_path = self.hass.config.path("configuration.yaml")

        def modify_config():
            # Read existing configuration as text
            if os.path.exists(config_path):
                with open(config_path, "r", encoding="utf-8") as f:
                    lines = f.readlines()
            else:
                lines = []

            # Check if homeassistant section exists
            has_homeassistant = False
            homeassistant_line = -1
            has_packages = False

            for i, line in enumerate(lines):
                if line.strip().startswith("homeassistant:"):
                    has_homeassistant = True
                    homeassistant_line = i
                if "packages:" in line:
                    has_packages = True
                    break

            if has_packages:
                _LOGGER.info("Packages already configured in configuration.yaml")
                return False  # Already configured, nothing added

            # Add packages configuration
            if has_homeassistant:
                # Find the indentation level of items under homeassistant
                indent = "  "  # Default 2 spaces
                # Insert after homeassistant: line
                insert_line = homeassistant_line + 1
                # Find correct position (after existing homeassistant items)
                while insert_line < len(lines) and lines[insert_line].startswith(indent) and not lines[insert_line].strip() == "":
                    insert_line += 1

                lines.insert(insert_line, f"{indent}packages: !include_dir_named packages\n")
            else:
                # Add homeassistant section at the beginning
                lines.insert(0, "homeassistant:\n")
                lines.insert(1, "  packages: !include_dir_named packages\n")
                lines.insert(2, "\n")

            # Write back atomically
            temp_fd, temp_path = tempfile.mkstemp(dir=os.path.dirname(config_path), text=True)
            try:
                with os.fdopen(temp_fd, 'w', encoding='utf-8') as f:
                    f.writelines(lines)
                shutil.move(temp_path, config_path)
            except Exception:
                if os.path.exists(temp_path):
                    os.unlink(temp_path)
                raise

            _LOGGER.info("Added packages configuration to configuration.yaml")
            return True  # Successfully added

        return await self.hass.async_add_executor_job(modify_config)

    async def _check_blueprint_exists(self) -> bool:
        """Check if Ultimate Climate Control blueprint exists."""
        blueprint_path = self.hass.config.path(
            "blueprints/automation/Chris971991/ultimate_climate_control.yaml"
        )
        exists = os.path.exists(blueprint_path)
        if exists:
            _LOGGER.info("Blueprint found at: %s", blueprint_path)
        else:
            _LOGGER.info("Blueprint not found, will attempt download from GitHub")
        return exists

    async def _download_blueprint_from_github(self) -> bool:
        """Download and install the latest blueprint from GitHub.

        Returns:
            True if successfully downloaded and installed, False otherwise.
        """
        try:
            blueprint_url = "https://raw.githubusercontent.com/Chris971991/Smart-Climate-Control/main/ultimate_climate_control.yaml"
            _LOGGER.info("Downloading blueprint from: %s", blueprint_url)

            # Download blueprint content
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    blueprint_url, timeout=aiohttp.ClientTimeout(total=10)
                ) as response:
                    if response.status != 200:
                        _LOGGER.error(
                            "Failed to download blueprint: HTTP %d", response.status
                        )
                        return False
                    blueprint_content = await response.text()

            # Validate downloaded content is a valid blueprint
            if not blueprint_content or len(blueprint_content) < 100:
                _LOGGER.error("Downloaded content is empty or too small (size: %d bytes)", len(blueprint_content) if blueprint_content else 0)
                return False

            if not blueprint_content.startswith("blueprint:"):
                _LOGGER.error("Downloaded content doesn't appear to be a valid blueprint (doesn't start with 'blueprint:')")
                return False

            # Validate YAML syntax to catch corrupted downloads
            try:
                yaml.safe_load(blueprint_content)
                _LOGGER.info("Blueprint YAML validation passed")
            except yaml.YAMLError as err:
                _LOGGER.error("Downloaded content is not valid YAML: %s", err)
                return False

            # Create blueprints directory structure
            blueprint_dir = self.hass.config.path("blueprints/automation/Chris971991")

            def prepare_and_write():
                try:
                    os.makedirs(blueprint_dir, exist_ok=True)
                except OSError as err:
                    if err.errno != errno.EEXIST:
                        raise
                blueprint_path = os.path.join(blueprint_dir, "ultimate_climate_control.yaml")

                # Atomic write
                temp_fd, temp_path = tempfile.mkstemp(dir=blueprint_dir, text=True)
                try:
                    with os.fdopen(temp_fd, 'w', encoding='utf-8') as f:
                        f.write(blueprint_content)
                    shutil.move(temp_path, blueprint_path)
                except Exception:
                    if os.path.exists(temp_path):
                        os.unlink(temp_path)
                    raise

                _LOGGER.info("Blueprint saved to: %s", blueprint_path)

            await self.hass.async_add_executor_job(prepare_and_write)

            # Reload automations to make blueprint appear in UI
            _LOGGER.info("Reloading automations to register blueprint...")
            await self.hass.services.async_call("automation", "reload", blocking=True)

            _LOGGER.info("Blueprint successfully installed and registered")
            return True

        except aiohttp.ClientError as err:
            _LOGGER.error("Network error downloading blueprint: %s", err)
            return False
        except Exception as err:
            _LOGGER.error("Unexpected error installing blueprint: %s", err)
            return False

    async def _create_helpers(
        self, hass: HomeAssistant, config: dict[str, Any]
    ) -> None:
        """Create all required helper entities via YAML package file."""
        room_name = config["room_name"]
        sanitized_name = sanitize_room_name(room_name)

        # Check if helpers already exist - if so, delete old package file first
        test_helper_id = f"input_text.climate_last_mode_{sanitized_name}"
        helpers_exist = await self._check_helper_exists(test_helper_id)

        if helpers_exist:
            _LOGGER.info(
                "Helpers for %s already exist - deleting old package file to avoid conflicts.", room_name
            )
            # Delete old package file to prevent duplicate ID warnings
            packages_dir = os.path.join(hass.config.config_dir, "packages")
            old_package_file = os.path.join(packages_dir, f"climate_control_{sanitized_name}.yaml")

            def delete_old_package():
                if os.path.exists(old_package_file):
                    os.unlink(old_package_file)
                    _LOGGER.info("Deleted old package file: %s", old_package_file)

            await hass.async_add_executor_job(delete_old_package)

            # Reload helpers to remove old entities from registry
            for domain in ["input_text", "input_datetime", "input_number", "input_boolean", "input_select"]:
                await hass.services.async_call(domain, "reload", blocking=True)

            await asyncio.sleep(1)  # Brief pause for cleanup

        # Always create base helpers
        base_helpers = ["last_mode", "last_change"]
        helpers_to_create = base_helpers.copy()

        # Add optional helpers based on features
        if config.get("enable_dynamic_adaptation", True):
            helpers_to_create.extend(FEATURE_HELPERS["dynamic_adaptation"])

        if config.get("enable_manual_override", True):
            helpers_to_create.extend(FEATURE_HELPERS["manual_override"])

        if config.get("enable_control_mode", True):
            helpers_to_create.extend(FEATURE_HELPERS["control_mode"])

        if config.get("enable_smart_mode", True):
            helpers_to_create.extend(FEATURE_HELPERS["smart_mode"])

        # Build YAML configuration for all helpers
        helpers_config = {}
        created_helpers = []

        for helper_key in helpers_to_create:
            helper_def = HELPER_DEFINITIONS[helper_key]
            entity_id = f"{helper_def['domain']}.climate_{helper_key}_{sanitized_name}"
            domain = helper_def["domain"]
            object_id = f"climate_{helper_key}_{sanitized_name}"

            # Initialize domain dict if needed
            if domain not in helpers_config:
                helpers_config[domain] = {}

            # Build helper configuration
            helper_config = {
                "name": helper_def["name"].format(room=room_name),
            }

            if helper_def.get("icon"):
                helper_config["icon"] = helper_def["icon"]

            if domain == "input_text":
                helper_config["initial"] = helper_def.get("initial", "")
                helper_config["max"] = helper_def.get("max_length", 255)

            elif domain == "input_datetime":
                helper_config["has_date"] = helper_def.get("has_date", True)
                helper_config["has_time"] = helper_def.get("has_time", True)

            elif domain == "input_number":
                helper_config["min"] = helper_def.get("min", 0)
                helper_config["max"] = helper_def.get("max", 100)
                helper_config["step"] = helper_def.get("step", 1)
                helper_config["initial"] = helper_def.get("initial", 0)
                helper_config["mode"] = helper_def.get("mode", "box")
                if "unit_of_measurement" in helper_def:
                    helper_config["unit_of_measurement"] = helper_def["unit_of_measurement"]

            elif domain == "input_boolean":
                helper_config["initial"] = helper_def.get("initial", False)

            elif domain == "input_select":
                helper_config["options"] = helper_def.get("options", [])
                # Use dynamic default for control_mode, otherwise use template default
                if helper_key == "control_mode" and config.get("default_control_mode"):
                    helper_config["initial"] = config["default_control_mode"]
                elif helper_def.get("initial"):
                    helper_config["initial"] = helper_def["initial"]

            helpers_config[domain][object_id] = helper_config
            created_helpers.append(entity_id)

        # Write YAML package file
        try:
            packages_dir = os.path.join(hass.config.config_dir, "packages")
            try:
                os.makedirs(packages_dir, exist_ok=True)
            except OSError as err:
                if err.errno != errno.EEXIST:
                    raise

            package_file = os.path.join(packages_dir, f"climate_control_{sanitized_name}.yaml")

            def write_package():
                # Atomic write
                temp_fd, temp_path = tempfile.mkstemp(dir=packages_dir, text=True)
                try:
                    with os.fdopen(temp_fd, 'w', encoding='utf-8') as f:
                        try:
                            yaml.dump(helpers_config, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
                        except yaml.YAMLError as err:
                            _LOGGER.error("Failed to serialize helpers YAML: %s", err)
                            raise
                        except Exception as err:
                            _LOGGER.error("Unexpected error writing helpers YAML: %s", err)
                            raise
                    shutil.move(temp_path, package_file)
                except Exception:
                    if os.path.exists(temp_path):
                        os.unlink(temp_path)
                    raise

            await hass.async_add_executor_job(write_package)
            _LOGGER.info("Created package file: %s", package_file)

            # Reload all input helper domains WITH BLOCKING to ensure availability
            reload_tasks = []
            for domain in helpers_config.keys():
                _LOGGER.info("Reloading %s...", domain)
                reload_tasks.append(hass.services.async_call(domain, "reload", blocking=True))

            # Wait for all reloads to complete
            await asyncio.gather(*reload_tasks)

            # Add delay to ensure entities are fully registered in state machine
            await asyncio.sleep(2)

            # Verify all helpers were successfully created
            _LOGGER.info("Verifying %d helpers were created...", len(created_helpers))
            for helper_id in created_helpers:
                if hass.states.get(helper_id) is None:
                    _LOGGER.error("Helper not available after reload: %s", helper_id)
                    raise Exception(f"Helper creation failed: {helper_id} - Entity not found in state machine")

            _LOGGER.info("All helpers verified successfully")

            self._created_helpers = created_helpers
            _LOGGER.info(
                "Successfully created %d helpers for room: %s",
                len(created_helpers),
                room_name,
            )

        except Exception as err:
            _LOGGER.error("Failed to create helpers package: %s", err)
            raise

    async def _create_automation(
        self, hass: HomeAssistant, config: dict[str, Any]
    ) -> str:
        """Create automation with blueprint."""
        room_name = config["room_name"]
        sanitized_name = sanitize_room_name(room_name)

        # Build helper entity IDs
        helpers = {
            "helper_last_mode": f"input_text.climate_last_mode_{sanitized_name}",
            "helper_last_change": f"input_datetime.climate_last_change_{sanitized_name}",
        }

        # Add optional helpers based on enabled features
        if config.get("enable_control_mode", True):
            helpers["helper_control_mode"] = f"input_select.climate_control_mode_{sanitized_name}"

        if config.get("enable_smart_mode", True):
            helpers["helper_presence_detected"] = f"input_datetime.climate_presence_detected_{sanitized_name}"
            helpers["helper_proximity_override"] = f"input_boolean.climate_proximity_override_{sanitized_name}"

        if config.get("enable_dynamic_adaptation", True):
            helpers["helper_temp_history"] = f"input_number.climate_temp_history_{sanitized_name}"
            helpers["helper_trend_direction"] = f"input_text.climate_trend_direction_{sanitized_name}"
            helpers["helper_mode_start_time"] = f"input_datetime.climate_mode_start_time_{sanitized_name}"
            helpers["helper_effectiveness_score"] = f"input_number.climate_effectiveness_score_{sanitized_name}"
            helpers["helper_temp_stable_since"] = f"input_datetime.climate_temp_stable_since_{sanitized_name}"
            helpers["helper_last_transition"] = f"input_text.climate_last_transition_{sanitized_name}"

        if config.get("enable_manual_override", True):
            if "helper_proximity_override" not in helpers:
                helpers["helper_proximity_override"] = f"input_boolean.climate_proximity_override_{sanitized_name}"

        # Build automation config with auto-calculated optimal settings
        comfort_width = config.get("comfort_zone_width", 1.0)

        automation_config = {
            "id": f"climate_control_{sanitized_name}",
            "alias": f"{room_name} Climate Control",
            "description": f"Smart climate control for {room_name} - Created by Smart Climate Control Setup Wizard",
            "use_blueprint": {
                "path": "Chris971991/ultimate_climate_control.yaml",
                "input": {
                    # Basic settings
                    "room_name": room_name,
                    "climate_entities": config["climate_entities"],
                    **helpers,

                    # Temperature settings (user-provided)
                    "target_temperature": config.get("target_temperature", 22),
                    "comfort_zone_width": comfort_width,
                    "enable_heating_mode": config.get("enable_heating", True),
                    "enable_cooling_mode": config.get("enable_cooling", True),

                    # Auto-configured stall detection (optimal defaults)
                    "escalation_temp_tolerance": comfort_width,  # Same as comfort width
                    "minimum_progress_rate": 0.01,  # Universal default (°C/min)
                    "stall_escalation_time": 15,    # Universal default (minutes)

                    # Auto-configured timing (user-configured compressor protection)
                    "check_interval": 5,         # Check every 5 minutes
                    "min_runtime_minutes": config.get("min_runtime_minutes", 15),
                    "min_off_time_minutes": config.get("min_off_time_minutes", 10),
                    "enforce_off_time_protection": config.get("enforce_off_time_protection", True),

                    # Behavior settings (user-provided)
                    "away_mode_action": config.get("away_mode_action", "eco"),
                    "smart_mode_behavior": config.get("smart_mode_behavior", "eco"),
                    "stability_behavior": config.get("stability_behavior", "off"),
                    "enable_eco_mode": config.get("enable_eco_mode", True),
                    "enable_notifications": config.get("enable_notifications", False),
                },
            },
        }

        # Add optional sensors
        if config.get("temperature_sensor"):
            automation_config["use_blueprint"]["input"]["temperature_sensor"] = config["temperature_sensor"]

        if config.get("room_presence_sensors"):
            automation_config["use_blueprint"]["input"]["room_presence_sensors"] = config["room_presence_sensors"]

        # Add presence detection entities
        if config.get("presence_persons"):
            automation_config["use_blueprint"]["input"]["presence_persons"] = config["presence_persons"]

        if config.get("presence_devices"):
            automation_config["use_blueprint"]["input"]["presence_devices"] = config["presence_devices"]

        # Set presence validation mode based on bedroom configuration
        if config.get("is_bedroom_with_bed_sensor", False):
            automation_config["use_blueprint"]["input"]["presence_validation_mode"] = "bedroom"
        else:
            automation_config["use_blueprint"]["input"]["presence_validation_mode"] = "smart"

        # Read existing automations
        automations_file = hass.config.path("automations.yaml")

        def read_automations():
            try:
                if os.path.exists(automations_file):
                    with open(automations_file, "r", encoding="utf-8") as f:
                        return yaml.safe_load(f) or []
                else:
                    return []
            except Exception as err:
                _LOGGER.error("Failed to read automations.yaml: %s", err)
                return []

        automations = await hass.async_add_executor_job(read_automations)

        # Check for automation ID conflict - if exists, replace it
        automation_id = automation_config["id"]
        existing_ids = [auto.get("id") for auto in automations if auto.get("id")]

        if automation_id in existing_ids:
            # Automation with this ID already exists - remove old one
            _LOGGER.info(
                "Automation ID '%s' already exists - replacing with updated configuration", automation_id
            )
            automations = [auto for auto in automations if auto.get("id") != automation_id]

        # Add new automation
        automations.append(automation_config)

        # Write back
        def write_automations():
            try:
                # Atomic write
                automations_dir = os.path.dirname(automations_file)
                temp_fd, temp_path = tempfile.mkstemp(dir=automations_dir, text=True)
                try:
                    with os.fdopen(temp_fd, 'w', encoding='utf-8') as f:
                        try:
                            yaml.dump(automations, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
                        except yaml.YAMLError as err:
                            _LOGGER.error("Failed to serialize automations YAML: %s", err)
                            raise
                        except Exception as err:
                            _LOGGER.error("Unexpected error writing automations YAML: %s", err)
                            raise
                    shutil.move(temp_path, automations_file)
                except Exception:
                    if os.path.exists(temp_path):
                        os.unlink(temp_path)
                    raise
                _LOGGER.info("Added automation to automations.yaml: %s", automation_config["id"])
            except Exception as err:
                _LOGGER.error("Failed to write automations.yaml: %s", err)
                raise

        await hass.async_add_executor_job(write_automations)

        # Reload automations
        try:
            await hass.services.async_call("automation", "reload", blocking=True)
            _LOGGER.info("Reloaded automations successfully")

            # Add delay to ensure automation is registered (increased from 1s to 3s)
            await asyncio.sleep(3)

            # Verify automation was loaded by checking if entity exists
            # Note: HA creates entity_id from alias, not id (e.g., "Office Climate Control" -> "automation.office_climate_control")
            slugified_alias = automation_config['alias'].lower().replace(' ', '_').replace('-', '_')
            automation_entity_id = f"automation.{slugified_alias}"
            if hass.states.get(automation_entity_id) is None:
                _LOGGER.error("Automation entity not found after reload: %s", automation_entity_id)
                raise Exception(f"Automation failed to load: {automation_entity_id}")

            _LOGGER.info("Automation verified: %s", automation_entity_id)

        except Exception as err:
            _LOGGER.error("Failed to reload automations: %s", err)

            # Try to validate automations.yaml to provide helpful error (non-blocking)
            def validate_yaml():
                try:
                    with open(automations_file, "r", encoding="utf-8") as f:
                        yaml.safe_load(f)
                except yaml.YAMLError as yaml_err:
                    _LOGGER.error("automations.yaml has invalid YAML: %s", yaml_err)
                    raise Exception(f"Automation file corrupted - YAML error: {yaml_err}")

            await hass.async_add_executor_job(validate_yaml)
            raise

        return automation_config["id"]

    async def _create_turnoff_automation(
        self, hass: HomeAssistant, config: dict[str, Any]
    ) -> str:
        """Create standalone automation to turn off AC when mode changes."""
        room_name = config["room_name"]
        sanitized_name = sanitize_room_name(room_name)

        # Helper entity IDs
        control_mode_helper = f"input_select.climate_control_mode_{sanitized_name}"
        last_mode_helper = f"input_text.climate_last_mode_{sanitized_name}"

        # Get comfort zone settings
        target_temp = config.get("target_temperature", 22)
        comfort_width = config.get("comfort_zone_width", 1.0)
        comfort_min = round(target_temp - comfort_width, 1)
        comfort_max = round(target_temp + comfort_width, 1)

        # Get enable settings
        enable_heating = config.get("enable_heating", True)
        enable_cooling = config.get("enable_cooling", True)

        # Climate entities
        climate_entities = config["climate_entities"]
        temp_sensor = config.get("temperature_sensor")

        # Build automation config
        turnoff_automation = {
            "id": f"climate_turnoff_{sanitized_name}",
            "alias": f"{room_name} Climate Turn-Off",
            "description": f"Turns off AC when switching to Smart mode and conditions are met - {room_name}",
            "trigger": [
                # Trigger ONLY on mode change to Smart (not periodic)
                {
                    "platform": "state",
                    "entity_id": control_mode_helper,
                    "to": "Smart",
                },
            ],
            "condition": [
                # Only run in Smart mode
                {
                    "condition": "state",
                    "entity_id": control_mode_helper,
                    "state": "Smart",
                },
                # AC must be on
                {
                    "condition": "template",
                    "value_template": f"{{{{ is_state('{climate_entities[0]}', 'cool') or is_state('{climate_entities[0]}', 'heat') or is_state('{climate_entities[0]}', 'heat_cool') or is_state('{climate_entities[0]}', 'auto') or is_state('{climate_entities[0]}', 'dry') or is_state('{climate_entities[0]}', 'fan_only') }}}}",
                },
            ],
            "action": [
                {
                    "variables": {
                        "current_temp": f"{{{{ states('{temp_sensor}') | float(22) }}}}" if temp_sensor else f"{{{{ state_attr('{climate_entities[0]}', 'current_temperature') | float(22) }}}}",
                        "comfort_min": comfort_min,
                        "comfort_max": comfort_max,
                        "enable_heating": enable_heating,
                        "enable_cooling": enable_cooling,
                    },
                },
                # Check if we should turn off
                {
                    "condition": "or",
                    "conditions": [
                        # Condition 1: Temperature in comfort zone
                        {
                            "condition": "template",
                            "value_template": "{{ current_temp >= comfort_min and current_temp <= comfort_max }}",
                        },
                        # Condition 2: Below comfort zone but heating disabled
                        {
                            "condition": "and",
                            "conditions": [
                                {
                                    "condition": "template",
                                    "value_template": "{{ current_temp < comfort_min }}",
                                },
                                {
                                    "condition": "template",
                                    "value_template": "{{ not enable_heating }}",
                                },
                            ],
                        },
                        # Condition 3: Above comfort zone but cooling disabled
                        {
                            "condition": "and",
                            "conditions": [
                                {
                                    "condition": "template",
                                    "value_template": "{{ current_temp > comfort_max }}",
                                },
                                {
                                    "condition": "template",
                                    "value_template": "{{ not enable_cooling }}",
                                },
                            ],
                        },
                    ],
                },
                # Turn off AC
                {
                    "service": "climate.turn_off",
                    "target": {
                        "entity_id": climate_entities,
                    },
                },
                # Update helper
                {
                    "service": "input_text.set_value",
                    "target": {
                        "entity_id": last_mode_helper,
                    },
                    "data": {
                        "value": "off",
                    },
                },
            ],
        }

        # Write automation to automations.yaml
        automations_path = hass.config.path("automations.yaml")

        # Read existing automations (non-blocking)
        def read_automations():
            try:
                if os.path.exists(automations_path):
                    with open(automations_path, "r", encoding="utf-8") as f:
                        return yaml.safe_load(f) or []
                else:
                    return []
            except Exception as err:
                _LOGGER.error("Failed to read automations.yaml: %s", err)
                return []

        existing = await hass.async_add_executor_job(read_automations)

        # Check if automation already exists - if so, replace it
        existing_ids = [auto.get("id") for auto in existing if isinstance(auto, dict)]
        if turnoff_automation["id"] in existing_ids:
            _LOGGER.info(
                "Turn-off automation ID '%s' already exists - replacing with updated configuration", turnoff_automation["id"]
            )
            existing = [auto for auto in existing if isinstance(auto, dict) and auto.get("id") != turnoff_automation["id"]]

        # Add new automation
        existing.append(turnoff_automation)

        # Write back (non-blocking)
        def write_automations():
            try:
                # Atomic write
                automations_dir = os.path.dirname(automations_path)
                temp_fd, temp_path = tempfile.mkstemp(dir=automations_dir, text=True)
                try:
                    with os.fdopen(temp_fd, 'w', encoding='utf-8') as f:
                        try:
                            yaml.dump(existing, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
                        except yaml.YAMLError as err:
                            _LOGGER.error("Failed to serialize turn-off automation YAML: %s", err)
                            raise
                        except Exception as err:
                            _LOGGER.error("Unexpected error writing turn-off automation YAML: %s", err)
                            raise
                    shutil.move(temp_path, automations_path)
                except Exception:
                    if os.path.exists(temp_path):
                        os.unlink(temp_path)
                    raise
                _LOGGER.info("Created turn-off automation: %s", turnoff_automation["id"])
            except Exception as err:
                _LOGGER.error("Failed to write automations.yaml: %s", err)
                raise

        await hass.async_add_executor_job(write_automations)

        # Reload automations
        try:
            await hass.services.async_call("automation", "reload", blocking=True)
            _LOGGER.info("Reloaded automations successfully")

            # Add delay to ensure automation is registered (increased from 1s to 3s)
            await asyncio.sleep(3)

            # Verify automation was loaded by checking if entity exists
            # Note: HA creates entity_id from alias, not id
            slugified_alias = turnoff_automation['alias'].lower().replace(' ', '_').replace('-', '_')
            automation_entity_id = f"automation.{slugified_alias}"
            if hass.states.get(automation_entity_id) is None:
                _LOGGER.error("Turn-off automation entity not found after reload: %s", automation_entity_id)
                raise Exception(f"Turn-off automation failed to load: {automation_entity_id}")

            _LOGGER.info("Turn-off automation verified: %s", automation_entity_id)

        except Exception as err:
            _LOGGER.error("Failed to reload automations: %s", err)

            # Try to validate automations.yaml to provide helpful error (non-blocking)
            def validate_yaml():
                try:
                    with open(automations_path, "r", encoding="utf-8") as f:
                        yaml.safe_load(f)
                except yaml.YAMLError as yaml_err:
                    _LOGGER.error("automations.yaml has invalid YAML: %s", yaml_err)
                    raise Exception(f"Automation file corrupted - YAML error: {yaml_err}")

            await hass.async_add_executor_job(validate_yaml)
            raise

        return turnoff_automation["id"]

    def _generate_dashboard_card(self, config: dict[str, Any]) -> str:
        """Generate Mushroom card YAML for dashboard."""
        room_name = config["room_name"]
        sanitized_name = sanitize_room_name(room_name)

        # Get the climate entity (first one if multiple)
        climate_entities = config.get("climate_entities", [])
        climate_entity = climate_entities[0] if climate_entities else "climate.your_ac"

        # Only generate if control mode is enabled
        if not config.get("enable_control_mode", True):
            return ""

        control_mode_entity = f"input_select.climate_control_mode_{sanitized_name}"

        card_yaml = f"""type: custom:mushroom-select-card
entity: {control_mode_entity}
name: {room_name} Climate
icon: mdi:air-conditioner
fill_container: false
layout: horizontal
card_mod:
  style: |
    ha-card {{
      background-color: rgba(0,0,0,0.35) !important;
      border-radius: 20px !important;
      height: 56px !important;
      min-height: 56px !important;
    }}
    .primary {{
      color: white !important;
    }}
    mushroom-select {{
      --select-height: 40px !important;
    }}
    mushroom-shape-icon {{
      {{% set mode = states('{control_mode_entity}') %}}
      {{% set ac_state = states('{climate_entity}') %}}
      {{% if mode == 'Auto' %}}
        --card-mod-icon: mdi:robot;
      {{% elif mode == 'Manual' %}}
        --card-mod-icon: mdi:hand-back-right;
      {{% elif mode == 'Smart' %}}
        --card-mod-icon: mdi:brain;
      {{% else %}}
        --card-mod-icon: mdi:air-conditioner;
      {{% endif %}}

      {{% if ac_state == 'off' %}}
        --icon-color: rgb(158, 158, 158) !important;
        --shape-color: rgba(158, 158, 158, 0.2) !important;
      {{% else %}}
        {{% if mode == 'Auto' %}}
          animation: spin 3s ease-in-out infinite alternate;
        {{% elif mode == 'Manual' %}}
          animation: wave 1s ease-in-out infinite;
        {{% elif mode == 'Smart' %}}
          animation: pulse 2s ease-in-out infinite;
        {{% endif %}}
      {{% endif %}}
      display: flex;
    }}
    @keyframes spin {{
      0%, 100% {{ transform: rotate(0deg); }}
      50% {{ transform: rotate(360deg); }}
    }}
    @keyframes wave {{
      0%, 100% {{ transform: rotate(0deg); }}
      25% {{ transform: rotate(-15deg); }}
      75% {{ transform: rotate(15deg); }}
    }}
    @keyframes pulse {{
      0%, 100% {{
        transform: scale(1);
        opacity: 1;
      }}
      50% {{
        transform: scale(1.1);
        opacity: 0.8;
      }}
    }}"""

        return card_yaml

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> config_entries.OptionsFlow:
        """Get the options flow for this handler."""
        return OptionsFlowHandler(config_entry)


class OptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options flow for the integration."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage the options."""
        if user_input is not None:
            # Check if user wants to show dashboard card
            if user_input.get("show_dashboard_card", False):
                return await self.async_step_show_card()

            # Check if user wants to uninstall
            if user_input.get("uninstall_room_setup", False):
                return await self.async_step_confirm_uninstall()

            # Check if user wants to reinstall
            if user_input.get("reinstall_room_setup", False):
                return await self.async_step_confirm_reinstall()

            return self.async_create_entry(title="", data=user_input)

        # Get dashboard card if available
        has_card = bool(self.config_entry.data.get("dashboard_card_yaml"))

        schema_dict = {
            vol.Optional(
                "enable_dynamic_adaptation",
                default=self.config_entry.data.get(
                    "enable_dynamic_adaptation", True
                ),
            ): cv.boolean,
            vol.Optional(
                "enable_manual_override",
                default=self.config_entry.data.get(
                    "enable_manual_override", True
                ),
            ): cv.boolean,
            vol.Optional(
                "enable_control_mode",
                default=self.config_entry.data.get("enable_control_mode", True),
            ): cv.boolean,
            vol.Optional(
                "enable_smart_mode",
                default=self.config_entry.data.get(
                    "enable_smart_mode", True
                ),
            ): cv.boolean,
        }

        # Add option to show dashboard card if it exists
        if has_card:
            schema_dict[vol.Optional("show_dashboard_card", default=False)] = cv.boolean

        # Add uninstall and reinstall options
        schema_dict[vol.Optional("uninstall_room_setup", default=False)] = cv.boolean
        schema_dict[vol.Optional("reinstall_room_setup", default=False)] = cv.boolean

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(schema_dict),
        )

    async def async_step_show_card(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Show the dashboard card YAML."""
        dashboard_card = self.config_entry.data.get("dashboard_card_yaml", "")
        room_name = self.config_entry.data.get("room_name", "Unknown Room")

        if not dashboard_card:
            return self.async_abort(reason="no_card_available")

        # Create notification with card YAML
        await self.hass.services.async_call(
            "persistent_notification",
            "create",
            {
                "title": f"🎨 {room_name} Dashboard Card",
                "message": f"""## Dashboard Control Card for {room_name}

Copy this YAML and add it to your dashboard:

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

**Note:** Requires `mushroom` and `card-mod` custom cards (install via HACS)""",
                "notification_id": f"climate_card_{self.config_entry.entry_id}",
            },
        )

        return self.async_abort(reason="card_shown")

    async def async_step_confirm_uninstall(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Confirm uninstall of room setup."""
        room_name = self.config_entry.data.get("room_name", "Unknown Room")

        if user_input is not None:
            if user_input.get("confirm"):
                # User confirmed - proceed with uninstall
                try:
                    await self._uninstall_room_setup(self.hass, self.config_entry)
                    return self.async_abort(reason="uninstall_successful")
                except Exception as err:
                    _LOGGER.error("Error during uninstall: %s", err, exc_info=True)
                    return self.async_abort(reason="uninstall_failed")
            else:
                # User cancelled - return to options menu
                return await self.async_step_init()

        return self.async_show_form(
            step_id="confirm_uninstall",
            data_schema=vol.Schema({
                vol.Required("confirm", default=False): cv.boolean,
            }),
            description_placeholders={"room_name": room_name},
        )

    async def async_step_confirm_reinstall(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Confirm reinstall of room setup."""
        room_name = self.config_entry.data.get("room_name", "Unknown Room")

        if user_input is not None:
            if user_input.get("confirm"):
                # User confirmed - uninstall then trigger new setup
                try:
                    await self._uninstall_room_setup(self.hass, self.config_entry)
                    # Abort with special reason that triggers reinstall
                    return self.async_abort(reason="reinstall_complete")
                except Exception as err:
                    _LOGGER.error("Error during reinstall: %s", err, exc_info=True)
                    return self.async_abort(reason="reinstall_failed")
            else:
                # User cancelled - return to options menu
                return await self.async_step_init()

        return self.async_show_form(
            step_id="confirm_reinstall",
            data_schema=vol.Schema({
                vol.Required("confirm", default=False): cv.boolean,
            }),
            description_placeholders={"room_name": room_name},
        )

    @staticmethod
    async def _uninstall_room_setup(hass: HomeAssistant, config_entry: config_entries.ConfigEntry) -> None:
        """Uninstall all entities and automations for this room setup."""
        room_name = config_entry.data.get("room_name", "Unknown Room")
        sanitized_name = room_name.lower().replace(" ", "_").replace("-", "_")

        _LOGGER.info("Starting uninstall for room: %s", room_name)

        # Step 1: Delete helper entities
        helpers_to_delete = [
            # Always created
            f"input_text.climate_last_mode_{sanitized_name}",
            f"input_datetime.climate_last_change_{sanitized_name}",
        ]

        # Conditional helpers
        if config_entry.data.get("enable_control_mode", True):
            helpers_to_delete.append(f"input_select.climate_control_mode_{sanitized_name}")

        if config_entry.data.get("enable_smart_mode", True):
            helpers_to_delete.extend([
                f"input_datetime.climate_presence_detected_{sanitized_name}",
                f"input_boolean.climate_proximity_override_{sanitized_name}",
            ])

        if config_entry.data.get("enable_dynamic_adaptation", True):
            helpers_to_delete.extend([
                f"input_number.climate_temp_history_{sanitized_name}",
                f"input_text.climate_trend_direction_{sanitized_name}",
                f"input_datetime.climate_mode_start_time_{sanitized_name}",
                f"input_number.climate_effectiveness_score_{sanitized_name}",
                f"input_datetime.climate_temp_stable_since_{sanitized_name}",
                f"input_text.climate_last_transition_{sanitized_name}",
            ])

        # Delete each helper entity
        for helper_id in helpers_to_delete:
            try:
                domain, entity_id_part = helper_id.split(".", 1)
                await hass.services.async_call(
                    domain,
                    "remove",
                    {"entity_id": helper_id},
                    blocking=True,
                )
                _LOGGER.info("Deleted helper: %s", helper_id)
            except Exception as err:
                _LOGGER.warning("Failed to delete helper %s: %s", helper_id, err)

        # Step 2: Delete automations from automations.yaml
        automations_file = hass.config.path("automations.yaml")

        # Automation IDs to delete
        main_automation_id = f"climate_control_{sanitized_name}"
        turnoff_automation_id = f"climate_turnoff_{sanitized_name}"

        def delete_automations():
            try:
                if os.path.exists(automations_file):
                    with open(automations_file, "r", encoding="utf-8") as f:
                        automations = yaml.safe_load(f) or []

                    # Filter out automations for this room
                    original_count = len(automations)
                    automations = [
                        a for a in automations
                        if a.get("id") not in [main_automation_id, turnoff_automation_id]
                    ]
                    deleted_count = original_count - len(automations)

                    if deleted_count > 0:
                        # Write back to file atomically
                        fd, temp_file = tempfile.mkstemp(
                            dir=os.path.dirname(automations_file),
                            prefix=".automations_",
                            suffix=".yaml",
                            text=True
                        )
                        try:
                            with os.fdopen(fd, "w", encoding="utf-8") as f:
                                yaml.dump(automations, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
                            shutil.move(temp_file, automations_file)
                            _LOGGER.info("Deleted %d automation(s) for room: %s", deleted_count, room_name)
                        except Exception:
                            if os.path.exists(temp_file):
                                os.unlink(temp_file)
                            raise
                    else:
                        _LOGGER.warning("No automations found to delete for room: %s", room_name)
            except Exception as err:
                _LOGGER.error("Failed to delete automations: %s", err)
                raise

        await hass.async_add_executor_job(delete_automations)

        # Step 3: Reload automation integration
        await hass.services.async_call("automation", "reload", blocking=True)
        _LOGGER.info("Reloaded automations after deletion")

        # Step 4: Delete helpers package file (if exists)
        package_file = hass.config.path(f"packages/climate_helpers_{sanitized_name}.yaml")

        def delete_package():
            try:
                if os.path.exists(package_file):
                    os.remove(package_file)
                    _LOGGER.info("Deleted package file: %s", package_file)
                else:
                    _LOGGER.info("Package file not found (may not exist): %s", package_file)
            except Exception as err:
                _LOGGER.warning("Failed to delete package file: %s", err)

        await hass.async_add_executor_job(delete_package)

        # Step 5: Remove config entry
        await hass.config_entries.async_remove(config_entry.entry_id)
        _LOGGER.info("Removed config entry for room: %s", room_name)

        _LOGGER.info("Uninstall complete for room: %s", room_name)