# 🚀 Complete Guided Setup - Smart Climate Control

## Overview

The **Smart Climate Helper Creator** now includes a **complete guided setup wizard** that creates EVERYTHING you need in just 5 easy steps!

### What Gets Created Automatically:

✅ **All Helper Entities** (up to 13 helpers based on features)
✅ **Complete Blueprint Automation** (fully configured and ready to use)
✅ **Automatic Configuration** (no manual YAML editing needed!)

**Total Setup Time: ~2-3 minutes per room!**

---

## 🎯 Prerequisites

Before starting the guided setup, ensure you have:

1. ✅ **Home Assistant** 2023.1.0 or newer
2. ✅ **HACS** installed and configured
3. ✅ **A/C units integrated** in Home Assistant (climate entities)
4. ✅ **Blueprint imported** (ultimate_climate_control.yaml)

---

## 📋 Installation Steps

### Step 1: Install via HACS

1. Open **HACS** in Home Assistant
2. Go to **Integrations**
3. Click **⋮ Menu** → **Custom Repositories**
4. Add repository:
   - **URL**: `https://github.com/Chris971991/Smart-Climate-Control`
   - **Category**: Integration
5. Click **Add**
6. Find "Smart Climate Helper Creator" and click **Download**
7. **Restart Home Assistant** (required!)

### Step 2: Import Blueprint

1. Go to **Settings** → **Automations & Scenes** → **Blueprints**
2. Click **Import Blueprint**
3. Paste URL: `https://github.com/Chris971991/Smart-Climate-Control/blob/main/ultimate_climate_control.yaml`
4. Click **Import**

---

## 🧙‍♂️ The Guided Setup Wizard

### Starting the Wizard

1. Go to **Settings** → **Devices & Services**
2. Click **+ Add Integration** (bottom right)
3. Search for "Smart Climate Helper Creator"
4. Click on it to start the wizard!

---

### Step 1 of 5: Room Name

**What you'll see:**
```
Welcome to the Smart Climate Control Setup Wizard!

This wizard will guide you through creating a complete climate
control automation for your room.

What will be created:
• Helper entities for tracking and automation
• Complete blueprint automation
• Fully configured climate control system
```

**What to enter:**
- **Room Name**: Enter the name of your room (e.g., "Living Room", "Master Bedroom", "Office")

**Tips:**
- Use descriptive names
- Spaces are fine (e.g., "Living Room" works perfectly)
- This name will be used for all helper entities and the automation

**Example:** `Living Room`

---

### Step 2 of 5: Feature Selection

**What you'll see:**
```
Choose which features to enable for Living Room.

All features are recommended for best performance!
```

**Options (all enabled by default):**

✅ **Dynamic Adaptation**
- Automatically escalates/de-escalates power based on effectiveness
- Monitors temperature progress and adjusts accordingly
- Creates 6 helper entities

✅ **Manual Override Detection**
- Detects when you manually change AC settings
- Prevents automation from fighting your manual changes
- Creates 2 helper entities

✅ **Control Mode Selection**
- Enables Auto/Smart/Manual mode switching
- Adds mode selector helper
- Creates 1 helper entity

✅ **Smart Mode**
- Enables presence detection and timeout logic
- Room-specific presence sensors
- Creates 1 helper entity

**Recommendation:** Keep all features enabled for full functionality!

---

### Step 3 of 5: Climate Entities (A/C Units)

**What you'll see:**
```
Select the A/C unit(s) for Living Room.

You can select multiple A/C units if your room has more than one.
```

**What to select:**
- Click the dropdown
- Select your A/C unit(s)
- You can select multiple if your room has several units

**Examples:**
- Single unit: `climate.living_room_ac`
- Multiple units: `climate.living_room_ac_1`, `climate.living_room_ac_2`

**Tip:** If you don't see your A/C, go back and make sure it's properly integrated in Home Assistant first!

---

### Step 4 of 5: Optional Sensors

