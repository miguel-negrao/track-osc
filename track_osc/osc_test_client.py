import argparse
import time

from pythonosc import udp_client


def clamp01(value):
    return max(0.0, min(1.0, value))


def run(ip, port, object_id, period, fps):
    client = udp_client.SimpleUDPClient(ip, port)
    dt = 1.0 / fps

    while True:
        start = time.monotonic()
        x = 0.0
        y = 0.0
        client.send_message("/object/created", [int(object_id), float(x), float(y)])
        print(f"/object/created {[int(object_id), float(x), float(y)]}")

        while True:
            elapsed = time.monotonic() - start
            if elapsed >= period:
                break

            progress = clamp01(elapsed / period)
            segment = progress * 4.0
            if segment < 1.0:
                x = segment
                y = 0.0
            elif segment < 2.0:
                x = 1.0
                y = segment - 1.0
            elif segment < 3.0:
                x = 3.0 - segment
                y = 1.0
            else:
                x = 0.0
                y = 4.0 - segment
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
    parser.add_argument(
        "--period",
        type=float,
        default=6.0,
        help="Seconds to complete a square before deletion",
    )
    parser.add_argument("--fps", type=float, default=30.0, help="Updates per second")
    args = parser.parse_args()

    run(
        ip=args.ip,
        port=args.port,
        object_id=args.id,
        period=args.period,
        fps=args.fps,
    )


if __name__ == "__main__":
    main()
