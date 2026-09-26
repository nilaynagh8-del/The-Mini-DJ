# MIDI Keyboard — Complete Manual

*How everything works and how to use it. Written for someone who has never
touched MIDI before.*

---

## Table of Contents

1. [What you built](#1-what-you-built)
2. [MIDI in 5 minutes](#2-midi-in-5-minutes)
3. [Installing the firmware](#3-installing-the-firmware)
4. [Powering the keyboard](#4-powering-the-keyboard)
5. [Using it — Performance mode](#5-using-it--performance-mode)
6. [Using it — Settings pages](#6-using-it--settings-pages)
7. [Using it — Beat mode (standalone drums)](#7-using-it--beat-mode-standalone-drums)
8. [How the code works](#8-how-the-code-works)
9. [Hardware reference — how the PCB works](#9-hardware-reference--how-the-pcb-works)
10. [Customizing](#10-customizing)
11. [Troubleshooting](#11-troubleshooting)

---

## 1. What you built

A 12-key USB MIDI controller **and** standalone drum machine:

| Part | What it is |
|---|---|
| 12 mechanical keys | Play notes (or drums) |
| 2 rotary encoders (left, right) | Turn = adjust · push = button (with tap/double/triple press) |
| 2 sliders (bottom RV1, top RV2) | Analog control of any MIDI CC |
| 240×240 color LCD | Live status: notes, sliders, encoders, playhead |
| 14 RGB LEDs | Under-key glow + 2 encoder LEDs |
| I2S header (J2) | Where the PCM5102 DAC plugs in for beat mode |
| Pico (RP2040) | The brain, runs CircuitPython |

Two power sources: **USB** (data + power) or **battery** (power only, via
your switch into VSYS). Both at once is fine — USB wins.

---

## 2. MIDI in 5 minutes

MIDI is just small text-like messages sent over USB. The ones this keyboard
sends:

| Message | Meaning | When we send it |
|---|---|---|
| **Note On** (note number, velocity) | "a key went down" | You press a key. Note 60 = middle C. Velocity = how hard (ours is fixed 100) |
| **Note Off** | "key came up" | You release |
| **Control Change** (CC#, value 0–127) | "a knob/slider moved" | You turn an encoder or move a slider. CC 1 = mod wheel, CC 7 = volume, CC 74 = filter cutoff — these are standard numbers synths already understand |
| **CC 123, value 0** | "all notes off" (panic) | Left-encoder single push |

Your DAW (Ableton, FL Studio, GarageBand, Reaper…) receives these and makes
sound with whatever instrument is selected. **The keyboard makes no sound by
itself** — it's a controller. Except in beat mode, where it synthesizes its
own drums.

---

## 3. Installing the firmware

### Easy way

1. Plug the Pico in (it's the big chip on your PCB — it's a Raspberry Pi Pico module).
2. Double-click `install.ps1` → "Run with PowerShell".
3. When it says so: unplug, **hold the BOOTSEL button**, plug back in, release.
4. Wait. Done.

The installer flashes CircuitPython (the interpreter) once, then copies the
firmware files. To update your own edits later, re-run it — the flash step
is skipped since CircuitPython is already on the chip.

### Manual way

1. Hold **BOOTSEL**, plug in USB, release → a drive `RPI-RP2` appears.
2. Drag `firmware/adafruit-circuitpython-raspberry_pi_pico-en_US-10.3.1.uf2` onto it.
3. Board reboots as `CIRCUITPY`.
4. Copy `code.py`, `boot.py`, and the `lib/` folder onto `CIRCUITPY`.

### Seeing errors

Open [code.circuitpython.org](https://code.circuitpython.org) in Chrome/Edge,
click "Serial" — or use the Mu editor. If something's wrong with the code,
the error prints there.

---

## 4. Powering the keyboard

### USB only (no battery needed)

Everything works, including beat mode if a DAC is connected.

### Battery + switch (portable)

You need: 3.7 V LiPo/Li-Ion or 4×AA pack (4.5–5.5 V), any small slide
switch, optional PCM5102 DAC for sound.

```
Battery (+) ──► switch ──► Pico VSYS (physical pin 39, back row)
Battery (–) ─────────────► Pico GND  (physical pin 38)
```

- Flip the switch → keyboard boots, octave LEDs flash, screen shows "MIDI".
- Plugging USB while the switch is on: safe, USB takes over.
- **Never** connect a battery straight to the 3V3 pin — VSYS only.

### Sound for beat mode (PCM5102, ~$3)

```
PCM5102   →   Pico
VIN       →   3V3  (pin 36)
GND       →   GND
BCK       →   GP15
LCK       →   GP16
DIN       →   GP17
SCK       →   GND  (also solder the SCK jumper pad on the module)
```

Headphones plug into the DAC module's own 3.5 mm jack. Volume is the top
slider while in beat mode.

---

## 5. Using it — Performance mode

This is the main screen after boot. Just play.

### Keys

Press → note plays, key lights up on the screen grid and on the PCB's LED.
Release → stops. You can hold as many as you want (N-key rollover).

**Three layouts** — switch with **triple-push of the right encoder** (screen
bursts a ring animation + name):

| Layout | Left block (6 keys) | Right block (6 keys) |
|---|---|---|
| **PIANO** | C3, D3, E3, F3, G3, A3 … continues chromatically → | …A#3 up to G#4 |
| **MIRROR** | C3 D3 E3 F3 G3 A3 | same + one octave up |
| **DRUMS** | notes C3–A3 | GM drum map (channel 10): kick, snare, hats, etc. |

### Left encoder

| Gesture | Action |
|---|---|
| Turn | Octave shift −2…+6 (shown top-left of screen) |
| Push ×1 | **Panic** — all notes off (red LED flash) |
| Push ×2 | Enter **beat mode** |
| Push ×3 | Enter **arpeggiator page** |

### Right encoder

| Gesture | Action |
|---|---|
| Turn | Sends the selected CC (default CC 74 cutoff) |
| Push ×1 | Cycle which CC it controls: CUTOFF → MOD → VOLUME → EXPR → REVERB |
| Push ×2 | Enter **CC remap page** |
| Push ×3 | Switch layout (PIANO → MIRROR → DRUMS) |

### Sliders

- Bottom (RV1) = **CC 1, mod wheel**
- Top (RV2) = **CC 7, channel volume**

The DAW responds automatically — no mapping needed for these two.

---

## 6. Using it — Settings pages

### CC Remap page (double-push RIGHT encoder)

Screen shows both sliders with their current CC number. **Move a slider** —
it now sends that number as you drag? No: moving a slider *changes* which CC
it sends (the number follows your position 0–127, pick one you like, e.g.
CC 74 for cutoff, CC 71 for resonance, CC 2 for breath). **Push right
encoder** to save and go back. Everything is stored in flash and remembered
after power-off.

### Arpeggiator page (triple-push LEFT encoder)

Hold some keys, and the arp plays them as a repeating pattern for you.

| Row | Turn RIGHT encoder to change |
|---|---|
| ON/OFF | enable/disable |
| RATE | 1/4, 1/8, 1/8T (triplet), 1/16 |
| MODE | UP, DOWN, UPDOWN |
| EXIT | — (or just push RIGHT encoder) |

LEFT encoder moves the yellow selection. Leaving the page saves settings.

### Beat mode

→ next section.

---

## 7. Using it — Beat mode (standalone drums)

**Enter: double-push LEFT encoder.** Screen becomes a 16-step grid. This is
a real drum machine that runs on battery, no computer.

### What's on screen

- Top: pattern letter (A–F), BPM, play indicator (green = playing)
- Middle: 6 rows (lanes) × 16 steps. Row = drum sound, column = time.
  Lit cell = drum fires when the playhead crosses that column.
- **White column** = playhead (where we are now)
- **Yellow outline** = cursor (the step you're editing)

| Lane | Sound |
|---|---|
| KCK | kick drum |
| SNR | snare |
| CLP | clap |
| HHC | closed hi-hat (short) |
| HHO | open hi-hat (rings out) |
| TOM | tom |

### Making your first beat

1. Double-push LEFT encoder → grid appears.
2. Turn LEFT encoder to move the yellow cursor to step 1.
3. Tap right-block keys to toggle drums at that step: key 1 = kick lane,
   key 2 = snare, key 3 = clap, key 4 = HHC, key 5 = HHO, key 6 = tom.
   (It auditions the sound as you toggle — headphones on!)
4. Move cursor to step 5, add a snare. Step 9: kick again. Classic.
5. Push RIGHT encoder → **plays**. Push again → stops.
6. Whack the left-block keys anytime — live finger-drumming on top.

### Controls while in beat mode

| Control | Action |
|---|---|
| LEFT encoder | Move step cursor 1–16 |
| RIGHT encoder | BPM 40–220 |
| Bottom slider | BPM macro (sweep to feel it) |
| Top slider | Volume |
| RIGHT push | Play / stop |
| LEFT hold + LEFT-encoder turn | Switch pattern slot A–F |
| LEFT tap | Exit beat mode (saves everything) |
| LEFT hold ~600 ms | Clear current pattern |

### Patterns

Six slots A–F, all saved to flash and reloaded at boot:

- **Hold LEFT-encoder push + turn LEFT encoder** → switches between slots
  A→B→C→D→E→F→A… The pattern letter in the top-left corner shows where you
  are. The play/stop state keeps going — swap patterns live mid-groove.
- **Hold LEFT push ~600 ms** → clear the current slot (all cells off).

### Battery life

RP2040 + LCD + LEDs ≈ 100–150 mA. A 2000 mAh LiPo runs ~13–20 hours.

---

## 8. How the code works

```
CIRCUITPY/
├── boot.py            ← runs first: keeps USB + serial console alive
├── code.py            ← entry point, calls md_kbd.app.run()
└── lib/md_kbd/
    ├── config.py      ← every pin number + timing constant
    ├── util.py        ├── gp(): GPIO number → Pin object
    ├── settings.py    ← keyboard settings in flash (NVM, offset 0)
    ├── layouts.py     ← key→note maps + hardware-bit→physical position
    ├── matrix.py      ← scans 14 switches (12 keys + 2 encoder pushes)
    ├── encoders.py    ← rotation tracking (hardware quadrature)
    ├── sliders.py     ← ADC reads with noise filtering
    ├── leds.py        ← SK6812 patterns (hue per note, slider mirror)
    ├── lcd.py         ← ST7789 driver + drawing + 5×7 font (PIO-SPI!)
    ├── ui.py          ← every screen (perf, remap, arp, beat, animation)
    ├── arp.py         ← arpeggiator engine
    ├── audio.py       ← drum synthesis + sequencer + flash patterns
    ├── midi_io.py     ← USB MIDI packet sender
    └── app.py         ← the brain: ties everything together
```

### The main loop (app.py `run()`)

Runs forever, ~500 times a second:

1. **Scan the matrix** — one row low at a time, read 7 columns; debounce.
2. **Scan encoders** — rotation deltas become octave/CC/BPM changes.
3. **Poll the arpeggiator** — fire scheduled notes.
4. **Poll sliders** every 15 ms — emit CC only if value moved ≥ 3 counts.
5. **Handle pushes** — tap/double/triple gesture state machine.
6. **Redraw UI** if dirty and ≥ 60 ms since last draw (never blocks keys).
7. **Render LEDs** every 40 ms.
8. **In beat mode**: poll the sequencer, which schedules drum hits against
   a monotonic clock — timing never drifts even if drawing hiccups.

### The clever bits

- **PIO-SPI screen** — GP21 (MOSI) can't do hardware SPI on RP2040, so a
  2-instruction PIO state machine shifts pixels at ~21 Mbit/s. Faster than
  bit-banging, and leaves SPI0 free.
- **N-key rollover** — every key has a diode, so simultaneous presses are
  all detected distinctly.
- **Lazy audio** — drum samples (~100 KB) only exist while beat mode is
  active; entering MIDI-only costs zero RAM.
- **NVM layout** — keyboard settings at offset 0 (32 B), beat patterns at
  offset 1024 (~600 B). Proven non-overlapping.
- **Gesture engine** — pushes are counted in a 450 ms window, dispatched
  once, so 1×/2×/3× presses never mis-fire.
- **Hysteresis sliders** — an untouched pot never spams the DAW with
  jittery CC values.

---

## 9. Hardware reference — how the PCB works

Every pin, verified from your KiCad netlist:

| Pico GPIO | Connected to |
|---|---|
| GP0, GP1, GP3, GP4, GP5, GP6 | matrix columns 1–5 + col 7 (SW6/SW12) |
| GP2 | matrix "encoder" column (SW13/SW14 pushes) |
| GP7, GP8 | matrix rows 3, 4 (driven low one at a time) |
| GP9 | SK6812 LED data (14 LEDs in a chain) |
| GP10, GP11 | right encoder A/B (SW13) |
| GP12, GP13 | left encoder A/B (SW14) |
| GP14 | LCD reset |
| GP15, GP16, GP17 | I2S to DAC: BCK / LRCK / DIN |
| GP18, GP21 | LCD SPI: SCK / MOSI (PIO bit-banged) |
| GP19, GP22 | LCD CS / DC |
| GP20 | LCD backlight |
| GP26/ADC0 | bottom slider RV1 |
| GP27/ADC1 | top slider RV2 |

### Matrix map (which bit = which key)

14 switches on 2 rows × 7 columns. Bit = row×7 + col:

| Bit | Key | Physical position |
|---|---|---|
| 0, 7 | SW4, SW10 | left block top: middle, right |
| 6, 0, 7 | left block top L→R: SW6, SW4, SW10 | |
| 13, 1, 8 | left block bottom L→R: SW12, SW5, SW11 | |
| 2, 3, 4 | right block column 1: SW1 top, SW2 mid, SW3 bottom | |
| 9, 10, 11 | right block column 2: SW7 top, SW8 mid, SW9 bottom | |
| 5 | SW13 push | **right encoder push** |
| 12 | SW14 push | **left encoder push** |

(The `layouts.py` `HW_BITS` tuple encodes exactly this — edit it there if a
key feels wrong.)

### LED chain order

From the PCB: `#0 = first LED the data pin reaches (D7)` then winds through
the board. `layouts.py` `LED_CHAIN2KEY` maps chain position → the 12 keys;
`LED_ENC_CHAIN = (13, 12)` are the two encoder LEDs (left, right).

---

## 10. Customizing

All the fun stuff is in `lib/md_kbd/config.py`:

```python
MIDI_CHANNEL = 0        # 0-15 → drums typically want 9
ENC_CC_TARGETS = (74, 1, 7, 11, 91)   # right-encoder CC cycle
ENC_CC_NAMES = ("CUTOFF", "MOD", "VOLUME", "EXPRS", "REVERB")
LCD_X_OFFSET = 0        # image shifted? try 2 or 3
LCD_Y_OFFSET = 0
LCD_SM_FREQ = 62_500_000  # lower to 31_250_000 if screen is flaky
SLIDER_DEADBAND = 3     # raise if sliders jitter
DEBOUNCE_MS = 10        # raise if keys double-fire
```

**Base note / octave range**: `layouts.py` → `BASE = 48` (C3). Try 36 or 60.

**Drum sounds**: `audio.py` → `DRUMS` tuple (GM note numbers) and the
`_kick()`, `_snare()` etc. functions to reshape the synthesis.

**Colors / layout of the screen**: `ui.py` constants at the top.

After any edit: save the file onto `CIRCUITPY` — it reboots and runs it.
Break something? Delete `code.py`'s import and the board shows a safe error
on the serial console; restore from this folder.

---

## 11. Troubleshooting

| Symptom | Fix |
|---|---|
| Screen black | Check LCD solder; lower `LCD_SM_FREQ`; check backlight pin |
| Screen image shifted | `LCD_X_OFFSET` / `LCD_Y_OFFSET` in config.py |
| Wrong key plays | Swap entries in `HW_BITS` (layouts.py) |
| LED lights wrong key | Swap entries in `LED_CHAIN2KEY` (layouts.py) |
| Encoder counts backwards | Swap the A/B pins in config.py |
| Keys double-fire | Raise `DEBOUNCE_MS` to 15–20 |
| Sliders jitter in DAW | Raise `SLIDER_DEADBAND` |
| No USB MIDI device | Re-run installer; try cable that carries data |
| Beat mode silent | Check DAC wiring; top slider up; SCK jumper on module |
| Beat mode crackles | Normal for 8-bit lo-fi engine; lower volume |
| Board shows `CIRCUITPY` but no code runs | `code.py` has an error — check serial console |
| Stuck notes | Left-encoder single push = panic |

---

*Generated for Nilay's MIDI Keyboard — KiCad project "Midi Keyboard", rev 4
sheet, firmware v1.1.*
