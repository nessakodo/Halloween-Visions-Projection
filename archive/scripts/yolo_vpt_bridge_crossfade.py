# yolo_vpt_bridge_crossfade.py
# Two-layer crossfade (Layer 1 = idle, Layer 2 = scare).
# In VPT: make Layer1 source=1video clip1; Layer2 source=1video clip2; both loop.
# Start with L1=1.0, L2=0.0. This script fades them.

import argparse, time
from ultralytics import YOLO
from pythonosc.udp_client import SimpleUDPClient

def fade(osc, layer, val):
    val = max(0.0, min(1.0, float(val)))
    osc.send_message(f"/{layer}layer/fade", val)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--conf", type=float, default=0.6)
    ap.add_argument("--vpt-host", default="127.0.0.1")
    ap.add_argument("--vpt-port", type=int, default=6666)
    ap.add_argument("--rise", type=float, default=0.25)  # seconds
    args = ap.parse_args()

    model = YOLO(args.model)
    osc = SimpleUDPClient(args.vpt_host, args.vpt_port)

    # Ensure clips running
    osc.send_message("/sources/1video/clipnr", 1); osc.send_message("/sources/1video/start", [])
    osc.send_message("/sources/1video/clipnr", 2); osc.send_message("/sources/1video/start", [])
    fade(osc, 1, 1.0); fade(osc, 2, 0.0)
    state = "idle"; last = 0.0

    for r in model.predict(source=0, stream=True, conf=args.conf, imgsz=640, verbose=False):
        detected = bool(getattr(r, "boxes", []))
        now = time.time()
        if detected and state != "scare":
            # crossfade up layer 2
            t0 = time.time()
            while time.time() - t0 < args.rise:
                p = (time.time() - t0)/args.rise
                fade(osc, 1, 1.0 - p); fade(osc, 2, p)
            fade(osc, 1, 0.0); fade(osc, 2, 1.0)
            state = "scare"
        elif not detected and state != "idle":
            t0 = time.time()
            while time.time() - t0 < args.rise:
                p = (time.time() - t0)/args.rise
                fade(osc, 1, p); fade(osc, 2, 1.0 - p)
            fade(osc, 1, 1.0); fade(osc, 2, 0.0)
            state = "idle"

if __name__ == "__main__":
    main()
