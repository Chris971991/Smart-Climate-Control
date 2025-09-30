# Smart Climate Helper Creator - HACS Integration Guide

## Overview

The **Smart Climate Helper Creator** is a custom Home Assistant integration that automatically creates all required helper entities for the Ultimate Smart Climate Control blueprint with a simple GUI interface.

**No more manual helper creation!** Just fill out a form and all 6-10 helper entities are created automatically.

## What It Does

This integration creates the following helper entities based on your selected features:

### Always Created (Required):
1. **Input Text**: `input_text.climate_last_mode_{room}` - Tracks last active mode
2. **Input DateTime**: `input_datetime.climate_last_change_{room}` - Timestamp of last change

### Dynamic Adaptation Feature (Recommended):
3. **Input Number**: `input_number.climate_effectiveness_{room}` - Effectiveness percentage (0-100%)
4. **Input Number**: `input_number.climate_escalation_count_{room}` - Escalation counter (0-10)
5. **Input DateTime**: `input_datetime.climate_escalation_start_{room}` - Escalation start time

### Manual Override Detection Feature:
6. **Input Boolean**: `input_boolean.climate_manual_override_{room}` - Manual override flag

### Control Mode Selection Feature:
7. **Input Select**: `input_select.climate_control_mode_{room}` - Auto/Smart/Manual selector

### Temperature History Tracking Feature (Optional):
8. **Input Text**: `input_text.climate_temp_history_{room}` - Temperature history data

## Installation

### Step 1: Add to HACS

1. Open **HACS** in Home Assistant
2. Go to **Integrations**
3. Click the **⋮ Menu** (top right corner)
4. Select **Custom Repositories**
5. Add the repository:
   - **URL**: `https://github.com/Chris971991/Smart-Climate-Control`
   - **Category**: Integration
6. Click **Add**

### Step 2: Install Integration

1. In HACS → Integrations, search for **"Smart Climate Helper Creator"**
2. Click on it and then click **Download**
3. **Restart Home Assistant** (required)

### Step 3: Add Integration Instance

1. Go to **Settings** → **Devices & Services**
2. Click **+ Add Integration** (bottom right)
3. Search for **"Smart Climate Helper Creator"**
4. Click on it to start the setup wizard

## Configuration

### Setup Wizard - Step 1: Room Name

**Enter the room name** for which you want to create climate helpers.

**Examples:**
- Living Room
- Master Bedroom
- Office
- Guest Room

**Important Notes:**
- Room names with spaces are fully supported
- The integration automatically converts room names to valid entity IDs
- Example: "Living Room" → entity IDs will use "living_room"

### Setup Wizard - Step 2: Features

Select which features you want to enable. This determines which helper entities are created.

#### Recommended Settings:

**✅ Enable Dynamic Adaptation** (Default: ON)
- Creates effectiveness tracking helpers
- Enables power escalation/de-escalation features
- Required for smart temperature control
- **Recommendation**: Keep enabled for best performance

**✅ Enable Manual Override Detection** (Default: ON)
- Creates manual override helper
- Detects when user manually changes AC settings
- Prevents automation from fighting user changes
- **Recommendation**: Keep enabled for better user experience

**✅ Enable Control Mode Selection** (Default: ON)
- Creates Auto/Smart/Manual mode selector helper
- Allows switching between automation modes
- Required for Smart mode and Adaptive mode
- **Recommendation**: Keep enabled if using Smart/Adaptive modes

**✅ Enable Temperature History Tracking** (Default: ON)
- Creates temperature history helper
- Stores previous temperature reading for effectiveness calculations
- **Required** for dynamic adaptation to work properly
- Used for temperature stability detection
- **Recommendation**: Keep enabled (required for dynamic adaptation features)

### Step 3: Confirmation

Click **Submit** and the integration will:
1. Validate your room name
2. Check for duplicate helpers
3. Create all selected helper entities
4. Display confirmation message

**✅ Done!** All helper entities are now created and ready to use with the blueprint.

## Using the Helpers with the Blueprint

After creating helpers, configure your blueprint automation:

1. Go to **Settings** → **Automations & Scenes**
2. Click **Create Automation** → **Use Blueprint**
3. Select **"Ultimate Smart Climate Control"**
4. In the helper configuration section, select the entities created:

**Example for "Living Room":**
- Helper Last Mode: `input_text.climate_last_mode_living_room`
- Helper Last Change: `input_datetime.climate_last_change_living_room`
- Helper Effectiveness: `input_number.climate_effectiveness_living_room`
- Helper Escalation Count: `input_number.climate_escalation_count_living_room`
- Helper Escalation Start: `input_datetime.climate_escalation_start_living_room`
- Helper Manual Override: `input_boolean.climate_manual_override_living_room`
- Control Mode Helper: `input_select.climate_control_mode_living_room`

## Multiple Rooms

To set up multiple rooms, simply add the integration multiple times:

1. Go to Settings → Devices & Services → Add Integration
2. Search for "Smart Climate Helper Creator"
3. Enter the new room name
4. Select features
5. Submit

**Each room gets its own unique set of helper entities.**

