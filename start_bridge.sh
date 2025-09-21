#!/bin/bash
# YOLO Hand Detection Bridge Launcher for HeavyM

echo "🎃 Halloween YOLO → HeavyM Bridge"
echo "================================="

# Check if Python virtual environment should be activated
if [ -d ".venv" ]; then
    echo "📦 Activating virtual environment..."
    source .venv/bin/activate
fi

# Check if required model exists
if [ ! -f "best.pt" ]; then
    echo "⚠️  Model file 'best.pt' not found in current directory"
    echo "💡 Make sure you have the YOLO hand detection model file"
    echo ""
fi

# Display current MIDI ports
echo "🎹 Available MIDI Ports:"
python -c "import mido; print('Outputs:', mido.get_output_names()); print('Inputs:', mido.get_input_names())" 2>/dev/null || echo "MIDI check failed"
echo ""

# Start the bridge
echo "🚀 Starting YOLO Hand Detection Bridge..."
echo "💡 Press Ctrl+C to stop"
echo ""

# Run with show flag by default
python scripts/yolo_hand_scare_bridge.py --show

echo ""
echo "🛑 Bridge stopped"