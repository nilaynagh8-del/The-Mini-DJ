# Key layouts and the hardware-bit -> physical position mapping.
#
# Hardware bit index = row*7 + col (see config.py). The physical panel:
#   left block is 3 columns x 2 rows, right block is 2 columns x 3 rows.
# HW_BITS[phys] = hardware bit index for physical key `phys`:
#   left block top L-to-R, left bottom L-to-R,
#   right block top-to-bottom column-major (2 wide x 3 tall).
HW_BITS = (
    # left block (0-5): top row then bottom row
    6, 0, 7,     # SW6, SW4, SW10   (top L->R)
    13, 1, 8,    # SW12, SW5, SW11  (bottom L->R)
    # right block (6-11): 2 cols x 3 rows, column-major (SW at x=181 then x=200)
    2, 3, 4,     # SW1 top, SW2 mid, SW3 bottom   (left column)
    9, 10, 11,   # SW7 top, SW8 mid, SW9 bottom   (right column)
)
# Encoder push bits (NOT in the physical map):
#   bit 5  = SW13 push = RIGHT encoder
#   bit 12 = SW14 push = LEFT encoder

BASE = 48  # C3

# 1) Piano: continuous chromatic run, left block then right block.
PIANO = tuple(BASE + i for i in range(12))

# 2) Mirrored: right block repeats left block one octave up.
_MIRROR_OFFS = (0, 2, 4, 5, 7, 9)
MIRROR = tuple(BASE + _MIRROR_OFFS[i % 6] + (12 if i >= 6 else 0)
               for i in range(12))

# 3) Left notes + right drum pads (General MIDI channel 10).
# kick, snare, closed hat, open hat, clap, low tom
DRUMS = (36, 38, 42, 46, 39, 45)
DRUM_CHANNEL = 9  # 0-based; GM drums = channel 10


def note_for(layout_id, phys_idx):
    """Return (midi_note, channel) for physical key 0..11."""
    if layout_id == 1:
        return MIRROR[phys_idx], 0
    if layout_id == 2:
        if phys_idx < 6:
            return PIANO[phys_idx], 0
        return DRUMS[phys_idx - 6], DRUM_CHANNEL
    return PIANO[phys_idx], 0


LAYOUT_NAMES = ("PIANO", "MIRROR", "DRUMS")

# LED chain position -> physical key (same 0-11 indexing).
LED_CHAIN2KEY = (6, 0, 3, 5, 2, 4, 1, 7, 10, 8, 11, 9)
LED_ENC_CHAIN = (13, 12)  # chain pos of left, right encoder LEDs
