#!/usr/bin/env python3
"""Manual MIDI test script for HeavyM Demo sequence control"""

import time
import argparse
import mido

def main():
    parser = argparse.ArgumentParser(description="Manual HeavyM MIDI Test")
    parser.add_argument("--sequence", choices=["sleep", "scare", "both"], default="both", 
                       help="Which sequence to trigger")
    parser.add_argument("--delay", type=float, default=2.0, 
                       help="Delay between sequences (for 'both' mode)")
    parser.add_argument("--port", default="YOLO-HeavyM Bridge", 
                       help="MIDI port name")
    args = parser.parse_args()

    try:
        # Create virtual MIDI port
        midi_out = mido.open_output(args.port, virtual=True)
        print(f"🎹 MIDI port '{args.port}' created")
        print(f"📍 HeavyM should see this port in MIDI input devices")
        
        # MIDI note assignments (matching bridge script)
        note_sleep = 60  # C4
        note_scare = 61  # C#4
        
        if args.sequence in ["sleep", "both"]:
            print(f"📤 Sending: MIDI Note {note_sleep} (C4) ON → sleepseq")
            msg = mido.Message('note_on', channel=0, note=note_sleep, velocity=127)
            midi_out.send(msg)
            time.sleep(0.1)
            msg_off = mido.Message('note_off', channel=0, note=note_sleep, velocity=0)
            midi_out.send(msg_off)
            print(f"📤 Sending: MIDI Note {note_sleep} (C4) OFF")
            
            if args.sequence == "both":
                print(f"⏱️  Waiting {args.delay}s...")
                time.sleep(args.delay)
        
        if args.sequence in ["scare", "both"]:
            print(f"📤 Sending: MIDI Note {note_scare} (C#4) ON → scareseq")
            msg = mido.Message('note_on', channel=0, note=note_scare, velocity=127)
            midi_out.send(msg)
            time.sleep(0.1)
            msg_off = mido.Message('note_off', channel=0, note=note_scare, velocity=0)
            midi_out.send(msg_off)
            print(f"📤 Sending: MIDI Note {note_scare} (C#4) OFF")
        
        print("✅ Test MIDI messages sent!")
        print("\n💡 Expected behavior:")
        print("   - HeavyM should see MIDI input activity")
        print("   - If mapped: sequences should switch immediately")
        print("   - Check HeavyM Preferences → Controls → MIDI")
        
        # Keep port alive for a moment
        print("\n⏳ Keeping MIDI port alive for 5 seconds...")
        time.sleep(5)
        
        midi_out.close()
        print("🔌 MIDI port closed")
        
    except Exception as e:
        print(f"❌ MIDI test failed: {e}")
        print("\n💡 Troubleshooting:")
        print("   - Ensure python-rtmidi is installed: pip install python-rtmidi")
        print("   - Check system MIDI permissions")

if __name__ == "__main__":
    main()