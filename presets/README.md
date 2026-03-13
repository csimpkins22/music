# Peripheral Glow — Logic Pro Preset Files

## Why not .channelstrip files?

Logic Pro's `.cst` (channel strip setting) format is a proprietary binary plist
with an undocumented internal structure. These files can only be created reliably
from within Logic Pro itself (Save Channel Strip Setting As...).

Instead, this directory provides **two alternatives** that achieve the same result:

### Option 1: Environment Setup Script (Recommended)
Run `setup_peripheral_glow.sh` — this opens an AppleScript in Script Editor
that creates the full 11-track project with all instruments, effects, and
mix settings pre-configured.

### Option 2: Retro Synth .pst Presets
The `retro_synth/` folder contains XML plist preset files for each Retro Synth
instance. Drop these into:
```
~/Music/Audio Music Apps/Plug-In Settings/Retro Synth/
```
Then load them from the preset menu inside Retro Synth.

## How to create your own .channelstrip files

Once you've set up the project (using either method above), you can save
channel strip settings for future use:

1. Click the **Setting** button at the top of any channel strip
2. Choose **Save Channel Strip Setting As...**
3. Name it (e.g., "PG - Organ Drone")
4. It saves to `~/Music/Audio Music Apps/Channel Strip Settings/`

This creates proper `.cst` files you can reload in any Logic project.
