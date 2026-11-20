# 🎛️ Frequency Analyzer - Visual Quick Reference

## What You're Looking At

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                    📡 FREQUENCY ANALYZER MHz DISPLAY              ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

┌─────────────────────────────────────────────────────────────────────┐
│                   📊 Audio Frequency Spectrum (0-20kHz)             │
│                                                                      │
│      |    /\         /\                                             │
│   M  |   /  \       /  \                                            │
│   a  |  /    \     /    \                    /\                     │
│   g  | /      \   /      \                  /  \                    │
│   n  |/        \_/        \                /    \                   │
│   i  |________________________\/__________/______\________________   │
│   t  └────────────────────────────────────────────────────────────  │
│   u    0kHz    5kHz     10kHz    15kHz     20kHz                    │
│   d    ◄─ Low Frequencies ─────────────► High Frequencies ►        │
└─────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────┐ ┌────────────────────────────────────┐
│   📡 RADIO BANDS               │ │ 🎵 DETECTED SIGNALS                │
│   Frequency Ranges              │ │                                    │
│                                │ │ Peak Frequency:                    │
│ 🟡 AM Radio                     │ │ 1234.5 Hz (1.23 kHz)              │
│    0.5 - 1.6 MHz                │ │ Magnitude: [████████░░░░] 345.2   │
│                                │ │                                    │
│ 🟠 CB Radio                     │ │ 📶 WiFi Networks Detected:         │
│    26.965 - 27.405 MHz          │ │ • MyNetwork - Ch6 2437MHz [███░░] │
│                                │ │ • Router_5G - Ch36 5180MHz [████░]│
│ 🟢 FM Radio                     │ │ • Guest - Ch11 2462MHz [██████]   │
│    88 - 108 MHz                 │ │                                    │
│                                │ │ (Signal strength shown as bars)    │
│ 🔵 WiFi 2.4GHz                  │ │                                    │
│    2400 - 2500 MHz              │ │ Network Info:                      │
│                                │ │ • Ch# = Channel number             │
│ 🔵 WiFi 5GHz                    │ │ • MHz = Frequency in megahertz     │
│    4900 - 5900 MHz              │ │ • [Bar] = Signal strength (0-100%) │
│                                │ │                                    │
│ 🟣 LTE/4G                       │ │                                    │
│    700 - 2600 MHz               │ │                                    │
└────────────────────────────────┘ └────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│ 📋 Common Frequencies (Reference Chart)                             │
│                                                                      │
│ Electrical Hum      :    60 MHz  │ WiFi 2.4 Ch6         : 2437 MHz  │
│ AM Radio Min        :   550 MHz  │ WiFi 2.4 Ch11        : 2462 MHz  │
│ AM Radio Max        :  1700 MHz  │ WiFi 5 UNII1         : 5180 MHz  │
│ CB Radio            :    27 MHz  │ WiFi 5 UNII3         : 5600 MHz  │
│ FM Radio Min        :    88 MHz  │ 4G LTE Band 1        : 2100 MHz  │
│ FM Radio Max        :   108 MHz  │ 4G LTE Band 3        : 1800 MHz  │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│ 🕐 Time: 14:30:45          [ESC] Exit  [SPACE] WiFi  [H] Help     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Quick Frequency Cheat Sheet

### What Each Band Is

