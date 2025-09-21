#!/usr/bin/env python3
"""Test MIDI port creation on this system"""

import mido
import time

def test_midi_ports():
    print("=== MIDI Port Diagnostic ===")
    
    # Check available backends
    print(f"MIDI Backend: {mido.backend}")
    print(f"Available outputs: {mido.get_output_names()}")
    print(f"Available inputs: {mido.get_input_names()}")
    
    # Try to create virtual port
    print("\n=== Testing Virtual Port Creation ===")
    try:
        print("Attempting to create virtual output port...")
        port = mido.open_output('Test-Virtual-Port', virtual=True)
        print("✅ Virtual output port created successfully!")
        
        print("Checking if port appears in system...")
        outputs = mido.get_output_names()
        inputs = mido.get_input_names()
        print(f"Outputs after creation: {outputs}")
        print(f"Inputs after creation: {inputs}")
        
        if 'Test-Virtual-Port' in outputs or 'Test-Virtual-Port' in inputs:
            print("✅ Virtual port is visible in system")
        else:
            print("⚠️  Virtual port created but not visible in system lists")
        
        print("\nKeeping port alive for 10 seconds...")
        print("🔍 Check HeavyM MIDI devices NOW")
        time.sleep(10)
        
        port.close()
        print("✅ Port closed successfully")
        
    except Exception as e:
        print(f"❌ Virtual port creation failed: {e}")
        print("\n💡 Possible solutions:")
        print("   - macOS may need Audio MIDI Setup configuration")
        print("   - Try installing additional MIDI drivers")
        print("   - Use external MIDI software like IAC Driver")
        
        # Try alternative approach
        print("\n=== Testing Alternative Approach ===")
        try:
            print("Trying to list all available backends...")
            import rtmidi
            midi_out = rtmidi.MidiOut()
            print(f"RtMidi available: {midi_out}")
            del midi_out
        except Exception as e2:
            print(f"RtMidi test failed: {e2}")

if __name__ == "__main__":
    test_midi_ports()