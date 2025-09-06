# yolo_vpt_bridge.py
# Minimal YOLO -> VPT bridge (clips mode by default)
# pip install ultralytics opencv-python python-osc

import argparse, time
from ultralytics import YOLO
from pythonosc.udp_client import SimpleUDPClient
import cv2

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--model", required=True)
    p.add_argument("--source", default=0, help="camera index or video file")
    p.add_argument("--class-names", nargs="*", default=None)
    p.add_argument("--conf", type=float, default=0.6)
    p.add_argument("--cooldown", type=float, default=1.5)
    p.add_argument("--vpt-host", default="127.0.0.1")
    p.add_argument("--vpt-port", type=int, default=6666)
    p.add_argument("--mode", choices=["clips","presets"], default="clips")
    p.add_argument("--idle-clip", type=int, default=1)
    p.add_argument("--scare-clip", type=int, default=2)
    p.add_argument("--idle-preset", type=int, default=1)
    p.add_argument("--scare-preset", type=int, default=2)
    p.add_argument("--show", action="store_true")
    return p.parse_args()

def set_idle(osc, args):
    if args.mode == "clips":
        osc.send_message("/sources/1video/clipnr", args.idle_clip)
        osc.send_message("/sources/1video/start", [])
    else:
        osc.send_message("/preset", args.idle_preset)

def set_scare(osc, args):
    if args.mode == "clips":
        osc.send_message("/sources/1video/clipnr", args.scare_clip)
        osc.send_message("/sources/1video/start", [])
    else:
        osc.send_message("/preset", args.scare_preset)

def main():
    args = parse_args()
    model = YOLO(args.model)
    osc = SimpleUDPClient(args.vpt_host, args.vpt_port)

    # Start idle
    state = "idle"
    set_idle(osc, args)
    last = 0.0

    src = int(args.source) if str(args.source).isdigit() else args.source
    cap = cv2.VideoCapture(src)
    if not cap.isOpened():
        print("ERROR: cannot open source", args.source); return

    for r in model.predict(source=cap, stream=True, conf=args.conf, imgsz=640, verbose=False):
        detected = False
        boxes = getattr(r, "boxes", [])
        if boxes:
            for b in boxes:
                cls_id = int(b.cls[0])
                conf = float(b.conf[0])
                cname = r.names.get(cls_id, str(cls_id))
                if args.class_names is None or cname in args.class_names:
                    detected = True
                if args.show and hasattr(r, "plot"):
                    frame = r.plot()
                    cv2.imshow("YOLO -> VPT", frame)
                    if cv2.waitKey(1) & 0xFF == 27:
                        cap.release(); cv2.destroyAllWindows(); return

        now = time.time()
        if detected and state != "scare" and (now - last) > args.cooldown:
            set_scare(osc, args); state = "scare"; last = now
        elif not detected and state != "idle" and (now - last) > args.cooldown:
            set_idle(osc, args); state = "idle"; last = now

if __name__ == "__main__":
    main()
