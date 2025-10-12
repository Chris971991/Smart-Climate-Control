# Ultimate Smart Climate Control Blueprint

## 🎉 NEW: Automated Setup Wizard!

**The easiest way to set up climate control just got even easier!** Install the companion **Smart Climate Control Setup Wizard** HACS integration for:

✅ **2-Minute Setup** - Complete room configuration in ~2 minutes (vs 30-60 minutes manual)
✅ **Zero Manual Helper Creation** - All 13 helper entities created automatically
✅ **Automatic Packages Configuration** - Wizard adds packages support to your configuration.yaml
✅ **Blueprint Automation Created** - Complete automation configured and ready to use
✅ **Dashboard Card Generator** - Auto-generates animated Mushroom card YAML for mode control
✅ **Safe & Non-Destructive** - Won't affect existing helpers or automations

**Installation:** See [Setup Wizard Installation](#setup-wizard-installation-method-1-recommended) below!

---

## Overview
A comprehensive Home Assistant blueprint for advanced climate control featuring **complete 3-tier temperature escalation**, intelligent presence detection, power efficiency optimization, and extensive customization options. This system provides automated climate management with LOW/MEDIUM/HIGH heating and cooling modes, smart fan speed control, and sophisticated presence-based automation.

## Key Features

### 🌡️ **Complete 3-Tier Temperature System with Stall Detection (v2.22.15)**
- **Intelligent Escalation**: LOW → MEDIUM → HIGH for both heating and cooling
- **Near-Target Stall Detection**: Automatically detects when system gets stuck close to target
- **Dynamic Escalation Logic**: Increases power when progress stalls for extended periods
- **Smart Priority System**: Escalation overrides de-escalation during stall scenarios
- **Graduated Fan Speeds**: Automatic selection from gentle to maximum power
- **Smart Thresholds**: Outside temperature compensation makes AC work harder on extreme days
- **Precise Control**: Temperature boundaries with hysteresis to prevent oscillation
- **Example Configuration (22°C target, ±2°C comfort zone)**:
  - **Comfort Zone**: 20-24°C (Eco/Off mode for energy savings)
  - **Cooling LOW**: 24.1°C (gentle, minimal fan speed)
  - **Cooling MEDIUM**: 25.0°C (balanced cooling, medium fan)
  - **Cooling HIGH**: 26.0°C (maximum cooling, high fan speed)
  - **Heating LOW**: 19.9°C (gentle, minimal fan speed)
  - **Heating MEDIUM**: 19.0°C (balanced heating, medium fan)
  - **Heating HIGH**: 18.0°C (maximum heating, high fan speed)

### 🎯 Advanced Features & Customization
- **Multi-Zone Control**: Manage 1 or multiple A/C units with synchronized operation
- **Smart Presence Detection**: Multiple validation modes (ANY/ALL/SMART/MAJORITY/BLE_PLUS)
- **6 Temperature Thresholds**: Fully configurable LOW/MEDIUM/HIGH for heating and cooling
- **Dynamic Fan Speed Selection**: Automatically matches your A/C unit's capabilities
- **Outside Temperature Compensation (v3.2.0)**: Makes AC work HARDER on extreme days to achieve your target (not change it)
- **Time-Based Scheduling**: Different temperatures for morning/day/evening/night
- **Window Detection**: Automatic AC shutdown when doors/windows open
- **Temperature Stability Detection**: Auto-off when equilibrium reached
- **Adaptive Control Mode**: Automatic mode switching based on room occupancy
- **Comprehensive Notifications**: Customizable alerts for all system actions

### 🧠 Intelligent Control Modes
- **Auto Mode**: Complete automation with temperature-based control and presence detection
- **Manual Mode**: User control with emergency temperature overrides only
- **Smart Mode**: Advanced automation with room-specific presence sensors and timeout logic
- **Adaptive Mode**: Automatically switches between Auto/Smart/Manual based on occupancy patterns

### 📡 Advanced Presence Detection
- **Multiple Sensor Types**: BLE, PIR, mmWave, door sensors, device presence
- **Validation Modes**: 
  - ANY: Any sensor triggers (most responsive)
  - ALL: All sensors must agree (most accurate)
  - SMART: BLE + Motion validation (prevents false triggers)
  - MAJORITY: Most sensors must agree (3+ sensors)
  - BLE_PLUS: BLE + at least one other sensor
- **Presence Timeout**: Configurable delay (5-120 min) before actions
- **Room-Specific Logic**: Each room can have different presence behavior

### 🎯 **Advanced Stall Detection & Recovery (NEW in v2.22.5)**
- **Near-Target Stall Detection**: Identifies when system is stuck ≤0.8°C from target for 15+ minutes
- **Intelligent Escalation Override**: Level 1 escalation takes priority over maximum de-escalation during stalls
- **Reduced De-escalation Sensitivity**: Level 3 (minimum power) now triggers at ≤0.3°C (was 0.5°C)
- **Smart Priority Logic**: Prevents "Silence" mode from blocking final temperature approach
- **Progressive Recovery**: Gentle power increase (Level 2 de-escalation) instead of maximum reduction
- **Real-World Example**: System stuck at 22.4°C → 22.0°C for 50+ minutes now escalates to complete cooling

### ⚡ Power Efficiency & Energy Savings

#### Advanced Energy Optimization Features

1. **Smart Temperature Stability Detection**
   - Automatically turns off when temperature equilibrium reached
   - Monitors temperature stability within tolerance (±0.3°C default)
   - Configurable stability duration (10-30 minutes)
   - Saves energy while maintaining comfort

2. **3-Tier Graduated Response**
   - LOW mode: Gentle operation with minimal power consumption
   - MEDIUM mode: Balanced efficiency and performance
   - HIGH mode: Maximum power only when necessary
   - Prevents over-cooling/heating and energy waste

3. **Dynamic Effectiveness Tracking**
   - Monitors system performance and adjusts power accordingly
   - Escalates power when progress stalls
   - De-escalates when approaching target temperature
   - Learns your AC's effectiveness over time

4. **Comfort Zone Operation**
   - Eco mode or complete shutdown within comfort zone
   - Saves 40-60% energy compared to constant operation
   - Configurable eco mode with setpoint offset
   - Outside temperature compensation for extreme conditions

5. **Runtime Protection & Hysteresis**
   - Minimum runtime and off-time protection
   - Temperature hysteresis prevents rapid cycling
   - Gradual temperature adjustments reduce overshooting
   - Extends equipment lifespan

## Installation Guide

### Method 1: Setup Wizard Installation (⭐ RECOMMENDED - Automated!)

The **Smart Climate Control Setup Wizard** is a complete 5-step guided setup that creates EVERYTHING automatically - helpers AND automation! No manual configuration needed!

#### Step 1: Install Setup Wizard via HACS
1. Open HACS in Home Assistant
2. Go to **Integrations**
3. Click ⋮ Menu (top right) → **Custom Repositories**
4. Add repository:
   - **URL**: `https://github.com/Chris971991/Smart-Climate-Control`
   - **Category**: Integration
5. Click **Add**
6. Find "Smart Climate Control Setup Wizard" and click **Download**
7. **Restart Home Assistant**

#### Step 2: Run the Automated Setup Wizard
1. Go to Settings → Devices & Services
2. Click **Add Integration**
3. Search for "Smart Climate Control Setup Wizard"
4. **The wizard will automatically:**
   - Check if packages are configured in configuration.yaml
   - **Add packages configuration automatically if missing** (restart required)
   - After restart, guide you through 5-step room setup:

**5-Step Wizard Process:**
- **Step 0 (Automatic):** Checks/adds packages configuration to configuration.yaml
- **Step 1:** Enter room name (e.g., "Master Bedroom", "Living Room")
- **Step 2:** Select features (all recommended - Dynamic Adaptation, Manual Override, Control Mode, Smart Mode)
- **Step 3:** Select your A/C units (supports multiple units per room)
- **Step 4:** Select optional sensors:
  - Temperature sensor for accurate readings
  - BLE sensors (e.g., sensor.phone_ble_area)
  - Motion sensors (PIR, mmWave)
  - Any occupancy detection sensors
- **Step 5:** Configure temperature settings (target temp, comfort zone, enable heating/cooling)
5. Click **Submit** - Everything created automatically!

**What gets created automatically:**
- ✅ Packages configuration in configuration.yaml (if needed)
- ✅ All 13 helper entities in /config/packages/climate_control_[room].yaml
- ✅ Complete blueprint automation in automations.yaml
- ✅ Dashboard card YAML (animated Mushroom card for mode control)
- ✅ Fully configured and ready to use!

**Features:**
- 🛡️ **Safe & Non-Destructive:** Won't affect existing helpers or automations
- 📦 **Package-Based Helpers:** Clean, isolated helper entities
- 🎨 **Dashboard Card:** Auto-generated animated Mushroom card YAML
- ♻️ **Reload Services:** Helpers available immediately (no full restart needed)
- 🔄 **Repeatable:** Set up multiple rooms easily

**Repeat for each room you want to control.**

**✅ Total Time: ~2 minutes per room vs 30-60 minutes manual setup!**

---

### Method 2: Manual Installation (Advanced Users)

#### Step 1: Blueprint Installation

**Option A: Direct Import (Recommended)**
1. Go to Settings → Automations & Scenes → Blueprints Tab
2. Click "Import Blueprint"
3. Paste this URL: `https://github.com/Chris971991/Smart-Climate-Control/blob/main/ultimate_climate_control.yaml`
4. Click "Preview Blueprint" then "Import Blueprint"

**Option B: Manual Installation**
1. Download `ultimate_climate_control.yaml`
2. Place in your Home Assistant config directory:
   ```
   config/blueprints/automation/ultimate_climate_control.yaml
   ```
3. Restart Home Assistant
4. Go to Settings → Automations → Blueprints → Import Blueprint

#### Step 2: Required Helper Entities
**⚠️ CRITICAL: Each automation instance (room) needs its own unique set of helpers**

Create via Settings → Devices & Services → Helpers → Create Helper

#### Basic Helpers (Required for ALL rooms):
```yaml
# ⚠️ REPLACE [room_name] with your actual room name (see naming guide below)
# Example: [room_name] = living_room, bedroom, office, etc.

1. Input Text Helper:
   Name: climate_last_mode_[room_name]
   Entity ID: input_text.climate_last_mode_[room_name]
   Icon: mdi:air-conditioner
   Purpose: Tracks the last active climate mode

2. Input DateTime Helper:
   Name: climate_last_change_[room_name] 
   Entity ID: input_datetime.climate_last_change_[room_name]
   Has Date: ✅ YES (Required)
   Has Time: ✅ YES (Required)
   Icon: mdi:clock-outline
   Purpose: Tracks when climate changes occurred for timing calculations
```

#### Smart/Adaptive Mode Helpers (Required for Smart/Adaptive modes):
```yaml
# ⚠️ REPLACE [room_name] with your actual room name

3. Input Select Helper:
   Name: climate_control_mode_[room_name]
   Entity ID: input_select.climate_control_mode_[room_name]
   Options: ["Auto", "Manual", "Smart"] (exactly as shown)
   Icon: mdi:tune-vertical
   Purpose: Controls which automation mode is active

4. Input DateTime Helper:
   Name: presence_last_detected_[room_name]
   Entity ID: input_datetime.presence_last_detected_[room_name]
   Has Date: ✅ YES (Required)
   Has Time: ✅ YES (Required)  
   Icon: mdi:account-clock
   Purpose: Tracks when presence was last detected for timeout calculations

5. Input Boolean Helper:
   Name: climate_proximity_override_[room_name]
   Entity ID: input_boolean.climate_proximity_override_[room_name]
   Icon: mdi:toggle-switch
   Purpose: Emergency override to bypass all automation
```

#### Advanced Feature Helpers (Optional but Recommended):
```yaml
# ⚠️ REPLACE [room_name] with your actual room name
# Dynamic Adaptation & Effectiveness Tracking

6. Input Number Helper:
   Name: climate_temp_history_[room_name]
   Entity ID: input_number.climate_temp_history_[room_name]
   Min: 0, Max: 50, Step: 0.1
   Unit: °C
   Purpose: Stores previous temperature for trend analysis

7. Input Number Helper:
   Name: climate_effectiveness_score_[room_name] 
   Entity ID: input_number.climate_effectiveness_score_[room_name]
   Min: 0, Max: 100, Step: 0.1
   Unit: %
   Purpose: Tracks how well the current mode is working (0-100%)

8. Input Text Helper:
   Name: climate_trend_direction_[room_name]
   Entity ID: input_text.climate_trend_direction_[room_name]
   Purpose: Tracks if temperature is rising/falling/stable

9. Input DateTime Helper:
   Name: climate_mode_start_time_[room_name]
   Entity ID: input_datetime.climate_mode_start_time_[room_name]  
   Has Date: ✅ YES, Has Time: ✅ YES
   Purpose: Tracks when current climate mode started

10. Input DateTime Helper:
    Name: temp_stable_since_[room_name]
    Entity ID: input_datetime.temp_stable_since_[room_name]
    Has Date: ✅ YES, Has Time: ✅ YES
    Purpose: Tracks when temperature became stable (for auto-off feature)

11. Input Text Helper:
    Name: climate_last_transition_[room_name]
    Entity ID: input_text.climate_last_transition_[room_name]
    Purpose: Prevents rapid switching between heating/cooling (hysteresis)
```

#### Adaptive Control Helpers (Optional - for automatic mode switching):
```yaml
# ⚠️ REPLACE [room_name] with your actual room name

12. Input Boolean Helper (Optional):
    Name: climate_adaptive_override_[room_name]
    Entity ID: input_boolean.climate_adaptive_override_[room_name]
    Purpose: Manually disable adaptive control when needed
```

### 📝 Room Naming Guide

#### Why Room Names Matter:
- **Debug Logs**: All log entries are prefixed with your room name for easy identification
- **BLE Detection**: Must match your BLE sensor output EXACTLY for presence detection
- **Multi-Room Setup**: Distinguishes between different automation instances

#### Naming Rules:
```yaml
✅ GOOD Examples:
- "Living Room" → [room_name] = living_room
- "Master Bedroom" → [room_name] = master_bedroom  
- "Office" → [room_name] = office
- "Kids Room" → [room_name] = kids_room

❌ AVOID:
- Special characters: !@#$%^&*()
- Numbers only: "Room1", "Room2" 
- Very long names (keep under 20 characters)
```

#### Helper Entity Naming Convention:
```
input_[type].climate_[function]_[room_name]

Examples:
Room: "Living Room" → [room_name] = living_room
Room: "Master Bedroom" → [room_name] = master_bedroom
Room: "Home Office" → [room_name] = home_office

Final Entity IDs:
- input_text.climate_last_mode_living_room
- input_text.climate_last_mode_master_bedroom  
- input_text.climate_last_mode_home_office
```

#### BLE Sensor Matching:
If using BLE presence detection, check your sensor state in Developer Tools:
```yaml
# Example: If your BLE sensor reports "Living Room"
Room Name in Blueprint: "Living Room" (exact match required)
[room_name] = living_room
Helper entities: input_text.climate_last_mode_living_room

# Example: If your BLE sensor reports "office"  
Room Name in Blueprint: "office" (exact match required)
[room_name] = office
Helper entities: input_text.climate_last_mode_office
```

### Step 3: Proximity Sensors (Optional)
Add to your `configuration.yaml` for proximity-based features:
```yaml
proximity:
  home:
    zone: home
    devices:
      - person.your_name
      - person.partner_name
    tolerance: 50
    unit_of_measurement: m
```

This creates:
- `sensor.home_nearest_distance` (distance in meters)
- `sensor.home_nearest_direction_of_travel` (towards/away/stationary/arrived)

### Step 4: Weather Integration (Optional)
Ensure you have a weather integration configured:
- Default: `weather.home` or `weather.forecast_home`
- Or configure a dedicated outdoor temperature sensor

### Step 5: Create Automation
1. Go to Settings → Automations & Scenes
2. Click "Create Automation" → "Use Blueprint"
3. Select "Ultimate Smart Climate Control - v2.22.5"
4. Configure all settings according to your preferences
5. **Important**: Test with debug logging enabled initially

### Step 6: Configuration Tips
1. **Start Simple**: Begin with basic Auto mode, add advanced features gradually
2. **Enable Debug Logging**: Initially enable for troubleshooting (disable after setup)
3. **Test Temperature Thresholds**: Verify all 6 thresholds work correctly
4. **Validate Presence Detection**: Ensure room sensors work as expected
5. **Monitor Effectiveness**: Check system logs for performance insights

## Usage Examples & Scenarios

### Control Mode Behaviors

#### **Auto Mode**
- Full temperature-based automation
- Presence detection via person entities and device tracking
- Proximity-based pre-conditioning
- Away mode when nobody home

#### **Smart Mode**
- Room-specific presence detection using BLE/PIR sensors
- Configurable presence timeout (5-120 minutes)
- Different behaviors for room absence vs. away from home
- More aggressive presence detection

#### **Manual Mode**
- Complete user control
- Only extreme temperature overrides active
- Manual override protection (configurable timeout)
- Instant automation disable

#### **Adaptive Mode**
- Automatically switches between Auto/Smart/Manual
- Based on room occupancy patterns
- Occupied delay: Switches to Smart when room occupied
- Vacant delay: Switches to Manual and turns off AC when room empty

### Real-World Scenarios

#### **Daily Usage**
- **Morning**: Scheduled temperature adjustment (cooler for waking up)
- **Work Hours**: Eco mode or off when room empty
- **Evening**: Comfort temperature when returning
- **Night**: Sleep-optimized temperature (18-21°C recommended)

#### **Presence Detection**
- **Brief Absence** (5-15 min): Presence timeout prevents shutdown
- **Room Change**: Smart sensors detect actual occupancy
- **Away from Home**: Global away mode with eco/off options
- **Approaching Home**: Pre-conditioning starts automatically

#### **Energy Optimization**
- **Comfort Zone**: AC turns off or eco mode (saves 40-60% energy)
- **Temperature Stable**: Auto-off when equilibrium reached
- **Window Open**: Immediate shutdown with auto-resume
- **Weather Compensation**: Adjusts thresholds based on outdoor temperature

## Configuration Guide

### Essential Settings

#### Climate Entity Configuration
- **Single Unit**: Select your A/C climate entity
- **Multiple Units**: Select all units for synchronized control
- **Temperature Source**: Use external sensor or A/C built-in sensor
- **Average Temperature**: Enable for multiple units (disable if using single external sensor)

#### Basic Temperature Settings
- **Target Temperature**: Your ideal room temperature (18-28°C)
- **Comfort Zone Width**: Temperature tolerance (±0.5 to ±3°C)
- **Response Aggressiveness**: How quickly system responds (1=gentle, 5=aggressive)
- **Advanced Overrides**: Manual control of all 6 temperature thresholds

#### Presence & Proximity
- **People to Track**: Person entities for global home/away detection
- **Presence Devices**: Additional devices (PCs, TVs, gaming consoles)
- **Room Presence Sensors**: BLE, PIR, mmWave sensors for room-specific detection
- **Validation Mode**: How multiple sensors work together
- **Proximity Sensors**: Distance and direction sensors for approach detection

### Temperature Control System

#### Automatic Threshold Calculation
Based on your target temperature and comfort zone width:
```
Target: 22°C, Comfort Zone: ±2°C, Aggressiveness: 2

Comfort Zone: 20.0°C - 24.0°C (Eco/Off mode)
Cooling LOW: 24.1°C (gentle, low fan)
Cooling MEDIUM: 25.0°C (balanced, medium fan)  
Cooling HIGH: 26.0°C (maximum, high fan)
Heating LOW: 19.9°C (gentle, low fan)
Heating MEDIUM: 19.0°C (balanced, medium fan)
Heating HIGH: 18.0°C (maximum, high fan)
```

#### Advanced Temperature Features
- **Outside Temperature Compensation**: Makes AC work harder to achieve target on extreme days
- **Time-Based Scheduling**: Different targets for morning/day/evening/night
- **Hysteresis Protection**: Prevents rapid switching at boundaries
- **Gradual Adjustments**: Reduces temperature overshooting
- **Manual Overrides**: Individual control of all 6 thresholds

#### Smart Fan Speed Selection
The system automatically detects and uses your A/C unit's fan capabilities:
- **Auto-Detection**: Matches Level 1-5, Low/Medium/High, Auto, Quiet, etc.
- **Graduated Response**: Low fan for gentle modes, high fan for emergency
- **Compatibility**: Works with all major A/C brands and fan speed formats

### Power Efficiency Settings

#### Comfort Zone Operation
- **Eco Mode**: Maintains temperature with minimal power (~150-250W)
- **Off Mode**: Complete shutdown for maximum savings (0W)
- **Auto Selection**: Choose eco for comfort, off for maximum efficiency

#### Temperature Stability Auto-Off
- **Automatic Detection**: Turns off when temperature equilibrium reached
- **Configurable Tolerance**: ±0.1°C to ±5.0°C stability range
- **Duration Setting**: 10-30 minutes of stable temperature required
- **Smart Logic**: Only activates within comfort zone boundaries

#### Runtime Protection
- **Minimum Runtime**: 5-30 minutes (prevents compressor damage)
- **Minimum Off Time**: 3-15 minutes (allows pressure equalization)
- **Gradual Adjustments**: 1-2°C steps prevent overshooting
- **Hysteresis**: Temperature tolerance prevents rapid switching

#### Dynamic Adaptation
- **Effectiveness Monitoring**: Tracks system performance over time
- **Smart Escalation**: Increases power when progress stalls
- **Predictive De-escalation**: Reduces power when approaching target
- **Learning System**: Adapts to your AC's characteristics

## Power Saving & Optimization

### Recommended Settings for Maximum Efficiency

#### Temperature Configuration
```yaml
# Efficient Settings Example
Target Temperature: 23°C
Comfort Zone Width: ±2°C (wider = more efficient)
Response Aggressiveness: 2 (balanced)
Eco Mode: Enabled
Stability Auto-Off: Enabled (±0.3°C, 15min)
```

#### Advanced Efficiency Features
1. **Smart Stability Detection**
   - Automatically turns off when job complete
   - Saves energy while maintaining comfort
   - Configurable sensitivity and duration

2. **Outside Temperature Compensation (v3.2.0)**
   - Makes AC work HARDER on extreme days (not easier)
   - Undershoots for cooling, overshoots for heating
   - Boosts fan speed on hot/cold days automatically
   - Factor: 0.1-0.2 for moderate compensation (recommended)

3. **Window Detection**
   - Immediate shutdown when windows/doors open
   - Automatic resume when closed
   - Prevents cooling/heating the outdoors

4. **Away Mode Optimization**
   - Eco: Maintains minimal climate (recommended)
   - Off: Maximum savings but slower recovery
   - Pre-conditioning: Smart approach detection

### Energy Monitoring & Analytics

#### Built-in Performance Tracking
- **Effectiveness Score**: 0-100% system performance rating
- **Temperature Trends**: Rising/falling/stable detection
- **Runtime Monitoring**: Tracks operational efficiency
- **Debug Insights**: Detailed decision-making logs

#### Efficiency Metrics
- **Comfort Zone Time**: Percentage in optimal range
- **Cycling Frequency**: Compressor start/stop events  
- **Power Level Usage**: Time spent in LOW/MEDIUM/HIGH modes
- **Stability Events**: Automatic shutdowns due to equilibrium

## Configuration Examples

### Basic Single Room Setup
```yaml
# Minimal configuration for beginners
Room Name: "Living Room"
Climate Entities: climate.living_room_ac
People: [person.john, person.jane]
Target Temperature: 23°C
Comfort Zone Width: ±2°C
Control Mode: Auto
Eco Mode: Enabled
Debug Logging: Enabled (initially)
```

### Advanced Multi-Zone Setup
```yaml
# Complete house automation
Climate Entities:
  - climate.living_room_ac
  - climate.bedroom_ac  
  - climate.office_ac
External Sensor: sensor.living_room_temperature
Presence Sensors:
  - sensor.phone_ble_area
  - binary_sensor.living_room_motion
Validation Mode: "smart"
Control Mode: "Smart"
Scheduling: Enabled
Outside Temperature Compensation: Enabled (factor: 0.2)
Window Sensors: [binary_sensor.patio_door]
```

### Maximum Efficiency Setup
```yaml
# Optimized for energy savings
Target Temperature: 24°C (summer) / 21°C (winter)
Comfort Zone Width: ±3°C (wider tolerance)
Eco Mode: Enabled
Stability Auto-Off: Enabled (±0.3°C, 15min)
Outside Temperature Compensation: Enabled
Gradual Adjustment: Enabled
Minimum Runtime: 20 minutes
Away Mode: "eco" with 2°C offset
Adaptive Control: Enabled
```

### Smart Home Integration
```yaml
# Advanced presence and automation
Room Presence Sensors:
  - sensor.phone_ble_area
  - binary_sensor.room_motion
  - binary_sensor.door_sensor
Validation Mode: "ble_plus"
Presence Timeout: 15 minutes
Adaptive Control: Enabled
Scheduling: Weekend schedule enabled
Notifications: Multiple services
Dynamic Adaptation: Enabled with all helpers
```

## Troubleshooting Guide

### Debug Logging Setup
1. **Enable Debug Logging** in blueprint settings
2. **View Logs**: Settings → System → Logs
3. **Filter**: Search for your room name or `blueprints.climate_control`
4. **Key Indicators**: Look for 🔍, 🌡️, ⚡, 🔥 prefixed messages

### Common Issues & Solutions

#### System Not Responding
```yaml
# Check these debug log messages:
- "CLIMATE CONTROL ACTIVATED": Automation triggered
- "should_activate: false": Control mode preventing action
- "runtime_lockout: ACTIVE": Minimum runtime protection active
- "Choose block completed - no conditions matched": In comfort zone (normal)
```

**Solutions**:
- Verify control mode is set to Auto or Smart
- Check presence detection is working
- Ensure temperature sensor is providing valid readings
- Confirm helper entities exist and are properly named

#### Rapid Cycling / Too Frequent Changes
```yaml
# Symptoms in debug logs:
- Frequent "MODE ACTIVATED" messages
- "runtime_lockout: ACTIVE" frequently
```

**Solutions**:
- Increase minimum runtime (20-30 minutes)
- Enable temperature stability auto-off
- Widen comfort zone (±3°C instead of ±1°C)
- Enable gradual adjustment
- Add hysteresis tolerance (0.5°C)

#### Temperature Thresholds Not Working
```yaml
# Debug log checks:
- "Cooling LOW/MEDIUM/HIGH conditions: True/False"
- "Temperature X°C exceeds Y°C threshold"
- Verify all 6 calculated thresholds are logical
```

**Solutions**:
- Check target temperature and comfort zone settings
- Verify outside temperature compensation isn't causing issues
- Ensure advanced temperature overrides are correct
- Test with simple configuration first

#### Presence Detection Issues
```yaml
# Debug messages to check:
- "PRESENCE VALIDATION DEBUG": Shows sensor states
- "Room Presence: DETECTED/Empty"
- "Validation Mode: ANY/ALL/SMART"
```

**Solutions**:
- Verify sensor states in Developer Tools
- Check BLE sensor reports correct room names
- Test different validation modes
- Ensure presence timeout is appropriate
- Check PIR sensor placement and sensitivity

### Advanced Troubleshooting

#### Energy Usage Higher Than Expected
1. **Check Stability Detection**: Ensure auto-off is working
2. **Review Comfort Zone**: Wider zones use less energy
3. **Verify Eco Mode**: Should be enabled for efficiency
4. **Monitor Away Mode**: Should activate when nobody home
5. **Check Window Detection**: Ensure it's working properly

#### Adaptive Control Not Working
```yaml
# Debug messages:
- "ADAPTIVE CONTROL: OCCUPIED → SWITCHING TO Smart MODE"
- "ADAPTIVE CONTROL: VACANT → SWITCHING TO Manual"
- "Override Protection" messages
```

**Solutions**:
- Verify all required helpers are created
- Check presence detection is working correctly
- Ensure occupied/vacant delays are appropriate
- Verify manual override timeout settings

### Performance Optimization

#### Best Practices for Reliable Operation
1. **Start Simple**: Begin with basic Auto mode, add features gradually
2. **Monitor Effectiveness**: Check effectiveness scores in debug logs
3. **Tune Thresholds**: Adjust based on your AC's performance
4. **Regular Maintenance**: Clean filters, check sensors periodically
5. **Seasonal Adjustments**: Update settings for summer/winter differences

#### Debug Log Interpretation
```yaml
# Key debug messages meaning:
"🎯 Status: Temperature X°C is perfect": System working correctly
"⚡ Response Aggressiveness": Shows escalation level
"🔍 SMART ESCALATION LEVEL X/4": Dynamic adaptation active
"🌡️ TEMP SET: [Mode]": Temperature command sent
"✅ All Good": No action needed, system stable
```

## Advanced Features & Integration

### Smart Home Integration

#### Voice Control Integration
- Works with Google Assistant, Alexa, Siri via Home Assistant
- Voice commands for mode switching and temperature adjustment
- Status announcements and alerts

#### Dashboard & UI Integration
```yaml
# Lovelace card example:
type: entities
title: Climate Control
entities:
  - input_select.climate_control_mode_living_room
  - sensor.living_room_temperature
  - climate.living_room_ac
  - input_boolean.climate_proximity_override_living_room
```

#### Notification Services
```yaml
# Multiple notification targets:
Primary: notify.mobile_app_phone
Additional:
  - notify.telegram_chat
  - notify.email
  - notify.pushbullet
```

### Energy Management Integration

#### Utility Rate Optimization
- Schedule intensive cooling/heating during off-peak hours
- Use eco mode during expensive rate periods
- Pre-condition before peak rate times
- Integration with time-of-use sensors

#### Solar Panel Integration
- More aggressive cooling when solar production is high
- Reduce operation when grid power is expensive
- Battery storage optimization

### Automation Ecosystem

#### Weather Integration
```yaml
# Automatic adjustments based on:
- Outdoor temperature
- Humidity levels
- Weather forecasts
- UV index
- Wind conditions
```

#### Security System Integration
- Away mode activation with alarm system
- Presence detection via security sensors
- Energy savings during vacation mode
- Emergency overrides during security events

#### IoT Device Integration
- Smart window sensors
- Air quality monitors
- Occupancy sensors
- Smart thermostats as temperature sources
- BLE beacon presence detection

## Support & Community

### Getting Help
- **GitHub Issues**: Report bugs and request features
- **Home Assistant Community**: General discussion and help
- **Debug Logs**: Always include relevant logs when reporting issues
- **Configuration Examples**: Share working configurations with the community

### Contributing
- Feature requests and suggestions welcome
- Bug reports with debug logs appreciated
- Configuration examples and use cases helpful for others
- Documentation improvements and corrections

### Repository Links
- **GitHub**: https://github.com/Chris971991/Smart-Climate-Control
- **Releases**: Check for latest versions and changelogs
- **Wiki**: Additional documentation and examples
- **Issues**: Bug reports and feature requests

## Version History

### **v3.3.3** (Current) - Manual Override False Detection Fix

**🐛 CRITICAL FIX: MODE CHANGE FALSE OVERRIDE ACTIVATION**
- **✅ FIXED**: Manual override no longer activates when switching modes (Smart→Manual→Smart)
- **✅ FIXED**: Added 5-minute buffer after mode changes to prevent false detections
- **🛡️ PROTECTION**: Mode transitions won't block automation for 1 hour anymore
- **🎯 RESULT**: Clean mode switching without triggering override protection

**What Was Broken:**
- **Before**: Smart→Manual→Smart → Periodic check detects state mismatch → Override activates → Automation blocked for 1 hour
- **Why**: Enhanced detection (v3.3.0) checked parameter mismatches, but mode changes cause temporary mismatches
- **Impact**: Every mode switch triggered 1-hour automation block (false positive)

**What Changed:**
- **Line 3700-3708**: Added mode change buffer condition to override activation check
- **Buffer**: 5 minutes after mode change, override activation is blocked
- **Logic**: `time_since_mode_change >= 5 minutes` must be TRUE to activate override
- **Result**: Mode transitions have time to settle before detection runs

**Real-World Impact:**
- **Before**: Switch Smart→Manual→Smart → Override active for 1 hour → Manual control only ❌
- **After**: Switch Smart→Manual→Smart → 5-min buffer → Automation resumes normally ✅

### **v3.3.2** - Off-Time Protection Fix

**🐛 CRITICAL FIX: 12-MINUTE COMPRESSOR PROTECTION**
- **✅ FIXED**: Mode changes no longer bypass 12-minute off-time protection
- **✅ FIXED**: System now checks BOTH helper mode AND actual AC state for protection enforcement
- **🛡️ PROTECTION**: Prevents rapid on/off cycles that can damage compressor
- **🎯 SCENARIO**: Smart→Manual→Smart no longer allows AC to turn on within 1-2 minutes

**What Was Broken:**
- **Before**: Mode change cleared helper to "off", state sync set it to "cooling_low", bypassed off-time check
- **Condition**: `last_mode == 'off'` didn't match "cooling_low", protection skipped
- **Result**: AC could turn on 1 minute after turning off (violation of 12-minute minimum)

**What Changed:**
- **Line 5795+**: Changed `last_mode == 'off'` to `(last_mode == 'off' or actual_ac_state == 'off')`
- **Coverage**: All 10 off-time protection checks (6 tier conditions + 4 inline time_protection_met)
- **Logic**: Now checks actual physical AC state, not just helper tracking state

**Real-World Impact:**
- **Scenario**: User switches Smart→Manual→Smart, AC turns off then tries to turn back on
- **Before**: AC off at 00:09, mode change at 00:08, AC turned on at 00:10 (1 min later) ❌
- **After**: AC off at 00:09, won't turn on until 00:21 (12 min later) ✅

### **v3.3.1** - Setup Wizard Translation Labels Fix

**🐛 BUG FIX: TRANSLATION LABELS**
- **✅ FIXED**: Setup Wizard UI now shows user-friendly labels instead of raw field names
- **📝 LABELS**: "👥 People to Track" instead of "presence_persons"
- **📱 CLARITY**: "📱 Presence Devices (optional)" instead of "presence_devices"

### **v3.3.0** - Enhanced Manual Override Detection

**🎯 MAJOR NEW FEATURE: SUPER ROBUST PARAMETER-LEVEL DETECTION**
- **✅ NEW**: Detects temperature setpoint changes (e.g., 20°C → 24°C user adjustment)
- **✅ NEW**: Detects fan speed changes (e.g., Fan 3 → Fan 5 manual selection)
- **✅ NEW**: Detects swing mode changes (e.g., vertical → horizontal manual change)
- **✅ NEW**: Detects HVAC mode changes (e.g., cool → heat manual switch)
- **✅ IMPROVED**: ON/OFF detection now synchronized with user's check_interval (not hardcoded)
- **✅ SUPER ROBUST**: Only checks during periodic_check trigger to eliminate false positives

**How It Works:**
- **Before Every Climate Service Call**: Captures expected values to helper entities
- **During Periodic Check**: Compares actual AC settings with expected values
- **Intelligent Tolerances**: ±0.5°C for temperature, case-insensitive for fan/swing modes
- **100% Coverage**: All 72 climate service calls have capture blocks (complete protection)

**Real-World Examples:**
1. **Temperature Change**: User changes 22°C → 24°C via HA UI → Detected → Override triggered
2. **Fan Speed Change**: User boosts Fan 3 → Fan 5 via remote → Detected → Override triggered
3. **Swing Mode Change**: User changes vertical → horizontal → Detected → Override triggered
4. **HVAC Mode Change**: User switches cool → heat → Detected → Override triggered
5. **AC Delayed Response**: AC takes 20 seconds to turn on → NOT detected (within buffer)

**Technical Architecture:**
- **4 New Helpers Required**: expected_temp, expected_fan, expected_swing, expected_hvac
- **Setup Wizard v3.9.0**: Auto-creates all 4 new helpers (no manual work)
- **Graceful Degradation**: All captures use `continue_on_error: true`
- **Synchronized Detection**: Uses check_interval instead of hardcoded 2-minute wait

**Documentation:**
- **Complete upgrade plan**: Manual_Override_Upgrade_Plan.md with 5 execution scenarios
- **README updated**: v3.3.0 features and helper requirements
- **Setup Wizard updated**: v3.9.0 with automatic helper creation

### **v3.2.2** - Template Syntax Error Hotfix

**🔥 CRITICAL HOTFIX**
- **✅ FIXED**: Removed inline Jinja2 comments causing TemplateSyntaxError (v3.2.1 broke all automations)
- **💥 ERROR**: `unexpected char '#' at 858` in manual_change_detected variable
- **🎯 IMPACT**: v3.2.1 automations couldn't load/reload - v3.2.2 fixes immediately

**What Was Broken:**
- **v3.2.1**: Inline `{# #}` comments inside parentheses in `manual_change_detected` logic
- **Result**: ALL automations failed validation with TemplateSyntaxError

**What Changed:**
- **Line 3444-3445**: Moved inline comments outside expression (before `{% set is_manual_change %}`)
- **Logic Unchanged**: Only comment placement fixed, detection logic identical

**Real-World Impact:**
- **Before**: All automations showed error on reload, wouldn't load
- **After**: Automations load without errors, manual override detection works

### **v3.2.1** - Critical Presence & Manual Override Fixes

**🐛 CRITICAL BUG FIXES**
- **✅ FIXED**: Smart mode presence confirmation delay now works correctly (was activating instantly)
- **✅ FIXED**: Manual override now detects HA UI shutoffs (AC turning OFF via climate card)
- **✅ FIXED**: Manual override now detects HA UI turn-ons (AC turning ON via climate card)
- **⚠️ BROKEN IN v3.2.1**: Template syntax error from inline comments (fixed in v3.2.2)

**What Changed:**
- **Line 3403**: Added explicit `{% elif control_mode == 'Auto' %}` block
- **Line 3450**: Added detection for `last_mode == 'off' and actual_state == 'on'`

### **v3.2.0** - Outside Temperature Compensation

**🌡️ NEW FEATURE: OUTSIDE TEMPERATURE COMPENSATION**
- **✅ NEW**: Makes AC work HARDER on extreme outdoor temperature days to ACHIEVE your target
- **🔥 COOLING**: Hot days (35°C outside) → AC undershoots (set to 20°C for 22°C target) + Fan boost
- **❄️ HEATING**: Cold days (10°C outside) → Heater overshoots (set to 24°C for 22°C target) + Fan boost
- **⚡ SMART**: Works WITH dynamic escalation - provides intelligent starting point, escalation monitors performance

### **v3.1.11** - Blueprint Source URL Metadata Fix

**🔧 METADATA FIX**
- **✅ FIXED**: Blueprint source_url corrected for proper re-import functionality in Home Assistant UI

### **v3.1.7** - Manual Override Re-Triggering After Mode Switch

**🐛 CRITICAL FIX: v3.1.6 REGRESSION**
- **✅ FIXED** - helper_change update now skips mode_change triggers to preserve timestamp clearing
- **🛡️ ENHANCED** - Mode change handler's PAST timestamp setting is now respected
- **⚡ BEHAVIOR** - Manual→Smart switch sets timestamp 2+ hours in past, no longer overwritten
- **🎯 IMPACT** - Override properly clears when switching from Manual mode and stays cleared

**What Changed:**
- **Before (v3.1.6):** helper_change updated on EVERY run → Overwrote PAST timestamp → Override re-activated
- **After (v3.1.7):** Skip update when `trigger.id == 'mode_change'` → Preserves timestamp → Override stays cleared
- **Result:** Manual→Smart/Auto switch properly clears override permanently

**Real-World Impact:**
- User switches Manual→Smart at 02:39 → Mode handler sets helper_change to 00:39 (2 hrs past)
- v3.1.6: Next check at 02:42 updates to NOW → 3.8 min ago → Override RE-ACTIVATES ❌
- v3.1.7: Next check skips update → Stays at 00:39 → 2+ hrs ago → Override STAYS CLEARED ✅

### **v3.1.6** - False Manual Override from AC Response Delay

**🐛 CRITICAL FIX: HELPER_CHANGE TIMESTAMP STALE DATA**
- **✅ FIXED** - Manual override no longer triggers when AC takes time to respond to commands
- **🛡️ ENHANCED** - `helper_change` now updates after EVERY automation action (not just mode changes)
- **⚡ BEHAVIOR** - 2-minute buffer now properly applies to most recent AC state change
- **🎯 IMPACT** - Eliminates false "manual change detected" when AC initialization is delayed

**What Changed:**
- **Before:** `helper_change` only updated on mode changes → Stale timestamps → False detections within 21 seconds of AC activation
- **After:** `helper_change` updates after ALL AC state changes → Fresh timestamps → Accurate 2-minute buffer protection
- **Result:** No more false manual override triggers from AC response delays or state synchronization issues

**Technical Details:**
- **Root Cause:** AC initialization didn't update `helper_change`, so manual detection compared against stale timestamp
- **Fix Location:** Added `helper_change` update at line 9980 (after main choose block, before final debug)
- **Protection:** Conditional block ensures helper exists before updating (`continue_on_error: true` for safety)
- **Coverage:** Applies to ALL AC state changes: turn on, turn off, temperature adjust, fan change, mode change

**Real-World Example (Office AC):**
- **02:05:00**: AC initialized to cooling_low (helper_change NOT updated - BUG!)
- **02:05:21** (21 sec later): Check runs, sees AC off, `time_since_change` = 0.4 min from OLD timestamp
- **Result:** False manual override triggered → 1-hour block → Temperature rose to 24.3°C unchecked
- **With Fix:** `helper_change` updated at 02:05:00 → 02:05:21 check sees 0.35 min < 2 min → No false detection

### **v3.1.5** - Manual Shutoff Detection During Settling Period

**🛡️ SAFETY ENHANCEMENT**
- **✅ FIXED** - Manual AC shutoffs now detected immediately, even within 5-min settling buffer
- **🛡️ SAFETY** - User can always turn off AC manually, automation respects it instantly
- **⚡ BEHAVIOR** - 5-min buffer prevents false positives but allows critical shutoff detection
- **🎯 IMPACT** - Best of both worlds - no false triggers from mode changes, but shutoffs work

### **v3.1.4** - Manual Override False Detection Fix

**🐛 CRITICAL FIX: MANUAL OVERRIDE FALSE DETECTION**
- **✅ FIXED** - Mode changes no longer trigger false manual override detection
- **🛡️ ENHANCED** - Manual detection strictly distinguishes automation actions from user actions
- **⚡ BEHAVIOR** - Added 5-minute buffer after mode changes + never flags 'off' state as manual
- **🎯 IMPACT** - Stops automation from blocking itself after legitimate mode switches

### **v3.1.3** - Smart Mode Grace Period Fix

**🐛 CRITICAL FIX: GRACE PERIOD ACTIVATION BUG**
- **✅ FIXED** - Grace period no longer activates from momentary sensor blips
- **🛡️ ENHANCED** - Confirmation delay now properly prevents false activations
- **⚡ BEHAVIOR** - Grace period requires prior CONFIRMED presence (not random motion detection)
- **🎯 IMPACT** - Stops AC from turning on when nobody is actually in the room

### **v3.0.11** - Comprehensive Test Suite & Validation

**🧪 TESTING & VALIDATION**
- **✅ REAL-WORLD TEST SUITE** - Added office_ac_test.py using actual production Office AC configuration
- **📊 22 TIMELINE TESTS** - Validates 8.5-hour work day: arrival → cooling → lunch break → afternoon → end of day
- **🎯 SMART PRESENCE** - Tests mmWave + BLE dual-sensor validation, false-positive prevention
- **🌡️ STABILITY AUTO-OFF** - Validates ±0.8°C tolerance, 10-minute duration, boundary conditions
- **🔧 BOUNDARY HANDLING** - Fixed test suite precision issues (comfort zone, stability tolerance)
- **✅ 100% PASS RATE** - All logic verified with production settings from climate.office_a_c

**💡 PRODUCTION VALIDATION**
- **Configuration Source**: Live Office AC automation (//192.168.50.45/config/automations.yaml)
- **Real Settings Tested**: 23°C target, 22-24°C comfort zone, SMART validation mode
- **Adaptive Control**: 5min occupied delay, 15min vacant delay, 3h manual override timeout
- **Test Coverage**: Temperature thresholds, presence logic, grace periods, adaptive switching

### **v3.0.10** - Temperature Stability Auto-Off Fix

**🐛 CRITICAL FIX: STABILITY DETECTION**
- **✅ FIXED STABILITY AUTO-OFF** - Removed redundant `not_in_continue_mode` check blocking shutoff
- **🔧 PROPER TRIGGERING** - Stability now activates when configured tolerance/duration met
- **📊 REAL-WORLD IMPACT** - AC turns off when stable within ±0.7°C for 15+ minutes (as configured)
- **✅ BACKWARD COMPATIBLE** - Other safeguards remain: comfort zone, target proximity, trend stability

### **v3.0.6** - Critical START Condition Presence Fix

**🐛 CRITICAL FIX: START CONDITION PRESENCE DETECTION**
- **✅ FIXED START CONDITIONS** - heating_low, cooling_low, and cooling_medium now require `should_activate` before starting
- **🚫 PREVENTS UNWANTED ACTIVATION** - AC will NOT turn on when temperature thresholds are met if nobody is in the room
- **🎯 3 MODES FIXED** - Added explicit `should_activate and` check to START conditions
- **🔧 PROPER LOGIC** - Continue conditions already worked (v3.0.3/v3.0.4), now START conditions match
- **📊 REAL-WORLD IMPACT** - AC won't activate at 18:13 when temp jumps from 24.0°C to 25.0°C with nobody present
- **✅ BACKWARD COMPATIBLE** - heating_high, cooling_high, heating_medium already had the check, now all 6 modes consistent

### **v3.0.5** - Blueprint Description Overhaul

**📋 DOCUMENTATION IMPROVEMENTS**
- **✨ STREAMLINED DESCRIPTION** - Reduced from 160 lines to 50 lines (70% reduction)
- **🚀 SETUP WIZARD PROMOTION** - Prominent callout directing users to automated setup
- **📖 FEATURE-FOCUSED** - Highlights capabilities instead of manual instructions
- **🔗 BETTER NAVIGATION** - Quick links to Setup Wizard, docs, and support
- **✅ PROFESSIONAL PRESENTATION** - Clean, scannable format with clear sections

### **v3.0.4** - Critical Smart Mode Timeout Fix

**🐛 CRITICAL FIX: PRESENCE TIMEOUT GRACE PERIOD**
- **✅ FIXED TIMEOUT LOGIC** - Smart mode now checks control mode BEFORE presence timeout
- **🚪 IMMEDIATE SHUTOFF** - AC exits immediately when `room_presence_detected` becomes false
- **⏱️ NO GRACE PERIOD IN SMART MODE** - Presence timeout only applies to Auto mode (as intended)
- **🔧 PROPER LOGIC ORDER** - `smart_presence_active` returns `room_presence_detected` directly for Smart mode
- **📊 REAL-WORLD IMPACT** - AC no longer continues running for 5+ minutes after leaving room
- **✅ BACKWARD COMPATIBLE** - Auto mode still has presence timeout grace period, Manual mode unchanged

### **v3.0.3** - Critical Smart Mode Continue Fix

**🐛 CRITICAL FIX: SMART MODE HYSTERESIS**
- **✅ FIXED CONTINUE CONDITION** - Smart mode now respects presence during "continue until target" phase
- **🚪 IMMEDIATE SHUTOFF** - AC turns off when presence is lost, even during active cooling/heating cycles
- **🎯 ALL 6 MODES FIXED** - Added presence check to LOW/MEDIUM/HIGH heating & cooling continue conditions
- **🔧 PROPER LOGIC** - `control_mode == 'Smart' and not smart_presence_active` returns False to exit cycle
- **📊 REAL-WORLD IMPACT** - Master Bedroom AC no longer runs when room is empty just because house presence is detected
- **✅ BACKWARD COMPATIBLE** - Auto and Manual modes unchanged, only Smart mode behavior improved

### **v3.0.2** - Smart Mode Presence Detection Fix
- **🐛 FIXED** - Smart mode no longer activates AC when user is in different room (e.g., AC in Master Bedroom when user in Office)
- **✅ ROOM-LEVEL PRESENCE** - Smart mode now only activates based on room presence detection
- **🏠 HOUSE-LEVEL PRESERVED** - Auto mode still uses house presence for whole-home automation
- **🔧 LOGIC UPDATE** - Added control mode check before house presence check in `smart_presence_active` variable

### **v3.0.1** - Packages Configuration Auto-Add Fix
- **🔧 FIXED** - Packages configuration now properly added to configuration.yaml automatically
- **📝 TEXT-BASED EDITING** - Uses text editing instead of YAML parsing to preserve `!include_dir_named` tags
- **✅ ZERO CONFIGURATION** - True automatic setup without manual configuration.yaml editing

### **v3.0.0** - Automated Setup Wizard Release
- **🎉 HACS INTEGRATION** - Complete Setup Wizard for automated helper creation
- **⏱️ 2-MINUTE SETUP** - Full room configuration in ~2 minutes vs 30-60 minutes manual
- **📦 PACKAGE-BASED HELPERS** - Safe, isolated YAML files in `/config/packages/` directory
- **🎨 DASHBOARD GENERATOR** - Auto-generates animated Mushroom card YAML
- **🛡️ SAFE APPROACH** - Won't affect existing helpers or automations

### **v2.22.15** - Repository Cleanup & Documentation Enhancement

**📋 COMPREHENSIVE DOCUMENTATION**
- **Complete Configuration Reference**: Added detailed explanations of all 40+ blueprint options
- **Step-by-Step Setup Guide**: Enhanced setup-new-room-guide.md with comprehensive instructions
- **Configuration Examples**: Added basic, advanced, cooling-only, and multi-zone setup templates
- **User-Friendly Explanations**: Detailed descriptions of every input option with ranges and best practices

**🗂️ REPOSITORY CLEANUP**
- **Removed Unused Files**: Cleaned up 6 unused template files for better project structure
- **Streamlined Documentation**: Focused on active blueprint-based setup approach
- **Improved Navigation**: Cleaner repository structure for easier user experience

### **v2.22.14** - Critical Auto-Off & Fan Speed Display Fixes
- **🎯 AUTO-OFF TARGET FIX** - AC now properly cools to 22°C instead of stopping early at 23.8°C due to wrong target temperature
- **📊 DISTANCE CALCULATION FIX** - Shows actual distance (1.8°C) instead of incorrect 0.0°C when system mode is "off"
- **⚡ FAN SPEED DISPLAY FIX** - Debug messages show actual fan speeds ("Silence", "3", "5") instead of confusing "Auto" labels
- **🛠️ TEMPLATE ERROR FIX** - Resolved UndefinedError preventing automation execution due to variable scope issues
- **🔧 VARIABLE SCOPE FIX** - Proper dependency order ensures all escalation/de-escalation features work correctly
- **🎯 ESCALATION SYSTEM VERIFIED** - Confirmed working optimally with 1-minute intervals for responsive performance adjustment
- **✅ BACKWARD COMPATIBLE** - All fixes maintain existing configurations without requiring user changes

### **v2.22.5** - Near-Target Stall Detection & Recovery
- **🎯 NEAR-TARGET STALL DETECTION** - Revolutionary logic detects when system gets stuck ≤0.8°C from target for 15+ minutes
- **⚡ INTELLIGENT ESCALATION** - Level 1 escalation automatically triggers to provide gentle push to final temperature
- **🔄 SMART PRIORITY SYSTEM** - Escalation takes priority over de-escalation during stall scenarios to prevent "Silence" mode blocking
- **🛡️ REDUCED DE-ESCALATION SENSITIVITY** - Level 3 maximum de-escalation now triggers at ≤0.3°C (was 0.5°C) with 90% effectiveness requirement
- **📊 PROGRESSIVE RECOVERY** - Added Level 2 de-escalation for 0.3-0.8°C range instead of jumping to maximum reduction
- **🔧 ALL 6 FAN SELECTION BLOCKS UPDATED** - Near-target stall override implemented across all heating/cooling modes
- **✅ REAL-WORLD VALIDATED** - Fixes actual user issue: system stuck at 22.4°C → 22.0°C for 50+ minutes now completes cooling

### **v2.22.4** - Manual Override Elimination & Current Mode Display Fix
- **🚫 COMPLETE MANUAL MODE REMOVAL** - Eliminated ALL automatic switching to Manual mode throughout entire codebase
- **🎮 DASHBOARD CONTROL ONLY** - Manual mode now ONLY accessible via explicit user dashboard selection
- **🔧 FIXED CURRENT MODE DISPLAY** - Shows "OFF" when AC actually off instead of misleading "IDLE" status
- **🛠️ ROOT CAUSE FIXES** - Removed band-aid solutions, implemented clean fixes for manual override false triggers
- **⏰ REDUCED OVERRIDE TIMEOUT** - Manual override auto-reset reduced from 1.5h to 5min in Smart mode
- **🔄 CLEAN ARCHITECTURE** - Eliminated workaround code, restored sophisticated control logic

### **v2.22.3** - Manual Override False Detection Fix
- **🐛 FIXED FALSE MANUAL OVERRIDE** - Resolved incorrect detection during routine checks and temperature changes
- **🎯 PRECISE DETECTION** - Manual override now only triggers on actual user AC setting changes
- **🚀 IMPROVED RESPONSIVENESS** - Eliminated blocking delays during normal operation
- **📊 ACCURATE DEBUG LOGGING** - Debug messages now correctly reflect actual system state

### **v2.22.2** - YAML Structure & Manual Override Fixes
- **🔧 CRITICAL YAML FIX** - Resolved parsing error from orphaned variables block
- **🚫 MANUAL MODE DISABLE #1** - First phase of removing automatic manual mode switching
- **⚡ FAN SPEED PRIORITY FIX** - Fixed de-escalation Level 2 to prioritize "auto" over numeric speeds
- **📊 ENHANCED DEBUG** - Added current fan speed to status logs for better monitoring

### **v2.22.1** - Foundation Stability & Logic Improvements
- **🛡️ STABILITY IMPROVEMENTS** - Enhanced error handling and template safety
- **🔧 LOGIC REFINEMENTS** - Improved conditional logic flow and variable validation
- **📋 DEBUG ENHANCEMENTS** - Better diagnostic information and troubleshooting support

### **v2.22.0** - Major Architecture Evolution
- **🏗️ CODEBASE MODERNIZATION** - Complete overhaul of control logic architecture
- **🌡️ ENHANCED TEMPERATURE CONTROL** - Improved threshold management and hysteresis
- **📱 BETTER PRESENCE DETECTION** - Refined sensor validation and room detection
- **⚙️ DYNAMIC ADAPTATION** - Advanced effectiveness tracking and power management

### **Previous Major Versions (v2.8.x - v2.21.x)**
- **v2.8.23**: Anti-short cycling & target-based control
- **v2.8.22**: Critical bug fixes & reliability improvements
- **v2.8.21**: Complete 3-tier implementation
- **v2.8.x**: Dynamic adaptation, stability detection, presence validation
- **v2.7.x**: Weather compensation, scheduling features
- **v2.6.x**: Smart mode, proximity control, window detection
- **v2.5.x**: Multi-zone support, fan speed optimization
- **v2.0.x**: Major architecture redesign
- **v1.0**: Initial release with basic climate control

### **Upcoming Features** (Future Versions)
- Machine learning temperature prediction
- Energy usage analytics and reporting
- Integration with smart grid systems
- Advanced air quality control
- Multi-room coordinated climate management
