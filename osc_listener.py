#!/usr/bin/env python3
"""Simple OSC listener for testing HeavyM integration"""

import argparse
from pythonosc import dispatcher
from pythonosc import osc_server

def osc_handler(unused_addr, *args):
    """Handle incoming OSC messages"""
    print(f"OSC: {unused_addr} {args}")

def main():
    parser = argparse.ArgumentParser(description="OSC Message Listener")
    parser.add_argument("--ip", default="127.0.0.1", help="The ip to listen on")
    parser.add_argument("--port", type=int, default=7000, help="The port to listen on")
    args = parser.parse_args()

    dispatcher_obj = dispatcher.Dispatcher()
    dispatcher_obj.set_default_handler(osc_handler)

    server = osc_server.ThreadingOSCUDPServer((args.ip, args.port), dispatcher_obj)
    print(f"🎧 OSC Listener started on {args.ip}:{args.port}")
    print("Press Ctrl+C to stop")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping...")
        server.shutdown()

if __name__ == "__main__":
    main()