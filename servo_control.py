#!/usr/bin/env python3
"""Small MG995 test using BCM GPIO numbering and conservative pulse limits."""
import argparse
import math
import time


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pin', type=int, default=18, help='BCM GPIO (default 18, physical pin 12)')
    parser.add_argument('--position', type=float, default=0,
                        help='Position from -1 to 1; 0 is center (default)')
    parser.add_argument('--seconds', type=float, default=2, help='Hold time, 0.1 to 60 seconds')
    parser.add_argument('--sweep', action='store_true', help='One small center/left/right/center test')
    parser.add_argument('--dry-run', action='store_true', help='Print commands without GPIO hardware')
    args = parser.parse_args()
    if not math.isfinite(args.position) or not -1 <= args.position <= 1:
        parser.error('--position must be between -1 and 1')
    if not math.isfinite(args.seconds) or not 0.1 <= args.seconds <= 60:
        parser.error('--seconds must be between 0.1 and 60')
    if not 0 <= args.pin <= 27:
        parser.error('--pin must be a BCM GPIO number from 0 to 27')

    positions = [0, -0.5, 0.5, 0] if args.sweep else [args.position]
    if args.dry_run:
        for position in positions:
            print(f'GPIO {args.pin}: {1500 + position * 500:.0f} us for {args.seconds:g} s')
        print('Release signal')
        return

    try:
        from gpiozero import Servo
        from gpiozero.pins.lgpio import LGPIOFactory
    except ImportError:
        parser.exit(1, 'Install dependencies: sudo apt install python3-gpiozero python3-lgpio\n')

    factory = LGPIOFactory()
    try:
        with Servo(args.pin, initial_value=None, min_pulse_width=0.001,
                   max_pulse_width=0.002, frame_width=0.020,
                   pin_factory=factory) as servo:
            try:
                for position in positions:
                    print(f'Position {position:+.2f}; holding {args.seconds:g} seconds', flush=True)
                    servo.value = position
                    time.sleep(args.seconds)
            finally:
                servo.detach()
    except KeyboardInterrupt:
        print('\nStopped; signal released.')
    finally:
        factory.close()


if __name__ == '__main__':
    main()
