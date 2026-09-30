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

| Parts      | Price           |
|------------|-----------------|
| **1x [Raspberry PI Pico with headers](https://www.sparkfun.com/raspberry-pi-pico-2-with-headers.html?utm_source=google&utm_medium=cpc&utm_campaign=Generic+%7C+PMax&utm_content=Full+Catalog&gad_source=1&gad_campaignid=17479024039&gbraid=0AAAAADsj4EQmsDvz82Hst9oYgqH95IkjX&gclid=CjwKCAjww-3VBhAcEiwAwUUIu6L8YbgkTXDd5AfPm4zQAW7P8PbXcedCtt6K2ccCEoWBpJduEstlNxoCzmoQAvD_BwE)**  | $6.60 |
| **14x [through-hole 1N4148 Diodes](https://www.sparkfun.com/diode-small-signal-1n4148.html?utm_source=google&utm_medium=cpc&utm_campaign=Generic+%7C+PMax&utm_content=Full+Catalog&gad_source=1&gad_campaignid=17479024039&gbraid=0AAAAADsj4EQmsDvz82Hst9oYgqH95IkjX&gclid=CjwKCAjww-3VBhAcEiwAwUUIu16fH0brzaPF45hpGUsThg8ICQOK6fsUcsrrK9Vc8bTXAzBj6--0lBoCFfoQAvD_BwE)**  |$3.50 |
| **12x [MX-Style switches](https://www.amazon.com/GATERON-Yellow-Keyboard-Switches-Mechanical/dp/B0DYJVRB46/ref=sr_1_9?crid=3BOR3M65IW5AU&dib=eyJ2IjoiMSJ9.7yzZVHtLq6aPa1zS0Zx72SvcTVPnbtJpfILGixsmfHPROx_O7wytItw4YNMAsDJ3dyMbN7iUZi5_YafPZU3gp98PfIAYQXQ80DopFZZU4EukG4bbiWcyRzBdMHMKxkpgfGvv9MJtdIVgSXvuVjhq3GfIBhRmCTIQV1wagvLVnZfbHZ248NJYpy9drBez7_MJEUV_GdiWjGecbcagz1zQLjLEA-rgwE_SQP7MMT66MRo.KmOSA1BkH0YNT32uTxHCbGzCclLK01kKmLeR-iT17UA&dib_tag=se&keywords=mx%2Bswitches%2Bgateron%2Bmilky%2Byellow%2Bpros&qid=1790738935&sprefix=mx%2Bswitches%2Bgatreon%2Bmilky%2Byellow%2Bpro%2Caps%2C124&sr=8-9&th=1)**  | $9.99 |
| **2x [EC11 Rotary encoder](https://www.sparkfun.com/rotary-encoder-illuminated-rgb.html?utm_source=google&utm_medium=cpc&utm_campaign=Generic+%7C+PMax&utm_content=Full+Catalog&gad_source=1&gad_campaignid=17479024039&gbraid=0AAAAADsj4EQmsDvz82Hst9oYgqH95IkjX&gclid=CjwKCAjww-3VBhAcEiwAwUUIu02YrEf3qTTig8LygFCuF0xHmPunVouqvANyFPDiPHUQzV7tYWZrQBoCns4QAvD_BwE)**  | $9.90 |
| **1x [1.8 Inch TFT LCD Screen Display *(GND, VCC, SCL, SDA, RES, DC, CS, BL)](https://www.amazon.com/JESSINIE-Display-Arduino-128x160-Interface/dp/B0D31BGJWF)**  | $9.95 |
| **12x [blank DSA keycaps](https://www.sparkfun.com/cherry-mx-keycap-r2-opaque-black.html?utm_source=google&utm_medium=cpc&utm_campaign=Generic+%7C+PMax&utm_content=Brand&gad_source=1&gad_campaignid=17479024039&gbraid=0AAAAADsj4EQmsDvz82Hst9oYgqH95IkjX&gclid=CjwKCAjww-3VBhAcEiwAwUUIu2OeiSDNHx22K4ZE6aV56NB8pwd4icG4_PFrGK0aWvuLnZYkM45bNxoCcm4QAvD_BwE)**  | $12.6 |
| **2x [Bourns PTA2043-2210DPB103 slide potentometer](https://www.mouser.com/ProductDetail/Bourns/PTA2043-2210DPB103?qs=Zq5ylnUbLm4pc%2F056pq%252B3Q%3D%3D&srsltid=AU7gw4WNM2MZveNKfvVPV0_SmZF9u4hnq1oMDlnN0YbM8CMP3-jc-wWq)**  | $3.92 |
| **1x [TP4056 Type-c USB Battery Charger Module](https://www.amazon.com/TP4056-Lithium-Charging-Protection-Functions/dp/B0G2S8478G/ref=sr_1_12?channelId=500&clpRedir=Y&dib=eyJ2IjoiMSJ9.mmqI1134FS87MHz1mUcWtVKE3sKOUbRgY85vHnw8FviRq5ou6bM0zulAnjj4ekLBnNGpXWe_erXY_99X_G-GUQ0HgH-ANg7UWzEUVCcc5YJemGX9ltWloyWOwg3Z_cylKx-hfdA_bb2G8fc9eQksR8NV_u3HrbR3p7LinRevl0IQHVDV4-WsLpcZHJYb3NQAQJ8ZL20Rub3CatK6GH2OJOfJ28fwQLaTmCK-zbcmi5I.-6fUwXbOGhhLjiZD5YmpVVN1HHLkHNVNGr6zI44SAEk&dib_tag=se&keywords=tp4056%2Bmodule&plpRedirect=mhFallback&qid=1790739445&sr=8-12&th=1)**  | $3.90 |
| **1x [3000 MAH lipo 1s battery](https://www.amazon.com/JLJLUP-Rechargeable-Integrated-Protection-Development/dp/B0FH9XHXRT/ref=sr_1_8?crid=3J5GQ2GHVBT2&dib=eyJ2IjoiMSJ9.jTLPL8OQ8ajoyA2_4JA3kGxXLe3zJ6ubZ3lkO1YVvHH5Y6Lq6gkANDUM8MwYmcJutmJlHHmpsh89DobjiS2Y8xEZq9LfJvh3OjzBZPKKLDGX4uXM4z1HuBx2mJIpJR8hdfTMrcUrqV1Cvj6YuRvbypLQuIPnZf5GUw7-8Rfkk6oRfocO8unH-Lhk7p3P6-UQaISJwG-GspSMSPUgRQGxfY_hrAnTEDVe4fI3dQkDuwe1Kna_Y3zLADrGckDbJkzALlIKlI_N1n3SlQC_ggF0F9qBeSl0j2kX4v2xd1GJ1aA.fCT6CM22B56DXaKKZrPjMSLSDzbXcnhUfNMwc7Jy7_k&dib_tag=se&keywords=3000%2BMAH%2Blipo%2B1s%2Bbattery&qid=1790739508&sprefix=3000%2Bmah%2Blipo%2B1s%2Bbattery%2Caps%2C128&sr=8-8&th=1)**  | $9.99 |
| **1x [SS12D00 Mini Slide Switch](https://www.sparkfun.com/spdt-slide-switch.html?utm_source=google&utm_medium=cpc&utm_campaign=Generic+%7C+PMax&utm_content=Full+Catalog&gad_source=1&gad_campaignid=17479024039&gbraid=0AAAAADsj4EQmsDvz82Hst9oYgqH95IkjX&gclid=CjwKCAjww-3VBhAcEiwAwUUIu-FrtV2oVVqad4__7DMZayV6Yt9PTAYWBoaM9FzKOrpd1n_6mqxm0BoCI6sQAvD_BwE)**  | $0.95 |
| **Total not including PCB or 3d prints:**      | **$71.30**     |

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

