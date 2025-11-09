# Ultimate Smart Climate Control Blueprint

## 🎉 NEW: Automated Setup Wizard!

**The easiest way to set up climate control just got even easier!** Install the companion **Smart Climate Control Setup Wizard** HACS integration for:

✅ **2-Minute Setup** - Complete room configuration in ~2 minutes (vs 30-60 minutes manual)
✅ **Zero Manual Helper Creation** - All 20 helper entities created automatically (1 new in v3.16.0)
✅ **Automatic Packages Configuration** - Wizard adds packages support to your configuration.yaml
✅ **Blueprint Automation Created** - Complete automation configured and ready to use
✅ **Dashboard Card Generator** - Auto-generates animated Mushroom card YAML for mode control
✅ **Safe & Non-Destructive** - Won't affect existing helpers or automations

**Installation:** See [Setup Wizard Installation](#setup-wizard-installation-method-1-recommended) below!

---

## Overview
A comprehensive Home Assistant blueprint for advanced climate control featuring **complete 3-tier temperature escalation**, intelligent presence detection, **Command Gatekeeper System (90% reduction in command spam)**, **enhanced manual override detection**, power efficiency optimization, and extensive customization options. This system provides automated climate management with LOW/MEDIUM/HIGH heating and cooling modes, smart fan speed control, multi-sensor temperature averaging, and sophisticated presence-based automation.

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

#### 🚀 **Command Gatekeeper System (NEW v3.13.0)**
- **⚡ 90% REDUCTION IN COMMAND SPAM**: Commands only sent when AC state actually needs changing!
- **🎯 INSTANT MANUAL OVERRIDE DETECTION**: Reduced hardware delay from 45s → 5s (safe now!)
- **🛡️ SMART STATE TRACKING**: HVAC mode, fan speed, temperature, swing mode all compared before sending
- **🔥 NO MORE FIGHTING USER COMMANDS**: Automation "breathes" between checks, allows manual changes to persist
- **Before**: Sent commands EVERY trigger (1-60+ times per hour) even when nothing changed
- **After**: Commands only when state differs (90% reduction, ~5 commands/hour instead of ~60)

#### 🌡️ **Multi-Sensor Temperature Support (NEW v3.9.0)**
- **Multiple Temperature Sensors**: Support for multiple temp sensors per room
- **Smart Strategy**: Cooling uses WARMEST room, Heating uses COLDEST room, Both/Neither uses AVERAGE
- **Use Case**: Living Room AC also cools Media Room - system ensures both rooms reach target
- **Backward Compatible**: Single sensor still works perfectly

#### 📊 **Enhanced Manual Override Detection (v3.3.0, v3.15.2)**
- **Temperature Change**: User changes 22°C → 24°C via HA UI → Detected → Override triggered
- **Fan Speed Change**: User boosts Fan 3 → Fan 5 via remote → Detected → Override triggered
- **Swing Mode Change**: User changes vertical → horizontal → Detected → Override triggered
- **HVAC Mode Change**: User switches cool → heat → Detected → Override triggered
- **Bed ECO Mode Support**: Manual override now works during bed comfort ECO mode (v3.15.2)
- **Adaptive Timeout**: Override duration adjusts based on time of day (5min-2hrs)

#### 🛏️ **Bed Comfort ECO Mode with Fan-Only Power Savings (NEW v3.17.0)**
- **⚡ NEW v3.17.0: Fan-Only Mode**: Automatic switch from cooling → fan_only when stable/overshooting
  - **~85% Power Reduction**: Compressor OFF, fan only during stable periods
  - **Two Activation Scenarios**: Overshoot (below target) OR Stability (at target)
  - **Auto Return**: Returns to cooling when temp rises above threshold
  - **Configurable**: Toggle on/off, stability duration (1-10 min), return threshold, max overshoot
  - **Savings Example**: 6 hours/night in fan_only = ~4 kWh saved = $0.80-$1.20/night
- **Intelligent Takeover**: Only activates when taking over from existing cooling modes (respects your thresholds!)
- **Silent Operation**: Uses minimal fan speed (eco setting) for peaceful sleep
- **Precise Maintenance**: Maintains at your exact target temperature (not overshoot)
- **Dynamic Escalation**: Automatically increases fan if room not maintaining target
- **Grace Period**: Configurable 0-30 min buffer for bathroom trips (v3.15.0)
- **Smart Exit**: Returns to normal cooling when bed unoccupied beyond grace period
- **Manual Override**: Respects user's manual control - won't fight you (v3.15.2)
- **Perfect for Sleep**: Combines comfort, quiet operation, and maximum energy efficiency

#### 🎛️ **Core Features**
- **Multi-Zone Control**: Manage 1 or multiple A/C units with synchronized operation
- **Smart Presence Detection**: Multiple validation modes (ANY/ALL/SMART/MAJORITY/BLE_PLUS/BLE_MOTION/BLE_BED)
- **6 Temperature Thresholds**: Fully configurable LOW/MEDIUM/HIGH for heating and cooling
- **Dynamic Fan Speed Selection**: Automatically matches your A/C unit's capabilities
- **Outside Temperature Compensation (v3.2.0)**: Makes AC work HARDER on extreme days to achieve your target (not change it)
- **Time-Based Scheduling**: Different temperatures for morning/day/evening/night
- **Window Detection**: Automatic AC shutdown when doors/windows open
- **Temperature Stability Detection**: Auto-off when equilibrium reached
- **Comprehensive Notifications**: Customizable alerts for all system actions

### 🧠 Intelligent Control Modes (4 Modes)
- **Auto Mode**: House-wide automation with home/away detection
- **Smart Mode**: Room-specific presence with BLE/PIR/mmWave sensors (immediate shutoff when leaving)
- **Manual Mode**: Full user control with emergency temperature overrides only
- **Override Mode**: (Auto-set) User manually changed AC - automation paused temporarily with adaptive timeout

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
- ✅ All 19 helper entities in /config/packages/climate_control_[room].yaml
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

5. Input Boolean Helper (NEW v3.16.0):
   Name: presence_validation_active_[room_name]
   Entity ID: input_boolean.presence_validation_active_[room_name]
   Icon: mdi:account-check
   Purpose: Tracks presence validation state transitions (prevents false timer accumulation)

6. Input Boolean Helper:
   Name: climate_proximity_override_[room_name]
   Entity ID: input_boolean.climate_proximity_override_[room_name]
   Icon: mdi:toggle-switch
   Purpose: Emergency override to bypass all automation
```

#### Advanced Feature Helpers (Optional but Recommended):
```yaml
# ⚠️ REPLACE [room_name] with your actual room name
# Dynamic Adaptation & Effectiveness Tracking

8. Input Number Helper:
   Name: climate_temp_history_[room_name]
   Entity ID: input_number.climate_temp_history_[room_name]
   Min: 0, Max: 50, Step: 0.1
   Unit: °C
   Purpose: Stores previous temperature for trend analysis

9. Input Number Helper:
   Name: climate_effectiveness_score_[room_name] 
   Entity ID: input_number.climate_effectiveness_score_[room_name]
   Min: 0, Max: 100, Step: 0.1
   Unit: %
   Purpose: Tracks how well the current mode is working (0-100%)

10. Input Text Helper:
   Name: climate_trend_direction_[room_name]
   Entity ID: input_text.climate_trend_direction_[room_name]
   Purpose: Tracks if temperature is rising/falling/stable

11. Input DateTime Helper:
   Name: climate_mode_start_time_[room_name]
   Entity ID: input_datetime.climate_mode_start_time_[room_name]  
   Has Date: ✅ YES, Has Time: ✅ YES
   Purpose: Tracks when current climate mode started

12. Input DateTime Helper:
    Name: temp_stable_since_[room_name]
    Entity ID: input_datetime.temp_stable_since_[room_name]
    Has Date: ✅ YES, Has Time: ✅ YES
    Purpose: Tracks when temperature became stable (for auto-off feature)

13. Input Text Helper:
    Name: climate_last_transition_[room_name]
    Entity ID: input_text.climate_last_transition_[room_name]
    Purpose: Prevents rapid switching between heating/cooling (hysteresis)
```

#### Adaptive Control Helpers (Optional - for automatic mode switching):
```yaml
# ⚠️ REPLACE [room_name] with your actual room name

14. Input Boolean Helper (Optional):
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
- **Releases**: Check [GitHub Releases](https://github.com/Chris971991/Smart-Climate-Control/releases) for latest versions and changelogs
- **Wiki**: Additional documentation and examples
- **Issues**: Bug reports and feature requests

---

## License

This project is released under the MIT License.
