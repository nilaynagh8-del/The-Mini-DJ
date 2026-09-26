# Hardware pin configuration for the MIDI Keyboard PCB.
# Every GPIO below is derived from the KiCad netlist of
# "Midi Keyboard.kicad_pcb" by mapping the Pico symbol PIN NUMBER to its
# GPIO name (e.g. A1.10 -> pin 10 -> GPIO7). Double-checked twice.
# Do not edit casually.

# ---- USB MIDI ----
MIDI_CHANNEL = 0  # 0-15 (channel 1 in DAW terms)

# CC targets the right encoder cycles through (short push = next target)
ENC_CC_TARGETS = (74, 1, 7, 11, 91)
ENC_CC_NAMES = ("CUTOFF", "MOD", "VOLUME", "EXPRS", "REVERB")

# ---- Key matrix ----
# 2 rows x 7 columns, 14 switches (12 keys + 2 encoder pushes).
# Rows are driven outputs, cols are inputs with pull-ups (1N4148 in series).
ROW_PINS = (7, 8)   # GPIO7 = schematic "row 3", GPIO8 = "row 4"
# Columns in scan order (schematic col1,2,3,4,5,enc,col7):
COL_PINS = (0, 1, 4, 5, 6, 2, 3)  # GPIO numbers; GPIO2 = encoder pushes
# Hardware bit = rowIdx*7 + colIdx:
#  bit0 SW4 (L top-mid)    bit1 SW5 (L bot-mid)   bit2 SW1 (R-Lcol top)
#  bit3 SW2 (R-Lcol mid)   bit4 SW3 (R-Lcol bot)  bit5 RIGHT-encoder push
#  bit6 SW6 (L top-left)   bit7 SW10 (L top-right) bit8 SW11 (L bot-right)
#  bit9 SW7 (R-Rcol top)   bit10 SW8 (R-Rcol mid)  bit11 SW9 (R-Rcol bot)
#  bit12 LEFT-encoder push  bit13 SW12 (L bot-left)

# ---- Rotary encoders ----
ENC_LEFT_A = 12   # SW14 A (left encoder, nearer screen)
ENC_LEFT_B = 13   # SW14 B
ENC_RIGHT_A = 10  # SW13 A (right encoder)
ENC_RIGHT_B = 11  # SW13 B

# ---- Sliders (linear pots) ----
SLIDER_PINS = (26, 27)  # RV1 (bottom slider) = GPIO26/ADC0, RV2 top = ADC1

# ---- SK6812 RGB LED chain ----
LED_PIN = 9
LED_COUNT = 14
# chain-position -> physical key mapping lives in layouts.py (single source)

# ---- ST7789-class SPI LCD (PIO bit-banged: GP21 is not HW-SPI capable) ----
LCD_SCK = 18
LCD_MOSI = 21
LCD_CS = 19
LCD_DC = 22
LCD_RST = 14
LCD_BL = 20
LCD_WIDTH = 240
LCD_HEIGHT = 240
LCD_X_OFFSET = 0   # change to 2/3 if your panel shows a shifted image
LCD_Y_OFFSET = 0
LCD_SM_FREQ = 62_500_000  # PIO state machine clock -> 31.25 Mbit/s SPI

# ---- I2S audio out (PCM5102 DAC on header J2) ----
# Optional: only touched when beat mode is first used, so MIDI-only use
# never initializes audio.
I2S_BCK = 15   # GPIO15 -> PCM5102 BCK
I2S_LRCK = 16  # GPIO16 -> PCM5102 LRCK (LCK)
I2S_DIN = 17   # GPIO17 -> PCM5102 DIN

# ---- Timing ----
DEBOUNCE_MS = 10
SLIDER_DEADBAND = 3
SLIDER_INTERVAL_MS = 15
UI_MIN_INTERVAL_MS = 60
LED_INTERVAL_MS = 40
BEAT_GESTURE_MS = 450   # multi-press window for left-encoder pushes
BEAT_UI_MS = 100        # beat page playhead redraw interval
