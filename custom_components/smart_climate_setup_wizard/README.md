# Smart Climate Control Setup Wizard

**Version:** 3.0.2
**Author:** Chris971991

A complete guided setup wizard for the [Ultimate Smart Climate Control](https://github.com/Chris971991/Smart-Climate-Control) blueprint. Creates all required helper entities and automation configuration automatically—no manual YAML editing required!

---

## ✨ Features

✅ **2-Minute Setup** - Complete room configuration in just a few clicks
✅ **Zero Manual Work** - All helpers and automations created automatically
✅ **Package-Based** - Non-destructive helper creation using Home Assistant's package system
✅ **Dashboard Card Generator** - Optional Lovelace card generation for easy control
✅ **Safe & Isolated** - Each room's helpers are independent and organized
✅ **Bedroom Mode Support** - Intelligent sleep detection with bed sensor integration
✅ **Duplicate Detection** - Prevents conflicts with existing room setups

---

## 📋 Prerequisites

- **Home Assistant** 2023.1.0 or newer
- **HACS** installed and configured
- **Ultimate Smart Climate Control Blueprint** imported ([get it here](https://github.com/Chris971991/Smart-Climate-Control))
- **Climate entities** (A/C units) integrated in Home Assistant

---

## 🚀 Installation

### Method 1: Via HACS (Recommended)

1. Open **HACS** in Home Assistant
2. Go to **Integrations**
3. Click **⋮ Menu** (top right) → **Custom Repositories**
4. Add repository:
   - **URL**: `https://github.com/Chris971991/Smart-Climate-Control`
   - **Category**: **Integration**
5. Click **Add**
6. Search for **"Smart Climate Control Setup Wizard"**
7. Click **Download**
8. **Restart Home Assistant**

### Method 2: Manual Installation

1. Download the `custom_components/smart_climate_setup_wizard/` folder
2. Copy to `<config>/custom_components/smart_climate_setup_wizard/`
3. **Restart Home Assistant**

---

## 🎯 Quick Start Guide

### Step 1: Start the Wizard

1. Go to **Settings** → **Devices & Services**
2. Click **+ Add Integration**
3. Search for **"Smart Climate Control Setup Wizard"**
4. Click to start setup

### Step 2: Follow the Guided Steps

The wizard will guide you through:

1. **Room Name** - Enter the room name (e.g., "Living Room")
2. **Climate Entities** - Select your A/C units for this room
3. **Temperature Sensor** - Choose a temperature sensor (optional)
4. **Presence Sensors** - Select motion/BLE/bed sensors for Smart mode
5. **Bedroom Mode** - Enable if room has a bed occupancy sensor (NEW in v3.0.2)
6. **Temperature Settings** - Set target temps and comfort zones
7. **Advanced Options** - Configure scheduling, dynamic adaptation, etc.
8. **Dashboard Card** - Optionally generate a Lovelace control card

### Step 3: Done!

The wizard automatically creates:
- ✅ All required helper entities (in `packages/climate_helpers_[room].yaml`)
- ✅ Complete blueprint automation (fully configured)
- ✅ Optional dashboard card (ready to paste into Lovelace)

---

## 🛏️ Bedroom Mode (New in v3.0.2)

The wizard now intelligently handles bedrooms with bed occupancy sensors:

### What It Does

When you select presence sensors including a bed sensor, the wizard asks:

> **Is [Room Name] a bedroom with a bed occupancy sensor?**

- **YES** → Automatically selects **BEDROOM** validation mode
  - Detects presence when sleeping (bed sensor)
  - Detects presence when awake (motion sensor)
  - Prevents false positives (requires phone + bed OR motion)

- **NO** → Uses **SMART** validation mode
  - Requires both BLE and motion sensors
  - Standard presence detection for living areas

### Supported Bed Sensors

Any sensor reporting occupancy states:
- `binary_sensor.bed_occupancy`
- ESPHome bed sensors
- Pressure mat sensors
- Smart bed integrations

---

## 📦 How Helper Entities Are Created

The wizard uses Home Assistant's **package system** for clean, non-destructive helper creation:

### Package File Location
```
<config>/packages/climate_helpers_[room].yaml
```

### Benefits
- ✅ **Non-destructive** - Doesn't interfere with existing helpers
- ✅ **Organized** - Each room's helpers in one file
- ✅ **Easy to Remove** - Delete the package file to remove all helpers
- ✅ **Version Control Friendly** - Clean YAML files you can track

### Package Contents
Each package file contains all required helpers for that room:
- `input_text.climate_last_mode_[room]` - Last active mode tracker
- `input_datetime.climate_last_change_[room]` - Last change timestamp
- `input_select.climate_control_mode_[room]` - Auto/Smart/Manual selector
- Additional helpers based on enabled features

---

## 🔧 What Gets Created

### Always Created (Required)
- **Last Mode Tracker** (`input_text`) - Tracks last active temperature mode
- **Last Change Timestamp** (`input_datetime`) - When mode last changed

### Smart Mode Enabled
- **Control Mode Selector** (`input_select`) - Auto/Smart/Manual dropdown
- **Presence Detection Timestamp** (`input_datetime`) - When presence last detected
- **Proximity Override** (`input_boolean`) - Manual proximity override

### Dynamic Adaptation Enabled
- **Temperature History** (`input_number`) - Historical temperature data
- **Trend Direction** (`input_text`) - Rising/falling/stable
- **Mode Start Time** (`input_datetime`) - When current mode started
- **Effectiveness Score** (`input_number`) - Mode effectiveness percentage
- **Temperature Stable Since** (`input_datetime`) - Stability tracking
- **Last Transition** (`input_text`) - Last heating/cooling transition

---

## 🎮 Dashboard Card Generator

The wizard can generate a complete Lovelace card for room climate control:

### Features
- Current temperature display
- Target temperature adjustment
- Control mode selector (Auto/Smart/Manual)
- A/C unit controls
- Presence status indicators
- Compact, mobile-friendly design

### How to Use
1. Select **"Yes"** when asked to generate a dashboard card
2. Copy the generated YAML
3. Go to your dashboard → **Edit Dashboard**
4. **Add Card** → **Manual** (YAML editor)
5. Paste the YAML and save

---

## 🛡️ Duplicate Detection & Conflict Prevention

The wizard includes comprehensive checks to prevent conflicts:

### Room Name Duplication
- Checks if room already has a setup
- Prevents duplicate configurations
- Error: *"Climate control for this room already exists"*

### Climate Entity Conflicts
- Detects if A/C units are already controlled by another room
- Shows which room is using the conflicting entity
- Allows you to resolve conflicts before proceeding

### Safe Setup Flow
- Validates all inputs before creating entities
- Rolls back on errors
- Ensures clean, conflict-free configuration

---

## 🔄 Updating Existing Rooms

To modify an existing room's configuration:

1. **Delete the existing setup:**
   - Go to **Settings** → **Devices & Services**
   - Find the room in **Smart Climate Control Setup Wizard**
   - Click **Delete**

2. **Remove the package file:**
   - Delete `<config>/packages/climate_helpers_[room].yaml`

3. **Restart Home Assistant**

4. **Run the wizard again** with new settings

---

## 📖 Complete Documentation

For full blueprint documentation, features, and advanced configuration:

👉 [Ultimate Smart Climate Control Blueprint Documentation](https://github.com/Chris971991/Smart-Climate-Control)

---

## 🐛 Troubleshooting

### Wizard Not Appearing
- Ensure you've restarted Home Assistant after installation
- Check `<config>/custom_components/smart_climate_setup_wizard/` exists
- Check Home Assistant logs for errors

### Helpers Not Created
- Check `<config>/packages/` directory exists
- Verify `packages: !include_dir_named packages` in `configuration.yaml`
- Restart Home Assistant after wizard completes

### Automation Not Working
- Ensure the blueprint is imported first
- Check automation in **Settings** → **Automations & Scenes**
- Verify all selected entities exist and are available

### Bedroom Mode Not Working
- Ensure you selected the bed sensor in presence sensors list
- Verify you answered YES to the bedroom mode question
- Check automation shows `presence_validation_mode: bedroom`

---

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/Chris971991/Smart-Climate-Control/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Chris971991/Smart-Climate-Control/discussions)
- **Blueprint Documentation**: [README.md](https://github.com/Chris971991/Smart-Climate-Control/blob/main/README.md)

---

## 📝 Version History

### v3.0.2 (Latest)
- ✨ Added BEDROOM mode awareness and automatic selection
- ✨ New bedroom configuration step asks if room has bed sensor
- ✨ Wizard now guides users to include bed occupancy sensors
- ✨ Automatic validation mode selection (BEDROOM vs SMART)
- 🔧 Updated presence sensor step description for bed sensors
- 📋 Enhanced user guidance for bedroom setups

### v3.0.1
- ✨ Complete guided setup wizard
- ✨ Package-based helper creation
- ✨ Dashboard card generator
- ✨ Duplicate detection
- ✨ Climate entity conflict prevention
- 🐛 Initial stable release

---

## 📄 License

This integration is part of the Smart Climate Control project.

**Author:** Chris971991
**Repository:** https://github.com/Chris971991/Smart-Climate-Control
**Blueprint Version Compatibility:** v3.0.22+

---

## 🆕 What's New in Blueprint v3.0.22

The wizard now supports the latest blueprint features:

### ⚡ Smart Stall Detection
- **Time-Based Escalation** - Automatically boosts power if AC runs too long with poor progress
- **Configurable Thresholds** - Customize stall time (5-60min) and progress rate (0.001-0.1°C/min)
- **Accurate Runtime Tracking** - Fixed timer resets when AC turns ON/OFF

### 🎨 New Advanced Settings (Auto-Configured)
All new settings come with perfect defaults - no manual configuration needed:
- **Stall Escalation Time**: 15 minutes (balanced)
- **Minimum Progress Rate**: 0.01°C/min (average AC)
- **Temperature Stall Tolerance**: 1.0°C (now actually works!)

The wizard automatically applies these optimal defaults when creating your automation!
