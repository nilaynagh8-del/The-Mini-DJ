# MIDI Keyboard Firmware (CircuitPython 10.3.1)

Firmware for the custom 12-key MIDI keyboard PCB (RP2040 / Raspberry Pi Pico).
USB MIDI controller **and** a standalone pocket beat machine.

## What it does

| Control | Function |
|---|---|
| **12 keys** | Play notes (velocity fixed at 100). Three layouts, switch by **triple-pressing the right encoder**: PIANO / MIRROR / DRUMS |
| **Left encoder** | Turn = octave shift (−2…+6). Push = panic (all notes off). **Double-push = arpeggiator page** |
| **Right encoder** | Turn = assignable CC (cycles CUTOFF→MOD→VOLUME→EXPRESSION→REVERB on single push). **Double-push = CC remap page** |
| **Right encoder triple push** | Switch key layout (screen animation confirms) |
| **Bottom slider (RV1)** | CC 1 (mod wheel) by default, remappable |
| **Top slider (RV2)** | CC 7 (channel volume) by default, remappable |
| **Encoder pushes** | Both wired into the key matrix — they also light their SK6812 LEDs |
| **14× SK6812** | Keys glow while held (hue = note), sliders mirror position, encoders show value |
| **240×240 LCD** | Live view: layout, octave, key grid lighting up, slider bars, encoder values, arp status, USB status |

Layouts:
- **PIANO** — continuous chromatic run starting at C3 (MIDI 48), left block then right block
- **MIRROR** — right block repeats the left block one octave up (great for octave stabs)
- **DRUMS** — left block notes, right block General MIDI drum map on channel 10

Everything (layout, octave, CC assignments, arp settings) **saves to flash** automatically when you leave a settings page — survives power-off.

## Install (one click)

1. Double-click `install.ps1` (or right-click → Run with PowerShell)
2. Follow the prompts: unplug, hold **BOOTSEL**, replug, release
3. The script flashes CircuitPython and copies everything to `CIRCUITPY`
4. Done — your keyboard appears as a USB MIDI device

The script can be re-run anytime to update the firmware files (skip to the CIRCUITPY step — CircuitPython is already installed).

## Manual install

1. Hold BOOTSEL while plugging in USB → `RPI-RP2` drive appears
2. Drag `firmware/adafruit-circuitpython-raspberry_pi_pico-en_US-10.3.1.uf2` onto it
3. Board reboots as `CIRCUITPY`
4. Copy `lib/`, `code.py`, `boot.py` from this folder onto `CIRCUITPY`

## Playing it

- Plug into any DAW (Ableton, FL, GarageBand…) — it shows up as a standard USB MIDI keyboard
- Hold keys and use the DAW's learn function to map the sliders/encoders
- **Arpeggiator**: triple-push the *left* encoder. L-enc selects ON/OFF, RATE, MODE; R-enc changes the selected value; right-push exits (and saves)

## 🥁 Beat mode (standalone, no computer)

Turn your keyboard into a pocket drum machine: 6 synthesized drums through
the I2S header → PCM5102 DAC → headphones.

| Gesture | Action |
|---|---|
| **Double-push LEFT encoder** | Enter/exit beat mode |
| Right-block keys (6) | Toggle drum hit at the step cursor (and audition it) |
| Left-block keys (6) | Whack the drums live, finger-drumming style |
| Left encoder | Move the step cursor (1-16) |
| Right encoder | BPM 40-220 |
| Bottom slider | BPM macro |
| Top slider | Output volume |
| Right-encoder push | Play / stop |
| Left-encoder tap | Exit beat mode (saves) |
| Left-encoder hold 600 ms | Clear current pattern |

6 pattern slots (A-F) × 16 steps × 6 lanes, all saved to flash. Step cursor
is the yellow column; the white column sweeping is the playhead.

## 🔋 Battery power

You need: a 3.7 V LiPo/Li-Ion (or 4×AA pack, 4.5-5.5 V) + a small slide
switch + a PCM5102 DAC module (~$3).

Wiring:
- Battery **+** → one leg of the switch → Pico **VSYS** (pin 39)
- Battery **–** → Pico **GND** (pin 38)
- PCM5102: **VIN→3V3 (pin 36)**, **GND→GND**, **BCK→GP15**, **LRCK/LCK→GP16**, **DIN→GP17**, **SCK→GND** (tie the SCK jumper on the module), **3.3V logic jumper open**
- Headphones: 3.5mm jack on the PCM5102 module's L/R/G

USB and battery can both be connected — the Pico's power path IC handles it
(USB wins when present). The switch simply disconnects the battery.

Beat mode lazily initializes audio the first time you use it, so MIDI-only
sessions pay zero memory cost.

## Tuning / troubleshooting

| Symptom | Fix |
|---|---|
| Screen shows shifted/mirrored image | Edit `LCD_X_OFFSET` / `LCD_Y_OFFSET` in `lib/md_kbd/config.py`, or set MADCTL rotation (see lcd.py) |
| Screen stays black | Check LCD solder joints; try lowering `LCD_SM_FREQ` in config.py (e.g. `31_250_000`) |
| Wrong key plays | Swap entries in `HW_BITS` in `lib/md_kbd/layouts.py` |
| LED #N lights the wrong key | Swap entries in `LED_CHAIN2KEY` in `layouts.py` |
| Encoder counts backwards | Swap the A/B pin numbers in `config.py` (`ENC_*_A` / `ENC_*_B`) |
| Slider jitters | Raise `SLIDER_DEADBAND` in config.py |
| Serial console | `code.circuitpython.org` in a browser, or Mu editor — errors print there |

## Source layout

```
code.py                    entry point
boot.py                    USB bring-up (kept minimal)
lib/md_kbd/
  config.py                pins, timing, CC targets (from your KiCad netlist)
  layouts.py               key layouts + hardware-bit ↔ physical mapping
  matrix.py                2×7 debounced matrix scan
  encoders.py              rotaryio quadrature readers
  sliders.py               oversampled ADC with hysteresis
  leds.py                  SK6812 patterns
  lcd.py                   ST7789 driver (PIO-SPI) + framebuffer + 5×7 font
  ui.py                    all screen pages + layout animation
  arp.py                   arpeggiator engine
  midi_io.py               USB MIDI packet sender
  settings.py              flash-persisted settings (NVM)
  app.py                   main state machine
```

## Future: standalone synth

The PCB has an I2S header (GP15/16/17) ready for a PCM5102 DAC module. That's a v2 feature — sound generator so the keyboard makes noise with no computer attached.
