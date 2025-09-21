#!/usr/bin/env python3
"""Setup macOS MIDI for HeavyM integration"""

import subprocess
import time

def setup_macos_midi():
    print("🍎 macOS MIDI Setup for HeavyM")
    print("=" * 50)
    
    print("\n📋 Manual Setup Required:")
    print("1. Open 'Audio MIDI Setup' app (Applications > Utilities)")
    print("2. Window > Show MIDI Studio")
    print("3. Double-click 'IAC Driver'")
    print("4. ✅ Check 'Device is online'")
    print("5. Add a new port named 'YOLO-HeavyM'")
    print("6. Click 'Apply'")
    
    print("\n⏱️  Waiting 10 seconds for you to complete setup...")
    time.sleep(10)
    
    print("\n🔍 Testing MIDI ports after setup...")
    try:
        import mido
        outputs = mido.get_output_names()
        inputs = mido.get_input_names()
        
        print(f"Available outputs: {outputs}")
        print(f"Available inputs: {inputs}")
        
        # Look for IAC or YOLO ports
        yolo_ports = [p for p in outputs + inputs if 'YOLO' in p or 'IAC' in p]
        if yolo_ports:
            print(f"✅ Found MIDI ports: {yolo_ports}")
            return yolo_ports[0]  # Return first found port
        else:
            print("⚠️  No IAC or YOLO ports found")
            print("💡 Try: IAC Driver > Add Port > Name: 'YOLO-HeavyM'")
            return None
            
    except Exception as e:
        print(f"❌ MIDI test failed: {e}")
        return None

def test_midi_connection(port_name):
    """Test sending MIDI to the specified port"""
    if not port_name:
        print("❌ No port available for testing")
        return False
        
    try:
        import mido
        print(f"\n🎹 Testing MIDI connection to '{port_name}'...")
        
        midi_out = mido.open_output(port_name)
        
        # Send test note
        msg = mido.Message('note_on', channel=0, note=60, velocity=127)
        midi_out.send(msg)
        print("📤 Sent: Note 60 (C4) ON")
        
        time.sleep(0.1)
        
        msg_off = mido.Message('note_off', channel=0, note=60, velocity=0)
        midi_out.send(msg_off)
        print("📤 Sent: Note 60 (C4) OFF")
        
        midi_out.close()
        print("✅ MIDI test successful!")
        return True
        
    except Exception as e:
        print(f"❌ MIDI test failed: {e}")
        return False

if __name__ == "__main__":
    port = setup_macos_midi()
    
    if port:
        test_midi_connection(port)
        print(f"\n🎯 Next steps:")
        print(f"1. In HeavyM: Preferences > Controls > MIDI")
        print(f"2. Select '{port}' as MIDI input device")
        print(f"3. Run: python scripts/yolo_hand_scare_bridge.py --show")
    else:
        print(f"\n❌ Setup incomplete. Please:")
        print(f"1. Complete IAC Driver setup manually")
        print(f"2. Run this script again to test")