**What you'll see:**
```
Configure optional sensors for Living Room.

All sensors are optional but recommended for best accuracy!
```

**Options:**

**Temperature Sensor (optional):**
- External temperature sensor for more accurate room readings
- Usually more accurate than A/C built-in sensors
- Example: `sensor.living_room_temperature`

**Room Presence Sensors (optional, multiple):**
- BLE area sensors (e.g., `sensor.phone_ble_area`)
- PIR motion sensors (e.g., `binary_sensor.living_room_motion`)
- mmWave sensors
- Any sensor that indicates room presence

**Tips:**
- External temp sensor highly recommended!
- Presence sensors only needed if using Smart Mode
- You can skip both and click Submit (they're optional)

---

### Step 5 of 5: Temperature Settings

**What you'll see:**
```
Configure basic temperature settings for Living Room.

Almost there! Click Submit to create everything.

What happens next:
1. All helper entities will be created automatically
2. Your blueprint automation will be configured
3. Climate control will be ready to use immediately!
```

**Settings:**

**Target Temperature (°C):** `22` (default)
- Your ideal room temperature
- Range: 16-30°C

**Comfort Zone Width (±°C):** `2.0` (default)
- Temperature tolerance around target
- Example: 22°C ± 2°C = comfort zone 20-24°C
- Range: 0.5-5.0°C

**Enable Heating Mode:** ✅ (enabled by default)
- Turn ON for full climate control
- Turn OFF for cooling-only (hot climates)

**Enable Cooling Mode:** ✅ (enabled by default)
- Turn ON for full climate control
- Turn OFF for heating-only (cold climates)

**Click Submit!** 🚀

---

## ✅ What Happens After Submit

### Automatic Creation Process:

1. **Helper Entities Created** (13 helpers with all features):
   ```
   input_text.climate_last_mode_living_room
   input_datetime.climate_last_change_living_room
   input_number.climate_effectiveness_score_living_room
   input_number.climate_temp_history_living_room
   input_text.climate_trend_direction_living_room
   input_datetime.climate_mode_start_time_living_room
   input_datetime.climate_temp_stable_since_living_room
   input_text.climate_last_transition_living_room
   input_boolean.climate_manual_override_living_room
   input_boolean.climate_proximity_override_living_room
   input_select.climate_control_mode_living_room
   input_datetime.climate_presence_detected_living_room
   ```

2. **Automation Created** in `config/automations.yaml`:
   ```yaml
   - id: climate_control_living_room
     alias: Living Room Climate Control
     description: Smart climate control for Living Room - Created by Smart Climate Helper Creator
     use_blueprint:
       path: ultimate_climate_control.yaml
       input:
         room_name: Living Room
         climate_entities:
           - climate.living_room_ac
         helper_last_mode: input_text.climate_last_mode_living_room
         # ... all other helpers automatically mapped!
         target_temperature: 22
         comfort_zone_width: 2.0
         enable_heating_mode: true
         enable_cooling_mode: true
   ```

3. **Automations Reloaded** - Your new automation is immediately active!

### Success!

You'll see a confirmation and the integration will be added to your Devices & Services page.

Your climate control is now **fully operational**!

---

## 🎮 Using Your New Climate Control

### Immediate Usage

Your automation is now active and will:
- Monitor room temperature
- Control A/C based on your settings
- Track effectiveness and adapt power levels
- Detect manual overrides
- Respond to presence sensors (if configured)

### Control Mode Switching

If you enabled Control Mode Selection, you can switch modes:

1. Go to **Settings** → **Devices & Services** → **Helpers**
2. Find: `Climate Control Mode Living Room`
3. Change between:
   - **Auto** - Pure temperature-based control
   - **Smart** - Presence-aware control
   - **Manual** - User control only

### Monitoring

View your automation:
1. Go to **Settings** → **Automations & Scenes**
2. Find "Living Room Climate Control"
3. Click to see configuration
4. Enable debug mode for detailed logging

---

## 🔄 Setting Up Additional Rooms

To add more rooms:

1. Go to **Settings** → **Devices & Services**
2. Click **+ Add Integration**
3. Search "Smart Climate Helper Creator"
4. Run through the wizard again with different room name!

**Each room gets its own:**
- Set of helper entities
- Automation
- Independent configuration

---

## 🛠️ Advanced Configuration

### After Initial Setup

The wizard creates a basic working configuration. To customize further:

1. Go to **Settings** → **Automations & Scenes**
2. Find your room's automation
3. Click **⋮ Menu** → **Edit in YAML**
4. Modify advanced settings:
   - Temperature thresholds
   - Fan speeds
   - Timeout settings
   - Presence validation modes
   - And much more!

Refer to the [main README](README.md) for detailed configuration options.

---

## 📊 What You Get vs Manual Setup

### With Guided Setup (2-3 minutes):
1. Add integration
2. Answer 5 simple questions
3. Click Submit
4. ✅ DONE - Everything created and working!

### Manual Setup (30-60 minutes):
1. Create 13 helpers manually (10-15 min)
2. Name each helper correctly (5 min)
3. Configure each helper's settings (10 min)
4. Import blueprint (2 min)
5. Create automation from blueprint (5 min)
6. Select all helpers one by one (10 min)
7. Configure all settings (10 min)
8. Debug typos and misconfigurations (10-20 min)

**Time Saved: 27-57 minutes per room!** 🎉

---

## 🐛 Troubleshooting

### "No climate entities found"
- Make sure your A/C is integrated in Home Assistant
- Check Settings → Devices & Services for your A/C
- If it's there, restart Home Assistant

### "Already configured" error
- This room already has climate control setup
- Use a different room name
- Or delete the existing integration first

### Helpers not showing up
- Check Settings → Devices & Services → Helpers
- Search for your room name (e.g., "living_room")
- They should all be there with "Climate" in the name

### Automation not working
- Go to Settings → Automations
- Find your room's automation
- Check if it's enabled (toggle should be blue/on)
- Click on it to see any errors
- Check logs: Settings → System → Logs

### Want to start over
1. Settings → Devices & Services
2. Find "Smart Climate Helper Creator" entry for your room
3. Click **Delete**
4. Manually delete helpers: Settings → Helpers (search room name)
5. Delete automation: Settings → Automations
6. Run wizard again!

---

## 🎯 Best Practices

### For Best Results:

1. **Use External Temperature Sensor**
   - Much more accurate than A/C built-in sensors
   - Place in middle of room, seated height

2. **Enable All Features**
   - Dynamic Adaptation = smart power management
   - Manual Override = respects your changes
   - Control Modes = flexibility
   - Smart Mode = presence awareness

3. **Configure Presence Sensors**
   - If you have them, use them!
   - BLE + Motion = best accuracy
   - Use SMART validation mode

4. **Start with Defaults**
   - Target: 22°C
   - Comfort Width: ±2°C
   - Adjust after seeing how it works

5. **Enable Debug Logging Initially**
   - See what the automation is doing
   - Helps understand the system
   - Disable after you're comfortable

---

## 📚 Additional Resources

- **[Main README](README.md)** - Complete feature documentation
- **[Setup Guide](setup-new-room-guide.md)** - Detailed configuration reference
- **[Helper Audit](HELPER_AUDIT.md)** - Complete helper entity reference
- **[GitHub Issues](https://github.com/Chris971991/Smart-Climate-Control/issues)** - Report bugs or request features

---

## 🎉 Enjoy Your Automated Climate Control!

You now have a fully automated, intelligent climate control system that:
- ✅ Maintains perfect comfort automatically
- ✅ Adapts to your A/C's performance
- ✅ Saves energy with smart power management
- ✅ Respects your manual changes
- ✅ Responds to room presence
- ✅ Requires zero maintenance

**Welcome to the future of home climate control!** 🏠❄️🔥