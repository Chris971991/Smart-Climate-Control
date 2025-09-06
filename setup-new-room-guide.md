# Setting Up Climate Control for New Rooms

This guide explains how to add climate control functionality to new rooms using the provided templates.

## Prerequisites

Before setting up a new room, you need:
1. An `input_select` entity for the room's climate control mode
2. The mushroom-template-card custom component installed
3. Access to Home Assistant's script configuration

## Step 1: Create Input Select Entity

1. Go to **Settings > Devices & Services > Helpers**
2. Click **+ Create Helper**
3. Choose **Dropdown**
4. Configure:
   - **Name**: `Climate Control Mode [Room Display Name]`
   - **Entity ID**: `climate_control_mode_[room_name]`
   - **Options**: `Auto`, `Manual`, `Smart`
   - **Icon**: `mdi:air-conditioner`

## Step 2: Create the Script

1. Copy the content from `climate-control-script-template.yaml`
2. Replace all instances of:
   - `[ROOM_NAME]` with your room identifier (e.g., `living_room`, `bedroom`)
   - `[ROOM_DISPLAY]` with the display name (e.g., `Living Room`, `Bedroom`)
3. Add the script to your `scripts.yaml` file or create via Home Assistant UI
4. Restart Home Assistant or reload scripts

## Step 3: Create the Button

1. Copy the content from `mushroom-climate-control-button-template.yaml`
2. Replace all instances of `[ROOM_NAME]` with your room identifier
3. Add the button to your dashboard

## Example Setup for "Living Room"

### Input Select
- **Name**: `Climate Control Mode Living Room`
- **Entity ID**: `climate_control_mode_living_room`

### Script Name
```yaml
living_room_enable_climate_control_and_act_immediately:
```

### Button Configuration
```yaml
secondary: "{{ states('input_select.climate_control_mode_living_room') }}"
target:
  entity_id: script.living_room_enable_climate_control_and_act_immediately
```

## Mode Behavior

Each mode cycles to the next when the button is pressed:

- **Auto** → **Manual**: "Only proximity safety override active"
- **Manual** → **Smart**: "Aggressive presence detection active" 
- **Smart** → **Auto**: "Full automation active"

## Troubleshooting

- **Script not found error**: Ensure the script name in the button matches the actual script entity ID
- **Service call errors**: Use `script.turn_on` service instead of calling the script directly
- **YAML errors**: Check indentation and ensure all placeholders are replaced

## File Structure

```
Smart-Climate-Control/
├── mushroom-climate-control-button-template.yaml
├── climate-control-script-template.yaml
└── setup-new-room-guide.md
```