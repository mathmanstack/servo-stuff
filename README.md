# MG995 servo on Raspberry Pi

A small Python command-line test for a standard positional MG995 on Raspberry Pi OS.
Run this on the Pi connected to the servo, not on your Windows computer.

## Wiring (disconnect power first)

Use a regulated 5 V supply rated for at least 3 A for one servo. Do not use a
rectangular 9 V battery, the Pi's power pins, or the small breadboard regulator
to power this servo. Connect the supply directly to the servo with suitable wire.
Power the Pi separately through its normal power connector.

| Connection | Destination |
| --- | --- |
| Servo red | External supply +5 V |
| Servo brown/black | External supply negative |
| Pi GND, physical pin 6 | Same external supply negative |
| Servo orange/yellow signal | GPIO18, physical pin 12 |

GPIO numbers in the program are BCM numbers, not physical header pin numbers.
Confirm your servo's wire assignments. Leave the mechanism unloaded for the first test.
If the servo does not respond to the Pi's 3.3 V signal, check the wiring and the
input specification for your particular servo before adding a suitable level shifter.

## Install and run on the Pi

```bash
sudo apt update
sudo apt install -y git python3-gpiozero python3-lgpio
git clone https://github.com/mathmanstack/mg995-pi.git
cd mg995-pi
python3 servo_control.py --dry-run --sweep
python3 servo_control.py
python3 servo_control.py --sweep
```

The first hardware command centers the servo for two seconds, then releases the
signal. The sweep visits center, a small movement each way, then center, and stops.
Press Ctrl+C to stop early. Releasing the signal does not guarantee the mechanism
will hold its position; disconnect servo power if it keeps moving or straining.

```bash
python3 servo_control.py --position -0.5
python3 servo_control.py --position 0.5 --seconds 5
python3 servo_control.py --pin 18 --position 0
```

Positions are normalized commands, not measured angles. The script uses 50 Hz,
with a 1.5 ms center and a conservative 1–2 ms pulse range. Actual travel depends
on the servo; do not force it against a mechanical stop. A continuous-rotation
MG995 variant interprets these pulses as speed/direction instead of position.

If GPIO access is denied, check `groups`. On Raspberry Pi OS you can add your
user with `sudo usermod -aG gpio "$USER"`, then log out and log in again.
If the servo jitters, first check power and ground. Linux-timed GPIO can also
introduce jitter; a dedicated servo controller is preferable for precise motion.

## Validation

Dry-run exercises argument validation and command planning without GPIO libraries.
Physical motion must be tested on your Pi; it has not been verified on hardware.

Reference: [GPIO Zero Servo documentation](https://gpiozero.readthedocs.io/en/stable/api_output.html#servo).
