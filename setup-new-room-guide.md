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

### Required Configuration

#### Basic Settings
- **Room Name**: `Office` (display name used for logging and BLE detection)
- **Climate Entities**: Select your A/C unit(s) - supports multiple units
- **Last Mode Helper**: `input_text.climate_last_mode_office` (tracks automation state)
- **Last Change Helper**: `input_datetime.climate_last_change_office` (tracks timing)

#### Temperature Settings
- **Target Temperature**: `22°C` (your ideal room temperature)
- **Comfort Zone Range**: `±2°C` (temperature tolerance around target)
- **Enable Heating Mode**: `ON` (allows heating when cold)
- **Enable Cooling Mode**: `ON` (allows cooling when hot)
- **Response Aggressiveness**: `2 - Smooth` (how quickly system responds)

### Optional Configuration

#### Temperature Sensors
- **Temperature Sensor**: External sensor for more accurate readings
- **Use Average Temperature**: `ON` for multiple A/C units, `OFF` with external sensor

#### Advanced Temperature Controls
Enable **Advanced Temperature Controls** for precise threshold control:
- **Comfort Zone Min/Max**: Override automatic comfort zone calculation
- **Cooling/Heating Targets**: Set specific target temperatures for each mode
- **Low/Medium/High Thresholds**: Customize when each intensity level activates

#### Control Mode Integration
- **Control Mode Helper**: `input_select.climate_control_mode_office` (Auto/Manual/Smart selector)
- **Last Presence Helper**: `input_datetime.presence_last_detected_office` (Smart mode)
- **Proximity Override Helper**: `input_boolean.climate_proximity_override_office` (emergency override)

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

---

## 📋 Complete Configuration Reference

### 🌡️ Temperature Settings

#### Target Temperature
Your ideal room temperature that serves as the baseline for all calculations.
- **Range**: 18°C - 28°C
- **Default**: 23°C
- **Impact**: All other thresholds adjust proportionally when you change this

#### Comfort Zone Range (±°C)
Temperature tolerance around your target where the AC stays off for energy savings.
- **Range**: ±0.5°C - ±3°C
- **Default**: ±2°C
- **Examples**:
  - **±1°C**: Tight control (22-24°C), more activity, less efficient
  - **±2°C**: Balanced control (21-25°C), good efficiency (saves 40-60% energy)
  - **±3°C**: Loose control (20-26°C), very efficient, may feel less consistent

#### Response Aggressiveness
How quickly the system escalates to higher power modes beyond the comfort zone.
- **1 - Gentle**: Extreme modes at ±3°C from comfort (very efficient, slow response)
- **2 - Smooth**: Medium at comfort edge, high at +1°C, max at +2°C (recommended)
- **3 - Balanced**: Extreme modes at ±2°C from comfort (balanced efficiency/speed)
- **4 - Responsive**: Faster escalation for quicker temperature control
- **5 - Aggressive**: Immediate maximum power for fastest response

#### Heating/Cooling Mode Enable
Control which modes are allowed to activate.
- **Use Cases**:
  - **Both ON**: Full climate control (recommended)
  - **Cooling OFF**: Heating only (winter operation, cold climates)
  - **Heating OFF**: Cooling only (hot climates, people who run hot)
  - **Seasonal Control**: Disable unused modes for energy savings

### 📡 Presence & Proximity Settings

#### People to Track
Select person entities for home/away detection and proximity-based features.
- **Used For**: Away mode activation, pre-conditioning when approaching
- **Best Practice**: Include all household members for accurate detection

#### Presence Detection Devices
Additional sensors to supplement person presence detection.
- **Examples**:
  - Computer power states (`binary_sensor.pc_power`)
  - Smart TV status (`media_player.living_room_tv`)
  - Phone charging sensors (`binary_sensor.phone_charging`)
- **Purpose**: More accurate home/away detection when person entities aren't reliable

#### Proximity & Direction Sensors
Requires Home Assistant proximity integration setup.
- **Proximity Sensor**: Distance from home (`sensor.home_nearest_distance`)
- **Direction Sensor**: Travel direction (`sensor.home_nearest_direction_of_travel`)
- **States**: `towards`, `away`, `stationary`, `arrived`
- **Setup**: Settings → Integrations → Add → Proximity

#### Home Zone Distance
Defines your "home zone" boundary for proximity-based automation.
- **Range**: 1000m - 10000m
- **Default**: 5000m (5km)
- **Behavior**:
  - **Within zone**: Maintain comfort temperature
  - **Outside zone**: Switch to away mode
  - **Approaching**: Start pre-conditioning

### 🏠 Away Mode Settings

#### Away Mode Action
What happens when everyone leaves home:
- **OFF**: Complete shutdown (maximum energy savings, slow recovery)
- **ECO**: Wider temperature tolerance (balanced savings, moderate recovery)
- **MAINTAIN**: Keep current temperature (minimal savings, instant comfort)

#### Pre-conditioning
Starts cooling/heating before you arrive home.
- **Trigger**: Direction sensor shows "towards" + within approach distance
- **Benefit**: Room is comfortable immediately upon arrival
- **Requirement**: Proximity and direction sensors configured

### 🧠 Smart Mode Settings

#### Control Mode Helper
Input select with three options for mode switching:
- **Auto**: Temperature-based automation with global presence
- **Manual**: Full user control, no automation
- **Smart**: Room-specific presence detection with advanced features