```
🟡 YELLOW (AM Radio)
├─ 550 kHz (lowest AM station)
├─ 1200 kHz (middle of band)
└─ 1700 kHz (highest AM station)
   └─ Range: 0.5 - 1.6 MHz (Lower frequencies = longer range)

🟠 ORANGE (CB Radio)
├─ 26.965 MHz 
├─ 27.0 MHz (most popular)
└─ 27.405 MHz
   └─ Often used by: Truck drivers, hobbyists, emergency comms

🟢 GREEN (FM Radio)
├─ 88.1 MHz (lowest FM station)
├─ 100.0 MHz (typical big city)
└─ 107.9 MHz (typically highest)
   └─ Range: 88 - 108 MHz (Better quality than AM)

🔵 CYAN (WiFi 2.4 GHz)
├─ Ch 1: 2412 MHz◄──┐
├─ Ch 6: 2437 MHz   ├─ Non-overlapping
└─ Ch 11: 2462 MHz◄─┘  (recommended channels)
   └─ 2400-2500 MHz (Older but more range, more devices)

🔵 BLUE (WiFi 5 GHz)
├─ Ch 36: 5180 MHz
├─ Ch 100: 5500 MHz
└─ Ch 149: 5745 MHz
   └─ 4900-5900 MHz (Newer, faster, less interference)

🟣 MAGENTA (LTE/4G)
├─ 700 MHz (Band 28)
├─ 1800 MHz (Band 3 - common)
└─ 2600 MHz (Band 7 - high band)
   └─ 700-2600 MHz (Mobile phone networks)
```

---

## WiFi Channel Frequency Guide

### 2.4 GHz Band (13 Overlapping Channels)

```
Channel  Frequency   Overlaps
   1     2412 MHz    ↔ 2, 3, 4, 5
   2     2417 MHz    ↔ 1, 3, 4, 5, 6
   3     2422 MHz    ↔ 1, 2, 4, 5, 6, 7
   4     2427 MHz    ↔ 1, 2, 3, 5, 6, 7, 8
   5     2432 MHz    ↔ 1, 2, 3, 4, 6, 7, 8, 9
   6     2437 MHz    ↔ 2, 3, 4, 5, 7, 8, 9, 10  ← GOOD CHOICE
   7     2442 MHz    ↔ 3, 4, 5, 6, 8, 9, 10, 11
   8     2447 MHz    ↔ 4, 5, 6, 7, 9, 10, 11, 12
   9     2452 MHz    ↔ 5, 6, 7, 8, 10, 11, 12, 13
  10     2457 MHz    ↔ 6, 7, 8, 9, 11, 12, 13
  11     2462 MHz    ↔ 7, 8, 9, 10, 12, 13      ← GOOD CHOICE
  12     2467 MHz    ↔ 8, 9, 10, 11, 13
  13     2472 MHz    ↔ 9, 10, 11, 12

► BEST TO USE: Channels 1, 6, or 11 (NO OVERLAP!)
```

### 5 GHz Band (Many Non-Overlapping Channels)

```
UNII-1     UNII-2     UNII-3     UNII-4
(5150-5250) (5250-5350) (5470-5725) (5850-5925)

Ch 36-48   Ch 52-144  Ch 149-165 Ch 169+
5180-5240  5260-5730  5745-5825  5850-5925

► ADVANTAGE: Many non-overlapping channels!
► LESS INTERFERENCE: Fewer devices competing
► TRADE-OFF: Shorter range than 2.4GHz
```

---

## Frequency Scale Visual

```
10 Hz        100 Hz       1 kHz        10 kHz       100 kHz
|─ | ─ | ─ | ─ | ─ | ─ | ─ | ─ | ─ | ─ | ─ | ─ | ─ | ─ |
				▲ Electrical Hum (60 Hz)
						 ▲ Voice Frequencies


100 kHz      1 MHz        10 MHz       100 MHz      1 GHz
| ─ | ─ | ─ | ─ | ─ | ─ | ─ | ─ | ─ | ─ | ─ | ─ | ─ | ─ |
		▲ AM Radio              ▲ FM Radio
		(0.5-1.6)               (88-108)


1 GHz        10 GHz       100 GHz      1 THz
| ─ | ─ | ─ | ─ | ─ | ─ | ─ | ─ | ─ | ─ | ─ | ─ | ─ | ─ |
	 ▲ WiFi 2.4GHz        ▲ WiFi 5GHz
	 (2.4)                (5.0)

	 ▲ 4G LTE (0.7-2.6 GHz)
```

---

## What Changes What

### Signal Strength Factors

