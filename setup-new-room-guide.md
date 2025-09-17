# Setting Up Ultimate Smart Climate Control v2.22.14

This guide explains how to set up the Ultimate Smart Climate Control blueprint for new rooms. This system provides advanced 3-tier temperature control with intelligent escalation and presence detection.

## Quick Setup Overview

The Ultimate Smart Climate Control blueprint is designed for easy setup with minimal configuration. Each room requires:
1. **Climate entities** (your A/C units)
2. **Helper entities** for automation state tracking
3. **Blueprint automation** configured for the room

## Step 1: Install the Blueprint

### Option A: Direct Import (Recommended)
1. Go to **Settings > Automations & Scenes > Blueprints**
2. Click **Import Blueprint**
3. Enter URL: `https://github.com/Chris971991/Smart-Climate-Control/blob/main/ultimate_climate_control.yaml`
4. Click **Preview Blueprint** → **Import Blueprint**

### Option B: Manual Download
1. Download `ultimate_climate_control.yaml` from GitHub
2. Go to **Settings > Automations & Scenes > Blueprints**
3. Click **Import Blueprint** → **Upload** and select the file

## Step 2: Required Helper Entities

For each room, create these helper entities in **Settings > Devices & Services > Helpers**:

### Essential Helpers (Required)
1. **Control Mode Selector**
   - Type: **Dropdown**
   - Name: `Climate Control Mode [Room Name]`
   - Entity ID: `input_select.climate_control_mode_[room]`
   - Options: `Auto`, `Manual`, `Smart`
   - Icon: `mdi:air-conditioner`

2. **Last Mode Tracker**
   - Type: **Text**
   - Name: `[Room Name] Climate Last Mode`
   - Entity ID: `input_text.climate_last_mode_[room]`
   - Max Length: 50

3. **Last Change Timestamp**
   - Type: **Date & Time**
   - Name: `[Room Name] Climate Last Change`
   - Entity ID: `input_datetime.climate_last_change_[room]`

### Optional Helpers (For Advanced Features)
4. **Temperature History** (for effectiveness tracking)
   - Type: **Number**
   - Name: `[Room Name] Temperature History`
   - Entity ID: `input_number.temp_history_[room]`
   - Min: 0, Max: 50, Step: 0.1

5. **Override Status** (for manual override detection)
   - Type: **Toggle**
   - Name: `[Room Name] Manual Override`
   - Entity ID: `input_boolean.manual_override_[room]`

## Step 3: Create Blueprint Automation

1. Go to **Settings > Automations & Scenes > Automations**
2. Click **Create Automation** → **Use Blueprint**
3. Select **Ultimate Smart Climate Control**
4. Configure the automation:

### Basic Configuration
- **Room Name**: `Office` (display name)
- **Climate Entities**: Select your A/C unit(s)
- **Target Temperature**: `22°C` (your preferred temperature)
- **Control Mode Helper**: `input_select.climate_control_mode_office`
- **Last Mode Helper**: `input_text.climate_last_mode_office`
- **Last Change Helper**: `input_datetime.climate_last_change_office`

### Advanced Settings (Optional)
- **Temperature Sensor**: External sensor (if available)
- **Presence Sensors**: Motion, BLE, or other occupancy sensors
- **Temperature History Helper**: `input_number.temp_history_office`
- **Manual Override Helper**: `input_boolean.manual_override_office`

## Step 4: Test the Setup

1. **Save** the automation
2. Check the **Traces** tab for any errors
3. Test different control modes:
   - **Auto**: Temperature-based automation
   - **Smart**: Room presence detection + automation
   - **Manual**: Full user control

## Control Mode Behavior

### Auto Mode
- **Temperature-based automation** with home/away detection
- AC activates based on temperature thresholds
- Global presence detection for energy saving

### Smart Mode
- **Room-specific presence detection**
- Advanced occupancy sensing with multiple sensors
- Predictive cooling/heating based on room usage

### Manual Mode
- **Full user control** with no automation
- Emergency temperature overrides only
- Complete manual A/C operation

## Temperature Control System

The blueprint automatically configures **3-tier temperature control**:

### Example (22°C target, ±2°C comfort zone):
- **Comfort Zone**: 20.0-24.0°C (AC off for energy saving)
- **Cooling LOW**: 24.1°C (gentle cooling, minimal fan)
- **Cooling MEDIUM**: 25.0°C (balanced cooling, medium fan)
- **Cooling HIGH**: 26.0°C (maximum cooling, high fan)
- **Heating LOW**: 19.9°C (gentle heating, minimal fan)
- **Heating MEDIUM**: 19.0°C (balanced heating, medium fan)
- **Heating HIGH**: 18.0°C (maximum heating, high fan)

## Advanced Features

### Intelligent Escalation (v2.22.14)
- **Performance tracking** adjusts fan speeds based on effectiveness
- **Near-target stall detection** prevents getting stuck near target
- **Progressive escalation**: Level 1 → 2 → 3 → 4 based on performance
- **Smart de-escalation** reduces power as target approaches

### Universal A/C Compatibility
- **Auto-detects** available fan speeds and HVAC modes
- **Adapts** to different brands: Daikin, Mitsubishi, LG, Generic
- **Supports** all fan speeds: Level 1-5, Auto, Quiet, Silence

## Example Complete Setup

### Office Room Setup
```yaml
# Helper Entities
input_select.climate_control_mode_office
input_text.climate_last_mode_office
input_datetime.climate_last_change_office
input_number.temp_history_office
input_boolean.manual_override_office

# Automation Configuration
Room Name: Office
Climate Entities: climate.office_ac
Target Temperature: 22
Control Mode Helper: input_select.climate_control_mode_office
```

## Troubleshooting

### Common Issues
- **Automation not triggering**: Check helper entity IDs match exactly
- **Template errors in logs**: Ensure all required helpers are created
- **Fan speed not changing**: Verify A/C unit supports multiple fan modes
- **Manual override stuck**: Check manual override helper toggle state

### Debug Logging
Enable debug logging in the blueprint configuration to see detailed system operation, including:
- Temperature thresholds and decisions
- Fan speed selection logic
- Escalation/de-escalation actions
- Presence detection results

### Getting Help
- **Issues**: [GitHub Issues](https://github.com/Chris971991/Smart-Climate-Control/issues)
- **Documentation**: [README.md](https://github.com/Chris971991/Smart-Climate-Control/blob/main/README.md)
- **Latest Version**: Always use the direct import URL for updates

## Multiple Rooms

For multiple rooms, repeat Steps 2-3 for each room with unique helper entity names:
- `input_select.climate_control_mode_living_room`
- `input_select.climate_control_mode_bedroom`
- `input_select.climate_control_mode_kitchen`

Each room operates independently with its own configuration and automation.