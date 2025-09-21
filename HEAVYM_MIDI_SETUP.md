# HeavyM MIDI Setup Guide

## Overview
This guide explains how to set up MIDI control for HeavyM Demo version to work with the YOLO hand detection bridge.

## Why MIDI Instead of OSC?
- **HeavyM Demo**: OSC API is Pro-only, but MIDI mapping works in Demo
- **Cost**: Keep using free version while maintaining automation
- **Reliability**: MIDI mapping is more stable than OSC learning mode in Demo

## MIDI Bridge Configuration

### Bridge Script MIDI Notes
- **Note 60 (C4)**: Triggers sleep sequence (idle state)
- **Note 61 (C#4)**: Triggers scare sequence (hand detected)
- **Port Name**: "YOLO-HeavyM Bridge" (virtual MIDI port)

### Running the Bridge with MIDI
```bash
# Default mode (MIDI enabled)
python scripts/yolo_hand_scare_bridge.py --show

# Explicit MIDI mode
python scripts/yolo_hand_scare_bridge.py --use-midi --show

# Fall back to OSC (for Pro users)
python scripts/yolo_hand_scare_bridge.py --use-osc --show
```

## HeavyM Setup Steps

### 1. Enable MIDI Input
1. Open HeavyM
2. Go to **Preferences** → **Controls** → **MIDI**
3. Enable **MIDI Input**
4. Select **"YOLO-HeavyM Bridge"** as input device

### 2. Create Sequences
1. Create two sequences in HeavyM:
   - Name: **sleepseq** (idle/ambient content)
   - Name: **scareseq** (scare/activation content)
2. Make sure sequences are **not marked as Draft**

### 3. MIDI Learning Mode
1. In HeavyM, enable **MIDI Learning** mode
2. Click the **Play** button for **sleepseq**
3. Run: `python send_midi_test.py --sequence sleep`
4. HeavyM should map Note 60 (C4) to sleepseq Play button
5. Click the **Play** button for **scareseq**
6. Run: `python send_midi_test.py --sequence scare`
7. HeavyM should map Note 61 (C#4) to scareseq Play button
8. Disable **MIDI Learning** mode

### 4. Test Integration
```bash
# Test manual MIDI
python send_midi_test.py --sequence both

# Test full YOLO integration
python scripts/yolo_hand_scare_bridge.py --show
```

## Expected Behavior
- **No hand detected**: Sends Note 60 → HeavyM plays sleepseq
- **Hand detected**: Sends Note 61 → HeavyM plays scareseq
- **Transitions**: Immediate cut/fade based on HeavyM sequence settings

## Troubleshooting

### MIDI Port Not Visible in HeavyM
- Restart HeavyM after running the bridge script
- Check that virtual MIDI port is created: run `send_midi_test.py`
- Verify MIDI permissions on macOS/Windows

### Sequences Not Triggering
- Ensure sequences are not marked as **Draft**
- Verify MIDI learning mapped correct notes
- Check that sequence names match (case-sensitive)
- Test with MIDI monitor to confirm notes are being sent

### Bridge Script Issues
```bash
# Check MIDI setup
python -c "import mido; print('MIDI available:', len(mido.get_output_names()) >= 0)"

# Test MIDI manually
python send_midi_test.py --sequence both

# Run bridge with debugging
python scripts/yolo_hand_scare_bridge.py --debug --show
```

## Log Output Examples

### Successful MIDI Setup
```
HandScareController initialized
MIDI enabled: True
✓ MIDI virtual port 'YOLO-HeavyM Bridge' created
MIDI notes: Sleep=60 (C4), Scare=61 (C#4)
```

### MIDI Sequence Triggers
```
🖐️  HAND DETECTED! Confidence: 99.8%
   → Triggering SCARE mode
MIDI → Note 61 (C#4) ON (velocity 127) → scareseq
MIDI → Note 61 (C#4) OFF
   → SCARE timeout, returning to IDLE mode
MIDI → Note 60 (C4) ON (velocity 127) → sleepseq
MIDI → Note 60 (C4) OFF
```

## Version Compatibility
- **HeavyM Demo**: ✅ MIDI mapping supported
- **HeavyM Live**: ✅ MIDI mapping supported  
- **HeavyM Pro**: ✅ Can use either MIDI or OSC (`--use-osc` flag)

## Technical Notes
- MIDI notes use **channel 0** (channel 1 in some MIDI software)
- **Velocity 127** (maximum) for note-on events
- **100ms note duration** (note-on followed by note-off)
- Virtual MIDI port created automatically by bridge script