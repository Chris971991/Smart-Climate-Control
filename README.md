# Ultimate Smart Climate Control Blueprint

## Overview
A highly advanced Home Assistant blueprint for intelligent climate control with **3-tier temperature escalation**, power efficiency optimization, proximity-based pre-conditioning, and multi-zone support. Features intuitive LOW/MEDIUM/HIGH heating and cooling with graduated fan speeds for optimal comfort and efficiency.

## Key Features

### 🌡️ **NEW! 3-Tier Temperature System (v2.8.21)**
- **Intelligent Escalation**: LOW → MEDIUM → HIGH heating and cooling
- **Graduated Fan Speeds**: Gentle → Balanced → Maximum power
- **Perfect Boundary Logic**: No overlaps, smooth transitions
- **Single Degree Precision**: Responds at exactly 1°C intervals
- **Example (22°C target, ±2°C comfort)**: 
  - Cooling: 24.1°C (LOW) → 25°C (MEDIUM) → 26°C (HIGH)
  - Heating: 19.9°C (LOW) → 19°C (MEDIUM) → 18°C (HIGH)

### 🎯 Full Customization
- **Multi-unit support**: Control 1 or multiple A/C units simultaneously
- **Flexible presence detection**: Use persons, devices, or both
- **6 Temperature Thresholds**: Complete LOW/MEDIUM/HIGH for heating and cooling
- **Smart Fan Speeds**: Auto-selects appropriate speeds for each intensity level
- **Weather Compensation**: All thresholds adjust with weather conditions
- **Notification options**: Choose what and when to be notified

### 🧠 Smart Mode Control (NEW!)
- **Auto Mode**: Full automation with all features enabled
- **Manual Mode**: Keeps current climate settings, only proximity safety override active
- **Smart Mode**: Auto mode with aggressive presence detection and room-specific sensors
- **Presence Timeout**: Configurable delay (5-60 min) before taking action when leaving room
- **Proximity Zones**: Different behaviors based on distance from home
- **Room-Specific Presence**: Optional BLE/PIR sensors for accurate room occupancy

### ⚡ Power Efficiency Improvements

#### Why This Blueprint is More Efficient

1. **Eco Mode Instead of On/Off Cycling**
   - Maintains temperature with minimal fan speed
   - Prevents compressor cycling (3-5x power surge on startup)
   - Reduces wear on components

2. **Gradual Temperature Adjustments**
   - Adjusts setpoint gradually (1-2°C at a time)
   - Prevents aggressive cooling/heating cycles
   - Maintains steady-state operation

3. **Minimum Runtime Protection**
   - Ensures A/C runs for minimum time before mode changes
   - Prevents rapid cycling that wastes energy
   - Configurable runtime and off-time minimums

4. **Smart Pre-conditioning**
   - Only pre-cools/heats when necessary
   - Uses medium fan speeds for efficiency
   - Proximity-based activation

5. **Intelligent Away Mode**
   - Three options: Off, Eco, or Maintain
   - Eco mode keeps minimal climate control
   - Prevents extreme temperature swings

## Installation

1. **Copy Blueprint**: Place `ultimate_climate_control.yaml` in:
   ```
   config/blueprints/automation/
   ```

2. **Create Helper Entities** (REQUIRED - unique for each room):
   - Via UI: Settings → Devices & Services → Helpers → Create Helper
   - **Basic Helpers (Required)**:
     - Input Text: `input_text.climate_last_mode_living_room`
     - Input DateTime: `input_datetime.climate_last_change_living_room` (with date AND time)
   - **Smart Mode Helpers (Required for Smart Mode)**:
     - Input Select: `input_select.climate_control_mode_living_room` (Auto/Manual/Smart)
     - Input DateTime: `input_datetime.presence_last_detected_living_room` (presence tracking)
     - Input Boolean: `input_boolean.climate_proximity_override_living_room` (emergency override)
   - **Dynamic Adaptation Helpers (Optional)**:
     - Input Number: Temperature history, effectiveness scores
     - Input Text: Trend tracking
     - Input DateTime: Mode start times
   - Copy and rename for each room (bedroom, office, etc.)

3. **Setup Proximity Sensors**: Add to your `configuration.yaml`:
   ```yaml
   proximity:
     home:
       zone: home
       devices:
         - person.your_name  # Replace with your person entities
         - person.partner_name
       tolerance: 50
       unit_of_measurement: m
   ```
   This creates:
   - `sensor.home_nearest_distance` - Distance from home in meters
   - `sensor.home_nearest_direction_of_travel` - towards/away/stationary/arrived

