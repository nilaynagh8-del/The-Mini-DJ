# The-Mini-DJ
A small, portable, MIDI keyboard to make beats on the go.

*(or just a cooler way to make some beats)* 
<img width="986" height="579" alt="image" src="https://github.com/user-attachments/assets/dfcaae29-78cc-4468-861f-9d36c7313362" />



---

#Quick Start

1. Hold **BOOT** and plug in your Raspberry pi pico.
2. Drop `_______` onto the `RPI-RP2` drive.
3. Plug it back in and make some sound.

---

## Features

- **Display** to display custom memes or other info
- ** 2 Rotary encoders and button** for parameter adjustments.
- **12 keys** to make beats
- **2 sliders** to make additional parameter adjustments
- **LEDs** for some disco
---

## Defaults (if you don't want to change anything):

### Keys for left set:

| Row        | Key 1           | Key 2           | Key 3         | Key 4        |
|------------|-----------------|-----------------|---------------|--------------|
| **Top**    | Play/Pause      | Previous Track  | Next Track    | Rotary Encoder In This Spot|
| **Bottom** | Copy (Ctrl+C)   | Paste (Ctrl+V)  | Undo (Ctrl+Z) | Print Screen |

### Keys for right set:

| Row        | Key 1           | Key 2           |
|------------|-----------------|-----------------|
| **Row 1**  | Play/Pause      | Previous Track  | 
| **Row 2**  | Copy (Ctrl+C)   | Paste (Ctrl+V)  |
| **Row 3**  | Play/Pause      | Previous Track  | 
| **Row 4**  | Copy (Ctrl+C)   | Paste (Ctrl+V)  |
| **Row 5**  | Play/Pause      | Previous Track  | 
| **Row 6**  | Copy (Ctrl+C)   | Paste (Ctrl+V)  |
| **Row 7**  | Play/Pause      | Previous Track  | 
| **Row 8**  | Copy (Ctrl+C)   | Paste (Ctrl+V)  |


### Left Encoder:

- **Rotate left** → Volume Down
- **Rotate right** → Volume Up
- **Push** → Mute

### Right Encoder:

- **Rotate left** → Volume Down
- **Rotate right** → Volume Up
- **Push** → Mute

### Bottom Slider:

- **Rotate left** → Volume Down
- **Rotate right** → Volume Up
- **Push** → Mute

### Top Slider:

- **Rotate left** → Volume Down
- **Rotate right** → Volume Up
- **Push** → Mute


---

## What is this?

This is a MIDI keyboard I made to get into music production. This device can make all kinds of music. You can make various beats, change up different audio affects, and more!

## How it works and Issues I Faced

The Raspberry Pi Pico is placed on the bottom of the PCB along with the switch, battery charging module, battery, and the DAC. The rest of the components are on the top. This MIDI keyboard is running **Circuit python** and uses many different libraries to make the various parts work. Pretty obvious, but it uses the keys use a matrix layout.

When I was designing the PCB I wanted to make this MIDI keyboard as versatile and portable as possible. I also wanted to make it look clean and sleek. I had to reposition the components several times before I was satisfied. I also spent quite some time in CAD designing this case as I wanted to make it as clean as possible. It took me quite some while to find the right shape and and size without making it look awkward. It was quite a challenge connecting all the desired components to the Pi Pico as it only had so many pins. I ended up having to interpret different methods to save pins.

---

## BOM

- 1x Raspberry PI Pico with headers
- 12x through-hole 1N4148 Diodes
- 12x MX-Style switches
- 2x EC11 Rotary encoder
- 1.8 Inch TFT LCD Screen Display *(GND, VCC, SCL, SDA, RES, DC, CS, BL)*
- 12x blank DSA keycaps
- 4x M3x11mm screws
- Adafruit PCM5100 I2S DAC breakout
- SK6812MINI-E mini LEDs
- 1x 0.91 inch OLED display *(the pin order is GND-VCC-SCL-SDA, **MAKE SURE YOUR PCB MATCHES**)*
- Bourns PTA2043-2210DPB103 slide potentometer

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

