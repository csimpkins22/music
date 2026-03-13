#!/bin/bash
# Peripheral Glow — Logic Pro Project Setup Script
#
# This script generates an AppleScript that helps set up the
# Peripheral Glow project in Logic Pro. It copies preset files
# to the correct locations and provides step-by-step guidance.
#
# Usage: Run this on your Mac with Logic Pro installed.
#   chmod +x setup_peripheral_glow.sh
#   ./setup_peripheral_glow.sh

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PRESET_DIR="$HOME/Music/Audio Music Apps/Plug-In Settings/Retro Synth"
CHANNEL_STRIP_DIR="$HOME/Music/Audio Music Apps/Channel Strip Settings/Instrument"

echo "============================================"
echo "  Peripheral Glow — Logic Pro Setup"
echo "============================================"
echo ""

# Step 1: Copy Retro Synth presets
echo "Step 1: Installing Retro Synth presets..."
mkdir -p "$PRESET_DIR/Peripheral Glow"

if [ -d "$SCRIPT_DIR/retro_synth" ]; then
    cp "$SCRIPT_DIR/retro_synth/"*.plist "$PRESET_DIR/Peripheral Glow/" 2>/dev/null
    echo "  Copied presets to: $PRESET_DIR/Peripheral Glow/"
else
    echo "  Warning: retro_synth/ directory not found"
fi

echo ""
echo "Step 2: Open Logic Pro and create a new project (70 BPM, D minor, 4/4)"
echo ""
echo "Step 3: Create 11 Software Instrument tracks in this order:"
echo ""
echo "  Track  | Name               | Instrument              | Pan"
echo "  -------|--------------------|-----------------------|------"
echo "  1      | Organ Drone        | Vintage B3              | -20"
echo "  2      | Synth Arpeggio     | Retro Synth (Analog)    | +25"
echo "  3      | Synth Pad          | Retro Synth (Analog)    | +15"
echo "  4      | Bass               | Retro Synth (Analog)    |   0"
echo "  5      | Piano              | Studio Grand (Steinway) | -10"
echo "  6      | Vocal Melody       | Retro Synth (Analog)    |   0"
echo "  7      | Clean Guitar       | Retro Synth (FM)        | -30"
echo "  8      | Distorted Guitar   | Retro Synth (FM)        | +35"
echo "  9      | Strings            | Studio Strings          |   0"
echo "  10     | Synth Lead Motif   | Retro Synth (Analog)    | +10"
echo "  11     | Drums              | Drum Kit Designer       |   0"
echo ""
echo "Step 4: For Retro Synth tracks (2,3,4,6,7,8,10), load presets from:"
echo "  Retro Synth preset menu → User → Peripheral Glow → [preset name]"
echo ""
echo "Step 5: Import the MIDI file:"
echo "  File → Import → MIDI File → select 05_peripheral_glow.mid"
echo ""
echo "Step 6: Set up bus effects:"
echo "  Bus 1 (Reverb): ChromaVerb — Decay 2.8s, Wet 100%, Hall"
echo "  Bus 2 (Delay):  Stereo Delay — Dotted 1/8, Feedback 30%, Wet 100%"
echo ""
echo "Step 7: Master bus:"
echo "  Compressor: Threshold -14dB, Ratio 2.5:1, Attack 20ms, Release 150ms"
echo "  Channel EQ: +1dB @ 250Hz (warmth), -1dB @ 5kHz (lo-fi ceiling)"
echo ""
echo "For detailed track-by-track settings, see:"
echo "  guides/05_peripheral_glow_logic_pro_setup.md"
echo ""
echo "============================================"
echo "  Preset installation complete!"
echo "============================================"