4. **Optional Energy Tracking**: Add configuration from `helpers_configuration.yaml`

5. **Restart Home Assistant**

6. **Create Automation**:
   - Go to Settings → Automations
   - Click "Create Automation"
   - Choose "Ultimate Smart Climate Control - v2.8.21"
   - Configure all options to your preference

7. **Add Dashboard Scripts** (Optional):
   - Copy contents from `dashboard_control_script.yaml`
   - Add to your `scripts.yaml` or create via UI
   - Create dashboard buttons for mode control

## Smart Mode Scenarios

### Real-World Examples

#### **Bathroom Break (5 minutes away)**
- **Auto/Smart Mode**: Presence timeout prevents shutdown, climate continues
- **Manual Mode**: No change, keeps current settings

#### **Local Shop (<5km away)**
- **Auto/Smart Mode**: Near zone keeps comfort temperature, ready when you return
- **Manual Mode**: No change unless extreme temperature

#### **Different Room in House**
- **With Room Sensors**: Climate adjusts based on actual room occupancy
- **Without Room Sensors**: Uses GPS proximity + presence timeout

#### **Long Trip (>15km away)**
- **Auto/Smart Mode**: Far zone switches to eco mode or turns off
- **Manual Mode**: Keeps current settings + extreme temperature safety

#### **Dashboard Control**
- **Toggle Button**: Cycles Auto → Manual → Smart → Auto
- **Emergency Override**: Force cooling/heating regardless of mode

## Configuration Guide

### Essential Settings

#### Climate Entities
Select one or more A/C units to control. The blueprint will:
- Average temperatures across units
- Apply same settings to all units
- Coordinate operation for efficiency

#### Presence Configuration
- **People to Track**: Select person entities
- **Presence Devices**: Add PCs, TVs, or other indicators
- **Proximity Sensors**: Configure distance tracking

### 3-Tier Temperature Thresholds

#### Cooling Escalation (🌡️ NEW SYSTEM)
- **LOW Cooling** (e.g., 24.1°C): Gentle cooling with minimal fan, maximum efficiency
- **MEDIUM Cooling** (e.g., 25.0°C): Balanced cooling with medium fan speeds  
- **HIGH Cooling** (e.g., 26.0°C): Maximum cooling with high fan, emergency mode
- **Comfort Zone** (20.0-24.0°C): Eco mode or off

#### Heating Escalation (🔥 COMPLETELY RESTRUCTURED)
- **LOW Heating** (e.g., 19.9°C): Gentle heating with minimal fan, maximum efficiency
- **MEDIUM Heating** (e.g., 19.0°C): Balanced heating with medium fan speeds
- **HIGH Heating** (e.g., 18.0°C): Maximum heating with high fan, emergency mode

> **Note**: All thresholds automatically adjust based on your target temperature and comfort zone settings. Advanced users can override individual thresholds.

### Power Efficiency Settings

#### Eco Mode (Recommended: ON)
Instead of turning off completely:
- Maintains temperature with minimal energy
- Prevents temperature swings
- Reduces startup cycles

#### Gradual Adjustment (Recommended: ON)
- Adjusts temperature in 1-2°C increments
- Prevents aggressive operation
- Saves 15-20% energy

#### Runtime Protection
- **Minimum Runtime**: 10 minutes (prevents short cycling)
- **Minimum Off Time**: 5 minutes (protects compressor)

## Power Saving Recommendations

### Optimal Settings for Efficiency

1. **Temperature Ranges**
   - Cooling: Set to 24-26°C (not lower)
   - Heating: Set to 20-22°C (not higher)
   - Wider comfort zone = less operation

2. **Fan Speed Strategy**
   - Use AUTO when possible
   - High speed only for extreme temperatures
   - Eco mode with Level 1-2 for maintenance

3. **Away Mode**
   - Use "eco" instead of "off"
   - Prevents extreme temperature recovery
   - Saves 30-40% vs constant operation

4. **Pre-conditioning**
   - Enable only if commute is predictable
   - Set larger approaching distance (10km)
   - Uses less energy than rapid cooling/heating

### Energy Monitoring

The blueprint tracks:
- Runtime hours per day
- Cycling frequency
- Efficiency rating

Monitor these via:
- `sensor.climate_runtime_today`
- `sensor.climate_efficiency_rating`

## Example Configurations

### Single Room Setup
```yaml
Climate Entities: climate.bedroom_ac
People: person.john, person.jane
Comfort Zone: 22-24°C
Eco Mode: Enabled
Gradual Adjustment: Enabled
```