#### Room Presence Sensors
Sensors specific to this room for Smart mode operation:
- **Motion Sensors**: PIR, mmWave (`binary_sensor.office_motion`)
- **BLE Sensors**: Phone presence (`sensor.phone_ble_area`)
- **Door Sensors**: Room entry/exit (`binary_sensor.office_door`)
- **Other**: Any sensor indicating room occupancy

#### Presence Validation Modes
How multiple sensors are interpreted:
- **ANY**: Any sensor triggers (most responsive, may have false positives)
- **ALL**: All sensors must agree (most accurate, may miss brief presence)
- **SMART**: BLE + Motion validation (prevents false triggers from adjacent rooms)
- **MAJORITY**: Most sensors must agree (requires 3+ sensors)
- **BLE_PLUS**: BLE + at least one other sensor (good for open floor plans)

#### Adjacent Room Names
For open-plan spaces where BLE might detect you in nearby areas:
- **Format**: Comma-separated list: `Kitchen, Dining, Living Room`
- **Purpose**: AC activates when BLE detects you in main room OR adjacent rooms
- **Example**: Living room AC turns on when detected in Kitchen (open plan)

### 🔧 Dynamic Adaptation Settings

#### Effectiveness Check Interval
How often the system evaluates performance and adjusts power levels:
- **Range**: 3-15 minutes
- **Default**: 5 minutes
- **Impact**: Shorter intervals = more responsive escalation/de-escalation

#### Override Timeout
How long manual override protection lasts after manual changes:
- **Options**: 30min, 1h, 2h, 4h, 8h, 12h, 24h
- **Default**: 4 hours
- **Purpose**: Prevents automation from immediately overriding your manual adjustments

#### Escalation/De-escalation Thresholds
Fine-tune when the system increases or decreases power:
- **Escalation Threshold**: Distance from target that triggers power increases
- **De-escalation Threshold**: How close to target before reducing power
- **Effectiveness Threshold**: Minimum performance level before escalating

### 🏢 Multi-Zone Settings

#### Fan Speed Control
Universal compatibility with different A/C brands:
- **Auto-Detection**: System reads available fan modes from your A/C
- **Supported**: Level 1-5, Auto, Quiet, Silence, Low/Medium/High
- **Fallback**: Uses Auto mode if specific speeds unavailable

#### Temperature Averaging
For multiple A/C units in the same room:
- **ON**: Average temperature from all units (recommended for multiple units)
- **OFF**: Use first unit only (recommended with external sensor)

### 🔍 Debug & Monitoring

#### Debug Logging
Enable detailed logging for troubleshooting:
- **Content**: Temperature decisions, fan speed selection, presence detection
- **Location**: Settings → System → Logs (search for your room name)
- **Performance**: Minimal impact, safe to leave enabled

#### Helper Entity Monitoring
Track automation behavior through helper entities:
- **Last Mode**: Shows current automation state
- **Last Change**: Timestamp of last automation action
- **Temperature History**: Used for effectiveness calculations
- **Manual Override**: Shows when manual override is active

---

## 🎯 Configuration Examples

### Basic Setup (Minimal Configuration)
```yaml
Room Name: Office
Climate Entities: climate.office_ac
Target Temperature: 22°C
Comfort Zone Range: ±2°C
Control Mode Helper: input_select.climate_control_mode_office
Last Mode Helper: input_text.climate_last_mode_office
Last Change Helper: input_datetime.climate_last_change_office
```

### Advanced Setup (Full Features)
```yaml
# Basic Settings
Room Name: Living Room
Climate Entities: [climate.living_room_ac1, climate.living_room_ac2]
Temperature Sensor: sensor.living_room_temperature
Use Average Temperature: ON

# Temperature Control
Target Temperature: 23°C
Comfort Zone Range: ±1.5°C
Response Aggressiveness: 3 - Balanced
Enable Heating: ON
Enable Cooling: ON

# Smart Mode
Control Mode Helper: input_select.climate_control_mode_living_room
Room Presence Sensors: [binary_sensor.living_room_motion, sensor.phone_ble_area]
Presence Validation: SMART
Adjacent Room Names: Kitchen, Dining

# Presence & Proximity
People to Track: [person.john, person.jane]
Proximity Sensor: sensor.home_nearest_distance
Direction Sensor: sensor.home_nearest_direction_of_travel
Home Zone Distance: 3000m

# Away Mode
Away Mode Action: ECO
Enable Pre-conditioning: ON

# Dynamic Adaptation
Effectiveness Check Interval: 5 minutes
Override Timeout: 4 hours
Enable Debug Logging: ON
```

### Cooling-Only Setup (Hot Climate)
```yaml
Room Name: Bedroom
Climate Entities: climate.bedroom_ac
Target Temperature: 24°C
Comfort Zone Range: ±2°C
Enable Heating: OFF  # Cooling only
Enable Cooling: ON
Response Aggressiveness: 4 - Responsive  # Quick cooling
Away Mode Action: OFF  # Complete shutdown when away
```

### Multi-Zone Setup (Large Room)
```yaml
Room Name: Open Plan Living
Climate Entities: [climate.living_ac, climate.dining_ac, climate.kitchen_ac]
Temperature Sensor: sensor.central_living_temperature
Use Average Temperature: OFF  # Use external sensor
Target Temperature: 22°C
Adjacent Room Names: Kitchen, Dining, Family Room
Presence Validation: MAJORITY  # Multiple sensors
```