**Example:**
- Living Room helpers: `climate_*_living_room`
- Bedroom helpers: `climate_*_bedroom`
- Office helpers: `climate_*_office`

## Helper Entity Naming Convention

All helpers follow this pattern:
```
{domain}.climate_{helper_type}_{room_name_sanitized}
```

**Examples:**
- "Living Room" → `input_text.climate_last_mode_living_room`
- "Master Bedroom" → `input_datetime.climate_last_change_master_bedroom`
- "Home Office" → `input_number.climate_effectiveness_home_office`

## Updating Features

You can update which features are enabled through the integration options:

1. Go to Settings → Devices & Services
2. Find "Smart Climate Helper Creator" integration
3. Click on the room name
4. Click **Configure**
5. Update feature selections

**⚠️ Important:** Changing options does NOT automatically create or delete helpers. You may need to:
- Manually create missing helpers for newly enabled features
- Manually delete helpers for disabled features (optional - they don't hurt if left)

## Uninstalling

### Remove Integration Instance
1. Go to Settings → Devices & Services
2. Find the room entry under "Smart Climate Helper Creator"
3. Click **Delete**

**⚠️ Note:** Removing the integration does NOT delete the helper entities. This is intentional to prevent data loss.

### Delete Helper Entities (Optional)
If you want to completely remove helpers:
1. Go to Settings → Devices & Services → Helpers
2. Search for `climate_*_{room_name}`
3. Click each helper → **Delete**

## Troubleshooting

### "Already Configured" Error
**Problem:** You tried to add helpers for a room that already exists.

**Solution:**
- If you want to recreate helpers, first delete the existing integration instance
- Then add a new integration instance for that room

### Helpers Not Appearing
**Problem:** Created integration but can't find helper entities.

**Solutions:**
1. Check Settings → Devices & Services → Helpers
2. Search for your room name (e.g., "living_room")
3. Verify entities exist with correct naming pattern
4. Try restarting Home Assistant

### Wrong Features Enabled
**Problem:** Created helpers but need different features.

**Solutions:**
- **Add missing helpers manually** (Settings → Helpers → Create Helper)
- **OR** Delete integration instance and recreate with correct features
- Unused helpers don't cause problems if left in place

### Integration Not Found in HACS
**Problem:** Can't find "Smart Climate Helper Creator" in HACS.

**Solutions:**
1. Verify you added the custom repository correctly
2. Check repository URL: `https://github.com/Chris971991/Smart-Climate-Control`
3. Make sure category is set to "Integration"
4. Try refreshing HACS (⋮ Menu → Reload)

### Service Call Errors
**Problem:** Integration fails to create helpers.

**Solutions:**
1. Check Home Assistant logs: Settings → System → Logs
2. Verify you have permissions to create helpers
3. Try creating a helper manually first to test permissions
4. Restart Home Assistant and try again

## Technical Details

### Files Created
The integration installs to:
```
config/custom_components/smart_climate_helper_creator/
├── __init__.py
├── config_flow.py
├── manifest.json
├── strings.json
└── translations/
    └── en.json
```

### Services Used
The integration uses standard Home Assistant services:
- `input_text.create`
- `input_datetime.create`
- `input_number.create`
- `input_boolean.create`
- `input_select.create`

### Compatibility
- **Home Assistant**: 2023.1.0 or newer
- **HACS**: Any version
- **Blueprint**: Ultimate Smart Climate Control v2.22.16+

## Version Compatibility

| Helper Creator Version | Blueprint Version | Compatible |
|------------------------|-------------------|------------|
| v2.22.16               | v2.22.16          | ✅ Yes     |
| v2.22.16               | v2.22.15          | ✅ Yes     |
| v2.22.16               | v2.22.x           | ✅ Yes     |
| v2.22.16               | v2.x.x            | ⚠️ Mostly  |

**Recommendation:** Keep both the helper creator and blueprint updated to the latest version.

## Support & Issues

If you encounter any issues:

1. **Check the logs**: Settings → System → Logs
2. **Review this guide**: Make sure you followed all steps
3. **Report issues**: [GitHub Issues](https://github.com/Chris971991/Smart-Climate-Control/issues)

When reporting issues, please include:
- Home Assistant version
- Helper Creator version
- Room name you tried to configure
- Error message from logs
- Steps to reproduce

## Benefits Summary

### Why Use the Helper Creator?

**Without Helper Creator:**
- ⏱️ 30+ minutes per room
- 📝 Create 6-10 helpers manually
- 🎯 Risk of typos in entity IDs
- 📋 Complex configuration copying
- 😓 Tedious and error-prone

**With Helper Creator:**
- ⏱️ 2 minutes per room
- 🖱️ Fill out simple form
- ✅ Automatic entity ID generation
- 🎯 Zero configuration errors
- 😊 Fast and foolproof

## Future Enhancements

Planned features for future versions:
- Bulk room creation (multiple rooms at once)
- Helper validation and repair tools
- Migration tool for existing manual helpers
- Blueprint configuration export
- One-click full setup (integration + automation)

---

**Made with ❤️ for the Home Assistant Community**

For complete blueprint documentation, see [README.md](README.md)