```
Obstacles Block WiFi                Range vs Frequency
Thick        Medium      Open          ▲
walls ◄──────────────► Space         Long│
-30dBm       -60dBm    -70dBm        │   └─ Low Freq (AM)
									 │
Excellent  Good  Fair   Weak      Range  WiFi 2.4 GHz
[████]   [███░]  [██░░]  [░░░░]         ││
										│
									Short└─ High Freq (5GHz)
```

---

## How to Identify Networks

### Example: You See This

```
• MyNetwork - Ch6 2437MHz [████████░░]
```

**Breaking It Down:**

| Part | Meaning |
|------|---------|
| `•` | Active network (available) |
| `MyNetwork` | Your router's name (SSID) |
| `Ch6` | WiFi channel 6 |
| `2437MHz` | Actual carrier frequency (2.437 GHz) |
| `[████████░░]` | Signal strength (75% - Good) |

---

## Common Issues & What They Show

### Issue: "Many networks on same channel"
```
• Router1 - Ch6 2437MHz [████]
• Router2 - Ch6 2437MHz [█████]
• Router3 - Ch6 2437MHz [███]

✓ SOLUTION: Switch to Ch1 or Ch11
  (See 2.4GHz channel chart above)
```

### Issue: "Only 2.4GHz network"
```
• MyNetwork - Ch6 2437MHz [████]

✓ MEANS: Router is older, or 5GHz turned off
✓ TRADE-OFF: More range but slower
```

### Issue: "Both 2.4 and 5GHz same router"
```
• MyRouter - Ch6 2437MHz [████]      ← Older devices
• MyRouter_5G - Ch36 5180MHz [████]  ← Newer devices

✓ GOOD PRACTICE: Dual band for compatibility
```

---

## Frequency Conversion Quick Math

### Convert Channel to Frequency

**2.4 GHz Band:**
```
Frequency = 2407 + (Channel × 5) MHz

Example: Channel 6
= 2407 + (6 × 5)
= 2407 + 30
= 2437 MHz ✓
```

**5 GHz Band:**
```
Frequency = 5000 + (Channel × 5) MHz

Example: Channel 36
= 5000 + (36 × 5)
= 5000 + 180
= 5180 MHz ✓
```

---

## What The Numbers Mean

### Magnitude
```
0        100       200       300        400    500
|────────|────────|────────|────────|────────|
Weak     Moderate Medium   Strong   Very Strong
[░░░░░░] [████░░] [██████] [████████] [██████████]
```

### Signal Strength %
```
0%        25%      50%      75%       100%
|────────|────────|────────|────────|
Unusable  Weak     Fair     Good    Excellent
   ░░░░    ████     ██████   ████████ ██████████
```

---

## Keyboard Shortcuts

```
╔════════════════════════════════════╗
║  Key        Function               ║
╠════════════════════════════════════╣
║  H          Show/Hide Help          ║
║  SPACE      Force WiFi Scan         ║
║  ESC        Exit Application        ║
╚════════════════════════════════════╝
```

---

## Quick Facts

- **60 Hz** = Power line hum (ALWAYS present)
- **440 Hz** = Musical A note 
- **2407 MHz** base frequency for 2.4GHz WiFi calculation
- **5000 MHz** base frequency for 5GHz WiFi calculation
- **Three good channels** = 1, 6, 11 (2.4GHz non-overlapping)
- **Five MHz** = Gap between adjacent WiFi channels
- **1000 MHz** = 1 GHz (gigahertz)

---

## You're an Expert When You Know:

✅ What frequency means (oscillations/second)
✅ Difference between Hz, kHz, MHz, GHz
✅ Why different bands exist (regulation, range trade-offs)
✅ How to read a spectrum graph
✅ What your WiFi channel is and its frequency
✅ Why separating networks by channel helps
✅ What AM/FM radio frequencies are
✅ Why 2.4GHz and 5GHz exist

---

**Now you can see the wireless spectrum in action! 📡✨**
