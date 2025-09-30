"""Config flow for Smart Climate Helper Creator integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant, callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import entity_registry as er
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

DOMAIN = "smart_climate_helper_creator"

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
        "initial": "Auto",
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
    """Handle a config flow for Smart Climate Helper Creator."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            room_name = user_input["room_name"]
            sanitized_name = sanitize_room_name(room_name)

            # Check if this room already exists
            await self.async_set_unique_id(f"climate_helpers_{sanitized_name}")
            self._abort_if_unique_id_configured()

            # Store user input for next step
            self.context["user_input"] = user_input
            return await self.async_step_features()

        data_schema = vol.Schema(
            {
                vol.Required("room_name"): cv.string,
            }
        )

        return self.async_show_form(
            step_id="user", data_schema=data_schema, errors=errors
        )

    async def async_step_features(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the features selection step."""
        errors = {}

        if user_input is not None:
            # Merge with previous input
            room_input = self.context["user_input"]
            room_input.update(user_input)

            # Create all helpers
            try:
                await self._create_helpers(self.hass, room_input)

                # Create config entry
                return self.async_create_entry(
                    title=f"{room_input['room_name']} Climate Helpers",
                    data=room_input,
                )
            except Exception as err:
                _LOGGER.error("Error creating helpers: %s", err)
                errors["base"] = "create_failed"

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
                "room_name": self.context["user_input"]["room_name"]
            },
        )

    async def _create_helpers(
        self, hass: HomeAssistant, config: dict[str, Any]
    ) -> None:
        """Create all required helper entities."""
        room_name = config["room_name"]
        sanitized_name = sanitize_room_name(room_name)

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

        # Create each helper
        created_helpers = []
        for helper_key in helpers_to_create:
            helper_def = HELPER_DEFINITIONS[helper_key]
            entity_id = f"{helper_def['domain']}.climate_{helper_key}_{sanitized_name}"

            # Prepare service data
            service_data = {
                "name": helper_def["name"].format(room=room_name),
                "icon": helper_def.get("icon"),
            }

            # Add domain-specific attributes
            if helper_def["domain"] == "input_text":
                service_data["initial"] = helper_def.get("initial", "")
                service_data["max"] = helper_def.get("max_length", 255)

            elif helper_def["domain"] == "input_datetime":
                service_data["has_date"] = helper_def.get("has_date", True)
                service_data["has_time"] = helper_def.get("has_time", True)

            elif helper_def["domain"] == "input_number":
                service_data["min"] = helper_def.get("min", 0)
                service_data["max"] = helper_def.get("max", 100)
                service_data["step"] = helper_def.get("step", 1)
                service_data["initial"] = helper_def.get("initial", 0)
                service_data["mode"] = helper_def.get("mode", "box")
                if "unit_of_measurement" in helper_def:
                    service_data["unit_of_measurement"] = helper_def[
                        "unit_of_measurement"
                    ]

            elif helper_def["domain"] == "input_boolean":
                service_data["initial"] = helper_def.get("initial", False)

            elif helper_def["domain"] == "input_select":
                service_data["options"] = helper_def.get("options", [])
                service_data["initial"] = helper_def.get("initial")

            # Call the service to create the helper
            try:
                await hass.services.async_call(
                    helper_def["domain"],
                    "create",
                    service_data,
                    blocking=True,
                )
                created_helpers.append(entity_id)
                _LOGGER.info("Created helper: %s", entity_id)
            except Exception as err:
                _LOGGER.error("Failed to create helper %s: %s", entity_id, err)
                raise

        _LOGGER.info(
            "Successfully created %d helpers for room: %s",
            len(created_helpers),
            room_name,
        )

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
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
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
            ),
        )