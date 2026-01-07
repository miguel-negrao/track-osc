import argparse
import math
import time

from pythonosc import udp_client


def clamp01(value):
    return max(0.0, min(1.0, value))


def run(ip, port, object_id, center_x, center_y, radius, period, fps):
    client = udp_client.SimpleUDPClient(ip, port)
    dt = 1.0 / fps

    while True:
        start = time.monotonic()
        angle = 0.0
        x = clamp01(center_x + radius * math.cos(angle))
        y = clamp01(center_y + radius * math.sin(angle))
        client.send_message("/object/created", [int(object_id), float(x), float(y)])
        print(f"/object/created {[int(object_id), float(x), float(y)]}")

        while True:
            elapsed = time.monotonic() - start
            if elapsed >= period:
                break

            angle = 2.0 * math.pi * (elapsed / period)
            x = clamp01(center_x + radius * math.cos(angle))
            y = clamp01(center_y + radius * math.sin(angle))
            client.send_message("/object/movement", [int(object_id), float(x), float(y)])
            time.sleep(dt)

        client.send_message("/object/deleted", int(object_id))
        print(f"/object/deleted {[int(object_id)]}")
        time.sleep(0.1)


def main():
    parser = argparse.ArgumentParser(
        description="Send test OSC messages for a single moving object."
    )
    parser.add_argument("--ip", default="127.0.0.1", help="OSC server IP")
    parser.add_argument("--port", type=int, default=8000, help="OSC server port")
    parser.add_argument("--id", type=int, default=1, help="Object id")
    parser.add_argument("--center-x", type=float, default=0.5)
    parser.add_argument("--center-y", type=float, default=0.5)
    parser.add_argument("--radius", type=float, default=0.25)
    parser.add_argument(
        "--period",
        type=float,
        default=4.0,
        help="Seconds to complete a circle before deletion",
    )
    parser.add_argument("--fps", type=float, default=30.0, help="Updates per second")
    args = parser.parse_args()

    run(
        ip=args.ip,
        port=args.port,
        object_id=args.id,
        center_x=args.center_x,
        center_y=args.center_y,
        radius=args.radius,
        period=args.period,
        fps=args.fps,
    )


if __name__ == "__main__":
    main()
