# The-Mini-DJ
A small, portable, MIDI keyboard to make beats on the go.

*(or just a cooler way to make some beats)* 
<img width="986" height="579" alt="image" src="https://github.com/user-attachments/assets/dfcaae29-78cc-4468-861f-9d36c7313362" />



---

## Quick Start

1. Download this repo and open the `firmware` folder.
2. Hold **BOOTSEL** and plug in the Pico — a drive called `RPI-RP2` appears.
3. Run `install.ps1` (right-click → Run with PowerShell). It flashes CircuitPython,
   then waits for the `CIRCUITPY` drive and copies all the code on automatically.
34. Plug it back in and make some sound.

---

## Features

- **2 Rotary encoders and button** for parameter adjustments.
- **12 keys** to make beats
- **2 sliders** to make additional parameter adjustments
- **LEDs** for some disco
- **Standalone beat machine** — 16-step sequencer, 6 patterns, runs on battery, no computer
- **3 key layouts** (piano / mirror / drums) with on-screen switching
- **Arpeggiator** with rate & direction controls
- **2 rotary encoders** (pushable) + **2 sliders**, all remappable on the fly
- **1.8" color display** with live view of keys, sliders, and layout
---

## Defaults (if you don't want to change anything):

### Keys for left set:

| Row        | Key 1           | Key 2           | Key 3         | 
|------------|-----------------|-----------------|---------------|
| **Top**    | PIANO: C3 (48) · MIRROR: C3 · DRUMS: C3     | PIANO: C#3 (49) · MIRROR: D3 · DRUMS: D3  | PIANO: D3 (50) · MIRROR: E3 · DRUMS: E3 |
| **Bottom** | PIANO: D#3 (51) · MIRROR: F3 · DRUMS: F3   | PIANO: E3 (52) · MIRROR: G3 · DRUMS: G3  | PIANO: F3 (53) · MIRROR: A3 · DRUMS: A3 |

### Keys for right set:

| Row        | Key 1           | Key 2           |
|------------|-----------------|-----------------|
| **Row 1**  | PIANO: F#3 (54) · MIRROR: C4 · DRUMS: Kick (36, ch10) | PIANO: G3 (55) · MIRROR: D4 · DRUMS: Snare (38, ch10)  | 
| **Row 2**  | PIANO: G#3 (56) · MIRROR: E4 · DRUMS: Closed Hat (42, ch10) | PIANO: A3 (57) · MIRROR: F4 · DRUMS: Open Hat (46, ch10) |
| **Row 3**  | PIANO: A#3 (58) · MIRROR: G4 · DRUMS: Clap (39, ch10) | PIANO: B3 (59) · MIRROR: A4 · DRUMS: Tom (45, ch10) | 


### Left Encoder:

- **Rotate** → Octave shift (−2 to +6, shown on screen)
- **Push ×1** → Panic / all-notes-off
- **Push ×2** → Enter Beat Mode (standalone drum machine)
- **Push ×3** → Arpeggiator page (hold keys + it plays them for you)
- In Beat Mode: rotate = step cursor · hold + rotate = switch pattern A–F · hold 600 ms = clear pattern · tap = exit & save

### Right Encoder:

- **Rotate** → Sends the selected MIDI CC (default: CC 74 filter cutoff)
- **Push ×1** → Cycle CC target: Cutoff (74) → Mod (1) → Volume (7) → Expression (11) → Reverb (91)
- **Push ×2** → CC Remap page (move a slider to reassign its CC)
- **Push ×3** → Switch key layout (screen animation confirms)
- In Beat Mode: rotate = BPM (40–220) · push = play/stop

### Bottom Slider:

- **Slide** → CC 1 (Mod Wheel) by default — remappable to any CC 0–127 via the remap page. In Beat Mode: BPM macro.


### Top Slider:

- **Slide** → CC 7 (Channel Volume) by default — remappable. In Beat Mode: headphone/output volume.

---

## What is this?