### Whole House Setup
```yaml
Climate Entities: 
  - climate.living_room_ac
  - climate.bedroom_ac
  - climate.office_ac
People: All household members
Away Mode: Eco (maintains 26°C cooling, 20°C heating)
Pre-conditioning: 10km distance
```

### Energy-Conscious Setup
```yaml
Comfort Zone: 20-25°C (wider range)
Eco Mode: Enabled
Gradual Adjustment: Enabled
Fan Speed Eco: Level 1
Away Mode: Eco with 2°C offset
Min Runtime: 15 minutes
```

## Troubleshooting

### Enable Debug Logging
1. **Turn on debug mode** in the blueprint settings
2. **View logs**: Settings → System → Logs
3. **Filter by**: `blueprints.climate_control`
4. **Look for**: 🔍 CLIMATE DEBUG messages

Debug logs show:
- Trigger events and reasons
- Current temperature and thresholds
- Decision logic (which mode activated)
- Why no action was taken
- All condition evaluations

### A/C Cycling Too Frequently
- Increase minimum runtime (15-20 min)
- Enable gradual adjustment
- Widen comfort zone
- Check debug logs for rapid mode changes
- Look for "runtime_lockout: ACTIVE" messages

### Not Cooling/Heating Fast Enough
- Check if temperature is within the 3-tier escalation ranges
- Verify debug logs show correct threshold conditions
- Look for "LOW/MEDIUM/HIGH conditions: True" messages
- Ensure fan speeds are configured for your A/C unit

### Understanding the New 3-Tier System (v2.8.21)
- **Debug logs show all 6 thresholds**: cooling_low, cooling_medium, cooling_high, heating_low, heating_medium, heating_high
- **"Choose block completed - no conditions matched"**: Temperature is in comfort zone (working correctly)
- **Threshold calculations**: Based on target temperature ± comfort zone ± aggressiveness
- **Fan speed selection**: Automatic based on A/C capabilities and intensity level

### High Energy Usage
- Enable eco mode
- Widen comfort zone
- Check away mode settings
- Review debug logs for cycling patterns

### Automation Not Triggering
1. Enable debug logging
2. Check "Last triggered" in automations list
3. Verify helper entities exist and are named correctly
4. Ensure someone is "home" in the system
5. Check temperature sensor is providing valid readings

## Advanced Features

### Custom Notification Services
Add multiple notification services:
```yaml
Notification Service: notify.mobile_app_phone
Additional Services:
  - notify.email
  - notify.telegram
```

### Integration with Energy Tariffs
Combine with utility rate sensors:
- Reduce operation during peak rates
- Pre-cool/heat during off-peak
- Use eco mode during expensive periods

## Support

For issues or suggestions, please check the Home Assistant community forums or create an issue in the repository.

## Version History

### **v2.8.21** (Latest) - Complete 3-Tier System
- **🎯 FULLY IMPLEMENTED** - Complete LOW/MEDIUM/HIGH system for both heating and cooling
- **🔥 NEW Heating Structure** - Completely restructured with proper LOW (19.9°C, gentle), MEDIUM (19.0°C, balanced), HIGH (18.0°C, maximum) 
- **❄️ Enhanced Cooling Logic** - LOW (24.1°C, gentle), MEDIUM (25.0°C, balanced), HIGH (26.0°C, maximum)
- **🌡️ Perfect Escalation** - Intuitive temperature-based escalation with appropriate fan speeds
- **🔍 Complete Debug Output** - All 6 thresholds shown with proper condition evaluations
- **⚙️ Dynamic Compatibility** - Full integration with existing dynamic adaptation system

### **v2.8.20** - Three-Tier Foundation  
- **Three-Tier System Implementation** - Added consistent LOW/MEDIUM/HIGH levels for both heating and cooling
- **New Cooling LOW Mode** - Gentle cooling at 24.1°C with minimal fan speed for maximum efficiency  
- **Enhanced Thresholds** - All 6 temperature thresholds now properly defined with weather compensation
- **Improved Debug Output** - Shows all 6 thresholds and detailed condition evaluations

### **v2.8.19** - Logic Corrections
- **Fixed Heating Threshold Logic** - Swapped heating low/medium thresholds so naming matches behavior

### **v2.8.18** - Critical Boundary Fix
- **Fixed Heating/Cooling Threshold Overlap** - Prevented boundary overlaps at exact comfort zone edges

### Previous Versions (v2.8.16 and earlier)
- Enhanced runtime lockout debug, dynamic adaptation, stability detection, presence validation, proximity-based control, weather compensation, and core climate control features

### **v1.0** - Original Release
- Initial release with full customization and power efficiency features