This is a MIDI keyboard I made to get into music production. This device can make all kinds of music. You can make various beats, change up different audio affects, and more!

## How it works and Issues I Faced

The Raspberry Pi Pico is placed on the bottom of the PCB along with the switch, battery charging module, battery, and the DAC. The rest of the components are on the top. This MIDI keyboard is running **Circuit python** and uses many different libraries to make the various parts work. Pretty obvious, but it uses the keys use a matrix layout.

When I was designing the PCB I wanted to make this MIDI keyboard as versatile and portable as possible. I also wanted to make it look clean and sleek. I had to reposition the components several times before I was satisfied. I also spent quite some time in CAD designing this case as I wanted to make it as clean as possible. It took me quite some while to find the right shape and and size without making it look awkward. It was quite a challenge connecting all the desired components to the Pi Pico as it only had so many pins. I ended up having to interpret different methods to save pins.

## How to use in detail

Flash the firmware with install.ps1 (hold BOOTSEL while plugging in when prompted), then plug into any DAW — it appears as a standard USB MIDI keyboard and the 12 keys play notes immediately (velocity fixed at 100; the PCB has no velocity sensing). The screen shows a live view: layout name, octave, keys lighting up as you press, slider positions, encoder values, and arpeggiator status. The left encoder shifts octave (−2…+6), single-push is a panic button, double-push enters the standalone beat machine (6 synthesized drums over the I2S header into a PCM5102 — 16-step sequencer, 6 pattern slots, finger-drumming on the left keys, all persisted to flash, runs from battery with no computer), and triple-push opens the arpeggiator (rate 1/4–1/16, up/down/updown). The right encoder is an assignable macro control — single-push cycles what it sends (cutoff → mod → volume → expression → reverb), double-push opens the CC remap page where moving a slider live-reassigns which CC it transmits, and triple-push switches the key layout (PIANO chromatic run / MIRROR octaves / DRUMS + GM drum map) with a full-screen animation. Every setting — layout, octave, CC assignments, arp config, beats, BPM — saves to flash automatically and survives power-off. To adjust behavior, edit lib/md_kbd/config.py (pins, CC targets, debounce, slider deadband, screen offsets) and lib/md_kbd/layouts.py (base note, key→note maps, LED order), save to the CIRCUITPY drive, and it reboots with your changes; the serial console at code.circuitpython.org shows any errors.



---

## BOM

- 1x Raspberry PI Pico with headers
- 14x through-hole 1N4148 Diodes
- 12x MX-Style switches
- 2x EC11 Rotary encoder
- 1.8 Inch TFT LCD Screen Display *(GND, VCC, SCL, SDA, RES, DC, CS, BL)*
- 12x blank DSA keycaps
- 4x M3x11mm screws
- Adafruit PCM5100 I2S DAC breakout
- 14x SK6812MINI-E mini LEDs
- 2x Bourns PTA2043-2210DPB103 slide potentometer
- TP4056 Type-c USB Battery Charger Module
- 3000 MAH lipo 1s battery
- SS12D00 Mini Slide Switch

---

## Renders/Images

<img width="900" height="655" alt="image" src="https://github.com/user-attachments/assets/0041ad86-4cff-447f-a05f-24bce1619767" />
<img width="1072" height="827" alt="image" src="https://github.com/user-attachments/assets/1fd356e4-0b4a-4dc3-8db4-82f466d46f36" />
<img width="682" height="434" alt="image" src="https://github.com/user-attachments/assets/841f9d17-566b-40c3-9733-6829479ca439" />
<img width="1101" height="745" alt="image" src="https://github.com/user-attachments/assets/e51db4bf-cdae-47a9-ae6e-734aa0240c1f" />





---

## Credits

Big shout out to **Hack Club** for giving me the opportunity to make this macropad. I would also like to thank [Logan Peterson](https://github.com/SharKingStudios/SplashPad/tree/main), as I modeled my readme.md after his hackpad's since I was amazed by how well written it was.

---

